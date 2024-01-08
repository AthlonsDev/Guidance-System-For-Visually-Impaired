import torch
import torch.nn as nn
from utils import intersection_over_union

class YoloLoss(nn.Module):
    def __init__(self):
        super().__init__()
        self.mse = nn.MSELoss() #Mean Squared Error
        self.bce = nn.BCEWithLogitsLoss() #Binary Cross Entropy
        self.entropy = nn.CrossEntropyLoss() #Cross Entropy Loss
        self.sigmoid = nn.Sigmoid()

        #constants
        #class and object are valued more than box and class
        self.lamdba_class = 1
        self.lamdba_noobj = 10
        self.lamdba_obj = 1
        self.lamdba_box = 10

    def froward(self, predictions, target, anchors):
        obj = target[..., 0] == 1 #Object exists
        noobj = target[..., 0] == 0 #Object does not exist

        #No object loss
        no_object_loss = self.bce(
            (predictions[..., 0:1][noobj]), (target[..., 0:1][noobj])
        )

        #Object loss
        anchors = anchors.reshape(1, 3, 1, 1, 2) #Reshape anchors to match predictions
        box_preds = torch.cat([self.sigmoid(predictions[..., 1:3]), torch.exp(predictions[..., 3:5]) * anchors], dim=-1) #Convert predictions to x, y, w, h format
        ious = intersection_over_union(box_preds[obj], target[..., 1:5][obj]).detach() #Detach to prevent gradients from flowing backwards.
        object_loss = self.bce((predictions[..., 0:1][obj]), (ious * target[..., 0:1][obj]))


        #Box coordinates loss
        predictions[..., 1:3] = self.sigmoid(predictions[..., 1:3]) #x, y coordinates
        target[..., 3:5] = torch.log(
            (1e-16+target[..., 3:5] / anchors)
        )
        box_loss = self.mse(predictions[..., 1:5][obj], target[..., 1:5][obj])

        #Class loss
        class_loss = self.entropy(
            (predictions[..., 5:][obj]), target[..., 5][obj].long()
        )

        return(
            self.lamdba_box * box_loss
            + self.lamdba_obj * object_loss
            + self.lamdba_noobj * no_object_loss
            + self.lamdba_class * class_loss
        )