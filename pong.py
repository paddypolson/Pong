__author__ = 'Paddy'

'''
Pong.
A simple recreation of the age old classic in Python and PyGame
'''

import pygame
import time
import settings_parse


class Direction:

    def __init__(self):

        self.d = [1, 1]

    def y_toggle(self):

        self.d[1] = -self.d[1]

    def x_toggle(self):

        self.d[0] = -self.d[0]


class Paddle:

    def __init__(self, size, speed, x):

        self.size = size
        self.speed = speed
        self.distance = 0
        self.x = x
        self.y = 0
        self.surface = pygame.Surface(size)
        self.surface.fill((40, 40, 40))

    def add_distance(self, distance):

        self.distance += distance

    def update(self, time):

        pass


class Ball:

    def __init__(self, radius, speed, position):

        self.radius = radius
        self.diameter = self.radius * 2
        self.speed = speed
        self.position = position
        self.last_position = self.position
        self.direction = Direction()
        self.surface = pygame.Surface((self.diameter, self.diameter))
        pygame.draw.circle(self.surface, (0, 0, 255), (self.radius, self.radius), self.radius)

    def paddle_bounce(self):
        '''

        :return:
        '''
        self.direction.x_toggle()

    def wall_bounce(self):
        '''

        :return:
        '''
        self.direction.y_toggle()

    def update(self, time_elapsed, limits):

        self.last_position = self.position
        self.position = [x + (time_elapsed * self.speed * d) for x, d in zip(self.position, self.direction.d)]

        # Check for over run
        if int(self.position[0]) <= 0:
            self.paddle_bounce()

        elif int(self.position[0]) >= (limits[0] - self.diameter):
            self.paddle_bounce()

        elif int(self.position[1]) <= 0:
            self.wall_bounce()

        elif int(self.position[1]) >= (limits[1] - self.diameter):
            self.wall_bounce()


def main():

    pygame.init()
    game_clock = pygame.time.Clock()

    settings = settings_parse.parse_settings('settings.cfg')

    window_name = 'Pong'
    window_resolution = settings['x_resolution'], settings['y_resolution']

    flags = 0
    if settings['full_screen']:
        flags = pygame.FULLSCREEN

    pygame.display.set_caption(window_name)
    window = pygame.display.set_mode(window_resolution, flags, 32)

    # Font used for FPS counter
    basic_font = pygame.font.SysFont(None, 48)

    if settings['player_one'] == 'human':

        pass

    else:

        pass

    if settings['player_two'] == 'human':

        pass

    else:

        pass

    ball = Ball(10, 200, window.get_rect().center)

    last_time = time.time()

    while True:

        current_time = time.time()
        time_elapsed = last_time - current_time
        last_time = current_time

        events = pygame.event.get()

        # Handle events
        for event in events:

            if event.type == pygame.QUIT:
                pygame.quit()

        # Update game objects
        ball.update(time_elapsed, window_resolution)

        # Render
        window.fill((0, 0, 0))
        window.blit(ball.surface, ball.position)

        fps = basic_font.render(str(game_clock.get_fps()), True, (255, 255, 255), (0, 0, 0))
        window.blit(fps, (0, 0))

        game_clock.tick()

        # Update the display
        pygame.display.update()


if __name__ == '__main__':

    main()
