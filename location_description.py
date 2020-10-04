#objects
#TODO Read them from file


class Object:
    def __init__(self, name, x, y, length, height):
        self.name = name
        self.x = x
        self.y = y
        self.length = length
        self.height = height


# A = Object("A", 5, 15, 30, 15)
# B = Object("B", 45, 150, 90, 25)
# C = Object("C", 200, 115, 80, 55)
# field_height = 400
# field_length = 400

#Objects from this picture:
# (0) Image: 'data/samples\dog.jpg'
#  bike at 144.09793, 568.79895, 113.62761, 447.58099
#  dog at 129.81325, 314.50992, 221.97189, 522.70416
# truck at 468.16602, 688.88599, 83.17181, 170.87808


field_height = 600
field_length = 700

A = Object("rower", 144.09793, 113.62761, 568.79895 - 144.09793, 447.58099 - 113.62761)
B = Object("pies", 129.81325, 221.97189, 314.50992 - 129.81325, 522.70416 - 221.97189)
C = Object("ciężarówka", 468.16602, 83.17181, 688.88599 - 468.16602, 170.87808 - 83.17181)

objects = []
objects.append(A)
objects.append(B)
objects.append(C)




#Funkcje przynaleznosci
#TODO zakladam, ze wszystkie beda trapezami


class Property:
    def __init__(self, name, saliency, argument_type, mem_values, sentence):
        self.name = name
        self.saliency = saliency
        self.argument_type = argument_type
        self.mem_values = mem_values
        self.sentence = sentence


#Add properties:
prop1 = Property("left edge", 0.9, 'b_l', [-2, -2, -1, -0.85], "Przy lewej krawędzi.")
prop2 = Property("left", 0.8, 'b_l', [-10,-0.9,-0.6,0], "W lewej części")
prop3 = Property("length center", 0.9, 'c_lr', [-0.2,-0.05,0.05,0.2], "Na środku szerokości")
prop4 = Property("right", 0.8, 'b_r', [0,0.6,0.9,10], "Z prawej")
prop5 = Property("right edge", 0.9, 'b_r', [0.85,1,2,2], "Przy prawej krawędzi")
prop6 = Property("top egde", 0.7, 'b_t', [-2,-2,-1,-0.85], "Przy górnej krawędzi")
prop7 = Property("top", 0.5, 'b_t', [-10,-0.9,-0.6,0], "Na górze")
prop8 = Property("center height",0.8,'c_tb', [-0.2,-0.05,0.05,0.2], "Na środku wysokości")
prop9 = Property("bottom", 0.5, 'b_b', [0,0.6,0.9,10], "Na dole")
prop10 = Property("bottom edge", 0.7, 'b_b', [0.85,1,2,2], "Przy dolnej krawędzi")
properties = []
properties.append(prop1)
properties.append(prop2)
properties.append(prop3)
properties.append(prop4)
properties.append(prop5)
properties.append(prop6)
properties.append(prop7)
properties.append(prop8)
properties.append(prop9)
properties.append(prop10)

#Add_relations (they are like properties)
rel1 = Property("on the right", 0.8, 'd_lr', [0,0.01,0.5,2], "Po prawej stronie od")
rel2 = Property("on he left", 0.8, 'd_lr', [-2,-0.5,-0.01,0], "Po lewej stronie od")
rel3 = Property("above", 0.8, 'd_tb', [-2,-0.5,-0.01,0], "Powyżej")
rel4 = Property("below", 0.8, 'd_tb', [0,0.01,0.5,2], "Poniżej")
relations  = []
relations.append(rel1)
relations.append(rel2)
relations.append(rel3)
relations.append(rel4)
class Rule:
    def __init__(self, name, saliency, prop1, prop2, operator, sentence):
        self.name = name
        self.saliency = saliency
        self.prop1 = prop1
        self.prop2 = prop2
        self.operator = operator
        self.sentence = sentence

rule1 = Rule("center", 1, prop3.name, prop8.name, "min", "Na środku")
rule2 = Rule("top left corner", 1, prop1.name, prop6.name, "min", "Lewy, górny narożnik")
rule3 = Rule("top right corner", 1, prop5.name, prop10.name, "min", "Prawy, górny narożnik")
rule4 = Rule("bottom right corner", 1, prop5.name, prop10.name, "min", "Prawy, dolny narożnik")
rule5 = Rule("bottom left corner", 1, prop1.name, prop10.name,"min", "Lewy, dolny narożnik")
rule6 = Rule("top left", 1, prop2.name, prop7.name, "min", "Lewa, górna część")
rule7 = Rule("top right", 1, prop4.name,prop7.name, "min", "Prawa, górna część")
rule8 = Rule("bottom right", 1, prop4.name, prop9.name, "min", "Prawa, dolna część")
rule9 = Rule("bottom left", 1, prop2.name, prop9.name, "min", "Lewa, dolna część")


rules = []
rules.append(rule1)
rules.append(rule2)
rules.append(rule3)
rules.append(rule4)
rules.append(rule5)
rules.append(rule6)
rules.append(rule7)
rules.append(rule8)
rules.append(rule9)

for obj in objects:
    obj.boundary_left = 2*obj.x/field_length - 1
    obj.boundary_right = 2 * (obj.x + obj.length )/ field_length - 1
    obj.boundary_top = 2 * obj.y / field_height - 1
    obj.boundary_bottom = 2 * (obj.y + obj.height) / field_height - 1
    obj.size = (obj.length/field_length)*(obj.height/field_height)#saliency

def membership_function_x_value(type, obj, obj2): ##rename_it
    if type == 'b_l':
        return obj.boundary_left
    elif type == 'b_r':
        return obj.boundary_right
    elif type == 'c_lr':
        return (obj.boundary_left + obj.boundary_right)/2
    elif type == 'b_t':
        return obj.boundary_top
    elif type == 'b_b':
        return obj.boundary_bottom
    elif type == 'c_tb':
        return (obj.boundary_top + obj.boundary_bottom)/2
    elif type == 'd_lr':
        return (obj.boundary_right + obj.boundary_left)/2 - (obj2.boundary_right + obj2.boundary_left)/2
    elif type == 'd_tb':
        return (obj.boundary_top + obj.boundary_bottom)/2 - (obj2.boundary_top + obj2.boundary_bottom)/2
    elif type == 'd':
        print("Nieobsługiwane")
        return 7000
    else:
        print("Coś poszło nie tak ;/")
        return -7100

def membership_y_value(property, value):
    if value < property.mem_values[0]:
        return 0
    elif value < property.mem_values[1]:
        return (value - property.mem_values[0])/(property.mem_values[1]-property.mem_values[0])
    elif value < property.mem_values[2]:
        return 1
    elif value < property.mem_values[3]:
        return (property.mem_values[3] - value)/(property.mem_values[3]-property.mem_values[2])
    else:
        return 0


#TODO omijamy położenie względem obiektów (wartość 0 w drugim obiekcie)

obj_prop = []
for prop in properties:
    temp = []
    for obj in objects:
        temp.append(membership_y_value(prop, membership_function_x_value(prop.argument_type, obj, 0)))
    obj_prop.append(temp)

#print(obj_prop)

obj_rel = []
for rel in relations:
    tempOutside = []
    for objOutside in objects:
        tempInside = []
        for objInside in objects:
            tempInside.append(membership_y_value(rel, membership_function_x_value(rel.argument_type, objOutside, objInside)))
        tempOutside.append(tempInside)
    obj_rel.append(tempOutside)

#print(obj_rel)
#print (obj_prop[0][1])
pred = []

#counter = 0#table starts from 0
for i in range(len(objects)):
    for j in range(len(properties)):
        if obj_prop[j][i] >0:
            temp = []
            temp.append(properties[j].name)#nazwa zamiast id
            temp.append(obj_prop[j][i] * objects[i].size * properties[j].saliency)
            temp.append(0)
            temp.append(i)
            temp.append(-1)
            temp.append(j)
            temp.append(obj_prop[j][i])
            pred.append(temp)
            #counter = counter + 1

    for k in range(len(objects)):
        for j in range(len(relations)):
            if obj_rel[j][i][k] > 0:
                temp = []
                temp.append(relations[j].name) #nazwa zamiast id
                temp.append(obj_rel[j][i][k] * objects[i].size * relations[j].saliency)
                temp.append(0)
                temp.append(i)
                temp.append(k)
                temp.append(j)
                temp.append(obj_rel[j][i][k])
                pred.append(temp)
                #counter = counter+ 1

print(pred)#TODO do poprawienia, bo coś jest chyba nie tak

#TODO Add Rule Predicates

#rule_pred = [] Od razu dodam do pred
for i in range(len(rules)):
    for j in range(len(pred)):
        if pred[j][0] == rules[i].prop1:
            obj_found = pred[j][3]
            for k in range(len(pred)):
                if pred[k][0] == rules[i].prop2 and pred[k][3] == obj_found:
                    if pred[j][6] != 0 and pred[k][6] != 0:
                        ruleobj_cf = min(pred[j][6], pred[k][6])#TODO Na razie zawsze jest tam minimum
                        temp = []
                        temp.append(rules[i].name)
                        temp.append(ruleobj_cf * objects[obj_found].size * rules[i].saliency)
                        temp.append(0)
                        temp.append(obj_found)
                        temp.append(-2)
                        temp.append(i)
                        temp.append(ruleobj_cf)
                        pred.append(temp)


# for predicate in pred:
#     print(predicate)

desc = []
for i in range(len(pred)):
    if pred[i][4] == -1:
        zdanie = objects[pred[i][3]].name + " " + properties[pred[i][5]].sentence
    elif pred[i][4] == -2:
        zdanie = objects[pred[i][3]].name + " " + rules[pred[i][5]].sentence
    else:
        zdanie = objects[pred[i][3]].name + " " + relations[pred[i][5]].sentence + " " + objects[pred[i][4]].name
    desc.append(zdanie)


for description in desc:
    print(description)

    #TODO Select predicates



