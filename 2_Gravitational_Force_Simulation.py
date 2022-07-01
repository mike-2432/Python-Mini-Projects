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

GREY = (220, 220, 220)

FPS = 60
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

		# For convenience using the surface as the mass
		self.mass = self.radius**2 * math.pi 
	
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
			x_attraction = x_distance * 0.001 * (self.mass * particle.mass) / distance**2
			y_attraction = y_distance * 0.001 * (self.mass * particle.mass) / distance**2

			# Creating the velocity
			self.x_vel += x_attraction / self.mass
			self.y_vel += y_attraction / self.mass

		# Updating the position
		self.x += self.x_vel
		self.y += self.y_vel

	# Border Collision
	def border_collision(self):
		if (self.x + self.radius) >= WIDTH and self.x_vel > 0 or (self.x - self.radius) <= 0 and self.x_vel < 0:
			self.x_vel *= -0.5
		if (self.y + self.radius) >= HEIGHT and self.y_vel > 0 or (self.y - self.radius) <= 0 and self.y_vel < 0:
			self.y_vel *= -0.5


# ====================================
# Merge particles after collision
# ====================================
def merge_particles(particle_list):

	# Iterating over all particle combinations
	for particle_1 in particle_list:
		for particle_2 in particle_list:

			# Preventing collision with itself
			if particle_1 == particle_2:
				continue

			# Creating a collision treshold
			collision_treshold = (particle_1.radius+particle_2.radius)*(1/4)

			# Creating the collision
			if abs(particle_1.x - particle_2.x) < collision_treshold and abs(particle_1.y - particle_2.y) < collision_treshold:
				if particle_1.radius > particle_2.radius:					
					particle_1.radius += particle_2.radius*0.5
					particle_list.remove(particle_2)
					return
				else:
					particle_2.radius += particle_1.radius*0.5
					particle_list.remove(particle_1)
					return


# ====================================
# The main loop
# ====================================
def main():

	particle_list = []
	for _ in range(15):
		particle_list.append(Particle(
			random.randint(100,900),	# X
			random.randint(100,900),	# Y
			random.uniform(-0.05,0.05),	# X_Vel
			random.uniform(-0.05,0.05),	# Y_Vel
			random.randint(1,4),		# Radius
			GREY						# Color
		))

	# Running the main loop
	run = True	
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
			particle.border_collision()
			particle.draw()
		merge_particles(particle_list)

		# Update the screen
		pygame.display.update()
		CLOCK.tick(FPS)
		

# ====================================
# Running the program
# ====================================
if __name__ == '__main__':
	main()