import pygame
import math
import random
pygame.init()


# ====================================
# Globals
# ====================================
WIDTH, HEIGHT = 1000, 1000
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Space Gravity')

GREY = (150, 150, 150)

FPS = 120
CLOCK = pygame.time.Clock()


# ====================================
# Creating the Particle class
# ====================================
class Particle:
	def __init__(self, x, y, x_vel, y_vel, radius, color):
		self.x = x
		self.y = y
		self.x_vel = x_vel
		self.y_vel = y_vel
		self.radius = radius
		self.color = color
		self.mass = self.radius**2
	

	# Drawing the Particles
	def draw(self):
		pygame.draw.circle(WIN, self.color, (self.x, self.y), self.radius)


	# Moving the Particles
	def move(self, particle_list):
		
		for particle in particle_list:
			if self == particle:
				continue

			# Getting the distance between self and the other particle
			x_distance = particle.x - self.x
			y_distance = particle.y - self.y
			distance = math.sqrt(x_distance**2 + y_distance**2)
			
			# Calculating the attraction
			# F = G(mass1 * mass2) / D^2
			x_attraction = x_distance * 0.0002 * (self.mass * particle.mass) / distance**2
			y_attraction = y_distance * 0.0002 * (self.mass * particle.mass) / distance**2

			# Creating the velocity
			self.x_vel += x_attraction / self.mass
			self.y_vel += y_attraction / self.mass

		# Updating the position
		self.x += self.x_vel
		self.y += self.y_vel


	# Border Collision
	def checkBorderCollision(self):
		if (self.x + self.radius) >= WIDTH and self.x_vel > 0 or (self.x - self.radius) <= 0 and self.x_vel < 0:
			self.x_vel *= -0.5
		if (self.y + self.radius) >= HEIGHT and self.y_vel > 0 or (self.y - self.radius) <= 0 and self.y_vel < 0:
			self.y_vel *= -0.5


# ====================================
# The main loop
# ====================================
def main():

	run = True	

	particle_list = []
	for _ in range(10):
		particle_list.append(Particle(
			random.randint(100,900),	# X
			random.randint(100,900),	# Y
			random.uniform(-0.05,0.05),	# X_Vel
			random.uniform(-0.05,0.05),	# Y_Vel
			random.randint(1,15),		# Radius
			GREY						# Color
		))

	# Running the main loop
	while run:

		# Events
		for event in pygame.event.get():
			# Exit simulation
			if event.type == pygame.QUIT:
				run = False
			
		# Draw everything
		WIN.fill((30, 30, 30))

		for particle in particle_list:
			particle.move(particle_list)
			particle.checkBorderCollision()
			particle.draw()

		# Update the screen
		pygame.display.update()
		CLOCK.tick(FPS)
		

# ====================================
# Running the program
# ====================================
if __name__ == '__main__':
	main()