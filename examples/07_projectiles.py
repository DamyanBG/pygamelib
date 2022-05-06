import examples_includes  # noqa: F401
from pygamelib import engine, board_items, base, constants
from pygamelib.gfx import core
from pygamelib.assets import graphics

black_circle = f"-{graphics.GeometricShapes.BLACK_CIRCLE}"
circle_jot = "-\U0000233E"


def manage_fireballs():
    global g
    for item in g.current_board().get_movables():
        if "fireball" in item.name:
            item.range -= 1
            if item.range == 0:
                item.animation = None
                item.model = graphics.Models.EXPLOSION
                item.actuator.stop()
            elif item.range < 0:
                item.model = g.current_board().ui_board_void_cell
                g.current_board().clear_cell(item.pos[0], item.pos[1])


def redraw_screen():
    global g
    g.clear_screen()
    nb_blocks = int((g.player.mp / g.player.max_mp) * 20)
    print(
        "Mana ["
        + graphics.BLUE_RECT * nb_blocks
        + graphics.BLACK_RECT * (20 - nb_blocks)
        + "]"
    )
    g.display_board()
    # manage_fireballs()


def update(g: engine.Game, key, dt):
    if key == "Q":
        g.stop()
    elif key == "1":
        viewport = [10, 10]
        g.partial_display_viewport = viewport
    elif key == "2":
        viewport = [15, 30]
        g.partial_display_viewport = viewport
    elif key == "3":
        viewport = [20, 20]
        g.partial_display_viewport = viewport
    if key == " " and g.player.mp >= 4:
        fireball = board_items.Projectile(
            name="fireball",
            model=base.Text.red_bright(black_circle),
            hit_model=graphics.Models.COLLISION,
        )
        fireball.animation = core.Animation(
            auto_replay=True,
            animated_object=fireball,
            refresh_screen=None,
            display_time=0.5,
        )
        fireball.animation.add_frame(base.Text.red_bright(black_circle))
        fireball.animation.add_frame(base.Text.red_bright(circle_jot))
        fireball.range = 7
        fireball.set_direction(constants.RIGHT)
        g.add_projectile(1, fireball, g.player.pos[0], g.player.pos[1] + 1)
        g.player.mp -= 6

    elif key == engine.key.UP:
        g.move_player(constants.UP, 1)
    elif key == engine.key.DOWN:
        g.move_player(constants.DOWN, 1)
    elif key == engine.key.LEFT:
        g.move_player(constants.LEFT, 1)
    elif key == engine.key.RIGHT:
        g.move_player(constants.RIGHT, 1)

    redraw_screen()
    g.actuate_npcs(1)
    g.actuate_projectiles(1)
    g.animate_items(1)
    for f in g.current_board().get_movables():
        print(f"{f.name} position {f.pos}")
    if g.player.mp < 4:
        print(f"{g.player.model} I'm all out of mana")
    if g.player.mp < 20:
        g.player.mp += 0.02
    else:
        g.player.mp = 20


b = engine.Board(
    ui_borders=graphics.WHITE_SQUARE,
    ui_board_void_cell=graphics.BLACK_SQUARE,
    size=[20, 20],
    player_starting_position=[5, 5],
)
wall = board_items.Wall(sprixel=core.Sprixel(graphics.Models.BRICK))
b.place_item(wall, 1, 6)
b.place_item(wall, 1, 7)
b.place_item(wall, 1, 8)
b.place_item(wall, 1, 9)
b.place_item(wall, 2, 9)
b.place_item(wall, 3, 9)
b.place_item(wall, 4, 9)

g = engine.Game.instance(mode=constants.MODE_RT, user_update=update)
g.add_board(1, b)
g.player = board_items.Player(
    sprixel=core.Sprixel(graphics.Models.MAGE), name="The Maje"
)
g.player.mp = 20
g.player.max_mp = 20
g.change_level(1)
g.run()
