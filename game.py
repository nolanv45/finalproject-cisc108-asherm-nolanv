from dataclasses import dataclass
import random
import time
from designer import *

BOULDER_DROP_SPEED = 10
set_window_color("blue")
HEART_LIMIT = 3


@dataclass
class Boulder:
    boulder_object: DesignerObject
    speed: int


@dataclass
class World:
    background_image: DesignerObject
    player: DesignerObject
    boulders: list[Boulder]
    hearts: list[DesignerObject]
    player_lives: int
    heart_counter: DesignerObject
    invincible: bool
    invincible_timer: int
    elapsed_game_timer: DesignerObject
    game_start_time: int



def create_world() -> World:
    """ Create the world """

    return World(create_background(), create_player(), [], [], 3,
                 text("red", "Lives left: ", 30, get_width() / 2, 80, font_name="Arial"),False, 0, text("blue", "Time played: ", 30, get_width() / 2, 50, font_name="Arial"), time.time())


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
    heart.x = random.randint(0, get_width())
    heart.y = 0
    return heart

def spawn_heart(world: World):
    if len(world.hearts) < HEART_LIMIT:
        heart_chance = random.randint(1,200)
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
    new_boulder = Boulder(emoji('🪨'), random.randint(5,10))

    new_boulder.boulder_object.x = random.randint(0, get_width())
    new_boulder.boulder_object.y = get_height() * -1
    new_boulder.boulder_object.scale = (random.random() + 1)
    return new_boulder

def spawn_boulders(world: World):
    not_too_many_boulders = len(world.boulders) < get_width()
    random_spawning = random.randint(0,10) == 5
    if not_too_many_boulders and random_spawning:
        world.boulders.append(create_boulder())

def drop_boulders(world: World):
    for boulder in world.boulders:
        boulder.boulder_object.y += boulder.speed

def boulder_out_of_bounds(world: World):
    for boulder in world.boulders:
        if boulder.boulder_object.y > get_height():
            destroy(boulder.boulder_object)
            world.boulders.remove(boulder)


def player_is_hurt(world: World):
    invincible_function(world)
    move_forward(world.player, 25, 270)
    world.player_lives -= 1
    update_lives(world)

def invincible_function(world: World):
    world.invincible = True
    world.player.alpha = .5


def is_invincible_timer_up(world:World):
    if time.time() - world.invincible_timer > 1.5:
        world.invincible = False
        world.player.alpha = 1
def boulder_collision(world: World):
    for boulder in world.boulders:
        if colliding(world.player, boulder.boulder_object) and not world.invincible:
            destroy(boulder.boulder_object)
            world.boulders.remove(boulder)
            world.invincible_timer = time.time()
            player_is_hurt(world)




def update_lives(world):
    """Updates player's lives"""
    world.heart_counter.text = "Lives left: " + str(world.player_lives)

def heart_collision(world: World):
    if world.player_lives < 3:
        for heart in world.hearts:
            if colliding(world.player, heart):
                destroy(heart)
                world.hearts.remove(heart)
                world.player_lives += 1
                update_lives(world)


def game_over_screen(world: World):
    """Shows game over screen"""
    world.background_image = rectangle('black', get_width(), get_height())
    world.heart_counter = text('red',"GAME OVER!!!")

def no_player_lives(world: World):
    """Returns True if player's lives equals 0"""
    if world.player_lives == 0:
        return True

def hits_bottom_screen(world: World):
    if world.player.y >= get_height():
        return True
def game_timer(world: World):
    elapsed_time = (time.time() - world.game_start_time) // 1
    world.elapsed_game_timer.text = 'Time played: ' + (str(elapsed_time))


when('starting', create_world)
when('typing', player_move)
when('updating', player_glide_down)
when('updating', update_heart_counter)
when('updating', background_glide_down)
when('updating', heart_glide_down)
when('updating', heart_out_of_bounds)
when('updating', spawn_heart)
when('updating', spawn_boulders)
when('updating', drop_boulders)
when('updating', boulder_out_of_bounds)
when('updating', boulder_collision)
when('updating', heart_collision)
when('updating', is_invincible_timer_up)
when('updating', game_timer)
when(no_player_lives, game_over_screen, pause)
when(hits_bottom_screen, game_over_screen, pause)
start()