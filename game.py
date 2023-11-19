from dataclasses import dataclass
from designer import *
from random import randint

BOULDER_DROP_SPEED = 10
set_window_color("blue")
HEART_LIMIT = 3

@dataclass
class World:
    background_image: DesignerObject
    player: DesignerObject
    boulders: list[DesignerObject]
    hearts: list[DesignerObject]
    player_lives: int
    heart_counter: DesignerObject


def create_world() -> World:
    """ Create the world """

    return World(create_background(), create_player(), [], [], 3,
                 text("red", "Lives left: ", 30, get_width() / 2, 80, font_name="Arial"))


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

def heart_glide_down(world: World):
    for heart in world.hearts:
        move_forward(heart, 3, 270)

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
    heart.y = 0
    return heart

def spawn_heart(world: World):
    if len(world.hearts) < HEART_LIMIT:
        heart_chance = randint(1,200)
        if heart_chance == 5:
            world.hearts.append(create_heart())

def heart_out_of_bounds(world: World):
    for heart in world.hearts:
        if heart.y > get_height():
            destroy(heart)
            world.hearts.remove(heart)


def update_heart_counter(world: World):
    """ Update the hearts """
    world.heart_counter.text = "Lives left: " + str(world.player_lives)

def create_boulder():
    boulder = emoji('🪨')
    boulder.x = randint(0, get_width())
    boulder.y = get_height() * -1
    return boulder

def spawn_boulders(world: World):
    not_too_many_boulders = len(world.boulders) < get_width()
    random_spawning = randint(0,10) == 5
    if not_too_many_boulders and random_spawning:
        world.boulders.append(create_boulder())

def drop_boulders(world: World):
    for boulder in world.boulders:
        boulder.y += BOULDER_DROP_SPEED

def boulder_out_of_bounds(world: World):
    for boulder in world.boulders:
        if boulder.y > get_height():
            destroy(boulder)
            world.boulders.remove(boulder)

when('starting', create_world)
when('typing', player_move)
when('updating', player_glide_down)
when('updating', update_heart_counter)
when('updating', background_glide_down)
when('updating', heart_glide_down)
when('updating', heart_out_of_bounds)
when('updating', spawn_heart)
start()