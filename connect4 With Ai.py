import numpy as np
import pygame
import sys
import math
import random

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

empty = 0

player = 0
AI = 1 

player_piece= 1
AI_piece = 2

window_length = 4

def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board

def drop_piece(board, row, col, piece):
	board[row][col] = piece

def is_valid_location(board, col):
	return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

def print_board(board):
	print(np.flip(board, 0))

def winning_move(board, piece):
	# Check horizontal locations for win
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# Check vertical locations for win
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Check positively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Check negatively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True

def evaluate_window(window, piece):
	score=0
	opp_piece = player_piece
	if piece == player_piece:
		opp_piece=AI_piece


	if window.count(piece) == 4:
		score +=100
	elif window.count(piece) == 3 and window.count(empty)==1:
		score+=10
	elif window.count(piece) == 2 and window.count(empty)==2:
		score+=5


	if window.count(opp_piece) == 3 and window.count(empty)==1:
		score -=80
	elif window.count(opp_piece) == 2 and window.count(empty)==2:
		score-=9


	return score

def score_position(board, piece):
	score = 0
	#score center columm preference for AI
	center_array = [int(i) for i in list(board[:,COLUMN_COUNT//2])]
	center_count = center_array.count(piece)
	score += center_count *1


	# score horizontal
	for r in range(ROW_COUNT):
		row_array = [int(i) for i in list (board[r,:])]
		for c in range(COLUMN_COUNT-3):
			window = row_array[c:c+window_length]
			score+=evaluate_window(window,piece)

	# return score this makes it alittle stupid 

	## score vertival
	for c in range(COLUMN_COUNT):
		col_array = [int(i) for i in list (board[:,c])]
		for r in range(ROW_COUNT-3):
			window = col_array[r:r+window_length]
			score+=evaluate_window(window,piece)
	# return score

	#positive slop score diaganols
	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window =[board[r+i][c+i] for i in range(window_length)]
			score+=evaluate_window(window,piece)

	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window =[board[r+3-i][c+i] for i in range(window_length)]
			score+=evaluate_window(window,piece)

	return score


def get_valid_location(board):
	valid_location = []
	for col in range (COLUMN_COUNT):
		if is_valid_location(board, col):
			valid_location.append(col)
	return valid_location

def pick_best_move (board,piece):
	valid_location = get_valid_location(board)
	best_score=-100000
	best_col = random.choice(valid_location)

	for col in valid_location:
		row = get_next_open_row(board, col)
		temp_board = board.copy()
		drop_piece(temp_board, row, col, piece)
		score = score_position(temp_board,piece)
		if score > best_score:
			best_score = score
			best_col = col
	return best_col

def draw_board(board):
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):		
			if board[r][c] == player_piece:
				pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == AI_piece: 
				pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()


board = create_board()
print_board(board)
game_over = False

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

turn = random.randint(player, AI)

myfont = pygame.font.SysFont("monospace", 75)

while not game_over:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			posx = event.pos[0]
			if turn == player:
				pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)


		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			#print(event.pos)
			# Ask for Player 1 Input
			if turn == 0:
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE))

				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, player_piece)

					if winning_move(board, player_piece):
						label = myfont.render("Player 1 wins!!", 1, RED)
						screen.blit(label, (40,10))
						game_over = True
					turn += 1
					turn = turn % 2
					print_board(board)
					draw_board(board)


	# # Ask for Player 2 Input
	if turn == AI and not game_over:	

		col = pick_best_move(board,AI_piece)
		# col = random.randint(0,COLUMN_COUNT-1)

		if is_valid_location(board, col):
			pygame.time.wait(500)
			row = get_next_open_row(board, col)
			drop_piece(board, row, col, AI_piece)

			if winning_move(board, AI_piece):
				label = myfont.render("CPU Wins!!", 1, YELLOW)
				screen.blit(label, (40,10))
				game_over = True

			print_board(board)
			draw_board(board)

		turn += 1
		turn = turn % 2

	if game_over:
		pygame.time.wait(3000)