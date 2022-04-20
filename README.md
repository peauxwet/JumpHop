# JumpHop
Simple re-creation of a popular game. I'll let you guess.


CLASS Player:
	Player class is a child of the pygame.Rect class. It inherits all of the Rect class's properties, but adds the additional attributes isJumping, isFalling, and changeY. These are used for the player's jump mechanics.

FUNCTION newPlatform:
	The new platform function is responsible for anything to do with spawning a new platform...hence the name. It will check if the platList (the list used for saving all platforms created) has a length of zero. If it does, it will spawn a new platform close to the player. After a platform is created, every new platform is spawned 150 to 40 pixels away from the previous platform. 

FUNCTION checkCollision:
	The check collision function is responsible for stopping the player on a platform and ending the game.
		- It checks if the player has fallen onto a platform by using the pygame.Rect.clipline() function. This is done by performing the following operations in order (assuming all are True): 
	 		1. check if the player is falling
	 		2. check if the top line of any platform collides with the player
	 		3. two possible scenarios:
	 			- if the player collides with a line: stop the player from falling and align the bottom of the player with the top of the platform
	 			- if the player does not collide with a platform: set the player's "isFalling" attribute equal to true
	 	- It ends the game by performing the following operations in order (assuming all are True):
	 		1. check if the player is falling
	 		2. check if the top of the player is higher than game window (Y value in pygame windows is backwards)
	 		3. close the window/end the game.
	 
FUNCTION checkJump:
	The check jump function is responsible for making the character move upwards in a parabolic-like motion. It also tells the game when the character has stopped jumping. 
		- The player jump animation is done by performing the following operations in order (assuming all are True):
			1. check if player's "isJumping" attribute is set to True
			2. check if player's "changeY" attribute is higher than 0
			3. subtract player's Y coordinate by the amount of "changeY"
			4. subtract value of player's attribute "changeY" by 1
		- To tell the game that the player has stopped jumping steps above must be done until the player's "changeY" value is less than or equal to 0. Once that has happened, the following steps will be executed to tell the game that the player has stopped jumping.
			1. check if the player's "isJumping" attribute is set to True
			2. check if the player's "changeY" value is equal 0
			3. set the player's "isJumping" value equal to False
			4. set the player's "isFalling" value equal to True

FUNCTION checkFalling:
	The check falling function is responsible for the falling animation. It is only called after a jump has been finished or if a player leaves a platform without jumping. It does this by performing the following steps in order:
		- check if the player's "isFalling" attribute is True
		- add the player's "changeY" value to the player's Y coordinate
		- increase the value of "changeY" by .5

FUNCTION checkScroll:
	The check scroll function is responsible for removing old platforms that have gone off the screen. It does this by performing the following steps in order:
		- check if the player is not falling and if the player goes above a certain point on the screen
		- iterate throught every platform
		- for every platform that has a height below the height of the screen, remove it from the list of platforms to be printed
