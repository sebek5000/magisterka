import common
import location_description as LD
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib.ticker import NullLocator
from tkinter import *
from PIL import ImageTk, Image

size_of_movement = 100 # how much to move up, left, up or down the object
percentage_of_size_change = 10 # how much enlarge, reduce the object
chosen_object = 0 # currently chosen object's index
new_name = "new_object" # name for new object

# Read starting "picture" from json
read_json = common.read_objects_from_json('json/interactive.txt')
field_height = read_json[0]
field_width = read_json[1]
objects = read_json[2]


# Start TK field
root = Tk()
root.geometry("1000x700+300+150")
root.resizable(width=True, height=True)
img = Image.open('json_box.png')
img = img.resize((400, 400), Image.ANTIALIAS)
img = ImageTk.PhotoImage(img)
panel = Label(root, image=img)
panel.image = img
# text field, https://effbot.org/tkinterbook/pack.htm
text_widget = Label(root, text='DUPA')
text_widget.pack(side=BOTTOM)

# TODO RuntimeWarning: More than 20 figures have been opened. Figures created through the pyplot interface
#  (`matplotlib.pyplot.figure`) are retained until explicitly closed and may consume too much memory.
#  (To control this warning, see the rcParam `figure.max_open_warning`). plt.figure()


# refresh image after change from png file
def refresh_image():
    global text_widget
    image = Image.open('json_box.png')
    image = image.resize((400, 400), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(image)
    panel.configure(image=image)
    panel.image = image
    text_widget['text'] = LD.location_description(field_height, field_width, objects)




# draw changes in the png file
def draw():
    imgToDraw = np.array(Image.new('RGB', (field_width, field_height)))
    plt.figure()
    fig, ax = plt.subplots(1)
    ax.imshow(imgToDraw)
    for obj in objects:
        plt.text(
            float(obj.x),
            float(obj.y),
            s=obj.name,
            color="white",
            verticalalignment="top",
            bbox={"color": 'red', "pad": 0},
        )
        edgecolor = 'blue'
        if objects[chosen_object] == obj:
            edgecolor = 'yellow'
        bbox = patches.Rectangle((float(obj.x), float(obj.y)), float(obj.width), float(obj.height),
                                 linewidth=2, edgecolor=edgecolor, facecolor="none")
        ax.add_patch(bbox)
    plt.axis("off")
    plt.gca().xaxis.set_major_locator(NullLocator())
    plt.gca().yaxis.set_major_locator(NullLocator())
    plt.savefig(f"json_box.png", bbox_inches="tight", pad_inches=0.0)
    plt.close()


# Options to manipulate objects on screen
def up():
    objects[chosen_object].y = objects[chosen_object].y - size_of_movement
    draw()
    common.save_objects_to_json(field_height, field_width, objects, 'json/interactive.txt')
    # panel.pack_forget()
    refresh_image()


def down():
    objects[chosen_object].y = objects[chosen_object].y + size_of_movement
    draw()
    common.save_objects_to_json(field_height, field_width, objects, 'json/interactive.txt')
    refresh_image()


def left():
    objects[chosen_object].x = objects[chosen_object].x - size_of_movement
    draw()
    common.save_objects_to_json(field_height, field_width, objects, 'json/interactive.txt')
    refresh_image()


def right():
    objects[chosen_object].x = objects[chosen_object].x + size_of_movement
    draw()
    common.save_objects_to_json(field_height, field_width, objects, 'json/interactive.txt')
    refresh_image()


def next():
    global chosen_object
    if chosen_object == len(objects) - 1:
        chosen_object = 0
    else:
        chosen_object = chosen_object + 1
    draw()
    refresh_image()

# TODO think about have constant middle, not upper-left corner when changing size
def enlarge():
    objects[chosen_object].width = objects[chosen_object].width * ((100 + percentage_of_size_change)/100)
    objects[chosen_object].height = objects[chosen_object].height * ((100 + percentage_of_size_change) / 100)
    draw()
    common.save_objects_to_json(field_height, field_width, objects, 'json/interactive.txt')
    refresh_image()


def reduce():
    objects[chosen_object].width = objects[chosen_object].width * ((100 - percentage_of_size_change)/100)
    objects[chosen_object].height = objects[chosen_object].height * ((100 - percentage_of_size_change) / 100)
    draw()
    common.save_objects_to_json(field_height, field_width, objects, 'json/interactive.txt')
    refresh_image()


def add():
    global new_name
    new_object = common.Object(new_name, 0, 0, 100, 100)
    objects.append(new_object)
    draw()
    common.save_objects_to_json(field_height, field_width, objects, 'json/interactive.txt')
    refresh_image()
    new_name = new_name + "1"


def delete():
    global chosen_object
    objects.pop(chosen_object)
    # if len(objects) == 0:
    #     root.abort()
    if chosen_object == len(objects) - 1:
        chosen_object = 0
    draw()
    common.save_objects_to_json(field_height, field_width, objects, 'json/interactive.txt')
    refresh_image()


# TODO: change position of buttons
btn = Button(root, text='góra', command=up).pack(side = LEFT)
btn1 = Button(root, text='dół', command=down).pack(side = LEFT)
btn2 = Button(root, text='lewo', command=left).pack(side = LEFT)
btn3 = Button(root, text='prawo', command=right).pack(side = LEFT)
btn4 = Button(root, text='następny', command=next).pack(side = LEFT)
btn5 = Button(root, text='powiększ', command=enlarge).pack(side = LEFT)
btn6 = Button(root, text='pomniejsz', command=reduce).pack(side = LEFT)
btn7 = Button(root, text='dodaj', command=add).pack(side = LEFT)
btn8 = Button(root, text='usuń', command=delete).pack(side = LEFT)
panel.pack()
# draw beginning state of the picture
draw()
refresh_image()


# start field
root.mainloop()
# TODO how to turn it off after closing?
# based on:
# https://stackoverflow.com/questions/10133856/how-to-add-an-image-in-tkinter
# #https://www.c-sharpcorner.com/blogs/basics-for-displaying-image-in-tkinter-python

