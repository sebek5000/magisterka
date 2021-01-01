import common
import numpy as np

# TODO do it for all files in directory
json_file = 'json/sheep.txt'

data = common.read_objects_from_json(json_file)

height = data[0]
width = data[1]
objects = data[2]
sorted_objects = []

for obj in objects:
    sorted_objects.append([obj.name, obj.x, obj.x + obj.width, obj.y, obj.y + obj.height])

sorted_objects.sort(key=lambda p: p[1], reverse=True)

new_objects = []
repeats = []
temp = []
name = ''
for so in sorted_objects:
    if so[0] != name:
        repeats.append(temp)
        temp = []
        name = so[0]
    temp.append(so)
repeats.append(temp)
repeats.remove([])

def merge(objects):
    objects = np.array(objects)
    x1 = min(objects[:, 1])
    x2 = max(objects[:, 2])
    y1 = min(objects[:, 3])
    y2 = max(objects[:, 4])
    return common.Object('group of '+ objects[0][0], x1, y1, float(x2) - float(x1), float(y2) - float(y1))


# TODO For the tme being there are all objects with the same name processed, need to choose correct ones
for r in repeats:
    if len(r) > 1:
        new_objects.append(merge(r))
    else:
        new_objects.append(common.Object(r[0][0], r[0][1], r[0][3], r[0][2]-r[0][1], r[0][4] - r[0][3]))
for obj in new_objects:
    print(obj)

common.save_objects_to_json(height, width, new_objects, 'json/sheepChanged.txt')
