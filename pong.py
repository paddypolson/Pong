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

    def __init__(self, size, speed, position):

        self.size = size
        self.speed = speed
        self.direction = 0
        self.position = list(position)
        self.surface = pygame.Surface(size)
        self.surface.fill((40, 40, 40))
        self.rect = self.surface.get_rect()

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
            self.position[1] += time_elapsed * self.speed * self.direction


class Ball:

    def __init__(self, radius, speed, position):

        self.radius = radius
        self.diameter = self.radius * 2
        self.speed = speed
        self.position = position
        self.direction = Direction()
        self.surface = pygame.Surface((self.diameter, self.diameter))
        self.rect = self.surface.get_rect()
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

    def get_corners(self):

        return [self.position,
                (self.position[0] + self.diameter, self.position[1]),
                (self.position[0], self.position[1] + self.diameter),
                (self.position[0] + self.diameter, self.position[1] + self.diameter)]

    def update(self, time_elapsed, limits):

        self.position = [x + (time_elapsed * self.speed * d) for x, d in zip(self.position, self.direction.d)]

        # Check for over run
        if int(self.position[0]) <= 0:

            # Should be score point
            self.paddle_bounce()

        elif int(self.position[0]) >= (limits[0] - self.diameter):

            # Should be score point
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
    paddle_one = Paddle((10,100), 300, (0, window.get_rect().centery - 50))

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

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:

                    paddle_one.move_up()

                elif event.key == pygame.K_DOWN:

                    paddle_one.move_down()

            if event.type == pygame.KEYUP:

                paddle_one.stop()

        # Update game objects
        ball.update(time_elapsed, window_resolution)
        paddle_one.update(time_elapsed, window_resolution)

        if paddle_one.collision(ball):
            print 'bounce'
            ball.paddle_bounce()

        # Render
        window.fill((0, 0, 0))
        window.blit(ball.surface, ball.position)
        window.blit(paddle_one.surface, paddle_one.position)

        if settings['show_fps']:
            fps = basic_font.render(str(game_clock.get_fps()), True, (255, 255, 255), (0, 0, 0))
            window.blit(fps, (0, 0))

        game_clock.tick()

        # Update the display
        pygame.display.update()


if __name__ == '__main__':

    main()
