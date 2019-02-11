"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = "obstacle"
HUMAN = "human"
ZOMBIE = "zombie"


class Zombie(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
            
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        newzombie = (row, col)
        self._zombie_list.insert(self.num_zombies(), newzombie)

                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)     
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        for zombie in self._zombie_list:
            yield zombie
        # replace with an actual generator

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        newhuman = (row, col)
        self._human_list.insert(self.num_humans(), newhuman)
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list) 
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        # replace with an actual generator
        for human in self._human_list:
            yield human
        
    def compute_distance_field(self, entity_type):
        """
        Function computes a 2D distance field
        Distance at member of entity_queue is zero
        Shortest paths avoid obstacles and use distance_type distances
        """
            

        visited = poc_grid.Grid(poc_grid.Grid.get_grid_height(self), poc_grid.Grid.get_grid_width(self))
        
        
        
        distancefield = []
        
        for item in range(poc_grid.Grid.get_grid_height(self)):
            twodlistpart = []
            for seconditem in range(poc_grid.Grid.get_grid_width(self)):
                twodlistpart.append((poc_grid.Grid.get_grid_height(self) * poc_grid.Grid.get_grid_width(self)))
                seconditem = seconditem
            distancefield.append(twodlistpart)
        
        
        boundry = poc_queue.Queue()
        
        if entity_type == 'zombie':
            listtype = self.zombies()
        else:
            listtype = self.humans()

        for item in listtype:
            boundry.enqueue(item)
            distancefield[item[0]][item[1]] = 0
            visited.set_full(item[0], item[1])

        
        while boundry:
            current_cell = boundry.dequeue()
            for neighbour in visited.four_neighbors(current_cell[0], current_cell[1]):
                if visited.is_empty(neighbour[0], neighbour[1]) == True and Zombie.is_empty(self, neighbour[0], neighbour[1]) == True:
                    visited.set_full(neighbour[0], neighbour[1])
                    boundry.enqueue((neighbour[0], neighbour[1]))
                    distancefield[neighbour[0]][neighbour[1]] = distancefield[current_cell[0]][current_cell[1]] + 1
                   
        print distancefield
        return distancefield
        
    
    def move_humans(self, zombie_distance):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        #for item in distance field...find largest
        
        iterations = 0
        for item in self.humans():
            minimum = 0
            minimum_coords = []
            for neighbour in Zombie.eight_neighbors(self, item[0], item[1]):
                if zombie_distance[neighbour[0]][neighbour[1]] > minimum and zombie_distance[neighbour[0]][neighbour[1]] != Zombie.get_grid_height(self) * Zombie.get_grid_width(self):
                    minimum = zombie_distance[neighbour[0]][neighbour[1]]
                    minimum_coords = (neighbour[0], neighbour[1])
                self._human_list[iterations] = minimum_coords
            iterations += 1
            
            
        return self._human_list
            
    
    def move_zombies(self, human_distance):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        
        iterations = 0
        choice = 0
        for item in self.zombies():
            coordinateslist = []
            for neighbour in Zombie.four_neighbors(self, item[0], item[1]):
                print human_distance[neighbour[0]][neighbour[1]],'vs', human_distance[item[0]][item[1]]
                if human_distance[neighbour[0]][neighbour[1]] < human_distance[item[0]][item[1]]:
                    print human_distance[neighbour[0]][neighbour[1]], 'is less than', human_distance[item[0]][item[1]]
                    coordinateslist.append(neighbour)
                    choice = random.choice(coordinateslist)

                    
                if len(coordinateslist) > 0:
                    choice = random.choice(coordinateslist)
                else:
                    choice = self._zombie_list[iterations]
                    
            self._zombie_list[iterations] = choice
            iterations += 1
               
        return self._zombie_list

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

poc_zombie_gui.run_gui(Zombie(30, 40))