import arcade


class Right_Menu:
    def __init__(self, main_window, width, height, x_offset):
        self.main_window = main_window
        self.width = width
        self.height = height
        self.x_offset = x_offset

        self.grid = self.main_window.grid
        self.grid_position = None

    def click(self, x, y):
        # TODO: make it do something when click menu you lazy bum
        # TODO: just make this work already
        # TODO: you will not have upgrades until you get this done
        # TODO: this will stick out like sore thumb until you finish
        pass

    def draw(self):
        self.menu_y = self.height-25

        self.add_text(f"Money: £{0}")

        # if nothing is selected, end function here
        if self.grid_position is None:
            return

        # if wall tile selected
        if self.grid_position["sprite_list"] == self.main_window.wall_tiles:
            self.add_text(f"Current Upgrade Level: {0}")

    def add_text(self, text, x=0, height=50,
                 bg_color=arcade.color.GREEN,
                 text_color=arcade.color.RED):
        arcade.draw_rectangle_filled(center_x=self.x_offset + self.width / 2,
                                     center_y=self.menu_y,
                                     width=self.width,
                                     height=height,
                                     color=bg_color)
        arcade.draw_text(start_x=x + self.x_offset + self.width/2,
                         start_y=self.menu_y,
                         color=text_color,
                         text=text,
                         anchor_x="center",
                         anchor_y="center")
        self.menu_y -= height

