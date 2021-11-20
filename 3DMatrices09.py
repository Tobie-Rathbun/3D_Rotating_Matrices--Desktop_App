#created by Tobie Rathbun

import pygame
import numpy as np
from math import *

white = (255,255,255)
red = (255,0,0)
black = (0,0,0)

width, height = 800, 600
pygame.display.set_caption("3D projection in pygame!")
screen = pygame.display.set_mode((width, height))


scale = 100
circle_pos = [width/2, height/2]

angle = 0


points = []
#all cube vertices
points.append(np.matrix([-1,-1, 1]))
points.append(np.matrix([ 1,-1, 1]))
points.append(np.matrix([ 1, 1, 1]))
points.append(np.matrix([-1, 1, 1]))
points.append(np.matrix([-1,-1,-1]))
points.append(np.matrix([ 1,-1,-1]))
points.append(np.matrix([ 1, 1,-1]))
points.append(np.matrix([-1, 1,-1]))

projection_matrix = np.matrix([
	[1, 0, 0],
	[0, 1, 0]
	])

projected_points = [
	[n, n] for n in range(len(points))
		#initializes array
]

def connect_points(i, j, points):
	pygame.draw.line(screen, red, (points[i][0], points[i][1]), (points[j][0], points[j][1]))

clock = pygame.time.Clock()

#mainloop
while True:
	clock.tick(60)
	for event in pygame.event.get():
		#exit on quit
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		#exit on escape
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				exit()
			
	#update stuff
	
	#rotation matrix
	rotation_x = np.matrix([
		[1, 0, 0],
		[0, cos(angle), -sin(angle)],
		[0, sin(angle), cos(angle)],
	])
	rotation_y = np.matrix([
		[cos(angle), 0, sin(angle)],
		[0, 1, 0],
		[-sin(angle), 0, cos(angle)],
	])
	rotation_z = np.matrix([
		[cos(angle), -sin(angle), 0],
		[sin(angle), cos(angle), 0],
		[0, 0, 1],
	])
	
	angle += .01
	
	screen.fill(white)

	#drawing stuff
	
	
	i = 0
	for point in points:
		rotated2d = np.dot(rotation_z, point.reshape((3,1)))
		rotated2d = np.dot(rotation_y, rotated2d)
		
		projected2d = np.dot(projection_matrix, rotated2d)
		
		
		x = int(projected2d[0][0] * scale) + circle_pos[0]
		y = int(projected2d[1][0] * scale) + circle_pos[1]
		
		projected_points[i] = [x, y]
		pygame.draw.circle(screen, black, (x, y), 5)
		i += 1
	
	#side a
#	connect_points(0, 1, projected_points)
#	connect_points(1, 2, projected_points)
#	connect_points(2, 3, projected_points)
#	connect_points(3, 0, projected_points)
	
	#side c
#	connect_points(4, 5, projected_points)
#	connect_points(5, 6, projected_points)
#	connect_points(6, 7, projected_points)
#	connect_points(7, 4, projected_points)
	
#	connect_points(0, 4, projected_points)
#	connect_points(1, 5, projected_points)
#	connect_points(2, 6, projected_points)
#	connect_points(3, 7, projected_points)
	
	for p in range(4):
		connect_points(p, (p+1) % 4, projected_points)
			#if p passes 4, it goes back to 0
		connect_points(p+4, ((p+1) % 4) + 4, projected_points)
		connect_points(p, (p+4), projected_points)


	pygame.display.update()
