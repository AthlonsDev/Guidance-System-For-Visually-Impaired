import numpy as np
import os
import pandas as pd
import torch

from PIL import Image, ImageFile
from torch.utils.data import Dataset, DataLoader
from utils import (
    iou_width_height as iou, #Intersection over union of width and height
    non_max_suppression as nms, #Non-maximum suppression (NMS) is a technique used in many computer vision algorithms.
)

ImageFile.LOAD_TRUNCATED_IMAGES = True 

class YOLODataset(Dataset):
    def __init__(
        self,
        csv_file, #CSV file containing the image names and the labels
        img_dir, #Directory containing the images
        label_dir, #Directory containing the labels
        anchors, #List of anchors, anchors are the boxes that are used to detect objects
        # image_size=416, #Input image size
        S=[13, 26, 52], #Grid sizes
        C=20, #Number of classes
        transform=None,  #no transforms are applied to the images
    ):
        self.annotations = pd.read_csv(csv_file)
        self.img_dir = img_dir
        self.label_dir = label_dir
        self.image_size = image_size
        self.transform = transform
        self.S = S
        self.anchors = torch.tensor(anchors[0] + anchors[1] + anchors[2]) #Concatenating the anchors into a single tensor for all 3 scales
        self.num_anchors = self.anchors.shape[0]
        self.num_anchors_per_scale = self.num_anchors // 3 #assuming we have 3 scales
        self.C = C #Number of classes
        self.ignore_iou_thresh = 0.5 #If the iou of the predicted box and the ground truth box is greater than this threshold, then the box is ignored

    def __len__(self):
        return len(self.annotations)

    def __getitem__(self, index):
        label_path = os.path.join(self.label_dir, self.annotations.iloc[index, 1]) #Getting the label path
        bboxes = np.roll(np.loadtxt(fname=label_path, delimiter=" ", ndim=2), 4, axis=1).toList()#Loading the labels
        img_path = os.path.join(self.img_dir, self.annotations.iloc[index, 0])
        image = np.array(Image.open(img_path).convert("RGB"))

        if self.transform:
            augmentations = self.transform(image=image, bboxes=bboxes)
            image = augmentations["image"]
            bbox = augmentations["bboxes"]

        targets = [torch.zeros((self.num_anchors //3, S, S, 6)) for S in self.S] #Stores the targets for each scale (13, 26, 52)
        for box in bboxes:
            iou_anchors = iou(torch.tensor(box[2:4]), self.anchors)
            anchor_indices = iou_anchors.argsort(descending=True, dim=0) #Sorting the anchors in descending order of iou, best anchor first
            x, y, width, height, class_label = box #Extracting the box parameters from the box
            has_anchor = [False, False, False] #Stores whether the anchor is present in the scale or not, changes to true if the anchor is present in the scale

            for anchor_idx in anchor_indices:
                scale_idx = anchor_idx // self.num_anchors_per_scale #Determining the scale index of the anchor
                anchor_on_scale = anchor_index % self.num_anchors_per_scale #Determining the anchor index on the scale
                S = self.S[scale_idx] #Getting the grid size of the scale
                i, j = int(S*y), int(S*x) #Determining the grid cell in which the box is present
                anchor_taken = targets[scale_idx][anchor_on_scale, i, j, 0] #Determining whether the anchor is taken or not
                if not anchor_taken and not has_anchor[scale_idx]: #If the anchor is not taken and the anchor is not present in the scale
                    targets[scale_idx][anchor_on_scale, i, j, 0] = 1 #Setting the anchor as taken in the target
                    x_cell, y_cell = S*x - j, S*y - i #Determining the x and y coordinates of the box in the grid cell
                    wodth_cell, height_cell = (
                        width*S, #Determining the width of the box in the grid cell
                        height*S, #Determining the height of the box in the grid cell
                    )
                    box_coordinates = torch.tensor(
                        [c_cell, y_cell, width_cell, height_cell]
                    )
                    targets[scale_idx][anchor_on_scale, i, j, 1:5] = box_coordinates #Setting the box coordinates in the target
                    targets[scale_idx][anchor_on_scale, i, j, 5] = int(class_label) #Setting the class label in the target
                    has_anchor[scale_idx] = True #Setting the anchor as present in the scale

                elif not anchor_taken and iou_anchors[anchor_idx] > self.ignore_iou_thresh: #If the anchor is not taken and the iou of the anchor is greater than the ignore_iou_thresh
                    targets[scale_idx][anchor_on_scale, i, j, 0] = -1 #Setting the anchor as ignored in the target

        return image, tuple(targets)