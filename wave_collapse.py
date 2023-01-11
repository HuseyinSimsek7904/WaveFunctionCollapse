import random
import sys

sys.setrecursionlimit(100000)


class WaveFunctionCollapse:
    def __init__(self, data_set, connections:dict, width, height):
        self.tile_data = data_set
        self.connections = connections

        sockets = list(self.connections.keys())

        # Check if the connections are valid
        for tile in self.tile_data:
            for socket in tile:
                if socket not in sockets:
                    raise ValueError(f"Connections for {socket} are not defined.")

        for socket, allowed in self.connections.items():
            for other in allowed:
                if other not in sockets:
                    raise ValueError(f"Unknown socket type, {socket}.")

                if socket not in self.connections[other]:
                    raise ValueError(f"Weird rule in connections.")

        self.tiles = []

        self.neighbors = ()
        self.tile_size = 0

        self.width = width
        self.height = height

        self.generate_data()

        self.reset_tiles()

    @property
    def length(self):
        return self.width * self.height

    def generate_data(self):
        self.tile_size = len(self.tile_data)

    def reset_tiles(self):
        self.tiles.clear()

        for i in range(self.width * self.height):
            self.create_null_tile()

    def create_null_tile(self):
        self.tiles.append([False for _ in range(self.tile_size)])

    @property
    def lowest_entropy(self):
        lowest_entropy = None
        selected_tiles = []
        for tile_no, tile in enumerate(self.tiles):
            entropy = self.tile_size - sum(tile)

            if not entropy:
                # todo: add backtracking
                raise NotImplementedError

            if entropy == 1:
                continue

            if lowest_entropy is None or entropy < lowest_entropy:
                lowest_entropy = entropy
                selected_tiles.clear()

            if entropy <= lowest_entropy:
                selected_tiles.append(tile_no)

        if lowest_entropy is None:
            raise ValueError("All the tiles are known.")

        return random.choice(selected_tiles)

    def decrease_entropy(self):
        selected_tile_no = self.lowest_entropy
        available_tile_types = tuple(no for no, a in enumerate(self.tiles[selected_tile_no]) if not a)
        selected_tile_type = random.choice(available_tile_types)
        self.tiles[selected_tile_no] = [i != selected_tile_type for i in range(self.tile_size)]

        self.check_neighbors(selected_tile_no)

    def check_neighbors(self, no):
        sockets = set(), set(), set(), set()

        for tile_type, tile_possible in enumerate(self.tiles[no]):
            if tile_possible:
                continue

            for direction, socket in enumerate(self.tile_data[tile_type]):
                sockets[direction].add(socket)

        x = no % self.width
        y = no // self.height

        if x > 0:
            self.check_neighbor(no - 1, sockets, 3)

        if y > 0:
            self.check_neighbor(no - self.width, sockets, 0)

        if x < self.width - 1:
            self.check_neighbor(no + 1, sockets, 1)

        if y < self.height - 1:
            self.check_neighbor(no + self.width, sockets, 2)

    def get_available_sockets(self, sockets):
        for socket in sockets:
            yield from self.connections[socket]

    def check_neighbor(self, tile_no, sockets, side_no):
        available_sockets = tuple(self.get_available_sockets(sockets[side_no]))

        tile = self.tiles[tile_no]
        difference = False

        for neighbor_type, neighbor_type_available in enumerate(tile):
            if neighbor_type_available:
                continue

            if self.tile_data[neighbor_type][(side_no + 2) % 4] not in available_sockets:
                tile[neighbor_type] = True
                difference = True

        if difference:
            self.check_neighbors(tile_no)

    def find_superposition(self):
        while True:
            try:
                self.decrease_entropy()

            except ValueError:
                return

    @property
    def superposition_values(self):
        for tile in self.tiles:
            possibilities = []
            for tile_type, tile_available in enumerate(tile):
                if tile_available:
                    continue

                possibilities.append(tile_type)

            yield tuple(possibilities)

    def print_superpositions(self):
        superposition = tuple(self.superposition_values)

        for row_no in range(self.height):
            print(*(str(i[0]).rjust(2, " ") for i in superposition[row_no * self.height:(row_no + 1) * self.height]))
