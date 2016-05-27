# models.py
# YOUR NAME(S) AND NETID(S) HERE
# DATE COMPLETED HERE
"""Models module for Breakout

This module contains the model classes for the Breakout game. That is anything that you
interact with on the screen is model: the paddle, the ball, and any of the bricks.

Technically, just because something is a model does not mean there has to be a special 
class for it.  Unless you need something special, both paddle and individual bricks could
just be instances of GRectangle.  However, we do need something special: collision 
detection.  That is why we have custom classes.

You are free to add new models to this module.  You may wish to do this when you add
new features to your game.  If you are unsure about whether to make a new class or 
not, please ask on Piazza."""
import random # To randomly generate the ball velocity
from constants import *
from game2d import *


# PRIMARY RULE: Models are not allowed to access anything except the module constants.py.
# If you need extra information from Play, then it should be a parameter in your method, 
# and Play should pass it as a argument when it calls the method.


class Paddle(GRectangle):
    """An instance is the game paddle.
    
    This class contains a method to detect collision with the ball, as well as move it
    left and right.  You may wish to add more features to this class.
    
    The attributes of this class are those inherited from GRectangle.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        
        _paddle [GRectangle]: ?????????????????????????????????????????????????????????????????????????????????????????????????????????????????
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    # INITIALIZER TO CREATE A NEW PADDLE
    def __init__(self, x, y, w, h, fc, lc):
        self._paddle = GRectangle.__init__(self, x=x, y=y, width = w, height = h, fillcolor = fc, linecolor = lc)
    
    # METHODS TO MOVE THE PADDLE AND CHECK FOR COLLISIONS
    def collidePaddle (self,ball):
        """Returns: True if the ball collides with this brick, False otherwise. REMEMBER TO CITE ???????????????????????????????
        
        Parameter ball: The ball to check
        Precondition: ball is of class Ball"""
        if self.contains(ball.x + ball.width/2, ball.y + ball.height/2): #(+x, +y)
            return True
        if self.contains(ball.x - ball.width/2, ball.y + ball.height/2) and ball._vy <=0: #(-x, +y)
            return True
        if self.contains(ball.x - ball.width/2, ball.y - ball.height/2) and ball._vy <=0: #(-x, -y)
            return True
        if self.contains(ball.x + ball.width/2, ball.y - ball.height/2) and ball._vy <=0: #(+x, -y)
            return True
        else:
            return False
    
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Brick(GRectangle):
    """An instance is the game paddle.
     
    This class contains a method to detect collision with the ball.  You may wish to 
    add more features to this class.
    
    The attributes of this class are those inherited from GRectangle.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    
        _brick [GRectangle]: The brick to create
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getBrick(self):
        return self._brick
    
    # INITIALIZER TO CREATE A BRICK
    def __init__(self, l, y, w, h, fc, lc):
        GRectangle.__init__(self, left=l, y=y, width = w, height = h, fillcolor = fc, linecolor = lc)
        
    # METHOD TO CHECK FOR COLLISION
    def collideBrick(self, ball):
        """Returns: True if the ball collides with this brick, False otherwise. REMEMBER TO CITE ????????????????????????
        
        Parameter ball: The ball to check
        Precondition: ball is of class Ball"""
        if self.contains(ball.x + ball.width/2, ball.y + ball.height/2): #(+x, +y) 
            return True
        if self.contains(ball.x - ball.width/2, ball.y + ball.height/2): #(-x, +y) 
            return True
        if self.contains(ball.x - ball.width/2, ball.y - ball.height/2): #(-x, -y) 
            return True
        if self.contains(ball.x + ball.width/2, ball.y - ball.height/2): #(+x, -y)
            return True
        else:
            return False


    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Ball(GEllipse):
    """Instance is a game ball.
    
    We extend GEllipse because a ball must have additional attributes for velocity.
    This class adds this attributes and manages them.
    
    INSTANCE ATTRIBUTES:
        _vx [int or float]: Velocity in x direction 
        _vy [int or float]: Velocity in y direction 
    
    The class Play will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with no
    setters for the velocities.
    
    How? The only time the ball can change velocities is if it hits an obstacle
    (paddle or brick) or if it hits a wall.  Why not just write methods for these
    instead of using setters?  This cuts down on the amount of code in Gameplay.
    
    NOTE: The ball does not have to be a GEllipse. It could be an instance
    of GImage (why?). This change is allowed, but you must modify the class
    header up above.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    # INITIALIZER TO SET RANDOM VELOCITY
    def __init__(self, x, y, d, f):
        GEllipse.__init__(self, x=x, y=y, width=d, height=d, fillcolor=f)
        self._vx = random.uniform(1.0, 5.0)
        self._vx = self._vx * random.choice([-1, 1])
        self._vy = -5.0
    
    
    # METHODS TO MOVE AND/OR BOUNCE THE BALL
    def moveBall(self):
        self.x = self.x + self._vx
        self.y = self.y + self._vy
        
    def bounceBall(self):
        if (self.y + self.height/2) >= GAME_HEIGHT or (self.y - self.height/2) <= 0:
            self._vy = -self._vy
        if (self.x + self.width/2) >= GAME_WIDTH or (self.x - self.width/2) <= 0:
            self._vx = -self._vx
    
    def bounceOffWalls(self):
        if (self.y + self.height/2) >= GAME_HEIGHT:
            self._vy = -self._vy
        if (self.x + self.width/2) >= GAME_WIDTH or(self.x - self.width/2) <= 0:
            self._vx = -self._vx
    
        
    def reboundfromPaddle(self):
        #account for what side of the paddle
        if self._vy <= 0:
            self._vy = -self._vy
        self._vx = -self._vx    
    
    
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def outOfBounds(self):
        if (self.y - self.height/2) <= 0:
            return True
        else:
            return False
    
    


# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE