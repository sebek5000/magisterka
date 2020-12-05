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

    f = open("settings/test.txt", "r")
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

    # # Add properties:
    # prop1 = Property("left edge", 0.9, 'b_l', [-2, -2, -1, -0.85], "is by the left edge.")
    # prop2 = Property("left", 0.8, 'b_l', [-10, -0.9, -0.6, 0], "is on the left side.")
    # prop3 = Property("length center", 0.9, 'c_lr', [-0.2, -0.05, 0.05, 0.2], "is in te middle of width.")
    # prop4 = Property("right", 0.8, 'b_r', [0, 0.6, 0.9, 10], "is on the right side.")
    # prop5 = Property("right edge", 0.9, 'b_r', [0.85, 1, 2, 2], "is by the right edge.")
    # prop6 = Property("top egde", 0.7, 'b_t', [-2, -2, -1, -0.85], "is by the top edge.")
    # prop7 = Property("top", 0.5, 'b_t', [-10, -0.9, -0.6, 0], "is on the top side.")
    # prop8 = Property("center height", 0.8, 'c_tb', [-0.2, -0.05, 0.05, 0.2], "is in the middle of height.")
    # prop9 = Property("bottom", 0.5, 'b_b', [0, 0.6, 0.9, 10], "is on the bottom side.")
    # prop10 = Property("bottom edge", 0.7, 'b_b', [0.85, 1, 2, 2], "is by the bottom edge.")
    # properties = [prop1, prop2, prop3, prop4, prop5, prop6, prop7, prop8, prop9, prop10]

    # Add relations (they are like properties)
    # rel1 = Property("on the right", 0.8, 'd_lr', [0, 0.01, 0.5, 2], "is to the right of")
    # rel2 = Property("on he left", 0.8, 'd_lr', [-2, -0.5, -0.01, 0], "is to the left of")
    # rel3 = Property("above", 0.8, 'd_tb', [-2, -0.5, -0.01, 0], "is above")
    # rel4 = Property("below", 0.8, 'd_tb', [0, 0.01, 0.5, 2], "is below")
    # relations = [rel1, rel2, rel3, rel4]

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

    for rule in rule_lines:
        propParams = rule.split(',')
        rules.append(Rule(propParams[0], int(propParams[1]), properties[int(propParams[2])].name,
                          properties[int(propParams[3])].name, propParams[4], propParams[5].replace('\n', '')))

    # # Add rules
    # rule1 = Rule("center", 1, properties[2].name, properties[7].name, "min", "is in the center.")
    # rule2 = Rule("top left corner", 1, properties[0].name, properties[5].name, "min", "is int top-left corner.")
    # rule3 = Rule("top right corner", 1, properties[4].name, properties[9].name, "min", "is in the top-right corner.")
    # rule4 = Rule("bottom right corner", 1, properties[4].name, properties[9].name, "min", "is in the bottom-right corner.")
    # rule5 = Rule("bottom left corner", 1, properties[0].name, properties[9].name, "min", "is in the bottom-left corner.")
    # rule6 = Rule("top left", 1, properties[1].name, properties[6].name, "min", "is on the top-left side.")
    # rule7 = Rule("top right", 1, properties[3].name, properties[6].name, "min", "is on the top-right side.")
    # rule8 = Rule("bottom right", 1, properties[3].name, properties[8].name, "min", "is on the bottom-right side.")
    # rule9 = Rule("bottom left", 1, properties[1].name, properties[8].name, "min", "is on the bottom-left side.")
    # rules = [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9]

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
                if obj_rel[j][i][k] > 0:
                    temp = [relations[j].name, obj_rel[j][i][k] * objects[i].size * relations[j].saliency, 0, i, k, j,
                            obj_rel[j][i][k]]
                    rel_pred.append(temp)

    for i in range(len(rules)):
        for j in range(len(pred)):
            if pred[j][0] == rules[i].prop1:
                obj_found = pred[j][3]
                for k in range(len(pred)):
                    if pred[k][0] == rules[i].prop2 and pred[k][3] == obj_found:
                        if pred[j][6] != 0 and pred[k][6] != 0:
                            ruleobj_cf = min(pred[j][6], pred[k][6])  # TODO Na razie zawsze jest tam minimum
                            temp = [rules[i].name, ruleobj_cf * objects[obj_found].size * rules[i].saliency, 0,
                                    obj_found,
                                    -2, i, ruleobj_cf]
                            pred.append(temp)
    # Sort
    rel_pred.sort(key=lambda p: p[1], reverse=True)
    rel_pred_out = []
    print("sorted rel predicates:")
    for pr in rel_pred:#pr[5]-> numer relacji
        for pr2 in rel_pred:
            if pr[5] == 0 or pr[5] == 1:
                if pr2[5] == 4 and pr2[3] == pr[3] and pr2[4] == pr[4]:
                    # print("pomnożę: " + objects[pr[3]].name + " " + relations[pr[5]].sentence + " " + objects[pr[4]].name + " CF: " + str(pr[1]) +
                    #       " i " + objects[pr2[3]].name + " " + relations[pr2[5]].sentence + " " + objects[pr2[4]].name + " CF: " + str(pr2[1]))
                    #Minimum jednak
                    pr[1] = min(pr[1], pr2[1])
                    pred.append(pr)
            if pr[5] == 2 or pr[5] == 3:
                if pr2[5] == 5 and pr2[3] == pr[3] and pr2[4] == pr[4]:
                    # print("pomnożę: " + objects[pr[3]].name + " " + relations[pr[5]].sentence + " " + objects[pr[4]].name + " CF: " + str(pr[1]) +
                    #       " i " + objects[pr2[3]].name + " " + relations[pr2[5]].sentence + " " + objects[pr2[4]].name + " CF: " + str(pr2[1]))
                    pr[1] = min(pr[1], pr2[1])
                    pred.append(pr)
                    # print(objects[pr[3]].name + " " + relations[pr[5]].sentence + " " + objects[pr[4]].name + " CF: " + str(pr[1]))

    # Sort
    pred.sort(key=lambda p: p[1], reverse=True)
    print("sorted predicates:")
    for pr in pred:
        if pr[4] == -1:
            print(objects[pr[3]].name + " " + properties[pr[5]].sentence + " CF: " + str(pr[1]))
        elif pr[4] == -2:
            print(objects[pr[3]].name + " " + rules[pr[5]].sentence + " CF: " + str(pr[1]))
        else:
            print(objects[pr[3]].name + " " + relations[pr[5]].sentence + " " + objects[pr[4]].name + " CF: " + str(
                pr[1]))

    # Predicate selection
    used = []
    for obj in objects:
        used.append(0)

    for i in range(len(pred)):
        # if pred[i][4] < 0:
        if used[pred[i][3]] < 1:  # To może być zmienna
           used[pred[i][3]] = used[pred[i][3]] + 1
           pred[i][2] = 1

        #TODO: what to do with the opposite rule?
        # else:
        #     if used[pred[i][3]] < 1:
        #         used[pred[i][3]] = used[pred[i][3]] + 1
        #         pred[i][2] = 1
    pred_out = []
    for i in range(len(pred)):
        if pred[i][1] > 0 and pred[i][2] == 1:
            pred_out.append(pred[i])

    # Print sentences
    # TODO make them more like a sentence
    desc = []
    for i in range(len(pred_out)):
        if pred_out[i][4] == -1: #predicate
            sentence = objects[pred_out[i][3]].name + " " + properties[pred_out[i][5]].sentence
        elif pred_out[i][4] == -2: #rule
            sentence = objects[pred_out[i][3]].name + " " + rules[pred_out[i][5]].sentence
        else: #relation
            sentence = objects[pred_out[i][3]].name + " " + relations[pred_out[i][5]].sentence + " " + objects[
                pred_out[i][4]].name
        desc.append(sentence)
    TEXT = ''
    for description in desc:
        # print(description)
        TEXT = TEXT + description + '\n'
    return TEXT

# location_description(field_height, field_width, objects)
