
import random
import math
# a=[random.randint(100,999) for i in range(24)]
# a=[100+i for i in range(31)]
def treeprint(a):
    if str(type(a))=="<class 'numpy.ndarray'>":
        a=list(a)
    height = math.log(len(a))/math.log(2)+1
    height = int(height)
    spacing = 4
    spaces_per_row = spacing * 2**(height - 1)
    index = 0
    the_str = ""

    space_locations = None
    for row in range(height-1,-1,-1):
        row_str = ""
        line_location = 0
        len_of_full_bottom_row = int(2**(height-1))
        if space_locations is None:
            zeros_list = [0 for i in range(2**height-2**(height-1)-1)]
            space_locations = [i*spacing for i in range(len_of_full_bottom_row)]
            space_locations = zeros_list + space_locations
        for entry in range(2**row-1,2**(row+1)-1):
            print("entry: "+str(entry))
            if entry < len(a):
                if row == height-1:
                    row_str += " "
                    line_location += 1
                    row_str += str(a[entry])
                    line_location += spacing
                else:
                    child_1_pos = space_locations[entry*2+1]
                    child_2_pos = space_locations[entry*2+2]
                    new_pos = int((child_1_pos + child_2_pos) / 2)
                    space_locations[entry]=new_pos
                    for i in range(new_pos-line_location):
                        row_str += " "
                        line_location += 1
                    row_str += str(a[entry])
                    line_location += (spacing - 1)
        row_str += "\n"
        the_str = row_str + the_str

    print(the_str)