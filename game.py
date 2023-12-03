from dataclasses import dataclass
import random
import time
from designer import *

set_window_color("blue")
HEART_LIMIT = 2
high_score = 0


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
    counter_box_outline: DesignerObject
    heart_counter: DesignerObject
    invincible: bool
    invincible_timer: float
    elapsed_game_timer: DesignerObject
    game_start_time: float


@dataclass
class GameOverScreen:
    background_image: DesignerObject
    game_over_text: DesignerObject
    play_again_text: DesignerObject
    high_score_text: DesignerObject


def create_world() -> World:
    """ Create the world """

    return World(create_background(), create_player(), [], [], 3, rectangle('white', 300, 60, y=65, anchor='center'),
                 text("red", "Lives left: ", 30, get_width() / 2, 80, font_name="Arial"), False, 0,
                 text("blue", "Time played: ", 30, get_width() / 2, 50, font_name="Arial"), time.time())


def create_background() -> DesignerObject:
    """ Creates terrain in background of game """
    background = image("https://as2.ftcdn.net/v2/jpg/01/61/99/47/1000_F_161994703_AgIEG3T74954bRN8HQRw5VtFsh16TmuU.jpg")
    background.scale_y = 2
    background.scale_x = 1.5
    background.y = -400
    return background


def background_glide_down(world: World):
    """ Constantly brings background down to make it look like player is falling """
    move_forward(world.background_image, 0.5, 270)


def create_player() -> DesignerObject:
    """ Creates the player """
    player = image("https://i.imgur.com/niSehBi.png")
    player.scale = .15

    player.y = get_height() * (1 / 3)
    return player


def move_left(world: World):
    """ Helper function that allows player to move left so long as they are not on the left edge of the screen """
    if world.player.x > 20:
        world.player.flip_x = True
        move_forward(world.player, 15, 180)


def player_glide_down(world: World):
    """ Have player constantly move down """
    move_forward(world.player, .5, 270)


def heart_glide_down(world: World):
    """ Makes hearts fall down the screen """
    for heart in world.hearts:
        move_forward(heart, 3, 270)

def move_right(world: World):
    """ Helper function that allows player to move right so long as they are not on the right edge of the screen """
    if world.player.x < get_width()-20:
        world.player.flip_x = False
        move_forward(world.player, 15, 0)


def move_up(world: World):
    """ Helper function that allows player to move up so long as they are not at the top of the screen. Also
    makes player image flip to create the illusion of player climbing upwards
    """
    if world.player.y > 20:
        if world.player.flip_x == False:
            world.player.flip_x = True
        elif world.player.flip_x == True:
            world.player.flip_x = False
        move_forward(world.player, 15, 90)


def move_down(world: World):
    """ Helper function that allows player to move down. Also makes player image flip to create the illusion of
    player climbing downwards
    """
    if world.player.flip_x == False:
        world.player.flip_x = True
    elif world.player.flip_x == True:
        world.player.flip_x = False
    move_forward(world.player, 15, 270)


def player_move(world: World, key: str):
    """ Makes player move based on whatever directional key is put in """
    if key == "left":
        move_left(world)
    elif key == "right":
        move_right(world)
    elif key == "up":
        move_up(world)
    elif key == "down":
        move_down(world)


def create_heart() -> DesignerObject:
    """ Creates the heart """
    heart = emoji("❤")
    heart.x = random.randint(0, get_width())
    heart.y = 0
    return heart

def spawn_heart(world: World):
    """ Makes hearts appear on screen """
    if len(world.hearts) < HEART_LIMIT:
        heart_chance = random.randint(1,200)
        if heart_chance == 5:
            world.hearts.append(create_heart())

def heart_out_of_bounds(world: World):
    """ Makes hearts disappear once they reach the bottom of the screen """
    for heart in world.hearts:
        if heart.y > get_height():
            destroy(heart)
            world.hearts.remove(heart)


def update_heart_counter(world: World):
    """ Update the hearts """
    world.heart_counter.text = "Lives left: " + str(world.player_lives)

def create_boulder() -> Boulder:
    """ Creates the boulder """
    new_boulder = Boulder(emoji('🪨'), random.randint(5,10))

    new_boulder.boulder_object.x = random.randint(0, get_width())
    new_boulder.boulder_object.y = get_height() * -1
    new_boulder.boulder_object.scale = (random.random() + 1)
    return new_boulder

def spawn_boulders(world: World):
    """ Makes boulders appear on screen """
    not_too_many_boulders = len(world.boulders) < get_width()
    random_spawning = random.randint(0,10) == 5
    if not_too_many_boulders and random_spawning:
        world.boulders.append(create_boulder())

def drop_boulders(world: World):
    """ Makes boulders fall down the screen at varying speeds """
    for boulder in world.boulders:
        boulder.boulder_object.y += boulder.speed

def boulder_out_of_bounds(world: World):
    """ Makes boulders disappear once at the bottom of the screen """
    for boulder in world.boulders:
        if boulder.boulder_object.y > get_height():
            destroy(boulder.boulder_object)
            world.boulders.remove(boulder)


def player_is_hurt(world: World):
    """ Decreases the player's lives if they are hit by a boulder and pushes them down """
    invincible_function(world)
    move_forward(world.player, 25, 270)
    world.player_lives -= 1
    update_lives(world)

def invincible_function(world: World):
    """ Makes the player invincible and transparent for a short time after being hit by a boulder """
    world.invincible = True
    world.player.alpha = .5


def is_invincible_timer_up(world:World):
    """ Helper function that tests if the player has been invincible for more than 1.5 seconds """
    if time.time() - world.invincible_timer > 1.5:
        world.invincible = False
        world.player.alpha = 1
def boulder_collision(world: World):
    """ Makes boulder disappear after it collides with player """
    for boulder in world.boulders:
        if colliding(world.player, boulder.boulder_object) and not world.invincible:
            destroy(boulder.boulder_object)
            world.boulders.remove(boulder)
            world.invincible_timer = time.time()
            player_is_hurt(world)


def update_lives(world: World):
    """ Updates player's lives """
    world.heart_counter.text = "Lives left: " + str(world.player_lives)

def heart_collision(world: World):
    """ Makes heart disappear once it collides with player, and updates player's lives so long as
    they have less than 3 lives
    """
    if world.player_lives < 3:
        for heart in world.hearts:
            if colliding(world.player, heart):
                destroy(heart)
                world.hearts.remove(heart)
                world.player_lives += 1
                update_lives(world)


def create_game_over_screen(new_score : float) -> GameOverScreen:
    """Shows game over screen"""
    global high_score
    if new_score > high_score:
        high_score = new_score

    return GameOverScreen(rectangle('black', get_width(), get_height()),text('yellow',"GAME OVER!!!", 100, get_width()/2, get_height()/2, font_name="Impact"),
                          text('yellow',"Press Space to Play Again!", 50, get_width()/2, get_height()/1.5, font_name="Arial"),
                          text('yellow',"High Score: " + str(high_score), 50, get_width()/2, get_height()/1.3, font_name="Arial"))


def no_player_lives(world: World):
    """Returns True if player's lives equals 0"""
    if world.player_lives == 0:
        new_score = (time.time() - world.game_start_time) // 1
        change_scene('game_over', new_score=new_score)

def hits_bottom_screen(world: World):
    """ Creates game over screen once player reaches the bottom of the screen """
    if world.player.y >= get_height():
        new_score = (time.time() - world.game_start_time) // 1
        change_scene('game_over', new_score=new_score)

def game_timer(world: World):
    """ Creates game timer """
    elapsed_time = (time.time() - world.game_start_time) // 1
    world.elapsed_game_timer.text = 'Time played: ' + (str(elapsed_time))


def return_to_origin(world: World) -> World:
    """ Resets the background screen when the player reaches the top of the image """
    if world.background_image.y == 1000:
        world.background_image.y = -400
        return World(world.background_image, world.player, world.boulders, world.hearts, world.player_lives, world.counter_box_outline,
                 world.heart_counter, world.invincible, world.invincible_timer, world.elapsed_game_timer, world.game_start_time)

def restart(key: str):
    """ Restarts the game after player loses if they press the space key """
    if key == "space":
        push_scene('game')

when('starting: game', create_world)
when('typing: game', player_move)
when('updating: game', player_glide_down)
when('updating: game', update_heart_counter)
when('updating: game', background_glide_down)
when('updating: game', heart_glide_down)
when('updating: game', heart_out_of_bounds)
when('updating: game', spawn_heart)
when('updating: game', spawn_boulders)
when('updating: game', drop_boulders)
when('updating: game', boulder_out_of_bounds)
when('updating: game', boulder_collision)
when('updating: game', heart_collision)
when('updating: game', is_invincible_timer_up)
when('updating: game', game_timer)
when('updating: game', no_player_lives)
when('updating: game', hits_bottom_screen)
when('starting: game_over', create_game_over_screen)
when('updating: game', return_to_origin)
when('typing: game_over', restart)
start()