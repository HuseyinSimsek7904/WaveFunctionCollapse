# WaveFunctionCollapse
This is my try on creating the wave function collapse algorithm.

wave_collapse.py contains the class for creating tilemaps, you can use it for creating maps. This class does not have a rotation calculator but that can be created easily.

To create a tilemap; you will need a tileset, which contains the socket types of the tiles. This dataset should be in the form:

    [tile1, tile2, ..., tileN]
   
Every tile should be in the form:

    [socket1, socket2, socket3, socket4]
     Up       Right    Down     Left
   
To start, create a WaveFunctionCollapse object from wave_collapse.py. It takes three argument; tileset, width and height. Then you can just call find_superposition. That will decrease the entropy till there is only one tileset. Then you can use superposition_values to get the values. That returns a generator, might want to convert it to tuple. That tuple will have width x height items; as the tile goes right, index increases by one and as it goes down, index increases by width.

Tiles will have their sockets matched equally when the algorithm is run.

Example code:

    import wave_collapse

    tileset = (
      (0, 0, 1, 1),
      (0, 1, 1, 0),
      (1, 1, 0, 0),
      (1, 0, 0, 1)
    )
    wfc = wave_collapse.WaveFunctionCollapse(tileset, 8, 8)
    wfc.find_superposition()

    for i, b in enumerate(wfc.superposition_values):
      # i is the item index, b is a tuple that contains the possible values the tile can get.
      # b should have only one item since we called find_superposition.

      # Find the row no
      x = i % 8

      # Find the collumn no
      y = i // 8

      # Print every tile's coordinate that's type is 0.
      if b[0] == 0:
        print(f"({x}, {y})")
  

tilemap_renderer.py contains the file that creates visuals using wave function collapse. It uses the class from wave_collapse.py.
You can use the command prompt or power shell to run the program.

- To create a .png file:

      py tilemap_renderer.py path_of_data png width height

- To create a .gif file that shows its evolution

      py tilemap_renderer.py path_of_data gif width height
  
For example,
 
    py .\tilemap_renderer.py .\datasets\triangles\ png 32 32
  
will create a 32x32 .png image in ".\datasets\triangles\".

# Problems:
  - Since program runs with recursion, it can actually reach the recursion limit in Python. To solve this problem, an option to use loops can be added.
  - Algoritm makes the sockets MATCH EXACTLY EQUALY. That makes it impossible to create some interesting patterns. To add more pattern types, there could be a socket mapping that stores which socket types goes with which type.
  - Algorithm does not contain backtracking. Right now if algorithm creates an impossible pattern, it just restarts from nothing. Instead there could be a backtracking list that helps the algorithm to rewind a little back and keep going.
  - Code has no comments :P
