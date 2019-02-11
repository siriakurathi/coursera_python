"""
Clone of 2048 game.
"""

import poc_2048_gui    
import random
#import user34_0ROG5qaZZn_3

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.    
OFFSETS = {UP: (1, 0), 
           DOWN: (-1, 0), 
           LEFT: (0, 1), 
           RIGHT: (0, -1)} 
   
def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    # replace with your code
    result = []
    result_index = 0
    merged_last_tile = False
    for dummy_a in line:
        result.append(0)
    for temp_b in line:
        if temp_b!= 0:
            if result_index == 0:
                result[result_index] = temp_b
                result_index += 1
            elif result[result_index - 1] == temp_b and merged_last_tile == False:
                result[result_index - 1] += temp_b
                #result_index++
                merged_last_tile = True
            else:
                result[result_index] = temp_b
                merged_last_tile = False
                result_index += 1
            #result_index += 1  
    return result
    #line1 = [0,0,0,0]
    #return []

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        # replace with your code
        self.height = grid_height
        self.width = grid_width
        self.counter = 0
        self.reset()
        up_arr = []
        for dummy_a in range(self.width):
            up_arr.append((0,dummy_a))
        down_arr = []
        for dummy_a in range(self.width):
            down_arr.append((self.height-1,dummy_a))
        left_arr = []
        for dummy_a in range(self.height):
            left_arr.append((dummy_a,0))
        right_arr = []
        for dummy_a in range(self.height):
            right_arr.append((dummy_a, self.width-1))
            
        self.direction_set = { UP: up_arr,
                               DOWN: down_arr,
                               LEFT: left_arr,
                               RIGHT: right_arr}
        #print self.direction_set
    def reset(self):
        """
        Reset the game so the grid is empty.
        """
        # replace with your code
        self.grid = [ [0 for dummy_col in range(self.width)] for dummy_row in range(self.height)]
    
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        # replace with your code
        for temp_a in range(self.height):
            for temp_b in range(self.width):
                
                print str(self.grid[temp_a][temp_b]) + " " 
            print "\n"

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        # replace with your code

        return self.height
    
    def get_grid_width(self):
        """
        Get the width of the board.
        """
        # replace with your code
        return self.width
                            
    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        # replace with your code
        #print self.grid
        #print "\n"
        iterations = 4
        if direction == UP or direction == DOWN:
            iterations = self.height
        else:
            iterations = self.width
        temp_row_col = (0,0)
        for row_or_col_first in self.direction_set[direction]:
            row_or_col_temp_arr = []
            for temp_c in range(0,iterations):
                if temp_c == 0:
                    temp_row_col = row_or_col_first
                else:
                    temp_row_col = tuple(map(sum,zip(temp_row_col,OFFSETS[direction])))
                #print temp_row_col
                row_or_col_temp_arr.append(self.grid[temp_row_col[0]][temp_row_col[1]])
                        
            #print row_or_col_temp_arr
            merged_arr = merge(row_or_col_temp_arr)
            #print merged_arr
            
            for temp_c in range(0,iterations):
                if temp_c == 0:
                    temp_row_col = row_or_col_first
                else:
                    temp_row_col = tuple(map(sum,zip(temp_row_col,OFFSETS[direction])))
                    
                self.grid[temp_row_col[0]][temp_row_col[1]] = merged_arr[temp_c]                

        self.new_tile()
                
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty 
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        # replace with your code
        #print self.grid
        #print "\n"
        non_zeroes = []
        counter = 0
        for temp_a in range(self.height):
            for temp_b in range(self.width):
                if(self.grid[temp_a][temp_b] == 0):
                    non_zeroes.append(counter)
                counter += 1
        if len(non_zeroes) > 0:
            temp_tile_index = random.randrange(len(non_zeroes))
            tile_index = non_zeroes[temp_tile_index]
            temp_row = tile_index / self.width
            temp_col = tile_index % self.width
            self.counter += 1
            rand_num = random.randrange(0,10)
            if (rand_num < 9):
                self.grid[temp_row][temp_col] = 2
            else:
                self.grid[temp_row][temp_col] = 4
   
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """        
        # replace with your code
        self.grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """        
        # replace with your code
        return self.grid[row][col]
  
poc_2048_gui.run_gui(TwentyFortyEight(4, 5))
#user34_0ROG5qaZZn_3.run_test(merge)