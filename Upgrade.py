import arcade

FILENAME_START = "img/towers/pistol/tower_pistol_"
UPGRADE_IMAGE_FILES = [f"{FILENAME_START}rightdown.png",
                       f"{FILENAME_START}lv2_rightdown.png",
                       f"{FILENAME_START}lv3rightdown.png"]
TEXTURES = [arcade.load_texture(i) for i in UPGRADE_IMAGE_FILES]


class Upgrade(arcade.Sprite):
    def __init__(self, level=0):
        super().__init__()
        self.level = level

        self.base_prices = {
            0: 200,
            1: 1000,
            2: 5000
        }

        self.textures = TEXTURES
        self.level = level
        self.set_texture(level)

    def level_up(self):
        self.level += 1
        self.set_texture(self.level)
