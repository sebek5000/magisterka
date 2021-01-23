import common
import numpy as np
import os


def group_all_files(directory):

    arr = [os.path.basename(x) for x in os.listdir(directory)]

    for json_file in arr:
        json_file = json_file.replace('\\', '/')
        data = common.read_objects_from_json(directory + '\\' + json_file)

        height = data[0]
        width = data[1]
        objects = data[2]
        sorted_objects = []

        for obj in objects:
            sorted_objects.append([obj.name, obj.x, obj.x + obj.width, obj.y, obj.y + obj.height])

        sorted_objects.sort(key=lambda p: p[0], reverse=True)

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
        repeats.remove([])  # delete empty array

        def merge(objects):
            objects = np.array(objects)
            x1 = min(objects[:, 1])
            x2 = max(objects[:, 2])
            y1 = min(objects[:, 3])
            y2 = max(objects[:, 4])
            name = objects[0][0]
            if not name.startswith('group of '):
                name = 'group of ' + name
            return [name, x1, x2, y1, y2]

        def are_objects_close(obj1, obj2):
            if abs(0.5*(float(obj1[2]) + float(obj1[1])) - 0.5*(float(obj2[2]) + float(obj2[1]))) < width/3 and abs(0.5*(float(obj1[4]) + float(obj1[3])) - 0.5*(float(obj2[4]) + float(obj2[3]))) < height/3:
                return True
            return False

        def choose_objects_to_merge(objects):
            finish = False
            while not finish:
                for obj in objects:
                    merged = False
                    for obj2 in objects:
                        if obj != obj2 and are_objects_close(obj, obj2):
                            objects_to_merge = [obj, obj2]
                            objects.append(merge(objects_to_merge))
                            objects.remove(obj)
                            objects.remove(obj2)
                            merged = True
                            break
                    if merged:
                        finish = False
                        break
                    finish = True

            for obj in objects:
                new_objects.append(common.Object(obj[0], obj[1], obj[3], float(obj[2]) - float(obj[1]), float(obj[4]) - float(obj[3])))

        for r in repeats:
            if len(r) > 1:
                choose_objects_to_merge(r)
            else:
                new_objects.append(common.Object(r[0][0], r[0][1], r[0][3], r[0][2]-r[0][1], r[0][4] - r[0][3]))
        for obj in new_objects:
            print(obj)

        common.save_objects_to_json(height, width, new_objects, directory + '\\' + json_file)
