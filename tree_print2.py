import numpy as np
# a=np.array([2,2,2,2,1,2,1,1,1,0,0,2,1,0,0,0,0,0,0,0,0,0,0,1,1])

import time
import math
from PIL import Image,ImageDraw,ImageFont

def print_tree(tree,suffix=0):
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
        shrink_factor = .2
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
        tree=np.trim_zeros(tree)
        tree_size = tree.size
        new_tree_size = int(2**(math.log(tree.size)/math.log(2)//1+1))
        new_tree = np.zeros(new_tree_size-1)
        new_tree[:tree_size]=tree        
        tree=new_tree.astype(np.int32)
        tree=list(tree)
    #
    font_location = 'fonts/segoeuib.ttf'
    font_size = 55
    font = ImageFont.truetype(font_location, font_size)
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
        entry_position = [x_locations[i] + buf, row * pixels_per_row + pixels_per_row]
        if tree[i]!=0:
            position = place_text(draw,entry_position,str(tree[i]))
        text_locations.append(entry_position)
        parent_node_index = (i-1)//2
        line_ends = [text_locations[parent_node_index],entry_position]
        if i > 0 and tree[i]!=0:
            line_ends = shrink_line(line_ends)
            line_ends = [line_ends[0]+9,line_ends[1]+25,line_ends[2]+9,line_ends[3]+25]
            draw.line(line_ends,fill='green',width=5)
    name = "tree_pics/tree"+str(suffix)+".png"
    image.save(name)


# print_tree(a)

