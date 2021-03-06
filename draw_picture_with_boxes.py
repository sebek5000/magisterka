# Based on YOLOv3
# https://github.com/eriklindernoren/PyTorch-YOLOv3/blob/master/README.md
# This file is used to draw bounding boxes of objects described in json format.
# The picture is saved in main folder as "json_box.png"

import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib.ticker import NullLocator
from PIL import Image

with open('json/test.txt') as json_file:
    data = json.load(json_file)

img = np.array(Image.new('RGB', (data['picture_width'], data['picture_height'])))
plt.figure()
fig, ax = plt.subplots(1)
ax.imshow(img)

for obj in data['objects']:
    plt.text(
        float(obj['x']),
        float(obj['y']),
        s=obj['name'],
        color="white",
        verticalalignment="top",
        bbox={"color": 'red', "pad": 0},
    )
    bbox = patches.Rectangle((float(obj['x']), float(obj['y'])), float(obj['width']), float(obj['height']), linewidth=2, edgecolor='blue', facecolor="none")
    ax.add_patch(bbox)

plt.axis("off")
plt.gca().xaxis.set_major_locator(NullLocator())
plt.gca().yaxis.set_major_locator(NullLocator())
plt.savefig(f"json_box.png", bbox_inches="tight", pad_inches=0.0)
plt.close()
