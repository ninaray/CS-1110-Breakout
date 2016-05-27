# breakout.py
# Nina Ray and Brynn Richter, nr327 and ber65
# DATE COMPLETED HERE
"""Primary module for Breakout application

This module contains the main controller class for the Breakout application. There is no
need for any any need for additional classes in this module.  If you need more classes, 
99% of the time they belong in either the play module or the models module. If you 
are ensure about where a new class should go, 
post a question on Piazza."""
from constants import *
from game2d import *
from play import *


# PRIMARY RULE: Breakout can only access attributes in play.py via getters/setters
# Breakout is NOT allowed to access anything in models.py

class Breakout(GameApp):
    """Instance is the primary controller for the Breakout App
    
    This class extends GameApp and implements the various methods necessary for processing 
    the player inputs and starting/running a game.
    
        Method start begins the application.
        
        Method update either changes the state or updates the Play object
        
        Method draw displays the Play object and any other elements on screen
    
    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class.  Any initialization should be done in
    the start method instead.  This is only for this class.  All other classes
    behave normally.
    
    Most of the work handling the game is actually provided in the class Play.
    Play should have a minimum of two methods: updatePaddle(input) which moves
    the paddle, and updateBall() which moves the ball and processes all of the
    game physics. This class should simply call that method in update().
    
    The primary purpose of this class is managing the game state: when is the 
    game started, paused, completed, etc. It keeps track of that in an attribute
    called _state.
    
    INSTANCE ATTRIBUTES:
        view    [Immutable instance of GView; it is inherited from GameApp]:
                the game view, used in drawing (see examples from class)
        input   [Immutable instance of GInput; it is inherited from GameApp]:
                the user input, used to control the paddle and change state
        _state  [one of STATE_INACTIVE, STATE_COUNTDOWN, STATE_PAUSED, STATE_ACTIVE]:
                the current state of the game represented a value from constants.py
        _game   [Play, or None if there is no game currently active]: 
                the controller for a single game, which manages the paddle, ball, and bricks
        _mssg   [GLabel, or None if there is no message to display]
                the currently active message
    
    STATE SPECIFIC INVARIANTS: 
        Attribute _game is only None if _state is STATE_INACTIVE.
        Attribute _mssg is only None if  _state is STATE_ACTIVE or STATE_COUNTDOWN.
    
    For a complete description of how the states work, see the specification for the
    method update().
    
    You may have more attributes if you wish (you might need an attribute to store
    any text messages you display on the screen). If you add new attributes, they
    need to be documented here.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    
        _npress     Will specify later
        _last_keys  Specifiy later                      ?????????sjkfjkasdhfjkashdkjdshjkshdkjhsdagkjahsgdkhsdgkhaskjghsdakjghjsdgjkhsagsdjghjsdghksdjhg
        _time
    """
    
    # DO NOT MAKE A NEW INITIALIZER!
    
    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """Initializes the application.
        
        This method is distinct from the built-in initializer __init__ (which you 
        should not override or change). This method is called once the game is running. 
        You should use it to initialize any game specific attributes.
        
        This method should make sure that all of the attributes satisfy the given 
        invariants. When done, it sets the _state to STATE_INACTIVE and create a message 
        (in attribute _mssg) saying that the user should press to play a game."""
        
        self._npress = 0
        self._last_keys = 0
        self._state = STATE_INACTIVE
        self._game = None
        if self._state == STATE_INACTIVE:
            self._mssg = GLabel(text='Press any key to play', font_size=20, font_name='Arial', x=GAME_WIDTH/2, y=GAME_HEIGHT/2, linecolor=[0, 0, 0, 1])
        elif self._state !=STATE_INACTIVE:
            self._mssg = None
        self._time = 0
    
    def update(self,dt):
        """Animates a single frame in the game.
        
        It is the method that does most of the work. It is NOT in charge of playing the
        game.  That is the purpose of the class Play.  The primary purpose of this
        game is to determine the current state, and -- if the game is active -- pass
        the input to the Play object _game to play the game.
        
        As part of the assignment, you are allowed to add your own states.  However, at
        a minimum you must support the following states: STATE_INACTIVE, STATE_NEWGAME,
        STATE_COUNTDOWN, STATE_PAUSED, and STATE_ACTIVE.  Each one of these does its own
        thing, and so should have its own helper.  We describe these below.
        
        STATE_INACTIVE: This is the state when the application first opens.  It is a 
        paused state, waiting for the player to start the game.  It displays a simple
        message on the screen.
        
        STATE_NEWGAME: This is the state creates a new game and shows it on the screen.  
        This state only lasts one animation frame before switching to STATE_COUNTDOWN.
        
        STATE_COUNTDOWN: This is a 3 second countdown that lasts until the ball is 
        served.  The player can move the paddle during the countdown, but there is no
        ball on the screen.  Paddle movement is handled by the Play object.  Hence the
        Play class should have a method called updatePaddle()
        
        STATE_ACTIVE: This is a session of normal gameplay.  The player can move the
        paddle and the ball moves on its own about the board.  Both of these
        should be handled by methods inside of class Play (NOT in this class).  Hence
        the Play class should have methods named updatePaddle() and updateBall().
        
        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However, the game is
        still visible on the screen.
        
        The rules for determining the current state are as follows.
        
        STATE_INACTIVE: This is the state at the beginning, and is the state so long
        as the player never presses a key.  In addition, the application switches to 
        this state if the previous state was STATE_ACTIVE and the game is over 
        (e.g. all balls are lost or no more bricks are on the screen).
        
        STATE_NEWGAME: The application switches to this state if the state was 
        STATE_INACTIVE in the previous frame, and the player pressed a key.
        
        STATE_COUNTDOWN: The application switches to this state if the state was
        STATE_NEWGAME in the previous frame (so that state only lasts one frame).
        
        STATE_ACTIVE: The application switches to this state after it has spent 3
        seconds in the state STATE_COUNTDOWN.
        
        STATE_PAUSED: The application switches to this state if the state was 
        STATE_ACTIVE in the previous frame, the ball was lost, and there are still
        some tries remaining.
        
        STATE_COMPLETE: The application switches to this state if the state was STATE_ACTIVE in the previous frame,
        the ball was lost and there arekajhsglkhdsglhlg
        
        You are allowed to add more states if you wish. Should you do so, you should 
        describe them here.
        
        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        assert type(dt) == int or type(dt) == float
        if self._state == STATE_INACTIVE:
            self.whenInactive()
        if self._state == STATE_NEWGAME:
            self.newGame()
        if self._state == STATE_COUNTDOWN:
            self.countDown()
        if self._state == STATE_ACTIVE:
            self.whenActive()
        if self._state == STATE_PAUSED:
            self.whenPaused()
        if self._state == STATE_COMPLETE:
            self.whenComplete()
    def draw(self):
        """Draws the game objects to the view.
        
        Every single thing you want to draw in this game is a GObject.  To draw a GObject 
        g, simply use the method g.draw(self.view).  It is that easy!
        
        Many of the GObjects (such as the paddle, ball, and bricks) are attributes in Play. 
        In order to draw them, you either need to add getters for these attributes or you 
        need to add a draw method to class Play.  We suggest the latter.  See the example 
        subcontroller.py from class."""
        if (self._state == STATE_INACTIVE or self._state == STATE_COUNTDOWN or self._state == STATE_PAUSED or self._state == STATE_COMPLETE):
            self._mssg.draw(self.view)
        else:
            self._mssg = None
        if self._state >= STATE_NEWGAME:
            self._game.draw(self.view,self._state)
            
    def whenInactive(self):
        """This method includes what happens while in STATE_INACTIVE
        
        This method checks for the first key click and then begins a new game by changing state to NEW_GAME.
        """
        curr_keys = self.input.key_count
        change = curr_keys > 0 and self._last_keys == 0
        if self._npress == 0 and change: #If no keys have been pressed and change is True
            self._state = STATE_NEWGAME
            self._npress = self._npress + 1
    
            
    def newGame(self):
        """This method includes what happens while in STATE_NEWGAME
        
        This method changes the state to STATE_COUNTDOWN and initialized the game.
        """
        self._state = STATE_COUNTDOWN
        self._game = Play()
    
            
    def countDown(self):
        """This method includes what happens while in STATE_COUNTDOWN
        
        This method displays the countdown messages, serves the ball, and allows
        the paddle to begin moving."""
        if self._state == STATE_COUNTDOWN:
                if self._time == 0:
                    self._mssg.text = '3'
                if self._time/60 == 1:
                    self._mssg.text = '2'
                elif self._time/120 == 1:
                    self._mssg.text = '1'
                elif self._time >= 180:
                    self._state = STATE_ACTIVE
                    self._game.serveBall()
                self._time = self._time + 1
            
    def whenActive(self):
        """The method includes what happens while in STATE_ACTIVE
        
        This method updates the ball and paddle's positions and actions each frame.
        """
        
        self._game.updateBall()
        self._game.updatePaddle(self.input)
        if self._game.loseLife():
            self._state = STATE_PAUSED
        if self._game.loseGame():
            self._state = STATE_COMPLETE
        if self._game.winGame():
            self._state = STATE_COMPLETE
    
    def whenPaused(self):
        """This method includes what happens while in STATE_PAUSED.
        
        This method creates a message to be displayed in between turns.
        It also checks for a key press, and as soon as the key is pressed,
        it returns the game to STATE_COUNTDOWN to begin a new turn.
        """
        self._mssg = GLabel(text = "Press any key for a new ball", font_size = 20, font_name = "Arial", x = GAME_WIDTH/2, y = GAME_HEIGHT/2)
        self.last_keys = 0 #CITE!!!!!!!!!!!!
        self._npress = 0
        curr_keys = self.input.key_count
        change = curr_keys > 0 and self.last_keys == 0
        if self._npress == 0 and change:
            self._state = STATE_COUNTDOWN
            self._time = 0
            self._npress = self._npress + 1
    
    # HELPER METHODS FOR THE STATES GO HERE
    def whenComplete(self):
        """Creates a win/lose message depending on whether the player wins or loses the game.
        
        This method includes what should be done while in STATE_COMPLETE."""
        if self._game.loseGame():
            self._mssg = GLabel(text = "Sorry, you lost", font_size = 20, font_name = "Arial", x = GAME_WIDTH/2, y = GAME_HEIGHT/2)
        if self._game.winGame():
            self._mssg - GLabel(text = "Congratulations!!! You Won!!!!!!!!!!!!!", font_size = 20, font_name = "Arial", x = GAME_WIDTH/2, y = GAME_HEIGHT/2)
    
    
    
    
    
    
    