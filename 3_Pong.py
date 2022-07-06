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
PADDLE_SIZE = 150
FONT = pygame.font.SysFont('open-sans',40)

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
			puck.x_vel *= -1.08							# Slowly increasing the speed
			puck.x_vel = min(puck.x_vel, 25)			# Setting a max speed

			# Creating slightly different directions
			bounce_direction = random.uniform(0.85,1.3)	
			puck.y_vel *= bounce_direction

	if puck.object.colliderect(computer.object):
		if abs(puck.object.top - computer.object.bottom) < collision_tolerance and puck.y_vel < 0:
			puck.y_vel *= -1
		if abs(puck.object.bottom - computer.object.top) < collision_tolerance and puck.y_vel > 0:
			puck.y_vel *= -1
		if abs(puck.object.right - computer.object.left) < collision_tolerance and puck.x_vel > 0:
			puck.x_vel *= -1.08							# Slowly increasing the speed
			puck.x_vel = max(puck.x_vel, -25)			# Setting a max speed

			# Creating slightly different directions
			bounce_direction = random.uniform(0.85,1.3)		
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

# Create objects
def create_objects(level):
	player =  Player(PADDING, 					# x_position
					(HEIGHT/2)-(PADDLE_SIZE/2),	# y_position
					15, 						# Width
					PADDLE_SIZE,				# Height
					0, 							# x_vel (no x_vel)
					15, 						# y_vel (movement speed)
					WHITE)						# color

	computer = Player(WIDTH - 20 - PADDING,		# x_position
					(HEIGHT/2)-(PADDLE_SIZE/2),	# y_position
					15,							# Width
					PADDLE_SIZE,				# Height							
					0,							# x_vel (no x_vel)
					5+(level*2),					# y_vel (movement speed)
					WHITE)						# color

	puck = Puck(100, 400, 25, 25, 10+level, 7, WHITE)
	object_list = [player, computer, puck]
	return object_list

# Current level screen
def show_level(level):
	WIN.fill((30,30,30))
	label = FONT.render('Level ' + str(level), 5, (255,255,255))
	WIN.blit(label, (WIDTH/2 - label.get_width()/2, HEIGHT/2 - label.get_height()/2))
	pygame.display.flip()
	time.sleep(1)


# ====================================
# Main Loop
# ====================================
def game():
	level = 1

	# Creating instances of the classes
	object_list = create_objects(level)
	player, computer, puck = object_list

	# Showing the initial level
	show_level(level)
	
	# Running the game
	run = True
	while run:

		# Exit button handler
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return

		# Moving the objects
		for object in object_list:
			object.move()

		# Making the computer move
		computer_move(puck, computer)

		# Checking for collisions
		player_collision(puck, player, computer)

		# Checking for a goal
		if check_scored(puck):
			# Checking if the human player won
			if player_won(puck):
				level += 1
				show_level(level)

				# Resetting the objects
				object_list.clear()
				del object_list
				object_list = create_objects(level)
				player, computer, puck = object_list
				continue

			else:
				label = FONT.render('You lost...', 5, (255,255,255))
				WIN.blit(label, (WIDTH/2 - label.get_width()/2, HEIGHT/2 - label.get_height()/2))
				pygame.display.flip()
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
# Main Menu
# ====================================
def main_menu():

	# The menu loop
	run = True
	while run:
		WIN.fill((30,30,30))
		title = FONT.render('Press ENTER to begin', 5, (255,255,255))

		# Place font in the center
		WIN.blit(title, (WIDTH/2 - title.get_width()/2, HEIGHT/2 - title.get_height()/2))

		# Events
		pygame.display.update()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					game()
	pygame.quit()


# ====================================
# Running the program
# ====================================
if __name__=="__main__":
	main_menu()