import arcade

from Right_Menu import Right_Menu
from Upgrade import Upgrade
from peeps import eeeeeeeeeeenemy
TILE_SIZE = 32
MAP_HEIGHT = MAP_WIDTH = 800


class Window(arcade.Window):
    def __init__(self):
        super().__init__(width=1200, height=800, title="Dino tower defense")
        self.path_tiles = arcade.SpriteList()
        arcade.set_background_color(arcade.color.SKY_BLUE)
        self.wall_tiles = arcade.SpriteList()
        self.grid = [[{
            "upgrade": None,
            "is_base": False,
            "sprite_list": None,
            "tile": None,
        } for j in range(MAP_HEIGHT // TILE_SIZE + 1)]for i in range(MAP_WIDTH // TILE_SIZE + 1)]

        self.game_state = {
            "money": 0,
            "health": 1000,
            "stage": 1
        }

        self.make_your_map()
        
        enemy = eeeeeeeeeeenemy.Enemy(self, f"img/minotaur", scale=1, facing_right=False)
        self.enemy_list = arcade.SpriteList()
        self.enemy_list.append(enemy)

        self.selector = arcade.Sprite(filename="img/transparent_selector.png")
        self.selector.position = -50, -50
        self.upgrade_sprites = arcade.SpriteList()

        self.right_menu = Right_Menu(main_window=self,
                                     width=self.width - MAP_WIDTH - TILE_SIZE/2,
                                     height=self.height,
                                     x_offset=MAP_WIDTH + TILE_SIZE/2)

    def on_draw(self):
        arcade.start_render()
        self.wall_tiles.draw()
        self.path_tiles.draw()
        self.selector.draw()
        self.upgrade_sprites.draw()
        self.enemy_list.draw()
        self.enemy_list.update_animation()
        self.draw_health_bars(self.enemy_list)
        self.right_menu.draw()


    def on_update(self, delta_time: float):
        self.enemy_list.update()
        for i in self.enemy_list:
            if i.dead:
                self.enemy_list.remove(i)

    def make_your_map(self):
        grass_tiles = arcade.SpriteList()
        x = y = TILE_SIZE
        num = 800 - TILE_SIZE * 2

        direction = 1
        while num > 0:
            for i in range(num // TILE_SIZE):
                new_tile = arcade.Sprite(filename="img/buttback.png", center_x=x, center_y=y, scale=2)
                self.path_tiles.append(new_tile)
                grid_section = self.grid[x // TILE_SIZE][y // TILE_SIZE]
                grid_section["sprite_list"] = self.path_tiles
                grid_section["tile"] = new_tile
                x += direction * TILE_SIZE
            num -= TILE_SIZE
            for i in range(num // TILE_SIZE):
                new_tile = arcade.Sprite(filename="img/buttback.png", center_x=x, center_y=y, scale=2)
                self.path_tiles.append(new_tile)
                grid_section = self.grid[x // TILE_SIZE][y // TILE_SIZE]
                grid_section["sprite_list"] = self.path_tiles
                grid_section["tile"] = new_tile
                y += direction * TILE_SIZE
            num -= TILE_SIZE
            direction *= -1

        for i in range(MAP_WIDTH // TILE_SIZE + 1):
            for j in range(MAP_HEIGHT // TILE_SIZE + 1):
                tile_x = i * TILE_SIZE
                tile_y = j * TILE_SIZE

                can_add_tile = True
                for path_tile in self.path_tiles:
                    if path_tile.center_x == tile_x and path_tile.center_y == tile_y:
                        can_add_tile = False
                if can_add_tile:
                    new_tile = arcade.Sprite(filename="img/grass.png", center_x=tile_x, center_y=tile_y, scale=2)
                    self.wall_tiles.append(new_tile)
                    grid_section = self.grid[tile_x // TILE_SIZE][tile_y // TILE_SIZE]
                    grid_section["sprite_list"] = self.wall_tiles
                    grid_section["tile"] = new_tile

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        grid_x, grid_y = self.coordinate_to_grid(x, y)
        grid_section = self.grid[grid_x][grid_y]
        if x <= MAP_WIDTH and y <= MAP_HEIGHT:
            self.selector.position = grid_section["tile"].position
            # new_upgrade = Upgrade()
            # new_upgrade.position = self.selector.position
            # self.upgrade_sprites.append(new_upgrade)
            # new_upgrade.level_up()
            # new_upgrade.level_up()
            self.right_menu.grid_position = grid_section

        else:
            self.right_menu.click(x, y)

    @staticmethod
    def is_point_in_sprite(x, y, sprite: arcade.Sprite):
        return abs(x - sprite.center_x) <= TILE_SIZE // 2 and abs(y - sprite.center_y) <= TILE_SIZE // 2

    def coordinate_to_grid(self, x, y):
        if x > MAP_WIDTH or y > MAP_HEIGHT:
            raise Exception("accessing coordinate outside of grid")
        grid_x = (x + TILE_SIZE//2) // TILE_SIZE
        grid_y = (y + TILE_SIZE//2) // TILE_SIZE
        return grid_x, grid_y

    def draw_health_bars(self, sprite_list):
        for spr in sprite_list:
            if spr.animation != "dying":
                adjustment = spr.height/3
                h = 5
                arcade.draw_rectangle_filled(center_x=spr.center_x,
                                             center_y=spr.center_y + adjustment,
                                             width=spr.width/2, height=h,
                                             color=(220, 15, 15))
                arcade.draw_rectangle_filled(center_x=spr.center_x - spr.width*(1-spr.health/spr.max_health)/4,
                                             center_y=spr.center_y + adjustment,
                                             width=spr.width * spr.health/spr.max_health/2, height=h,
                                             color=(15, 255, 15))







if __name__ == "__main__":
    game_window = Window()
    arcade.run()






 # this function shows a bunch of lines and red dots and makes the game lag
# totally super useful function
def position_shift_demo():
    shift = .5
    width = MAP_WIDTH//TILE_SIZE
    for i in range(width):
        real_i = i + shift
        arcade.draw_line(real_i*TILE_SIZE, 0, real_i*TILE_SIZE, MAP_HEIGHT, arcade.color.BLACK)
        arcade.draw_line(0, real_i*TILE_SIZE, MAP_WIDTH, real_i*TILE_SIZE, arcade.color.BLACK)
    for i in range(width):
        real_i = i+shift
        for j in range(width):
            real_j = j + shift
            arcade.draw_circle_filled(real_i*TILE_SIZE, real_j*TILE_SIZE, 5, arcade.color.DARK_RED)
