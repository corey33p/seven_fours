import numpy as np
a=np.random.randint(0,99,(50))

import math
from PIL import Image,ImageDraw,ImageFont

def print_tree(tree):
    def get_node_x_locations(tree_height,im_size):
        locations = np.zeros(2**tree_height-1)
        items_in_last_row = 2**(tree_height - 1)
        pixels_per_entry = im_size / (items_in_last_row + 1)
        j=0
        for i in range(items_in_last_row-1,locations.size):
            locations[i]=j*pixels_per_entry
            j+=1
        index_first_item_last_row = items_in_last_row-1
        for i in range(index_first_item_last_row-1,-1,-1):
            childA = (i+1)*2-1
            childB = (i+1)*2
            locations[i] = (locations[childA]+locations[childB])/2
        return locations
    def place_text(draw,loc,text):
        w, h = draw.textsize(text)
        position = loc[0]-w/2,loc[1]-h/2
        draw.text(position,str(text),font=font,fill='green')
        return position
    def shrink_line(line_coordinates):
        # extend the line a bit to avoid gaps between the lines
        shrink_factor = .1
        rise= line_coordinates[1][1]-line_coordinates[0][1]
        run = line_coordinates[1][0]-line_coordinates[0][0]
        new_start_point_x = line_coordinates[0][0] + shrink_factor * run
        new_start_point_y = line_coordinates[0][1] + shrink_factor * rise
        new_end_point_x = line_coordinates[1][0] - shrink_factor * run
        new_end_point_y = line_coordinates[1][1] - shrink_factor * rise
        pseudo_coordinates=[new_start_point_x,new_start_point_y,
                            new_end_point_x,new_end_point_y]
        return pseudo_coordinates
    if str(type(tree))=="<class 'numpy.ndarray'>":
        tree=list(tree)
    #
    font_location = 'fonts/segoeuib.ttf'
    font = ImageFont.truetype(font_location, 40)
    #
    node_pix_size = 100
    height = int(math.log(len(tree))/math.log(2))+1
    tree_width = 2**(height-1)
    image_size = tree_width * node_pix_size
    image = Image.new("RGB",(image_size,image_size))
    draw = ImageDraw.Draw(image)
    #
    pixels_per_row = image_size / (height + 1)
    x_locations = get_node_x_locations(height,image_size)
    text_locations = []
    for i in range(len(tree)):
        row = int(math.log(i+1)/math.log(2))
        buf = node_pix_size / 2
        entry_position = [x_locations[i] + buf, row * pixels_per_row + buf]
        position = place_text(draw,entry_position,str(tree[i]))
        text_locations.append(position)
        parent_node_index = (i-1)//2
        line_ends = [text_locations[parent_node_index],position]
        if i > 0:
            line_ends = shrink_line(line_ends)
            line_ends = [_ + buf / 2 for _ in line_ends]
            draw.line(line_ends,fill='green',width=5)
    image.save("tree.png")

print_tree(a)
