class Button:
	def __init__(self, fill, callback, text, width, height, border):

				startBtn = pygame.Surface((300,50))
				startBtn.fill((0,210,255))
		self
				startBtnPos =  startBtn.get_rect()
				startBtnPos.centerx = self.screen.get_rect().centerx
				startBtnPos.top = 100

				font = pygame.font.Font(None, 36)
				
				text = font.render("Start Game", 1, (10,10, 10))
				textpos = text.get_rect()
				textpos.centerx = 150
				textpos.centery = 25
				startBtn.blit(text, textpos)
	def checkColision 