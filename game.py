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
    background = image(
        "https://media.istockphoto.com/id/1197030852/photo/view-at-autumn-appalachian-mountains.jpg?s=612x612&w=0&k=20&c=PoFJpB6KHW7b9RYDSG1912xSmx0AkYpEkWh3pacmZkk=")
    background.scale_y = 3
    background.scale_x = 3
    return background


def background_glide_down(world: World):
    move_forward(world.background_image, 0.5, 270)


def create_player() -> DesignerObject:
    player = emoji("😂")
    player.y = get_height() * (1 / 3)
    return player


def move_left(world: World):
    move_forward(world.player, 15, 180)


def player_glide_down(world: World):
    move_forward(world.player, .5, 270)


def move_right(world: World):
    move_forward(world.player, 15, 0)


def move_up(world: World):
    move_forward(world.player, 15, 90)


def move_down(world: World):
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


when('starting', create_world)
when('typing', player_move)
when('updating', player_glide_down)
when('updating', background_glide_down)
start()