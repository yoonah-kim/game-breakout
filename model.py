# model.py
# Augustine Lee (ayl43) and Yoonah Kim (yhk24)
# May 07, 2014
"""Model module for Breakout

This module contains the model classes for the Breakout game. Instances of
Model storee the paddle, ball, and bricks.  The model has methods for resolving
collisions between the various game objects.  A lot of your of your work
on this assignment will be in this class.

This module also has an additional class for the ball.  You may wish to add
more classes (such as a Brick class) to add new features to the game.  What
you add is up to you."""
from constants import *
from game2d import *
import random # To randomly generate the ball velocity


class Model(object):
    """An instance is a single game of breakout.  The model keeps track of the
    state of the game.  It tracks the location of the ball, paddle, and bricks.
    It determines whether the player has won or lost the game.  
    
    To support the game, it has the following instance attributes:
    
        bricks:  the bricks still remaining 
                  [list of GRectangle, can be empty]
        paddle:  the paddle to play with 
                  [GRectangle, never None]
        ball:    the ball 
                  [Ball, or None if waiting for a serve(state is in STATE_COUNTDOWN]
    """
    # As with the controller, any attributes that you add to this class
    # must be documented above, along with their invariants.
    
    # INITIALIZER (TO CREATE PADDLES AND BRICKS)

    def __init__(self):
        """Constructor Expression. Creates a new Model instance with bricks, paddle, and ball."""
        self.bricks = []
        self.getrowbricks()
        self.paddle = GRectangle(center_x = GAME_WIDTH/2, center_y = PADDLE_OFFSET,
                      width = PADDLE_WIDTH, height = PADDLE_HEIGHT,
                      linecolor = colormodel.BLACK, fillcolor = colormodel.BLACK)
        self.ball = Ball()
    # ADD ANY ADDITIONAL METHODS (PROPERLY SPECIFIED) HERE

    def createbricksrow(self, positiony, linecolor, fillcolor):
        """Creates rows of bricks, with the first two being red, next two being orange,
        next two being yellow, next two being green, and the final two being cyan.
        positiony is the y coordinate of the lower left corner of a brick of the next row.
        linecolor is the color of the outline color.
        fillcolor is the color of the interior of the brick.
        Preconditions:
        positiony is an int or float. linecolor is an instance of the RGB Class.
        fillcolor is an instance of the RGB Class."""
        nexthposition = 0
        for x in range(BRICKS_IN_ROW):
            self.bricks.append(GRectangle(x = BRICK_SEP_H/2 + nexthposition,
            y = positiony, width = BRICK_WIDTH,
            height = BRICK_HEIGHT, linecolor = linecolor,
            fillcolor = fillcolor))
            nexthposition=nexthposition + (BRICK_WIDTH + BRICK_SEP_H)

    def getrowbricks(self):
        """Creates entire list of bricks."""
        positiony = GAME_HEIGHT - BRICK_Y_OFFSET
        for x in range(BRICK_ROWS):
            if x%100 == 0 or x%100 == 1:
                linecolor = colormodel.RED
                fillcolor = colormodel.RED
            if x%100 == 2 or x%100 == 3:
                linecolor = colormodel.ORANGE
                fillcolor = colormodel.ORANGE
            if x%100 == 4 or x%100 == 5:
                linecolor = colormodel.YELLOW
                fillcolor = colormodel.YELLOW
            if x%100 == 6 or x%100 == 7:
                linecolor = colormodel.GREEN
                fillcolor = colormodel.GREEN
            if x%100 == 8 or x%100 == 9:
                linecolor = colormodel.CYAN
                fillcolor = colormodel.CYAN
            self.createbricksrow(positiony, linecolor, fillcolor)
            positiony = positiony - BRICK_SEP_V - BRICK_HEIGHT
    
    def moveball(self):
        """Moves the ball and handles collisions with the bricks and walls."""
        self.ball.center_x = self.ball.vx + self.ball.center_x
        self.ball.center_y = self.ball.vy + self.ball.center_y
        if self.ball.y + self.ball.height>= GAME_HEIGHT:
            self.ball.negativevy()
        #if self.ball.y <= 0:
         #   self.ball.negativevy()
        if self.ball.x + self.ball.width >= GAME_WIDTH or self.ball.x <=0:
            self.ball.negativevx()
        if self._getCollidingObject() == self.paddle and self.ball.vy < 0:
            self.ball.negativevy()
            self.ball.negativevx()
            Sound('saucer2.wav').play()
        elif self._getCollidingObject() == self.paddle and self.ball.vy > 0:
            None
        elif self._getCollidingObject() != None:
            self.bricks.pop(self.bricks.index(self._getCollidingObject()))
            self.ball.negativevy()
            Sound('plate2.wav').play()

    def _getCollidingObject(self):
        """Returns: GObject that has collided with the ball

        This method checks the four corners of the ball, one at a
        time. If one of these points collides with either the paddle
        or a brick, it stops the checking immediately and returns the
        object involved in the collision. It returns None if no
        collision occurred."""
        for bricks in self.bricks:
            if bricks.contains(self.ball.x, self.ball.y) \
            or bricks.contains(self.ball.x + BALL_DIAMETER, self.ball.y) \
            or bricks.contains(self.ball.x, self.ball.y+BALL_DIAMETER) \
            or bricks.contains(self.ball.x + BALL_DIAMETER, self.ball.y
            + BALL_DIAMETER):
                return bricks
            else:
                None
        if self.paddle.contains(self.ball.x, self.ball.y) or \
        self.paddle.contains(self.ball.x + BALL_DIAMETER, self.ball.y) \
        or self.paddle.contains(self.ball.x, self.ball.y+BALL_DIAMETER) \
        or self.paddle.contains(self.ball.x + BALL_DIAMETER, self.ball.y +
        BALL_DIAMETER):
            return self.paddle
        else:
            None


class Ball(GEllipse):
    """Instance is a game ball.
    
    We extend GEllipse because a ball needs attributes for
    velocity. This subclass adds these two attributes.
    
    INSTANCE ATTRIBUTES:
        vx: Velocity in x direction [int or float]
        vy: Velocity in y direction [int or float]
    
    You should add two methods to this class: an initializer to set the
    starting velocity  and a method to "move" the ball. The move method
    should adjust the ball position according to the velocity.
    
    NOTE: The ball does not have to be a GEllipse. It could be an instance
    of GImage (why?). This change is allowed, but then you will have to
    modify the class header up above.
    """
    
    # INITIALIZER TO SET VELOCITY

    def __init__(self):
        """Constructor expression. Creates a new Ball Instance with velocity x coordinates
        and velocity y coordinates."""
        self.ball = GEllipse.__init__(self, center_x = GAME_WIDTH/2, center_y =
                    GAME_HEIGHT/2, linecolor = colormodel.BLACK,
                    fillcolor = colormodel.BLACK, width = BALL_DIAMETER,
                    height = BALL_DIAMETER)
        self.vx = random.uniform(1.0, 5.0)
        self.vx = self.vx * random.choice([-1,1])
        self.vy = -5.0
    
    # METHOD TO MOVE BALL BY PROPER VELOCITY

    def negativevy(self):
        """Makes the vertical velocity negative."""
        self.vy = -(self.vy)

    def negativevx(self):
        """Makes the horizontal velocity negative."""
        self.vx = -(self.vx)
    
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


# ADD ANY ADDITIONAL CLASSES HERE