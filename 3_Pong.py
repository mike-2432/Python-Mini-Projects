import pygame
import random
import time
pygame.init()


# ====================================
# Globals
# ====================================
WIDTH, HEIGHT = 1200, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong')

WHITE = (255, 255, 255)

PADDING = 20

FPS = 60
CLOCK = pygame.time.Clock()


# ====================================
# Classes
# ====================================
# Initializing the parent class for all particles
class Squares():
	def __init__(self, x, y, width, height, x_vel, y_vel, color):
		self.x = x
		self.y = y
		self.width = width	
		self.height = height	
		self.x_vel = x_vel		
		self.y_vel = y_vel
		self.color = color

	def draw(self):
		pygame.draw.rect(WIN, self.color, self.object)

# The puck class with a distinct move function
class Puck(Squares):
	def __init__(self, x, y, width, height, x_vel, y_vel, color):
		super().__init__(x, y, width, height, x_vel, y_vel, color)

	def move(self):
		# Move the puck
		self.x += self.x_vel
		self.y += self.y_vel

		# Border Collision
		if self.y >= HEIGHT - self.height and self.y_vel > 0:
			self.y = HEIGHT - self.height
			self.y_vel *= -1

		if self.y <= 0 and self.y_vel < 0:
			self.y = 0
			self.y_vel *= -1

		# Create the puck particle after every movement
		self.object = pygame.Rect(self.x, self.y , self.width, self.height)
	
# The player class with a distinct move function
class Player(Squares):
	def __init__(self, x, y, width, height, x_vel, y_vel, color):
		super().__init__(x, y, width, height, x_vel, y_vel, color)
		
	def move(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_w]:
			self.y -= self.y_vel
			self.y = max(PADDING, self.y)
		if keys[pygame.K_s]:
			self.y += self.y_vel
			self.y = min((HEIGHT - PADDING - self.height), self.y)

		# Create the player paddle after every movement
		self.object = pygame.Rect(self.x, self.y, self.width, self.height)
	

# ====================================
# Functions
# ====================================

# Collision with the paddles
def player_collision(puck, player, computer):
	
	collision_tolerance = 40

	if puck.object.colliderect(player.object):
		if abs(puck.object.top - player.object.bottom) < collision_tolerance and puck.y_vel < 0:
			puck.y_vel *= -1
		if abs(puck.object.bottom - player.object.top) < collision_tolerance and puck.y_vel > 0:
			puck.y_vel *= -1
		if abs(puck.object.left - player.object.right) < collision_tolerance and puck.x_vel < 0:
			puck.x_vel *= -1.08					# Slowly increasing the speed
			puck.x_vel = min(puck.x_vel, 25)			# Setting a max speed

			# Creating slightly different directions
			bounce_direction = random.uniform(0.9,1.25)	
			puck.y_vel *= bounce_direction

	if puck.object.colliderect(computer.object):
		if abs(puck.object.top - computer.object.bottom) < collision_tolerance and puck.y_vel < 0:
			puck.y_vel *= -1
		if abs(puck.object.bottom - computer.object.top) < collision_tolerance and puck.y_vel > 0:
			puck.y_vel *= -1
		if abs(puck.object.right - computer.object.left) < collision_tolerance and puck.x_vel > 0:
			puck.x_vel *= -1.08					# Slowly increasing the speed
			puck.x_vel = max(puck.x_vel, -25)			# Setting a max speed

			# Creating slightly different directions
			bounce_direction = random.uniform(0.9,1.25)		
			puck.y_vel *= bounce_direction
	
# Making the computer move
def computer_move(puck, computer):
	if puck.object.centery > computer.object.centery and computer.object.bottom < HEIGHT - PADDING:
		computer.y += computer.y_vel
	if puck.object.centery < computer.object.centery and computer.object.top > 0 + PADDING:
		computer.y -= computer.y_vel

# Check if the computer or player has scored
def check_scored(puck):
	return puck.x < (0-(puck.width*2)) or puck.x > (WIDTH+puck.width)

# Check if the human player has won
def player_won(puck):
	return puck.x > WIDTH

		
# ====================================
# Main Loop
# ====================================
def game():
	# Create instances of the classes
	player =  Player(PADDING,		# x_position
			(WIDTH/2)-100, 		# y_position
			15, 			# Width
			150, 			# Height
			0, 			# x_vel (no x_vel)
			15, 			# y_vel (movement speed)
			WHITE)			# color

	computer = Player(WIDTH - 20 - PADDING,	# x_position
			(WIDTH/2)-100,		# y_position
			15,			# Width
			150,			# Height							
			0,			# x_vel (no x_vel)
			8,			# y_vel (movement speed)
			WHITE)			# color

	puck = Puck(100, 100, 25, 25, 10, 6, WHITE)
	
	object_list = [player, computer, puck]

	# Running the game
	run = True
	while run:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return

		# Move the objects
		for object in object_list:
			object.move()

		# Make the computer move
		computer_move(puck, computer)

		# Check for collisions
		player_collision(puck, player, computer)

		# Check for a score
		if check_scored(puck):
			if player_won(puck):
				print('You Won!')
				time.sleep(1)
				return
			else:
				print('You Lost...')
				time.sleep(1)
				return

		# Draw everything
		WIN.fill((30,30,30))
		for object in object_list:
			object.draw()

		# Update the screen
		pygame.display.update()
		CLOCK.tick(FPS)


# ====================================
# Running the program
# ====================================
if __name__=="__main__":
	game()
