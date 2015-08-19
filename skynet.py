__author__ = 'Paddy'

import pong


class AiPlayer(pong.Player):

    def __init__(self, player_id, position, joystick=None):

        pong.Player.__init__(self, player_id, position, joystick)
        self.target = None

    def target_ball(self, balls):

        closest = balls[0]

        for ball in balls:

            if ball.direction.d[0] > 0:

                if ball.position[0] > closest.position[0]:

                    closest = ball

        self.target = closest

    def update(self):

        if self.target:

            if self.paddle.get_center() > self.target.position[1]:

                # Move up
                self.paddle.direction = 1

            elif self.paddle.get_center() < self.target.position[1]:

                # Move down
                self.paddle.direction = -1
