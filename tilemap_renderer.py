from PIL import Image
import wave_collapse
import json


def create_superposition_image(width, height):
    import os

    with open("data.json") as file:
        json_data = json.load(file)

    tileset = {}

    if json_data["combined_tileset"]:
        # tileset.png should be (n*l)xl. n is the count of tiles and l is the size of a tile.
        tileset_ = Image.open("tileset.png")

        tile_count = tileset_.width // tileset_.height
        tile_size = tileset_.height

        for i in range(tile_count):
            tileset[i] = tileset_.crop((i * tile_size, 0, (i + 1) * tile_size, tile_size))

    else:
        tile_size = None
        for path in os.listdir("tileset"):
            image = Image.open("tileset/" + path)
            tileset[int(path[:-4])] = image

            if (tile_size is None or tile_size == image.width) and image.width == image.height:
                tile_size = image.width

            else:
                raise ValueError

    sockets = []
    sprites = []

    for tile_no, tile in enumerate(json_data["tiles"]):
        sprite = tileset[tile["sprite"]]
        socket = tile["sockets"]
        rotations = tile["rotations"]

        for rotation in rotations:
            new_sprite = sprite.rotate(90 * rotation)
            new_socket = socket[rotation:] + socket[:rotation]

            sprites.append(new_sprite)
            sockets.append(new_socket)

    wfc = wave_collapse.WaveFunctionCollapse(sockets, width, height)

    wfc.find_superposition()

    values = tuple(wfc.superposition_values)

    result = create_image(values, sprites, width, height, tile_size)
    result.save("result.png")


def create_superposition_gif(width, height):
    import os

    with open("data.json") as file:
        json_data = json.load(file)

    tileset = {}

    if json_data["combined_tileset"]:
        # tileset.png should be (n*l)xl. n is the count of tiles and l is the size of a tile.
        tileset_ = Image.open("tileset.png")

        tile_count = tileset_.width // tileset_.height
        tile_size = tileset_.height

        for i in range(tile_count):
            tileset[i] = tileset_.crop((i * tile_size, 0, (i + 1) * tile_size, tile_size))

    else:
        tile_size = None
        for path in os.listdir("tileset"):
            image = Image.open("tileset/" + path)
            tileset[int(path[:-4])] = image

            if (tile_size is None or tile_size == image.width) and image.width == image.height:
                tile_size = image.width

            else:
                raise ValueError

    sockets = []
    sprites = []

    for tile_no, tile in enumerate(json_data["tiles"]):
        sprite = tileset[tile["sprite"]]
        socket = tile["sockets"]
        rotations = tile["rotations"]

        for rotation in rotations:
            new_sprite = sprite.rotate(90 * rotation)
            new_socket = socket[rotation:] + socket[:rotation]

            sprites.append(new_sprite)
            sockets.append(new_socket)

    wfc = wave_collapse.WaveFunctionCollapse(sockets, width, height)

    while True:
        frames = []
        wfc.reset_tiles()

        while True:
            try:
                wfc.decrease_entropy()

                values = tuple(wfc.superposition_values)
                new_frame = create_image(values, sprites, width, height, tile_size)
                frames.append(new_frame)

            except ValueError:
                print(f"Generated {len(frames)} frames.")
                frames[0].save("result.gif", format="GIF", save_all=True, append_images=frames[1:])
                print("Saved as result.gif.")
                return

            except (NotImplementedError, RecursionError):
                break


def create_image(values, sprites, width, height, tile_size):
    result = Image.new("RGB", (width * tile_size, height * tile_size))

    for x in range(width):
        for y in range(height):
            tile_superpositions = values[x + y * width]

            if len(tile_superpositions) == 0:
                raise NotImplementedError("Empty superposition can not be rendered.")

            average = sprites[tile_superpositions[0]]

            for i, sprite_no in enumerate(tile_superpositions[:-1]):
                sprite = sprites[sprite_no]
                average = Image.blend(average, sprite, 1 / (i + 2))

            result.paste(average, (x * tile_size, y * tile_size))

    return result


def main():
    import sys

    _, type_, width, height = sys.argv
    width = int(width)
    height = int(height)

    if type_ == "png":
        create_superposition_image(width, height)

    elif type_ == "gif":
        create_superposition_gif(width, height)


if __name__ == '__main__':
    main()
