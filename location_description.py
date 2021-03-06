# This file is used to create a description of bounding boxes on the picture found by YOLOv3
# described in a json file.

import common

settings_file = "settings/test.txt"


def location_description(field_height, field_width, objects):
    # Properties - name, saliency(0-1), argument_type, mem_values - values for the membership function,
    # sentence - the description
    # assumed that all are trapezoid membership function
    class Property:
        def __init__(self, name, saliency, argument_type, mem_values, sentence):
            self.name = name
            self.saliency = saliency
            self.argument_type = argument_type
            self.mem_values = mem_values
            self.sentence = sentence

    f = open(settings_file, "r")
    property_lines = []
    relation_lines = []
    rule_lines = []
    kind_of_predicate = -1  # 0 - property, 1- relation, 2 - rule
    for x in f:
        if x.startswith('#'):
            kind_of_predicate = kind_of_predicate + 1
            continue
        if kind_of_predicate == 0:
            property_lines.append(x)
        elif kind_of_predicate == 1:
            relation_lines.append(x)
        elif kind_of_predicate == 2:
            rule_lines.append(x)
        else:
            print("Something went wrong in reading settings file!")

    properties = []
    relations = []
    rules = []
    for prop in property_lines:
        propParams = prop.split(',')
        properties.append(Property(propParams[0], float(propParams[1]), propParams[2],
                                   propParams[3].split(';'), propParams[4].replace('\n', '')))
    for rel in relation_lines:
        propParams = rel.split(',')
        relations.append(Property(propParams[0], float(propParams[1]), propParams[2],
                                  propParams[3].split(';'), propParams[4].replace('\n', '')))

    # Rules - name, saliency(0-1), prop1, prop2 - properties that need to be true to this rule to activate,
    # operator - operator that joins two properties, sentence - the description
    # assumed that all are trapezoid membership function
    class Rule:
        def __init__(self, name, saliency, prop1, prop2, operator, sentence):
            self.name = name
            self.saliency = saliency
            self.prop1 = prop1
            self.prop2 = prop2
            self.operator = operator
            self.sentence = sentence

    for rule in rule_lines:
        propParams = rule.split(',')
        rules.append(Rule(propParams[0], int(propParams[1]), properties[int(propParams[2])].name,
                          properties[int(propParams[3])].name, propParams[4], propParams[5].replace('\n', '')))

    # Normalize objects properties by the size of the image
    for obj in objects:
        obj.boundary_left = 2 * obj.x / field_width - 1
        obj.boundary_right = 2 * (obj.x + obj.width) / field_width - 1
        obj.boundary_top = 2 * obj.y / field_height - 1
        obj.boundary_bottom = 2 * (obj.y + obj.height) / field_height - 1
        obj.size = (obj.width / field_width) * (obj.height / field_height)  # saliency
        obj.width_center = (obj.boundary_right + obj.boundary_left)/2
        obj.height_center = (obj.boundary_bottom + obj.boundary_top)/2

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
        elif type == 'd_left':  # distance between A.right and B.left
            if obj2.boundary_right < obj.boundary_left or (obj.boundary_left < obj2.boundary_left and obj.boundary_right > obj2.boundary_right):
                return -5000
            return abs(obj2.boundary_left - obj.boundary_right) + abs(obj.height_center - obj2.height_center)
        elif type == 'd_right':  # distance between A.left and B.right
            if obj.boundary_left < obj2.boundary_right or (
                    obj.boundary_left < obj2.boundary_left and obj.boundary_right > obj2.boundary_right):
                return -5000
            return abs(obj.boundary_left - obj2.boundary_right) + abs(obj.height_center - obj2.height_center)
        elif type == 'd_below':  # distance between A.top and B.down
            if obj.boundary_bottom < obj2.boundary_top or (
                    obj.boundary_top < obj2.boundary_top and obj.boundary_bottom > obj2.boundary_bottom):
                return -5000
            return abs(obj.boundary_top - obj2.boundary_bottom) + abs(obj.width_center - obj2.width_center)
        elif type == 'd_above':  # distance between B.top and A.down
            if obj.boundary_top > obj2.boundary_bottom or (
                    obj.boundary_top < obj2.boundary_top and obj.boundary_bottom > obj2.boundary_bottom):
                return -5000
            return abs(obj2.boundary_top - obj.boundary_bottom) + abs(obj.width_center - obj2.width_center)
        elif type == 'd_inside':
            if obj2.boundary_left > obj.boundary_left or obj2.boundary_right < obj.boundary_right or obj2.boundary_top > obj.boundary_top or obj2.boundary_bottom < obj.boundary_bottom :
                return -5000
            return 0  # it should give the membership function value = 1
        elif type == 'd':
            print("Not supported")
            return 7000
        else:
            print("Something went wrong during calculating membership x value;/")
            return -7100

    # Calculate membership y value based on x value and the membership function
    def membership_y_value(property, value):
        if value < float(property.mem_values[0]):
            return 0
        elif value < float(property.mem_values[1]):
            return (value - float(property.mem_values[0])) / (
                    float(property.mem_values[1]) - float(property.mem_values[0]))
        elif value < float(property.mem_values[2]):
            return 1
        elif value < float(property.mem_values[3]):
            return (float(property.mem_values[3]) - value) / (
                    float(property.mem_values[3]) - float(property.mem_values[2]))
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
    rel_pred = []
    for i in range(len(objects)):
        for j in range(len(properties)):
            if obj_prop[j][i] > 0:
                temp = [properties[j].name, obj_prop[j][i] * objects[i].size * properties[j].saliency, 0, i, -1, j,
                        obj_prop[j][i]]
                pred.append(temp)

        for k in range(len(objects)):
            for j in range(len(relations)):
                if obj_rel[j][i][k] > 0 and i != k:
                    temp = [relations[j].name, obj_rel[j][i][k]* relations[j].saliency, 0, i, k, j, obj_rel[j][i][k]]
                    # deleted multiplying by size of object in relations
                    rel_pred.append(temp)

    for i in range(len(rules)):
        for j in range(len(pred)):
            if pred[j][0] == rules[i].prop1:
                obj_found = pred[j][3]
                for k in range(len(pred)):
                    if pred[k][0] == rules[i].prop2 and pred[k][3] == obj_found:
                        if pred[j][6] != 0 and pred[k][6] != 0:
                            ruleobj_cf = min(pred[j][6], pred[k][6])  # assumed it's min value
                            temp = [rules[i].name, ruleobj_cf * objects[obj_found].size * rules[i].saliency, 0,
                                    obj_found,
                                    -2, i, ruleobj_cf]
                            pred.append(temp)
    # Sort
    rel_pred.sort(key=lambda p: p[1], reverse=True)

    # for pr in rel_pred:  # pr[5]-> number of relations
    #     print(objects[pr[3]].name + " " + relations[pr[5]].sentence + " " + objects[pr[4]].name + " CF: " + str(pr[1]))

    # Sort
    pred.sort(key=lambda p: p[1], reverse=True)
    # print("sorted predicates:")
    # for pr in pred:
    #     if pr[4] == -1:
    #         print(objects[pr[3]].name + " " + properties[pr[5]].sentence + " CF: " + str(pr[1]))
    #     elif pr[4] == -2:
    #         print(objects[pr[3]].name + " " + rules[pr[5]].sentence + " CF: " + str(pr[1]))
    #     else:
    #         print(objects[pr[3]].name + " " + relations[pr[5]].sentence + " " + objects[pr[4]].name + " CF: " + str(
    #             pr[1]))

    def kindOfPredicate(pred):
        if pred[4] == -1:  # property
            if properties[pred[5]].argument_type == 'b_l' or properties[pred[5]].argument_type == 'c_lr' or properties[
                    pred[5]].argument_type == 'b_r':
                return 'X'
        if pred[4] == -2:  # rule
            if rules[pred[5]].name == 'width':
                return 'X'
            if rules[pred[5]].name == 'height':
                return 'Y'
            return 'BOTH'
        return 'Y'

    # Predicate selection
    usedX = []
    usedY = []
    for obj in objects:
        usedX.append(0)
        usedY.append(0)

    for i in range(len(pred)):
        if kindOfPredicate(pred[i]) == 'BOTH':
            if usedX[pred[i][3]] < 1 and usedY[pred[i][3]] < 1:
                usedX[pred[i][3]] = usedX[pred[i][3]] + 1
                usedY[pred[i][3]] = usedY[pred[i][3]] + 1
                pred[i][2] = 1
        elif kindOfPredicate(pred[i]) == 'X':
            if usedX[pred[i][3]] < 1:
                usedX[pred[i][3]] = usedX[pred[i][3]] + 1
                pred[i][2] = 1
        else:
            if usedY[pred[i][3]] < 1:
                usedY[pred[i][3]] = usedY[pred[i][3]] + 1
                pred[i][2] = 1
    pred_out = []
    for i in range(len(pred)):
        if pred[i][1] > 0 and pred[i][2] == 1:
            pred_out.append(pred[i])

    # Print sentences
    desc = []
    sentence = ''
    for i in range(len(pred_out)):
        if pred_out[i][4] == -1:  # predicate
            sentence = objects[pred_out[i][3]].name + " " + properties[pred_out[i][5]].sentence
        elif pred_out[i][4] == -2:  # rule
            sentence = objects[pred_out[i][3]].name + " " + rules[pred_out[i][5]].sentence
        sentence = sentence.capitalize()
        desc.append(sentence)

    usedRel = []
    for obj in objects:
        usedRel.append(0)

    # relations:
    for i in range(len(rel_pred)):
        # print("REL: " + str(rel_pred[i][1])) -> to print values for relations
        # Decided to use every object once (at least if there is an even number of them)
        if usedRel[rel_pred[i][3]] == 1 or usedRel[rel_pred[i][4]] == 1:
            continue
        sentence = objects[rel_pred[i][3]].name + " " + relations[rel_pred[i][5]].sentence + " " + objects[
            rel_pred[i][4]].name + '.'
        sentence = sentence.capitalize()
        usedRel[rel_pred[i][3]] = 1
        usedRel[rel_pred[i][4]] = 1
        desc.append(sentence)

    TEXT = ''
    for description in desc:
        TEXT = TEXT + description + '\n'
    return TEXT
