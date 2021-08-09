"""
If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.sprite_bullets_enemy_aims
"""

import arcade
import math
import random
import os
import time, datetime
import arcade.gui
from arcade.gui import UIManager

MOVE_SCREEN_WIDTH = 800
MOVE_SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Space Shooter Game Beta"
BULLET_SPEED = 10
BULLET_OFFSET_DISTANCE = 60 #offset the bullet from the enemy when it's shooting, so the enemy won't collide with its own bullet at first
ENEMY_MOVE_SPEED = 1
FIRING_RATE = 30
HP = 1000
MAX_ENEMIES = 50
ENEMY_HP = 10
HEALTH_BAR_LENGTH = 150
AMMO = 10
VOLUME = 1
ANGLE = 90

class MyFlatButton(arcade.gui.UIFlatButton):
    def on_click(self):
        print("Clicked flat button. ")

class MenuView(arcade.View):
    def on_show(self):
        self.background = arcade.load_texture("spacebackground.jpeg")

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        arcade.draw_text("Space Dodgers", SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", SCREEN_WIDTH/2, SCREEN_HEIGHT/2-75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        button_view = ButtonView()
        self.window.show_view(button_view)
        # instruction_view = InstructionView()
        # self.window.show_view(instruction_view)


class ButtonView(arcade.View): #ButtonView is inheriting the arcade.View class
    def __init__(self):
        super().__init__() #also initialize the super class (the parent class)
        self.ui_manager = UIManager()
        self.ui_manager.purge_ui_elements()
        global button_texture
        button_texture = arcade.load_texture(':resources:gui_basic_assets/red_button_normal.png')
        easy = MyFlatButton(
            'Easy',
            center_x=SCREEN_WIDTH// 2,
            center_y=SCREEN_HEIGHT//1.5,
            width=250,
            height=40,
            button_texture=button_texture, )
        self.ui_manager.add_ui_element(easy)
        medium = MyFlatButton(
            'Medium',
            center_x=SCREEN_WIDTH // 2,
            center_y=SCREEN_HEIGHT // 1.9,
            width=250,
            height=40,
            button_texture=button_texture, )
        self.ui_manager.add_ui_element(medium)
        hard = MyFlatButton(
            'Hard',
            center_x=SCREEN_WIDTH // 2,
            center_y=SCREEN_HEIGHT // 2.5,
            width=250,
            height=40,
            button_texture=button_texture, )
        self.ui_manager.add_ui_element(hard)


    def on_show(self):
        self.background = arcade.load_texture("spacebackground.jpeg")

    def on_click(self):
        """ Called when user lets off button """
        print(f"Click button. {self.input_box.text}")

    def on_draw(self):
        arcade.start_render()

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        instruction_view = InstructionView()
        self.window.show_view(instruction_view)


class InstructionView(arcade.View):
    def on_show(self):
        self.background = arcade.load_texture("spacebackground.jpeg")

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        arcade.draw_text("Instructions", SCREEN_WIDTH/2, SCREEN_HEIGHT/1.5,
                         arcade.color.WHITE, font_size=40, anchor_x="center")
        arcade.draw_text("Dodge the bullets and see how long you can last!", SCREEN_WIDTH/2, SCREEN_HEIGHT/1.8,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("You have 10 ammo, press R to reload\nBe warned, this will take some time!", SCREEN_WIDTH / 2,
                         SCREEN_HEIGHT / 2 - 40,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("Click to advance", SCREEN_WIDTH/2, SCREEN_HEIGHT/2-270,
                         arcade.color.WHITE, font_size=15, anchor_x="center")


    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = MyGame()
        self.window.show_view(game_view)

class MyGame(arcade.View): #inheritance
    """ Main application class """

    def __init__(self):
        super().__init__()

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        arcade.set_background_color(arcade.color.BLACK)

        self.frame_count = 0

        self.background = None
        self.enemy_list = None
        self.bullet_list = None
        self.player_list = None
        self.player = None
        self.hit_count = 0
        self.t0 = time.time()
        self.t1 = 0
        self.background_x = 0
        self.background_y = 0
        self.space_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False
        self.ammo = AMMO
        self.hp = HP
        self.enemy_hp = ENEMY_HP

        self.setup()

    def setup(self):
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()

        setattr(arcade.Sprite, "moving_down", True) #adding attributes to an class dynamically
        setattr(arcade.Sprite, "moving_left", True) #adding attributes to an class dynamically

        # Add player ship
        self.player = arcade.Sprite(":resources:images/space_shooter/playerShip1_orange.png", 0.5)
        self.player_list.append(self.player)


    def spawn_enemy(self,texture=":resources:images/cards/cardSpadesA.png"):
        enemy = arcade.Sprite(texture, 1)
        enemy.center_x = random.randint(0,SCREEN_WIDTH)
        enemy.center_y = SCREEN_HEIGHT
        enemy.angle = 180
        enemy.hp = ENEMY_HP
        self.enemy_list.append(enemy)


    def on_draw(self):
        """Render the screen. """

        arcade.start_render()
        self.background = arcade.load_texture("spacebackground.jpeg")
        arcade.draw_lrwh_rectangle_textured(self.background_x, self.background_y, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        arcade.draw_lrwh_rectangle_textured(self.background_x, self.background_y+SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.background_y -= 5
        if self.background_y <= -SCREEN_HEIGHT:
            self.background_y = 0

        self.enemy_list.draw()
        self.bullet_list.draw()
        self.player_list.draw()

        start_x = SCREEN_WIDTH*0.01
        start_y = SCREEN_HEIGHT*0.95
        arcade.draw_text(str(datetime.timedelta(seconds=self.t1)), start_x, start_y, arcade.color.YELLOW, 20, font_name='ARIAL ')

        start_x = SCREEN_WIDTH * 0.01
        start_y = SCREEN_HEIGHT * 0.9
        arcade.draw_text(f"Hits: {self.hit_count}", start_x, start_y, arcade.color.YELLOW, 20,font_name='ARIAL ')

        # if self.ammo == 0:
        #     arcade.draw_text("PRESS R TO RELOAD", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, arcade.color.WHITE, font_size=50, anchor_x="center")
        # if self.hp == 0:
        #     class(GameOverView) #make this redirect to game over screen

        arcade.draw_text(self.ammo * "|  ", self.player.center_x, self.player.center_y - 30, arcade.color.WHITE, font_size=20, anchor_x="center")

        self.hp_color = (255*(1-self.hp/HP), self.hp/HP * 255, 0)

        COLOUR = arcade.color.GREEN
        if self.hp > 0.8 * HP:
            COLOUR = arcade.color.GREEN
        elif self.hp > 0.3 * HP:
            COLOUR = arcade.color.YELLOW
        else:
            COLOUR = arcade.color.RED

        COLOUR = arcade.color.GREEN
        if ENEMY_HP == 100:
            COLOUR = arcade.color.GREEN
        elif ENEMY_HP == 50:
            COLOUR = arcade.color.RED

        arcade.draw_rectangle_filled(self.player.center_x, self.player.center_y +30, self.hp*HEALTH_BAR_LENGTH/HP, 10, self.hp_color)

        for enemy in self.enemy_list:
            arcade.draw_rectangle_filled(enemy.center_x, enemy.center_y + 30, enemy.hp*10, 8, COLOUR)

    def on_update(self, delta_time):
        """All the logic to move and the game logic goes here. """

        self.t1 = time.time() - self.t0
        self.frame_count += 1

        #spawn enemy ships
        list_enemies = [":resources:images/topdown_tanks/tank_green.png", ":resources:images/cards/cardSpadesA.png",
                        ":resources:images/items/gold_1.png",":resources:images/enemies/frog.png",":resources:images/tiles/mushroomRed.png"]
        if len(self.enemy_list) < MAX_ENEMIES:
            self.spawn_enemy(":resources:images/topdown_tanks/tank_green.png")

        # Loop through each enemy that we have
        for enemy in self.enemy_list:
            # print(enemy.center_y)
            if enemy.center_y > SCREEN_HEIGHT:
                enemy.moving_down = True
            if enemy.center_y < 0:
                enemy.moving_down = False

            if enemy.moving_down:
                enemy.center_y -= ENEMY_MOVE_SPEED
            else:
                enemy.center_y += ENEMY_MOVE_SPEED

            if enemy.center_x > SCREEN_WIDTH:
                enemy.moving_left = True
            if enemy.center_x < 0:
                enemy.moving_left = False

            if enemy.moving_left:
                enemy.center_x -= ENEMY_MOVE_SPEED
            else:
                enemy.center_x += ENEMY_MOVE_SPEED

            # First, calculate the angle to the player. We could do this
            # only when the bullet fires, but in this case we will rotate
            # the enemy to face the player each frame, so we'll do this
            # each frame.

            # Position the start at the enemy's current location
            start_x = enemy.center_x
            start_y = enemy.center_y

            # Get the destination location for the bullet
            dest_x = self.player.center_x
            dest_y = self.player.center_y

            # Do math to calculate how to get the bullet to the destination.
            # Calculation the angle in radians between the start points
            # and end points. This is the angle the bullet will travel.
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)  # this is the direction (angle) from the enemy to the player

            # Set the enemy to face the player.
            enemy.angle = math.degrees(angle) + 90

            # Shoot every 60 frames change of shooting each frame
            if self.frame_count % FIRING_RATE == 1:
                bullet = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png")
                bullet.center_x = start_x + BULLET_OFFSET_DISTANCE * math.cos(angle)
                bullet.center_y = start_y + BULLET_OFFSET_DISTANCE * math.sin(angle)

                # Angle the bullet sprite
                bullet.angle = math.degrees(angle)

                # Taking into account the angle, calculate our change_x
                # and change_y. Velocity is how fast the bullet travels.
                bullet.change_x = math.cos(angle) * BULLET_SPEED
                bullet.change_y = math.sin(angle) * BULLET_SPEED

                bullet.owner = "enemy"
                self.bullet_list.append(bullet)
        # print(len(self.bullet_list))

        # Get rid of the bullet when it flies off-screen
        for bullet in self.bullet_list:
            # if bullet.bottom > 600 or bullet.top < 0 or bullet.left > 800 or bullet.right < 0:

            if not (0 <= bullet.center_y <= SCREEN_HEIGHT and 0 <= bullet.center_x <= SCREEN_WIDTH):
                bullet.remove_from_sprite_lists()
                # print(len(self.bullet_list))

            if bullet.collides_with_sprite(self.player):
                bullet.remove_from_sprite_lists()
                self.hit_count += 1
                self.hp -= 1
                print(self.hp)
                print(self.hit_count)

                if self.hit_count == HP:
                    game_over_view = GameOverView()  # create a new instance of the game over class
                    game_over_view.time_taken = self.t1
                    self.window.set_mouse_visible(True)
                    self.window.show_view(game_over_view)  # switching to the game over screen

            for bullet2 in self.bullet_list:
                if bullet.collides_with_sprite(bullet2) and bullet != bullet2 and bullet.owner != bullet2.owner:
                    bullet.remove_from_sprite_lists()
                    bullet2.remove_from_sprite_lists()

            for enemy in bullet.collides_with_list(self.enemy_list):
                bullet.remove_from_sprite_lists()
                enemy.hp -= 1
                if enemy.hp == 0:
                    enemy.remove_from_sprite_lists()

        self.bullet_list.update()

    def player_shoot(self, offset=0, angle=0):
        if self.ammo > 0:
            start_x = self.player.center_x + offset
            start_y = self.player.center_y

            bullet = arcade.Sprite(":resources:images/space_shooter/laserRed01.png")
            bullet.center_x = start_x
            bullet.center_y = start_y + BULLET_OFFSET_DISTANCE

            bullet.angle = angle
            bullet.owner = "player"

            bullet.change_x = BULLET_SPEED * math.cos(math.radians(bullet.angle+90))
            bullet.change_y = BULLET_SPEED * math.sin(math.radians(bullet.angle+90))

            self.bullet_list.append(bullet)

            self.ammo -= 1

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """Called whenever the mouse moves. """
        self.player.center_x = x
        self.player.center_y = y

    def play(self):
        """ Play """
        self.sound.play(pan=self.pan, volume=self.volume)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.UP:
            self.player.center_y += 10
            self.up_pressed = True
        elif symbol == arcade.key.DOWN:
            self.player.center_y -= 10
            self.down_pressed = True
        elif symbol == arcade.key.LEFT:
            self.player.center_x -= 10
            self.left_pressed = True
        elif symbol == arcade.key.RIGHT:
            self.player.center_x += 10
            self.right_pressed = True

        if symbol == arcade.key.SPACE:
            self.player_shoot()
            self.space_pressed = True
            for i in range(-100, 100, 50):
                self.player_shoot(offset = i+1, angle = -i)

            #play sound
            sound = arcade.Sound(":resources:sounds/laser1.mp3")
            sound.play(volume=VOLUME)


        if self.ammo == 0 and symbol == arcade.key.R:
            self.ammo += AMMO

    def on_key_release(self, symbol: int, _modifiers: int):
        if symbol == arcade.key.UP:
            self.up_pressed = False
        elif symbol == arcade.key.DOWN:
            self.down_pressed = False
        elif symbol == arcade.key.RIGHT:
            self.right_pressed = False
        elif symbol == arcade.key.LEFT:
            self.left_pressed = False
        if symbol == arcade.key.SPACE:
            self.player_shoot()
            self.space_pressed = False

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        self.player_shoot()

class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()
        self.time_taken = 0
        self.file_saved = False

    def on_show(self):
        self.background = arcade.load_texture("spacebackground.jpeg")

    def on_draw(self):
        arcade.start_render()
        """
        Draw "Game over" across the screen.
        """
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        arcade.draw_text("Game Over", 240, 400, arcade.color.WHITE, 54)
        arcade.draw_text("Click to restart", 310, 300, arcade.color.WHITE, 24)

        time_taken_formatted = f"{round(self.time_taken, 3)} seconds\n"
        arcade.draw_text(f"Time taken: {time_taken_formatted}", SCREEN_WIDTH / 2, 200, arcade.color.WHITE, font_size=15, anchor_x="center")

        if not self.file_saved:
            with open("player_score.txt", "a") as file:
                file.write(time_taken_formatted)
                self.file_saved = True

        # output_total = f"Total Score: {self.window.total_score}"
        # arcade.draw_text(output_total, 10, 10, arcade.color.WHITE, 14)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = MyGame()
        self.window.show_view(game_view)

def main():
    """ Main method """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game = MyGame() #creating an instance of the game
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()

