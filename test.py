#!/usr/bin/env python
# encoding: utf-8

import sys
import pygame
import threading

pygame.init()

width = 320
height  = 480
size = width, height

speed = [3, 3] # The distance to move in each direction per loop
black = 0, 0, 0

screen = pygame.display.set_mode(size)

goat = pygame.image.load("goat.bmp")
goatrect = goat.get_rect()

# while 1:
# 	for event in pygame.event.get():
# 		if event.type == pygame.QUIT:
# 			sys.exit()
# 	goatrect = goatrect.move(speed)

# 	if goatrect.left < 0 or goatrect.right > width:
# 		speed[0] = -speed[0]
# 	elif goatrect.top < 0 or goatrect.bottom > height:
# 		speed[1] = -speed[1]

# 	screen.fill(black)
# 	screen.blit(goat, goatrect)
# 	pygame.display.flip()

import threading;

def do_every (interval, worker_func, iterations = 0):
  if iterations != 1:
    threading.Timer (
      interval,
      do_every, [interval, worker_func, 0 if iterations == 0 else iterations-1]
    ).start ();

  worker_func ();

def print_hw ():
  print "hello world";

def print_so ():
  print "stackoverflow"


# call print_so every second, 5 times total
do_every (1, print_so, 5);

# call print_hw two times per second, forever
do_every (0.5, print_hw);