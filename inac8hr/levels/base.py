import arcade
import random
from inac8hr.events import Event
from inac8hr.loaders import ImageLoader
from inac8hr.levels.tilemaps import TILEMAP
from inac8hr.layers import PlayableSceneLayer
from inac8hr.utils import LocationUtil
from inac8hr.globals import *
from inac8hr.particles import Bullet
from inac8hr.entities import DefenderUnit, AgentUnit, UnitList, UnitKeyedList, PollingStaUnit
from inac8hr.imports import *
from inac8hr.cycles import CycleClock
from inac8hr.scoring import ScoringEngine
from inac8hr.tuning import ScoringFactor

BOARD = [
        '%X%###############',
        '% %#% == ##### = #',
        '% %%% %% ####  # #',
        '%C=== %% #### ## #',
        '%%%%%%%% ####  # #',
        '## ===== ##### # #',
        '## ##########  # #',
        '## ## ==== ## ## #',
        '##  T #### ##  # #',
        '####E##### ### # #',
        '####E##### === # #',
        '####&###########O#']

BLOCK_SIZE = 40


class Level(PlayableSceneLayer):
    registered_inputs = [UserEvent.WINDOW_RESIZE]

    def __init__(self):
        self.scoring = ScoringEngine()
        self.cycle = CycleClock()
        self.full_health = 50
        self.map_plan = MapPlan(BOARD, 40)
        self.defenders = UnitKeyedList()
        self.enemies = UnitList()
        self.particles = UnitList()
        self.__state__ = LevelState.PLAYING
        self.scaling = 1
        self.score = 0
        self.sprite_list = None
        # self.generate_enemies()
        # self.generate_ballots()

    #
    # Arcade base overload functions
    #
    def draw(self):
        self.map_plan.draw()
        self.enemies.draw()
        self.defenders.draw()
        self.particles.draw()

    def clocked_update(self):
        self.cycle.update()
        if self.state == LevelState.PAUSED:
            self.pause()
            self.cycle.pause()
        elif self.state == LevelState.PLAYING:
            self.play()
            self.cycle.resume()
            if not self.cycle.started:
                self.cycle.start()
    #
    #
    #

    def set_state(self, value):
        self.__state__ = value

    def get_state(self):
        return self.__state__

    state = property(get_state, set_state)


    def pause(self):
        for e, d in zip(self.enemies, self.defenders.values()):
            e.pause()
            d.pause()

    def play(self):
        for p in self.particles:
            p.play()
        for e in self.enemies:
            if e.dead:
                self.calculate_the_dead(e)
            else:
                playing = True
                remove_list = []
                for p in self.particles:
                    if p.collides(e):
                        e.take_damage(p.damage)    
                        playing = False
                        p.dispose()
                        remove_list.append(p)
                    elif p.disarmed:
                        p.dispose()
                        remove_list.append(p)
                for i in remove_list:
                    self.particles.remove(i)
                if playing:
                    e.play()
        for d in self.defenders.values():
            selected_enemy = None
            dist = [[d.closest_rad(e), e] for e in self.enemies if 0 <= d.closest_rad(e) <= d.coverage_radius]
            sorted(dist, key=lambda x: x[0])
            if len(dist) > 0:
                selected_enemy = dist[0][1]
            if selected_enemy is not None:# and not selected_enemy.targeted:
                d.target_pos = selected_enemy.position
                bullet = d.shoot()
                if bullet is not None:
                    self.particles.append(bullet)
            d.play()
        # if len(self.enemies) == 0:
        #     self.generate_enemies()

    def generate_enemies(self):
        x, y = self.map_plan.get_initial_agent_position()
        initial_pos = x, y
        diff = 0
        for _ in range(4):
            files = ['Ballot_pink.png', 'Ballot_orange.png', 'Ballot_red.png']
            r = random.randint(0, len(files)-1)
            enemy = AgentUnit([f'assets/images/chars/{files[r]}'], initial_pos, self.full_health, GAME_PREFS.scaling, self.map_plan.switch_points)
            enemy.displace_position(0, diff)
            diff += 40
            self.enemies.append(enemy)
        self.full_health += 80

    def generate_ballots(self):
        x, y = self.map_plan.get_initial_station_location()
        initial_pos = x, y
        diff = 0
        for _ in range(4):
            files = ['Ballot_pink.png', 'Ballot_orange.png', 'Ballot_red.png']
            r = random.randint(0, len(files)-1)
            # GAME_PREFS.scaling = 1
            enemy = AgentUnit([f'assets/images/chars/{files[r]}'], initial_pos, self.full_health, 1, self.map_plan.ballot_switch_points)
            enemy.displace_position(0, diff)
            diff += 40
            self.enemies.append(enemy)
        self.full_health += 80

    def place_defender(self, x, y, category=None):
        self.defenders[(x, y)] = DefenderUnit(["assets/images/chars/shredder_40px.png", "assets/images/chars/unavail.png"], (x, y), GAME_PREFS.scaling)

    def is_defender_at(self, x, y):
        return (x, y) in self.defenders

    def get_defender_at(self, x, y):
        if self.is_defender_at(x, y):
            return self.defenders[(x, y)]
        else:
            return False

    def is_playing(self):
        return self.state == LevelState.PLAYING

    def on_resize(self):
        self.scaling = GAME_PREFS.scaling
        self.defenders.scale(GAME_PREFS.scaling)
        self.map_plan.scale(GAME_PREFS.scaling)

    def flow_along_the_path(self):
        pass

    def calculate_the_dead(self, enemy):
        pass


class MapPlan():
    def __init__(self, plan_list, block_size):
        self.block_size = block_size
        self.plan_array = plan_list
        self.switch_points = []
        self.ballot_switch_points = []
        self.determine_dimensions()
        self.gen_ballot_flow_points()
        self.calculate_all_switch_points()
        self.sprites = ExtendedSpriteList()
        self.init_sprites()
        self.exit = arcade.Sprite('assets/images/chars/ballot_box.png')
        self.exit_position = self.get_initial_exit_position()
        self.init_exit_sprite()

    def scale(self, scaling):
        self.sprites = ExtendedSpriteList() 
        self.init_sprites(scaling)

    def determine_dimensions(self):
        self.width = len(self.plan_array[0])
        self.height = len(self.plan_array)

    def init_exit_sprite(self):
        r, c = self.exit_position
        x, y = LocationUtil.get_sprite_position(r, c)
        self.exit.set_position(x, y)

    def gen_ballot_flow_points(self):
        x, y = self.get_initial_station_location()
        out_of_bounds = False
        board = list(self.plan_array)
        while not out_of_bounds:
            for offset_key in DIR_OFFSETS.keys():
                x_offset, y_offset = DIR_OFFSETS[offset_key]           
                check_pos = (x + x_offset, y + y_offset)
                status = self.is_path_routable(check_pos, board)
                if status == 0:
                    self.ballot_switch_points.append([check_pos, offset_key])
                    line = list(board[x])
                    line[y] = '-'
                    board[x] = ''.join(line)

                    x, y = check_pos

                    line = list(board[check_pos[0]])
                    line[check_pos[1]] = 'X'
                    board[check_pos[0]] = ''.join(line)

                elif status == 2:
                    out_of_bounds = True

    def preview_board_specific(self, board):
        for line in board:
            print(line)

    def calculate_all_switch_points(self):
        x, y = self.get_initial_agent_position()
        out_of_bounds = False
        board = list(self.plan_array)
        while not out_of_bounds:
            for offset_key in DIR_OFFSETS.keys():
                x_offset, y_offset = DIR_OFFSETS[offset_key]           
                check_pos = (x + x_offset, y + y_offset)
                status = self.is_obstacle_char(check_pos, board)
                if status == 0:
                    self.switch_points.append([check_pos, offset_key])
                    line = list(board[x])
                    line[y] = '-'
                    board[x] = ''.join(line)

                    x, y = check_pos

                    line = list(board[check_pos[0]])
                    line[check_pos[1]] = 'X'
                    board[check_pos[0]] = ''.join(line)

                elif status == 2:
                    out_of_bounds = True

    def init_sprites(self, scaling=1):
        for s in self.get_all_sprites(scaling):
            self.sprites.append(s)

    def draw_sprite(self, sprite, r, c):
        x, y = LocationUtil.get_sprite_position(r, c)
        sprite.set_position(x, y)
        sprite.draw()
        return sprite

    def get_all_sprites(self, scaling=1):
        sprites = []
        for r in range(0, self.height):
            for c in range(self.width):
                if self.is_available_in_tilemap((r, c)):
                    sprites.append(self.get_sprite_from_pos(r, c, scaling))
        return sprites

    def get_initial_entities_position(self, char):
        entities = []
        for i in range(len(self.plan_array)):
            for j in range(len(self.plan_array[i])):
                if self.plan_array[i][j] == char:
                    entities.append((i, j))
                    print(i, j)
        return entities

    def get_initial_entity_position(self, char):
        for i in range(len(self.plan_array)):
            for j in range(len(self.plan_array[i])):
                if self.plan_array[i][j] == char:
                    return (i, j)
        return (-1, -1)

    def get_initial_agent_position(self):
        return self.get_initial_entity_position('X')

    def get_initial_station_location(self):
        return self.get_initial_entity_position('&')

    def get_initial_exit_position(self):
        return self.get_initial_entity_position('O')

    def get_all_generators(self):
        return [PollingStaUnit(['assets/images/chars/ballot_box.png'], (x, y)) for x, y in self.get_initial_entities_position("&")]
#
# Arcade-based overridden functions
#
    def draw(self):
        self.sprites.draw()
        self.exit.draw()
#
#
#

    def get_sprite_from_pos(self, r, c, scaling):
        idx = self.plan_array[r][c]
        angle = 0
        if idx == "=":
            angle = 90
        sprite = arcade.Sprite(ImageLoader.get_texture_filename_from_index(idx),
                               scale=scaling)
        sprite.angle = angle
        x, y = LocationUtil.get_sprite_position(r, c)
        sprite.set_position(x, y)
        return sprite

    def is_available_in_tilemap(self, pos):
        return self.plan_array[pos[0]][pos[1]] in TILEMAP.keys()

    def is_wall_at(self, pos):
        board = self.plan_array
        if -1 <= pos[0] <= len(board) - 1 and -1 <= pos[1] <= len(board[0]) - 1:
            return board[pos[0]][pos[1]] == '#'
        else:
            return False

    def is_obstacle_char(self, pos, board):
        if -1 <= pos[0] <= len(board) - 1 and -1 <= pos[1] <= len(board[0]) - 1:
            if board[pos[0]][pos[1]] in ' |=CT':
                return 0
            elif board[pos[0]][pos[1]] == 'O':
                return 2
            else:
                return 1
        else:
            return 2

    def is_path_routable(self, pos, board):
        """
            Given a position, determine whether an agent can be routed through that or not
        """
        if -1 <= pos[0] <= len(board) - 1 and -1 <= pos[1] <= len(board[0]) - 1:
            if board[pos[0]][pos[1]] in ' |=CTE':
                return 0
            elif board[pos[0]][pos[1]] == 'O':
                return 2
            else:
                return 1
        else:
            return 2
