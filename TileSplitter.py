import PIL.Image
import pathlib
import shutil
import os
import xml.etree.ElementTree as ET


def split_tiles(filename, tile_width: int, tile_height: int,
                destination, x_margin: int = 0, y_margin: int = 0):
    x = 0
    y = 0
    counter = 1
    tile_image = PIL.Image.open(filename)

    destination = pathlib.Path(destination)
    if not destination.is_dir():
        destination.mkdir()

    while y < tile_image.height:
        while x < tile_image.width:
            new_tile = tile_image.crop((x, y, x+tile_width, y+tile_height))
            f = destination / f"{counter}.png"
            new_tile.save(f)
            if f.stat().st_size < 300:
                f.unlink()
            counter += 1
            x += tile_width+x_margin
        x = 0
        y += tile_height+y_margin


def split_tiles_and_fix_tsx(tsx_filename, destination):
    tsx_xml = ET.parse(tsx_filename)
    tileset_tag = tsx_xml.getroot()

    split_tiles(filename=tileset_tag.find("image").get('source'),
                tile_width=int(tileset_tag.get('tilewidth')),
                tile_height=int(tileset_tag.get('tileheight')),
                destination=destination)

    # backup tsx file
    tsx_filename = pathlib.Path(tsx_filename)
    shutil.copy2(tsx_filename, "backup_" + str(tsx_filename))

    tile_source = tileset_tag.find('image').get('source')

    tileset_tag.remove(tileset_tag.find('image'))
    grid_tag = ET.SubElement(tileset_tag, 'grid')
    grid_tag.set('orientation', 'orthogonal')
    grid_tag.set('width', '1')
    grid_tag.set('height', '1')

    for img_path in pathlib.Path(destination).glob('*'):
        tile_tag = ET.SubElement(tileset_tag, 'tile')
        tile_tag.set('id', img_path.stem)
        image_tag = ET.SubElement(tile_tag, 'image')
        image_tag.set('width', tileset_tag.get('tilewidth'))
        image_tag.set('height', tileset_tag.get('tileheight'))
        image_tag.set('source', str(img_path))

    tsx_xml.write(tsx_filename)






split_tiles("img/minotaur/Minotaur - Sprite Sheet.png", 96, 96, "img/minotaur/stuff")
#split_tiles_and_fix_tsx("tileset1.tsx", "img/TileSet1")


