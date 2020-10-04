classLabels = []
#TODO: change names of variables żeby nie zwariować

class ObjectClass:
    def __init__(self, name, preposition, plural):
        self.name = name
        self.preposition = preposition
        self.plural = plural

classFile = open("classes.txt")
for line in classFile:
     words = line.split(",")
     classLabels.append(ObjectClass(words[0], words[1], words[2].rstrip()))
classFile.close()

def searchForALabel(name):
    for label in classLabels:
        if name == label.name:
            return label
    print("Something went wrong. The class hasn't been found: " + name)#TODO: Exception?

class Picture:
    def __init__(self, name):
        self.name = name
        self.labels = []

    def basicDescription(self):
        mergedLabels = self.labels.copy()
        isChange = True
        change = False
        while isChange == True and len(mergedLabels)!=0:
            for label in mergedLabels:
                for label2 in mergedLabels:
                    if label2 != label:
                        if label.objectsFoundLabel.name == label2.objectsFoundLabel.name:
                            label.number += label2.number
                            mergedLabels.remove(label2)
                            change = True
                            isChange = True
                            break
                    isChange = False
                if change == True:
                   change = False
                   break
        description = ""
        numberOfLabels = len(mergedLabels)
        counter = 0
        if numberOfLabels == 0:
            return "Nothing was found on the picture."
        if numberOfLabels == 1:
            if mergedLabels[0].number == 1:
                return "The picture shows " + mergedLabels[0].objectsFoundLabel.preposition + " " + mergedLabels[0].objectsFoundLabel.name + "."
            else:
                return "The picture shows " + str(mergedLabels[0].number) + " " + mergedLabels[0].objectsFoundLabel.plural + "."
        for label in mergedLabels:
            if counter == numberOfLabels -1:
                if label.number == 1:
                    description += (" and " + label.objectsFoundLabel.preposition + " " + label.objectsFoundLabel.name + ".")
                else:
                    description += (" and " + str(label.number) + " " + label.objectsFoundLabel.plural + ".")
            elif counter == numberOfLabels -2:
                if label.number == 1:
                    description += (label.objectsFoundLabel.preposition + " " + label.objectsFoundLabel.name)
                else:
                    description += (str(label.number) + " " + label.objectsFoundLabel.plural)
            else :
                if label.number == 1:
                    description += (label.objectsFoundLabel.preposition + " " + label.objectsFoundLabel.name + ", ")
                else:
                    description += (str(label.number) + " " + label.objectsFoundLabel.plural + ", ")
            counter += 1
        return "The picture shows " + description

class Label:
    def __init__(self, name, x1, x2, y1, y2):
        self.objectsFoundLabel = searchForALabel(name)
        self.number = 1
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2


f = open("data.txt")
tempName = ""
pictures = []
counter = -1
for x in f:
    if x.startswith("("):
        tempName = x.replace("data/samples\\", "")
        pictures.append(Picture(tempName))
        counter += 1
    else:
        line = x.split(" at ")
        line[0] = line[0].replace(" ", "", 1)
        nums = line[1].split(", ")
        nums[3] = nums[3].rstrip()
        pictures[counter].labels.append(Label(line[0], float(nums[0]), float(nums[1]), float(nums[2]), float(nums[3])))
f.close()

for x in pictures:
    print(x.name)
    print(x.basicDescription())

