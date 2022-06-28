import pygame
import random
pygame.init()


# ====================================
# Globals
# ====================================
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity And Collision")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 150, 240)
RED = (190, 40, 50)
GREY = (120, 120, 120)
PURPLE = (150,60,255)
GREEN = (50, 230, 40)

COLORS = [WHITE,YELLOW,BLUE,RED,GREY,PURPLE,GREEN]

FPS = 60
CLOCK = pygame.time.Clock()



# ====================================
# Creating the ball class
# ====================================
class Ball():
	def __init__(self, x, y, x_vel, color, radius):
		self.x = x
		self.y = y
		self.color = color
		self.radius = radius

		self.acc = radius * 0.02
		self.x_vel = x_vel
		self.y_vel = 0

	# Function to draw the ball
	def draw(self):
		pygame.draw.circle(WIN, self.color, (self.x, self.y), self.radius)

	# Function for gravity
	def gravity(self):
		self.y_vel += self.acc
		self.y += self.y_vel
		self.x += self.x_vel

	# Function for collision
	def collision(self):
		if self.y >= HEIGHT - self.radius and self.y_vel > 0:
			self.y = HEIGHT - self.radius
			self.y_vel *= -1

		if self.y <= 0 + self.radius and self.y_vel < 0:
			self.y = 0 + self.radius
			self.y_vel *= -1

		if self.x >= WIDTH - self.radius and self.x_vel > 0 or self.x <= 0 + self.radius and self.x_vel < 0:
			self.x_vel *= -1



# ====================================
# Function for collision between balls
# ====================================
def ballCollision(balls):

	# Select every ball combination
	for i in range(len(balls)):
		for j in range(i+1, len(balls)):

			# Look for collision
			if abs(balls[i].x-balls[j].x) < (balls[i].radius+balls[j].radius) and abs(balls[i].y-balls[j].y) < (balls[i].radius+balls[j].radius):

				temp_x_vel = balls[i].x_vel
				temp_y_vel = balls[i].y_vel

				balls[i].x_vel = balls[j].x_vel
				balls[i].y_vel = balls[j].y_vel

				balls[j].x_vel = temp_x_vel
				balls[j].y_vel = temp_y_vel

				# Changing colors when touching for fun
				# Making one color win
				if balls[i].x_vel + balls[i].y_vel > balls[j].x_vel+balls[j].y_vel:
					balls[j].color = balls[i].color
				else:
					balls[i].color = balls[j].color


# ====================================
# The main loop
# ====================================
def main():

	# Creating random balls
	balls = []
	for _ in range(80):
		balls.append(Ball(
			random.randint(100,800),	# X
			random.randint(100,400),	# Y
			random.randint(-5,5),		# X_Vel
			random.choice(COLORS),		# Color
			random.randint(5,10)		# Radius
		))

	# Running the simulation
	run = True
	while run:

		# Check if 'EXIT' is clicked
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return
		
		# Move everything
		for i in balls:
			i.gravity()
			i.collision()

		# Check for collisions between balls
		ballCollision(balls)

		# Draw everything
		WIN.fill((30,30,30))
		for i in balls:
			i.draw()
	
		# Update the screen
		pygame.display.update()
		CLOCK.tick(FPS)

main()
pygame.quit()