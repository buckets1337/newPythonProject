"""my initial idea for this project is to create a turn-based, roguelike-style game that focuses less on combat, and more on crafting and construction.
This is going to be a bit harder for me to implement than the roguelike, but I'm going to try and build this using TDD methods and borrowing code from
the roguelike I just "finished".  I'll add more to this comment section later as new ideas and stuff occur to me."""


import libtcodpy as libtcod
import config_newPythonProject as config
import math
import textwrap
import random




class Rect:     #a rectangle on the map.  used to characterize a room.
    def __init__(self,x,y,w,h, is_rectangle=True):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h
        
    def center(self):
        center_x = (self.x1 + self.x2) / 2
        center_y = (self.y1 + self.y2) / 2
        return (center_x, center_y)
        
    def intersect(self, other):
        #returns true if this rectangle intersects with another rectangle
        return(self.x1 <= other.x2 and self.x2 >= other.x1 and self.y1 <= other.y2 and self.y2 >= other.y1)

class Tile:     #a tile of the map and it's properties

    def __init__(self, blocked, block_sight = None):
        self.blocked = blocked
        self.explored = False
        
        #by default, if a tile is blocked, it also blocks los
        if block_sight is None: block_sight = blocked
        self.block_sight = block_sight
        
class Map:      #a map object.  Represents the level map, must call new_map after initialization

    def __init__(self, x, y, blocked):
        self.x = x
        self.y = y
        self.blocked = blocked
        
    def new_map(self, x, y, name, blocked, no_of_rooms, no_of_intersects, room_min_size, room_max_size):
        global current_map, current_rooms
        self.x = x
        self.y = y
        self.blocked = blocked
        self.no_of_rooms = no_of_rooms
        self.room_min_size = room_min_size
        self.room_max_size = room_max_size
        
        #fill the map with blocked tiles
        map = [[Tile(blocked)
            for y in range(self.y) ]
                for x in range(self.x) ]
                
        #carves the rooms
        current_rooms = []
        num_rooms = 0
        room_intersects = 0
        current_map = map
        for r in range(no_of_rooms):
            self.generate_room(x, y, no_of_intersects, room_min_size, room_max_size)
            num_rooms += 1
            old_room = current_rooms[num_rooms - 1]
            new_room = current_rooms[num_rooms - 1]
            self.connect_with_tunnels(old_room, new_room)
        
    def generate_room(self, map_x_length, map_y_length, no_of_intersects, room_min_size, room_max_size):  #chooses random coords for the room and defines the shape of the room
        global current_rooms
        #random width and height
        w = libtcod.random_get_int(0,room_min_size, room_max_size)
        h = libtcod.random_get_int(0,room_min_size, room_max_size)
        #random position in bounds on the map
        x = libtcod.random_get_int(0,0,map_x_length - w - 1)
        y = libtcod.random_get_int(0,0,map_y_length - h - 1)
        #makes the room
        new_room = Rect(x,y,w,h)
        #check other rooms for an intersection
        failed = False
        
        room_intersects = 0
        for other_room in current_rooms:
            if new_room.intersect(other_room):
                room_intersects +=1
                if room_intersects >= no_of_intersects:
                    failed = True
                    break
                break
        if not failed:  #not over max number of intersections, so clear to build
            self.create_room(new_room)
            current_rooms.append(new_room)
        
    def create_room(self, room):  #creates rooms on the map
        global current_map
        #go through the tiles in the rectangle and make them passable
        for x in range(room.x1+1, room.x2):
            for y in range(room.y1+1, room.y2):
                current_map[x][y].blocked = False
                current_map[x][y].block_sight = False
                
    def connect_with_tunnels(self, old_room, new_room):   #connects an old room to a new room with a tunnel through their center points
        if len(current_rooms) == 1:
            #this is the starting room
            pass
            
        else:
            if libtcod.random_get_int(0,0,1) == 1:
                self.create_h_tunnel(old_room.x1, new_room.x1, old_room.y1)
                self.create_v_tunnel(old_room.y1, new_room.y1, new_room.x1)
            else:
                self.create_v_tunnel(old_room.y1, new_room.y1, new_room.x1)
                self.create_h_tunnel(old_room.x1, new_room.x1, new_room.y1)
                
    def create_h_tunnel(self, x1, x2, y):     #creates a horizontal segment of hallway
        global current_map
        for x in range(min(x1, x2), max(x1, x2) + 1):
            current_map[x][y].blocked = False
            current_map[x][y].block_sight = False
            
    def create_v_tunnel(self, y1, y2, x):     #creates a vertical segment of hallway
        global current_map
        for y in range(min(y1, y2), max(y1, y2) + 1):
            current_map[x][y].blocked = False
            current_map[x][y].block_sight = False
            
    def list_tile(self, x, y):    #returns a tile on the map
        global current_map
        return current_map[x][y]
        

#------------------------------------------------------------------------
#   Global Variables
#------------------------------------------------------------------------
current_map = []
current_rooms = []
map_list = []


