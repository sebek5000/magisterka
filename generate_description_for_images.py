import common
import location_description as LD
import os


def generate(directory):

    arr = os.listdir(directory)
    images_description = []

    for file in arr:
        data = common.read_objects_from_json(directory + '\\' + file)
        images_description.append(file.replace('.txt', '') + '\n' + LD.location_description(data[0], data[1], data[2]))

    for img in images_description:
        print(img)
