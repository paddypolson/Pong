__author__ = 'Paddy'

import pong


class AiPlayer(pong.Player):

    def __init__(self, player_id, position, joystick=None):

        pong.Player.__init__(self, player_id, position, joystick)
        self.target = None

    def target_ball(self, balls):

        # Find a new target if the old target has died
        if not (self.target in balls):
            self.target = balls[0]

        # Grab all the possible target candidates
        candidates = []
        # And remember the balls heading in the other direction
        secondary = []

        for ball in balls:

            if ball.direction.d[0] > 0:
                candidates.append(ball)

            else:
                secondary.append(ball)

        # Check for any possible target
        if candidates:
            # Find the closest target
            closest = candidates[0]

            for ball in candidates:

                if ball.position[0] > closest.position[0]:

                    closest = ball

            self.target = closest

        else:
            # Look for balls heading in the other direction
            closest = secondary[0]

            for ball in secondary:

                if ball.position[0] < closest.position[0]:

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
