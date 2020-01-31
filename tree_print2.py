import numpy as np
a=np.random.randint(0,99,(7))

import math
from PIL import Image,ImageDraw,ImageFont

def print_tree(tree):
    def get_node_x_locations(tree_height,im_size):
        locations = np.zeros(2**tree_height)
        items_in_last_row = 2**(tree_height - 1)
        print("items_in_last_row: " + str(items_in_last_row))
        pixels_per_entry = im_size / (items_in_last_row + 1)
        print("pixels_per_entry: " + str(pixels_per_entry))
        j=0
        for i in range(items_in_last_row,locations.size):
            locations[i]=j*pixels_per_entry
            j+=1
        index_first_item_last_row = items_in_last_row-1
        print("index_first_item_last_row: " + str(index_first_item_last_row))
        for i in range(index_first_item_last_row-1,-1,-1):
            parentA = (i+1)*2
            parentB = (i+1)*2+1
            locations[i] = (locations[parentA]+locations[parentB])/2
        return locations
    if str(type(tree))=="<class 'numpy.ndarray'>":
        tree=list(tree)
    #
    print("tree:\n" + str(tree))
    font_location = 'fonts/segoeuib.ttf'
    font = ImageFont.truetype(font_location, 20)
    #
    height = int(math.log(len(tree))/math.log(2))+1
    print("height: " + str(height))
    tree_width = 2**(height-1)
    image_size = tree_width * 60
    image = Image.new("RGB",(image_size,image_size))
    draw = ImageDraw.Draw(image)
    #
    pixels_per_row = image_size / (height + 1)
    x_locations = get_node_x_locations(height,image_size)
    print("x_locations:\n" + str(x_locations))
    for i in range(len(tree)):
        row = int(math.log(i+1)/math.log(2))
        entry_position = (x_locations[i], row * pixels_per_row)
        print("entry_position: " + str(entry_position))
        draw.text(entry_position,str(tree[i]),font=font,fill='green')
        image.save("tree.png")
        input("check it out, y'all")
    image.save("tree.png")

print_tree(a)
