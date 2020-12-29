import common
import location_description as LD
import os

folder_name = 'D:\Dokumenty\PyTorch_YOLO\PyTorch-YOLOv3\json'
arr = os.listdir('D:\Dokumenty\PyTorch_YOLO\PyTorch-YOLOv3\json')

images_description = []

for file in arr:
    data = common.read_objects_from_json(folder_name + '\\' + file)
    images_description.append(file + '\n' + LD.location_description(data[0], data[1], data[2]))


for img in images_description:
    print(img)
