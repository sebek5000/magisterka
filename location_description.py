# This file is used to create a description of bounding boxes on the picture found by YOLOv3
# described in a json file.

import common
# read_json = common.read_objects_from_json('json/street.txt')
# field_height = read_json[0]
# field_width = read_json[1]
# objects = read_json[2]

def location_description(field_height, field_width, objects):
    # Properties - name, saliency(0-1), argument_type, mem_values - values for the membership function,
    # sentence - the description
    # TODO I assumed that all are trapezoid membership function
    # TODO change description of those properties
    class Property:
        def __init__(self, name, saliency, argument_type, mem_values, sentence):
            self.name = name
            self.saliency = saliency
            self.argument_type = argument_type
            self.mem_values = mem_values
            self.sentence = sentence


    # Add properties:
    prop1 = Property("left edge", 0.9, 'b_l', [-2, -2, -1, -0.85], "Przy lewej krawędzi.")
    prop2 = Property("left", 0.8, 'b_l', [-10, -0.9, -0.6, 0], "W lewej części")
    prop3 = Property("length center", 0.9, 'c_lr', [-0.2, -0.05, 0.05, 0.2], "Na środku szerokości")
    prop4 = Property("right", 0.8, 'b_r', [0, 0.6, 0.9, 10], "Z prawej")
    prop5 = Property("right edge", 0.9, 'b_r', [0.85, 1, 2, 2], "Przy prawej krawędzi")
    prop6 = Property("top egde", 0.7, 'b_t', [-2, -2, -1, -0.85], "Przy górnej krawędzi")
    prop7 = Property("top", 0.5, 'b_t', [-10, -0.9, -0.6, 0], "Na górze")
    prop8 = Property("center height", 0.8, 'c_tb', [-0.2, -0.05, 0.05, 0.2], "Na środku wysokości")
    prop9 = Property("bottom", 0.5, 'b_b', [0, 0.6, 0.9, 10], "Na dole")
    prop10 = Property("bottom edge", 0.7, 'b_b', [0.85, 1, 2, 2], "Przy dolnej krawędzi")
    properties = [prop1, prop2, prop3, prop4, prop5, prop6, prop7, prop8, prop9, prop10]

    # Add relations (they are like properties)
    rel1 = Property("on the right", 0.8, 'd_lr', [0, 0.01, 0.5, 2], "Po prawej stronie od")
    rel2 = Property("on he left", 0.8, 'd_lr', [-2, -0.5, -0.01, 0], "Po lewej stronie od")
    rel3 = Property("above", 0.8, 'd_tb', [-2, -0.5, -0.01, 0], "Powyżej")
    rel4 = Property("below", 0.8, 'd_tb', [0, 0.01, 0.5, 2], "Poniżej")
    relations = [rel1, rel2, rel3, rel4]


    # Rules - name, saliency(0-1), prop1, prop2 - properties that need to be true to this rule to activate,
    # operator - operator that joins two properties, sentence - the description
    # TODO I assumed that all are trapezoid membership function
    # TODO change description of those properties
    class Rule:
        def __init__(self, name, saliency, prop1, prop2, operator, sentence):
            self.name = name
            self.saliency = saliency
            self.prop1 = prop1
            self.prop2 = prop2
            self.operator = operator
            self.sentence = sentence


    # Add rules
    rule1 = Rule("center", 1, prop3.name, prop8.name, "min", "Na środku")
    rule2 = Rule("top left corner", 1, prop1.name, prop6.name, "min", "Lewy, górny narożnik")
    rule3 = Rule("top right corner", 1, prop5.name, prop10.name, "min", "Prawy, górny narożnik")
    rule4 = Rule("bottom right corner", 1, prop5.name, prop10.name, "min", "Prawy, dolny narożnik")
    rule5 = Rule("bottom left corner", 1, prop1.name, prop10.name, "min", "Lewy, dolny narożnik")
    rule6 = Rule("top left", 1, prop2.name, prop7.name, "min", "Lewa, górna część")
    rule7 = Rule("top right", 1, prop4.name, prop7.name, "min", "Prawa, górna część")
    rule8 = Rule("bottom right", 1, prop4.name, prop9.name, "min", "Prawa, dolna część")
    rule9 = Rule("bottom left", 1, prop2.name, prop9.name, "min", "Lewa, dolna część")
    rules = [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9]


    # Normalize objects properties by the size of the image
    for obj in objects:
        obj.boundary_left = 2 * obj.x / field_width - 1
        obj.boundary_right = 2 * (obj.x + obj.width) / field_width - 1
        obj.boundary_top = 2 * obj.y / field_height - 1
        obj.boundary_bottom = 2 * (obj.y + obj.height) / field_height - 1
        obj.size = (obj.width / field_width) * (obj.height / field_height)  # saliency


    # Calculate membership function x value based on normalized properties of the object
    def membership_function_x_value(type, obj, obj2):
        if type == 'b_l':  # left side
            return obj.boundary_left
        elif type == 'b_r':  # right side
            return obj.boundary_right
        elif type == 'c_lr':  # center of width
            return (obj.boundary_left + obj.boundary_right) / 2
        elif type == 'b_t':  # top
            return obj.boundary_top
        elif type == 'b_b':  # bottom
            return obj.boundary_bottom
        elif type == 'c_tb':  # center of height
            return (obj.boundary_top + obj.boundary_bottom) / 2
        elif type == 'd_lr':  # distance between width centroids
            return (obj.boundary_right + obj.boundary_left) / 2 - (obj2.boundary_right + obj2.boundary_left) / 2
        elif type == 'd_tb':  # distance between height centroids
            return (obj.boundary_top + obj.boundary_bottom) / 2 - (obj2.boundary_top + obj2.boundary_bottom) / 2
        elif type == 'd':
            print("Not supported")
            return 7000
        else:
            print("Something went wrong during calculating membership x value;/")
            return -7100


    # Calculate membership y value based on x value and the membership function
    def membership_y_value(property, value):
        if value < property.mem_values[0]:
            return 0
        elif value < property.mem_values[1]:
            return (value - property.mem_values[0]) / (property.mem_values[1] - property.mem_values[0])
        elif value < property.mem_values[2]:
            return 1
        elif value < property.mem_values[3]:
            return (property.mem_values[3] - value) / (property.mem_values[3] - property.mem_values[2])
        else:
            return 0


    # Membership Value Function of an object to specific property
    obj_prop = []
    for prop in properties:
        temp = []
        for obj in objects:
            temp.append(membership_y_value(prop, membership_function_x_value(prop.argument_type, obj, 0)))
        obj_prop.append(temp)

    # Membership Value Function of two objects to specific relation
    obj_rel = []
    for rel in relations:
        tempOutside = []
        for objOutside in objects:
            tempInside = []
            for objInside in objects:
                tempInside.append(
                    membership_y_value(rel, membership_function_x_value(rel.argument_type, objOutside, objInside)))
            tempOutside.append(tempInside)
        obj_rel.append(tempOutside)


    # Add predicates - name, certainty factor, is_used, number of object, number of second object (for relations only),
    # number of property/relation, membership value
    pred = []
    for i in range(len(objects)):
        for j in range(len(properties)):
            if obj_prop[j][i] > 0:
                temp = [properties[j].name, obj_prop[j][i] * objects[i].size * properties[j].saliency, 0, i, -1, j,
                        obj_prop[j][i]]
                pred.append(temp)

        for k in range(len(objects)):
            for j in range(len(relations)):
                if obj_rel[j][i][k] > 0:
                    temp = [relations[j].name, obj_rel[j][i][k] * objects[i].size * relations[j].saliency, 0, i, k, j,
                            obj_rel[j][i][k]]
                    pred.append(temp)

    print(pred)

    for i in range(len(rules)):
        for j in range(len(pred)):
            if pred[j][0] == rules[i].prop1:
                obj_found = pred[j][3]
                for k in range(len(pred)):
                    if pred[k][0] == rules[i].prop2 and pred[k][3] == obj_found:
                        if pred[j][6] != 0 and pred[k][6] != 0:
                            ruleobj_cf = min(pred[j][6], pred[k][6])  # TODO Na razie zawsze jest tam minimum
                            temp = [rules[i].name, ruleobj_cf * objects[obj_found].size * rules[i].saliency, 0, obj_found,
                                    -2, i, ruleobj_cf]
                            pred.append(temp)

    # Sort
    pred.sort(key=lambda p: p[1], reverse=True)
    print(pred)

    # Predicate selection
    used = []
    for obj in objects:
        used.append(0)

    for i in range(len(pred)):
        if pred[i][4] < 0:
            if used[pred[i][3]] < 1:  # To może być zmienna
                used[pred[i][3]] = used[pred[i][3]] + 1
                pred[i][2] = 1
        else:
            if used[pred[i][3]] < 1 and used[pred[i][4]] == 1:
                used[pred[i][3]] = used[pred[i][3]] + 1
                pred[i][2] = 1
    pred_out = []
    for i in range(len(pred)):
        if pred[i][1] > 0 and pred[i][2] == 1:
            pred_out.append(pred[i])


    # Print sentences
    # TODO make them more like a sentence
    desc = []
    for i in range(len(pred_out)):
        if pred_out[i][4] == -1:
            sentence = objects[pred_out[i][3]].name + " " + properties[pred_out[i][5]].sentence
        elif pred_out[i][4] == -2:
            sentence = objects[pred_out[i][3]].name + " " + rules[pred_out[i][5]].sentence
        else:
            sentence = objects[pred_out[i][3]].name + " " + relations[pred_out[i][5]].sentence + " " + objects[
                pred_out[i][4]].name
        desc.append(sentence)
    TEXT = ''
    for description in desc:
        print(description)
        TEXT = TEXT + description + '\n'
    return TEXT

# location_description(field_height, field_width, objects)