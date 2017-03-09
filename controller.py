# controller.py
# Augustine Lee (ayl43) and Yoonah Kim (yhk24)
# May 07, 2014
"""Primary module for Breakout application

This module contains the controller class for the Breakout application.
There should not be any need for additional classes in this module.
If you need more classes, 99% of the time they belong in the model 
module. If you are ensure about where a new class should go, post a
question on Piazza."""
from constants import *
from game2d import *
from model import *


class Breakout(Game):
    """Instance is a Breakout Application
    
    This class extends Game and implements the various methods necessary
    for running the game.
    
        Method init starts up the game.
        
        Method update updates the model objects (e.g. move ball, remove bricks)
        
        Method draw displays all of the models on the screen
    
    Most of the work handling the game is actually provided in the class Model.
    Model should have a method called moveBall() that moves the ball and processes
    all of the game physics. This class should simply call that method in update().
    
    The primary purpose of this class is managing the game state: when is the 
    game started, paused, completed, etc. It keeps track of that in an attribute
    called _state.
    
    Instance Attributes:
        view:   the game view, used in drawing 
                [Immutable instance of GView, it is inherited from Game]
        _state: the current state of the game
                [one of STATE_INACTIVE, STATE_COUNTDOWN, STATE_PAUSED, 
                 STATE_ACTIVE, or STATE_COMPLETE]
        _model: the game model, which stored the paddle, ball, and bricks
                [GModel, or None if there is no game currently active
                 It is only None if _state is STATE_INACTIVE]
        _message: the initial welcome screen when user starts up game
                  [GLabel or None if no message]
        _previoustouch: the previous touch location
                [GView or None]
        _time:  the number of frames passed
                [int >= 0]
        _lives: the number of lives the user has left in the game:
                [0 <= int <= 3]
    """
    # You may add more attributes to this class, such as an attribute to store
    # any text messages you display on the screen. Any attributes that you add,
    # along with their invariants, must be documented here.
    
    # DO NOT MAKE A NEW INITIALIZER!
    
    # METHODS

    def init(self):
        """Initialize the game state.
        
        This method is distinct from the built-in initializer __init__.
        This method is called once the game is running. You should use
        it to initialize any game specific attributes.
        
        This method should initialize any state attributes as necessary 
        to statisfy invariants. When done, set the _state to STATE_INACTIVE
        and create a message saying that the user should press to
        play a game."""
        # IMPLEMENT ME
        self._state = STATE_INACTIVE
        self._message = GLabel(text = 'Click me!', font_size = 75, x = 90, y = 275,
        linecolor = colormodel.GREEN)
        self._model = None
        if self._state != STATE_INACTIVE:
            self._message = None
        self._previoustouch = None
        self._time = 0
        self._lives = 3
        Sound('cup1.wav').play()

    def countdownstateaction(self):
        """The actions the game will run if the state is STATE_COUNTDOWN."""
        self._message = None
        if self.view.touch != None and self._previoustouch != None:
            if self._model.paddle.x > GAME_WIDTH - PADDLE_WIDTH:
                self._model.paddle.x = GAME_WIDTH - PADDLE_WIDTH
            if self._model.paddle.x < 0:
                self._model.paddle.x = 0
            self._model.paddle.x = self._model.paddle.x + (self.view.touch.x -
            self._previoustouch.x)
        if self._time >= 180:
            self._state = STATE_ACTIVE
        else:
            self._time += 1

    def pausedstateaction(self):
        """The actions the game will run if the state is STATE_PAUSED."""
        if self._lives > 1:
            self._message = GLabel(text = 'Click me to try again!', font_size = 40,
            center_x = 70, center_y = 275,linecolor = colormodel.GREEN)
            if self.view.touch != None: 
                self._lives -= 1
                self._time = 0
                self._model.ball = Ball()
                Sound('Lightsaber.wav').play()
                self._state = STATE_COUNTDOWN
        else:
            self._message = GLabel(text = 'You lose :(!', font_size = 40,
            center_x = 70, center_y = 275, linecolor = colormodel.GREEN)
            Sound('Crowd Boo.wav').play()
            self._state = STATE_COMPLETE

    def activestateaction(self):
        """The actions the game will run if the state is STATE_ACTIVE."""
        self._model.moveball()
        if self.view.touch != None and self._previoustouch != None:
            if self._model.paddle.x > GAME_WIDTH - PADDLE_WIDTH:
                self._model.paddle.x = GAME_WIDTH - PADDLE_WIDTH
            if self._model.paddle.x < 0:
                self._model.paddle.x = 0
            self._model.paddle.x = self._model.paddle.x + (self.view.touch.x -
            self._previoustouch.x)
        if self._model.ball.y <= PADDLE_OFFSET:
            self._state = STATE_PAUSED
        if self._model.bricks == []:
            self._message = GLabel(text = 'Congratulations, you win!',
            font_size = 25, center_x = 70, center_y = 275,linecolor = colormodel.GREEN)
            Sound('Applause.wav').play()
            self._state = STATE_COMPLETE

    def update(self,dt):
        """Animate a single frame in the game.
        
        It is the method that does most of the work. Of course, it should
        rely on helper methods in order to keep the method short and easy
        to read.  Some of the helper methods belong in this class, and
        others belong in class Model.
        
        The first thing this method should do is to check the state of the
        game. One thing that you can do here to organize your code is to
        have a helper method for each of your states, as the game must do
        different things in each state.
        
        In STATE_INACTIVE, the method checks to see if the player clicks
        the mouse. If so, it starts a new game and switches to STATE_COUNTDOWN.
        
        STATE_PAUSED is similar to STATE_INACTIVE. However, instead of 
        starting a whole new game, it simply switches to STATE_COUNTDOWN.
        
        In STATE_COUNTDOWN, the game counts down until the ball is served.
        The player is allowed to move the paddle, but there is no ball.
        This state should delay three seconds.
        
        In STATE_ACTIVE, the game plays normally.  The player can move the
        paddle and the ball moves on its own about the board.
        
        While in STATE_ACTIVE, if the ball goes off the screen and there
        are lives left, it switches to STATE_PAUSED.  If the ball is lost 
        with no lives left, the game is over and it switches to
        STATE_COMPLETE. It should also switch to STATE_COMPLETE once there
        are no bricks left, since that means the player has won.
        
        While in STATE_COMPLETE, this method does nothing.
        
        You are allowed to add more states if you wish. Should you do so,
        you must describe them here.
        
        Precondition: dt is the time since last update (a float). This
        parameter can be safely ignored most of the time. It is only
        relevant for debugging if your game is running really slowly."""
        # IMPLEMENT ME
        if self._state == STATE_INACTIVE:
            if self.view.touch != None:
                self._state = STATE_COUNTDOWN
                self._model = Model()
        if self._state == STATE_PAUSED:
            self.pausedstateaction()
        if self._state == STATE_COUNTDOWN:
            self.countdownstateaction()
        if self._state == STATE_ACTIVE:
            self.activestateaction()
        self._previoustouch = self.view.touch
        
    def draw(self):
        """Draws the game objects to the view.
        
        Every single thing you want to draw in this game is a GObject. 
        To draw a GObject g, simply use the method g.draw(view).  It is 
        that easy!
        
        Many of the GObjects (such as the paddle, ball, and bricks) are
        attributes in Model. In order to draw them, you either need to
        add getters for these attributes or you need to add a draw method
        to class Model.  Which one you do is up to you."""
        # IMPLEMENT ME
        if self._message != None:
            self._message.draw(self.view)
        if self._state == STATE_COUNTDOWN or self._state == STATE_ACTIVE:
            for bricks in self._model.bricks:
                bricks.draw(self.view)
            self._model.paddle.draw(self.view)
        if self._state == STATE_ACTIVE:
            self._model.paddle.draw(self.view)
            self._model.ball.draw(self.view)
        
    # ADD HELPER METHODS HERE