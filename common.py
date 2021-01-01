import json

# Objects that are represented by bounding boxes in the picture, x and y are coordinates of the upper left vertex,
# name is the label of the class
class Object:
    def __init__(self, name, x, y, width, height):
        self.name = name
        self.x = float(x)
        self.y = float(y)
        self.width = float(width)
        self.height = float(height)
        self.width_center = (self.x + self.width)/2
        self.height_center = (self.y + self.height)/2


# Read height and width of image and objects from json file
def read_objects_from_json(json_file):
    with open(json_file) as json_file:
        data = json.load(json_file)
    field_height = data['picture_height']
    field_width = data['picture_width']
    objects = []
    for obj in data['objects']:
        objects.append(Object(obj['name'], obj['x'], obj['y'], obj['width'], obj['height']))
    return [field_height, field_width, objects]


def save_objects_to_json(height, width, objects, json_name):
    data = {}
    data['objects'] = []
    for obj in objects:
        data['objects'].append({
            'name': obj.name,
            'x': "%.5f" % obj.x,
            'y': "%.5f" % obj.y,
            'width': "%.5f" % obj.width,
            'height': "%.5f" % obj.height
        })
    data['picture_height'] = height
    data['picture_width'] = width
    with open(json_name, "w") as outfile:
        json.dump(data, outfile)