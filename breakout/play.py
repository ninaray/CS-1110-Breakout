# play.py
# YOUR NAME(S) AND NETID(S) HERE
# DATE COMPLETED HERE
"""Subcontroller module for Breakout

This module contains the subcontroller to manage a single game in the Breakout App. 
Instances of Play represent a single game.  If you want to restart a new game, you are 
expected to make a new instance of Play.

The subcontroller Play manages the paddle, ball, and bricks.  These are model objects.  
Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer."""
from constants import *
from game2d import *
from models import *


# PRIMARY RULE: Play can only access attributes in models.py via getters/setters
# Play is NOT allowed to access anything in breakout.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)

class Play(object):
    """An instance controls a single game of breakout.
    
    This subcontroller has a reference to the ball, paddle, and bricks. It animates the 
    ball, removing any bricks as necessary.  When the game is won, it stops animating.  
    You should create a NEW instance of Play (in Breakout) if you want to make a new game.
    
    If you want to pause the game, tell this controller to draw, but do not update.  See 
    subcontrollers.py from Lecture 25 for an example.
    
    INSTANCE ATTRIBUTES:
        _paddle [Paddle]: the paddle to play with 
        _bricks [list of Brick]: the list of bricks still remaining 
        _ball   [Ball, or None if waiting for a serve]:  the ball to animate
        _tries  [int >= 0]: the number of tries left 
    
    As you can see, all of these attributes are hidden.  You may find that you want to
    access an attribute in class Breakout. It is okay if you do, but you MAY NOT ACCESS 
    THE ATTRIBUTES DIRECTLY. You must use a getter and/or setter for any attribute that 
    you need to access in Breakout.  Only add the getters and setters that you need for 
    Breakout.
    
    You may change any of the attributes above as you see fit. For example, you may want
    to add new objects on the screen (e.g power-ups).  If you make changes, please list
    the changes with the invariants.
                  
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    # INITIALIZER (standard form) TO CREATE PADDLES AND BRICKS
    def __init__(self):
        self._bricks = []
        left = BRICK_SEP_H/2
        y = GAME_HEIGHT - BRICK_Y_OFFSET - BRICK_HEIGHT/2
        k = 0
        for r in range(BRICK_ROWS): #For each row
            for c in range(BRICKS_IN_ROW): #For each column in each row
                    self._bricks.append(Brick(left, y, BRICK_WIDTH, BRICK_HEIGHT, BRICK_COLORS[k], BRICK_COLORS[k])) #Creating a brick
                    left = left + (BRICK_SEP_H + BRICK_WIDTH) #Shifts to the right
                    #When this is done, there should be ONE row of 10 bricks
            y = y - (BRICK_SEP_V + BRICK_HEIGHT)
            left = BRICK_SEP_H/2            
            if r%2 != 0:
                k = k+1
        self._paddle = Paddle(GAME_WIDTH/2, PADDLE_HEIGHT/2 + PADDLE_OFFSET, PADDLE_WIDTH, PADDLE_HEIGHT, colormodel.BLACK, colormodel.BLACK)
            
            
    # UPDATE METHODS TO MOVE PADDLE, SERVE AND MOVE THE BALL
    def updatePaddle(self, inp):
        da = 0
        if inp.is_key_down('left'):
            da -= PADDLE_CHANGE
        if inp.is_key_down('right'):
            da += PADDLE_CHANGE
        
        if self._paddle.x >= (GAME_WIDTH - PADDLE_WIDTH/2):
            self._paddle.x = GAME_WIDTH - PADDLE_WIDTH/2
        if self._paddle.x <= PADDLE_WIDTH/2:
            self._paddle.x = PADDLE_WIDTH/2
        self._paddle.x = self._paddle.x + da
        
    def serveBall(self):
        self._ball = Ball(GAME_WIDTH/2, GAME_HEIGHT/2, BALL_DIAMETER, colormodel.MAGENTA)
    
    def updateBall(self):
        self._ball.moveBall()
        self._ball.bounceBall()
        if self._paddle.collidePaddle(self._ball) == True:
            self._ball.reboundfromPaddle()
        for b in self._bricks:       #?????????????????????????????????? ILLEGAL????????????????????????????????
            if b.collideBrick(self._ball) == True:
                #if self._bricks.index(b) == self._bricks[0] or self._bricks.index(b) == self._bricks[-1]:
                #self._ball.reboundfromBrick(lr)
                self._bricks.remove(b)
                self._ball.bounceBall()
    
    
    # DRAW METHOD TO DRAW THE PADDLES, BALL, AND BRICKS
    def draw(self, view, state):
        for b in self._bricks:
            b.draw(view)
        self._paddle.draw(view)
        if state == STATE_ACTIVE:
            self._ball.draw(view)
    
    # HELPER METHODS FOR PHYSICS AND COLLISION DETECTION
    
    
    # ADD ANY ADDITIONAL METHODS (FULLY SPECIFIED) HERE
    def loseLife(self):
        if self._tries > 0 and self._tries < 3 and self._tries == self._turns:
            self._turns = self._turns - 1
            return True
        else:
            return False
    
  
    def loseGame(self):
        if self._tries == 0:
            return True
        else:
            return False
    
    
    def winGame(self):
        if self._bricks == []:
            return True
        else:
            return False
