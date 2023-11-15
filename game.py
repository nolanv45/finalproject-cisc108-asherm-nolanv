from dataclasses import dataclass
from designer import *
from random import randint

BOULDER_DROP_SPEED = 10
set_window_color("blue")


@dataclass
class World:
    background_image: DesignerObject
    player: DesignerObject
    boulders: list[DesignerObject]
    hearts: list[DesignerObject]
    score: int
    score_counter: DesignerObject


def create_world() -> World:
    """ Create the world """

    return World(create_background(), create_player(), [], [], 0,
                 text("black", "Score: ", 20, get_width() / 2, 100, font_name="Arial"))


def create_background() -> DesignerObject:
    background = image("https://as2.ftcdn.net/v2/jpg/01/61/99/47/1000_F_161994703_AgIEG3T74954bRN8HQRw5VtFsh16TmuU.jpg")
    background.scale_y = 2
    background.scale_x = 1.5
    background.y = -400
    return background


def background_glide_down(world: World):
    move_forward(world.background_image, 0.5, 270)


def create_player() -> DesignerObject:
    player = image("https://i.imgur.com/niSehBi.png")
    player.scale = .15

    player.y = get_height() * (1 / 3)
    return player


def move_left(world: World):
    world.player.flip_x = True
    move_forward(world.player, 15, 180)


def player_glide_down(world: World):
    move_forward(world.player, .5, 270)


def move_right(world: World):
    world.player.flip_x = False
    move_forward(world.player, 15, 0)


def move_up(world: World):
    if world.player.flip_x == False:
        world.player.flip_x = True
    elif world.player.flip_x == True:
        world.player.flip_x = False
    move_forward(world.player, 15, 90)


def move_down(world: World):
    if world.player.flip_x == False:
        world.player.flip_x = True
    elif world.player.flip_x == True:
        world.player.flip_x = False
    move_forward(world.player, 15, 270)


def player_move(world: World, key: str):
    if key == "left":

        move_left(world)

    elif key == "right":
        move_right(world)
    elif key == "up":
        move_up(world)
    elif key == "down":
        move_down(world)


def create_heart() -> DesignerObject:
    heart = emoji("❤")
    heart.x = randint(0, get_width())
    heart.y = randint(0, -1 * get_height())
    return heart

def spawn_heart(world : World):



when('starting', create_world)
when('typing', player_move)
when('updating', player_glide_down)
when('updating', background_glide_down)
start()