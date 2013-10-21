#!/usr/bin/env python
# encoding: utf-8

import sys
import pygame
import threading

def do_every (interval, worker_func, iterations = 0):
  if iterations != 1:
    threading.Timer (
      interval,
      do_every, [interval, worker_func, 0 if iterations == 0 else iterations-1]
    ).start();

  worker_func();

def work():
	print "work work work"

def main():

	width = 320
	height  = 480
	size = width, height

	black = 0, 0, 0

	screen = pygame.display.set_mode(size)

	goat = pygame.image.load("goat.bmp")
	goatrect = goat.get_rect()
	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.KEYDOWN:			
				if event.key == pygame.K_DOWN:
					goatrect = goatrect.move([0,10])
				elif event.key == pygame.K_UP:
					goatrect = goatrect.move([0,-10])
				elif event.key == pygmae.K_RIGHT:
					goatrect = goatrect.move([10, 0])
				elif event.key == pygame.K_LEFT:
					goatrect = goatrect.move([-10,0])
		screen.fill(black)
		screen.blit(goat, goatrect)
		pygame.display.flip()

main()