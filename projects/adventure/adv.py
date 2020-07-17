from room import Room
from player import Player
from world import World

from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

traversal_path = []


path = []
graph = {}
graph[player.current_room.id] = player.current_room.get_exits()  #initialize 0 room with room as key and directions as values

while len(graph) < len(room_graph) -1: #while we havent explored everything
    moves = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'} # replaces opposite direction function
    if player.current_room.id not in graph: # if room hasnt been visited
        graph[player.current_room.id] = player.current_room.get_exits()  # add room to graph same way as 0 was init
        prev = path[-1]  # tracking where we came from (Thanks Sam)
        graph[player.current_room.id].remove(prev)  # no more stupid backtracking

    while len(graph[player.current_room.id]) == 0: # When you reach a dead end/have visited every room around you
        prev = path.pop() # get where you just came from
        traversal_path.append(prev) # add it to the path to go back where you came from until you have move options
        player.travel(prev) # the actual moving

    next_room = graph[player.current_room.id].pop(-1)
    path.append(moves[next_room])
    traversal_path.append(next_room)
    player.travel(next_room)

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

# print(f'\n{traversal_path}')



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
