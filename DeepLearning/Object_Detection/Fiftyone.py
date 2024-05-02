import cv2
import numpy as np

import fiftyone as fo
import fiftyone.brain as fob
import fiftyone.zoo as foz

dataset = foz.load_zoo_dataset("mnist", split="test")

# Construct a `num_samples x num_pixels` array of images
images = np.array([
    cv2.imread(f, cv2.IMREAD_UNCHANGED).ravel()
    for f in dataset.values("filepath")
])

# Compute 2D embeddings
results = fob.compute_visualization(dataset, embeddings=images, seed=51)

# Visualize embeddings, colored by ground truth label
plot = results.visualize(labels="ground_truth.label")
plot.show(height=720)