import arcade
import pathlib
import math
from PIL import ImageOps

folder = pathlib.Path("img/minotaur")
f = "die"
correct_range = list(range(78,81)) + list(range(89,92)) + list(range(100, 106))
DYING_TEXTURES = [arcade.load_texture(folder / f / f"{i}.png") for i in correct_range]

class Enemy(arcade.AnimatedWalkingSprite):
    def __init__(self, window, image_folder_path, scale=1, health=100, max_health=100,
                 animation_numbers=((122, 129), (1, 5)), facing_right=False):
        super().__init__(scale=scale)
        folder = pathlib.Path(image_folder_path)
        self.window = window
        self.health = health
        self.max_health = max_health
        self.dead = False
        self.animation = None
        self.anim_tick = 0
        self.animation_length = 0
        num = 0

        f = "walk"
        self.walk_left_textures = [arcade.load_texture(folder / f / f"{i}.png", mirrored=facing_right)
                                    for i in range(animation_numbers[num][0], animation_numbers[num][-1])]
        self.walk_right_textures = [arcade.load_texture(folder / f / f"{i}.png", mirrored=not facing_right)
                                   for i in range(animation_numbers[num][0], animation_numbers[num][-1])]

        num = 1
        f = "idle"
        self.stand_right_textures = [arcade.load_texture(folder / f / f"{i}.png", mirrored=facing_right)
                                     for i in range(animation_numbers[num][0], animation_numbers[num][-1])]
        self.stand_left_textures = [arcade.load_texture(folder / f / f"{i}.png", mirrored=not facing_right)
                                    for i in range(animation_numbers[num][0], animation_numbers[num][-1])]

        self.texture = self.walk_right_textures[0]
        self.position = self.window.path_tiles[0].position

        self.move_target = 1
        self.move_rate = 0.6

    def move(self):
        if self.move_rate < 0.001:
            self.change_x = 0
            self.change_y = 0
            return

        target = self.window.path_tiles[self.move_target]

        # distance between character and target
        x = target.center_x - self.center_x
        y = target.center_y - self.center_y


        self.change_x = x
        if abs(x) > 0.0001:
            self.change_x /= abs(x) * self.move_rate
        self.change_y = y
        if abs(y) > 0.0001:
            self.change_y /= abs(y) * self.move_rate
        if math.sqrt(x*x+y*y) < self.move_rate * 1.5:
            self.position = self.window.path_tiles[self.move_target].position
            self.move_target += 1

    def update(self):
        self.move()
        super().update()
        self.health -= .2
        self.death_check()

    def death_check(self):
        if self.health <= 0 and self.animation != "dying":
            self.move_rate = 0
            self.animation = "dying"
            self.animation_length = len(DYING_TEXTURES) - 1

    def update_animation(self, delta_time: float = 1/60):
        if self.change_x == 0:
            if self.center_x > self.window.width / 2:
                self.state = arcade.sprite.FACE_LEFT
            else:
                self.state = arcade.sprite.FACE_RIGHT
        super().update_animation()
        if self.animation is not None:
            self.anim_tick += delta_time
            if self.anim_tick >= self.animation_length:
                self.anim_tick = 0
            self.cur_texture_index = math.floor(self.anim_tick * 7)
            if self.animation == "dying":
                dying_texture = DYING_TEXTURES[self.cur_texture_index]
                # if facing left, flip image
                if self.state == arcade.sprite.FACE_LEFT:
                    dying_texture.image = ImageOps.mirror(dying_texture.image)
                self.texture = dying_texture
                if self.cur_texture_index >= self.animation_length:
                    self.dead = True
