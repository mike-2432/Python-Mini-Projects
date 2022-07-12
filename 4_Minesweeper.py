import pygame
import random
import math
import time
pygame.init()


# ====================================
# Globals
# ====================================
WIDTH, HEIGHT = 1000, 1000
BOARD_SIZE = 10
TILE_SIZE = int(WIDTH / BOARD_SIZE)
NUM_MINES = 6

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Minesweeper')
FONT = pygame.font.SysFont('open-sans',40)
FPS = 60
CLOCK = pygame.time.Clock()

BLACK = (30, 30, 30)
LIGHT_BlACK = (40,40,40)
WHITE = (150, 150, 150)
GREEN = (60, 250, 20)
YELLOW = (230, 250, 20)
TANGERINE = (250, 210, 20)
ORANGE = (250, 150, 80)
RED = (255, 0, 0)
COLOR_LIST = [GREEN, YELLOW, TANGERINE, ORANGE, RED]


# ====================================
# Board class
# ====================================
class Board():
	def __init__(self, board_size, num_mines):
		self.board_size = board_size
		self.num_mines = num_mines

		# Create a matrix containing lists with two values
		# The first values represents the amount of neighboring mines, a 9 indicates a mine
		# The second value shows if a tile is hidden or visible after being clicked on
		self.matrix = [[[0, 'hidden'] for col in range(self.board_size)] for row in range(self.board_size)]

		# Plant the mines
		self.plant_mines()
		# Calculate the neigbouring mines
		self.calculate_neighboring_mines()


	def plant_mines(self):		
		planted_mines = 0
		while planted_mines < self.num_mines:
			row = random.randint(0, self.board_size-1)
			col = random.randint(0, self.board_size-1)

			if self.matrix[row][col][0] == 9:
				continue

			self.matrix[row][col][0] = 9
			planted_mines += 1

	def calculate_neighboring_mines(self):
		# Assign values to the neighboring tiles
		# First: find the mines (9)
		for row in range(self.board_size):
			for col in range(self.board_size):
				if self.matrix[row][col][0] == 9:

					# Second: add 1 to the neighboring tiles
					for y in range(  max(0, row-1), min(self.board_size, row+2)  ):
						for x in range(  max(0, col-1), min(self.board_size, col+2)  ):
							if self.matrix[y][x][0] != 9:
								self.matrix[y][x][0] += 1

	def draw_interface(self):
		# Display the matrix
		for row in range(0, HEIGHT, TILE_SIZE):
			for col in range(0, WIDTH, TILE_SIZE):
				draw_grid = pygame.Rect(col, row, TILE_SIZE, TILE_SIZE)
				pygame.draw.rect(WIN, LIGHT_BlACK, draw_grid, 1)


		# Display the clicked tiles
		for row in range(self.board_size):
		 	for col in range(self.board_size):
		 		if self.matrix[row][col][1] == 'shown':
		 			create_square = pygame.Rect(col*TILE_SIZE, row*TILE_SIZE, TILE_SIZE, TILE_SIZE)

		 			# Set the color of the tiles
		 			number = self.matrix[row][col][0]
		 			if number == 9:
		 				color = RED
		 			elif 3 <= number <= 8:
		 				color = ORANGE
		 			else: 
		 				color = COLOR_LIST[number]

		 			pygame.draw.rect(WIN, color, create_square, 0)

	def check_win(self):
		score = 0
		for row in self.matrix:
			for tile in row:
				if tile[1] == 'shown':
					score += 1
		return score == self.board_size**2 - self.num_mines


# ====================================
# Functions
# ====================================
def check_borders(board, row, col):
	for y in range( max(0, row-1), min(BOARD_SIZE, row+2) ):
		for x in range( max(0, col-1), min(BOARD_SIZE, col+2) ):
			if board[y][x][1] == 'hidden' and board[y][x][0] == 0:
				board[y][x][1] = 'shown'
				check_borders(board, y, x)

def show_result(result):
	WIN.fill((30,30,30))
	label = FONT.render(result, 1, (255,255,255))
	WIN.blit(label, (WIDTH/2 - label.get_width()/2, HEIGHT/2 - label.get_height()/2))
	pygame.display.flip()
	time.sleep(2)


# ====================================
# Main Loop
# ====================================
def game():

	board = Board(BOARD_SIZE, NUM_MINES)
	loss = False
	win = False

	# Start the main loop
	run = True
	while run:

		# Event handlers
		for event in pygame.event.get():
			# Exit game
			if event.type == pygame.QUIT:
				return
			# Mouse clicks
			if event.type == pygame.MOUSEBUTTONUP:
				(x, y) = pygame.mouse.get_pos()
				
				# Get the corresponding position on the board
				col = math.floor(x / TILE_SIZE)
				row = math.floor(y / TILE_SIZE)
								
				# Show the clicked tiles
				board.matrix[row][col][1] = 'shown'

				# Check for a win or loss
				if board.matrix[row][col][0] == 9:
					loss = True					
				elif board.check_win():
					win = True

				# Display all the neighboring tiles with values of 0 
				check_borders(board.matrix, row, col)
					
		# Display the UI
		WIN.fill((30,30,30))
		board.draw_interface()

		# Update the screen
		pygame.display.update()
		CLOCK.tick(FPS)

		# Display win/loss
		if win == True:
			time.sleep(1)
			show_result('You Won!')
			return
		if loss == True:
			time.sleep(1)
			show_result('You lost...')
			return


# ====================================
# Main Menu
# ====================================
def main_menu():

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
if __name__ == '__main__':
	main_menu() 