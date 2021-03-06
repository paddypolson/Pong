__author__ = 'Paddy'

"""
Pong.
A simple recreation of the age old classic in Python and PyGame

Created by Paddy Polson, paddypolson@gmail.com
Copyright 2015

This implementation of Pong is for educational purposes (hopefully it is still a fun game to play). Some of the features
may be incomplete and some may be broken. I have tried to use programming patterns that are synonymous with good
programming style.

Controls:
Arrow keys to move both paddles up and down.
Space to release a new ball.

TODO:
Split player controls
Add game pad support
Add onscreen scoreboard
Add pause menu
Add randomness to ball creation (subject to play testing)
"""

import pygame
import time
import settings_parse
import random
import skynet
import pygame.gfxdraw as gfxdraw


class Player:
    """
    The player object. Mostly used to hold the paddle and the score for that player
    """

    def __init__(self, player_id, position, joystick=None):

        self.score = 0
        self.joystick = joystick
        self.id = player_id
        self.position = position
        self.paddle = Paddle(self.position)

    def add_score(self):

        self.score += 1


class Direction:
    """
    A simple direction object to aid in ball bouncing. Probably a more clever solution is possible but this fits my
    needs at the moment. Positive values in param 'd' indicates the ball moving up and to the left respectively.
    Negative would be the opposite.
    """

    def __init__(self, random_dir=0, player_towards=0):

        if not random_dir:
            self.d = [1, 1]

        elif player_towards:
            self.d = [random.uniform(0.6, 1), random.uniform(0.6, 1)]

        else:
            self.d = [random.uniform(0.6, 1), -random.uniform(0.6, 1)]

    def x_toggle(self):

        self.d[0] = -self.d[0]

    def up(self):

        self.d[1] = abs(self.d[1])

    def down(self):

        self.d[1] = -abs(self.d[1])

    def left(self):

        self.d[0] = abs(self.d[0])

    def right(self):

        self.d[0] = -abs(self.d[0])


class Paddle:
    """
    The paddle is the object that players use to bounce the ball between each other. Each paddle is controlled by one
    player and has a set speed and size. Direction of travel is controlled with the direction flag. A positive value
    means and upward direction. When the paddle is updated it takes an elapsed time value and calculates the distance to
    travel in that frame.
    The paddle should also check for ball collisions in each frame.
    """

    def __init__(self, position, size=(10, 150), speed=500):

        self.size = size
        self.speed = speed
        self.direction = 0
        self.position = list(position)
        self.surface = pygame.Surface(size)
        self.surface.fill((3, 54, 73))
        self.rect = self.surface.get_rect()

    def get_front(self):

        return self.position[0]

    def get_center(self):

        return self.position[1] + (self.size[1] / 2)

    def get_corners(self):

        return [self.position,
                (self.position[0] + self.size[0], self.position[1]),
                (self.position[0], self.position[1] + self.size[1]),
                (self.position[0] + self.size[0], self.position[1] + self.size[1])]

    def point_inside(self, point):

        corners = self.get_corners()

        return (corners[0][0] <= point[0] <= corners[1][0]) and (corners[0][1] <= point[1] <= corners[2][1])

    def collision(self, ball):

        for corner in ball.get_corners():

            if self.point_inside(corner):

                return True

        return False

    def move_up(self):

        self.direction = 1

    def move_down(self):

        self.direction = -1

    def stop(self):

        self.direction = 0

    def update(self, time_elapsed, limits):

        if self.position[1] < 0:
            self.position[1] = 0

        elif self.position[1] > (limits[1] - self.size[1]):
            self.position[1] = limits[1] - self.size[1]

        else:
            self.position[1] -= time_elapsed * self.speed * self.direction


class Ball:
    """
    The ball is the object moves around the playing board and players must try to avoid it falling off.
    """

    def __init__(self, radius, speed, position):

        self.radius = radius
        self.diameter = self.radius * 2
        self.speed = speed
        self.position = position
        self.direction = Direction(True)
        self.time_in_play = 0
        self.surface = pygame.Surface((self.diameter, self.diameter))
        self.rect = self.surface.get_rect()
        self.surface.set_colorkey((1, 1, 1))
        self.surface.fill((1, 1, 1))
        pygame.draw.circle(self.surface, (3, 101, 100), (self.radius, self.radius), self.radius)

    def paddle_bounce(self):
        '''

        :return:
        '''
        self.direction.x_toggle()

    def get_corners(self):

        return [self.position,
                (self.position[0] + self.diameter, self.position[1]),
                (self.position[0], self.position[1] + self.diameter),
                (self.position[0] + self.diameter, self.position[1] + self.diameter)]

    def update(self, time_elapsed, limits, players):

        self.speed += time_elapsed * 5

        self.position = [x + (time_elapsed * self.speed * d) for x, d in zip(self.position, self.direction.d)]

        # Check for over run
        if int(self.position[0]) <= 0:

            players[0].add_score()
            print [player.score for player in players]
            return False

        elif int(self.position[0]) >= (limits[0] - self.diameter):

            players[1].add_score()
            print [player.score for player in players]
            return False

        elif int(self.position[1]) <= 0:

            self.direction.up()

        elif int(self.position[1]) >= (limits[1] - self.diameter):

            self.direction.down()

        return True


def main():
    """
    The main game function. Welcome to the beginning of the end.
    :return:
    """

    # First we must initialize the pygame module and game clock before most things happen
    pygame.init()
    game_clock = pygame.time.Clock()

    # Grab the settings from the settings file. They are placed in a dictionary.
    settings = settings_parse.parse_settings('settings.cfg')

    window_name = 'Pong'
    window_resolution = settings['x_resolution'], settings['y_resolution']

    # Check to see if the game should run in full screen
    flags = 0
    if settings['full_screen']:
        flags = pygame.FULLSCREEN

    # Build the main game window according to the settings provided
    pygame.display.set_caption(window_name)
    window = pygame.display.set_mode(window_resolution, flags, 32)
    window_rect = window.get_rect()

    # Get the joysticks/gamepads connected
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    for joystick in joysticks:
        joystick.init()

    # Create the game and score area
    # The score area is along the top with a height 1/10th of the window
    score_height = window_rect.height / 10
    game_height = window_rect.height - score_height
    score_surface = pygame.Surface((window_rect.width, score_height))
    game_surface = pygame.Surface((window_rect.width, game_height))

    game_resolution = (settings['x_resolution'], game_height)

    # Font used for FPS counter
    fps_font = pygame.font.SysFont(None, 48)

    # Font used for score
    score_font = pygame.font.SysFont(None, score_height - 4)

    # The number of players in the game
    number_players = 2

    # Determine the players of the game
    if settings['player_one'] == 'human':

        pass

    else:

        pass

    if settings['player_two'] == 'human':

        pass

    else:

        pass

    # Create the starting game objects
    balls = [Ball(10, 200, window.get_rect().center)]
    players = [Player(0, (0, window.get_rect().centery - 50)),
               skynet.AiPlayer(0, (window.get_rect().right - 10, window.get_rect().centery - 50))]
    winner = players[1]

    # Initialize the variable game loop time step
    last_time = time.time()

    while True:

        # The heart of the variable game loop. Keeps track of how long a frame takes to complete
        current_time = time.time()
        time_elapsed = current_time - last_time
        last_time = current_time

        # Game clock used for fps calculation
        game_clock.tick()

        # Handle the pygame events
        # TODO: Move this to a more sensible place
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()

                elif event.key == pygame.K_UP:

                    [player.paddle.move_up() for player in players]

                elif event.key == pygame.K_DOWN:

                    [player.paddle.move_down() for player in players]

                elif event.key == pygame.K_SPACE:

                    balls.append(Ball(10, 200, window.get_rect().center))

            if event.type == pygame.KEYUP:

                [player.paddle.stop() for player in players]

            if (event.type == pygame.JOYAXISMOTION) and (event.axis == 1):

                players[event.joy].paddle.direction = -event.value

            if (event.type == pygame.JOYBUTTONUP) and (event.button == 0):

                player_paddle = players[event.joy].paddle

                ball = Ball(10, 200, player_paddle.position)
                ball.direction = Direction(True, event.joy)
                ball.position = [player_paddle.get_front(), player_paddle.get_center()]
                if not event.joy:
                    ball.position[0] = player_paddle.get_front() + player_paddle.size[0]
                balls.append(ball)

        # Update game objects
        for player in players:
            player.paddle.update(time_elapsed, game_resolution)

            for ball in balls:

                if player.paddle.collision(ball):
                    ball.paddle_bounce()

                if not (ball.update(time_elapsed, game_resolution, players)):

                    balls.remove(ball)

        if not balls:

            balls.append(Ball(10, 200, game_surface.get_rect().center))

        # Run AI
        for player in players:

            try:
                player.target_ball(balls)
                player.update()
            except AttributeError:
                pass

        # Render all game objects
        window.fill((0, 0, 0))

        # Draw the playing field
        board_colour = (232, 221, 203)
        line_colour = (205, 179, 128)
        width = game_surface.get_rect().width
        height = game_surface.get_rect().height
        center_x = game_surface.get_rect().centerx
        center_y = game_surface.get_rect().centery
        game_surface.fill(board_colour)
        pygame.draw.line(game_surface, line_colour, (0, 0), (width, 0), 4)
        pygame.draw.line(game_surface, line_colour, (width - 2, 0), (width - 2, height), 4)
        pygame.draw.line(game_surface, line_colour, (0, 0), (0, height), 4)
        pygame.draw.line(game_surface, line_colour, (0, height - 2), (width, height - 2), 4)
        pygame.draw.line(game_surface, line_colour, (center_x, 0), (center_x, height), 2)
        gfxdraw.aacircle(game_surface, center_x, center_y, 100, line_colour)
        gfxdraw.aacircle(game_surface, center_x, center_y, 101, line_colour)

        for ball in balls:
            game_surface.blit(ball.surface, ball.position)

        for player in players:
            game_surface.blit(player.paddle.surface, player.paddle.position)

        window.blit(game_surface, (0, score_height))

        # Draw The score
        score_string = str(players[0].score) + '   ' + str(players[1].score)
        score = score_font.render(score_string, True, board_colour, (0, 0, 0))
        score_surf_rect = score_surface.get_rect()
        score_rect = score.get_rect()
        score_surface.blit(score, (score_surf_rect.centerx - score_rect.centerx,
                                   score_surf_rect.centery - score_rect.centery))
        pygame.draw.line(score_surface, line_colour, (score_surf_rect.centerx, 0),
                         (score_surf_rect.centerx, score_surf_rect.height), 2)
        window.blit(score_surface, (0, 0))

        if settings['show_fps']:
            fps = fps_font.render(str(int(game_clock.get_fps())), True, (255, 255, 255), (0, 0, 0))
            window.blit(fps, (0, 0))

        # Update the display
        pygame.display.update()


if __name__ == '__main__':

    main()
