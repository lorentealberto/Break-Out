import pygame as py
from pygame.locals import QUIT, K_RIGHT, K_LEFT, K_SPACE

#CONFIGURACIÓN
SWIDTH 	= 640					#Anchura de la pantalla
SHEIGHT = 480					#Altura de la pantalla
FPS 	= 60					#Veces por segundo que se actualizará el juego
COLS 	= 10					#Nº de bloques por columna
ROWS 	= 1						#Nº de bloques por fila
BWIDHT 	= SWIDTH / COLS 		#Ancho del bloque
BHEIGHT = SHEIGHT / 3 / ROWS 	#Alto del bloque
BSIZE 	= 5						#Tamaño de la pelota
SPEED 	= 15					#Velocidad del jugador / pelota


#Clase que sirve para representar un bloque del juego
class Block(object):

	'''Constructor parametrizado
		+ x: Posición horizontal donde se colocará el bloque
		+ y: Posición vertical donde se colocará el bloque'''
	def __init__(self, x, y):
		self.body = py.Rect(x, y, BWIDHT, BHEIGHT)
		self.dead = False

	'''Dibuja el bloque en la pantalla
		+ screen: Superficie donde se dibujará el bloque'''
	def render(self, screen):
		py.draw.rect(screen, (255, 0, 0), self.body, 1)


#Clase que sirve para representar el conjunto de los bloques del juego
class Blocks(object):

	#Constructor por defecto
	def __init__(self):
		self.blocks = []
		self.addBlocks()

	'''Dibuja todos los bloques en la pantalla
		+ screen: Superficie donde se dibujarán todos los bloques'''
	def render(self, screen):
		for b in self.blocks:
			b.render(screen)

	#Método que comprueba si algún bloque ha sido golpeado por la pelota para poder eliminarlo
	def update(self):
		for b in self.blocks:
			if b.dead:
				self.blocks.remove(b)

	#Añade los bloques al juego dando a cada uno una posición determinada
	def addBlocks(self):
		for i in range(COLS):
			for j in range(ROWS):
				self.blocks.append(Block(i * BWIDHT, j * BHEIGHT))


'''Clase que sirve para representar al jugador'''
class Player(object):

	#Constructor por defecto
	def __init__(self):
		self.body = py.Rect(0, 0, 40, 15)
		self.body.x = SWIDTH / 2 - self.body.width / 2
		self.body.y = SHEIGHT - self.body.height * 3
		self.speed = SPEED

	'''Dibuja el jugador en la pantalla
		+ screen: Superficie donde se dibujará el jugador'''
	def render(self, screen):
		py.draw.rect(screen, (255, 255, 255), self.body)

	'''Actualiza el jugador
		+ ball: Objeto del tipo \pelota\ este objeto será utilizador por la IA para calcular
			la posición'''
	def update(self, ball):
		#self.controls()
		self.AI(ball)
		self.checkBounds()

	'''IA que juega automaticamente
		+ ball: Objeto del tipo \pelota\. Necesario para calcular la posición donde debe ir
			el jugador'''
	def AI(self, ball):
		if self.body.x + self.body.width / 2 > ball.body.x + ball.body.width / 2:
			self.body.move_ip(-self.speed, 0)
		if self.body.x + self.body.width / 2 < ball.body.x + ball.body.width / 2:
			self.body.move_ip(self.speed, 0)

	#Controles para un jugador humano
	def controls(self):
		key = py.key.get_pressed()

		if key[K_RIGHT]:
			self.body.move_ip(self.speed, 0)
		elif key[K_LEFT]:
			self.body.move_ip(-self.speed, 0)

	#Comprueba que el jugador no se salga de la pantalla
	def checkBounds(self):
		if self.body.x < 0:
			self.body.x = 0
		elif self.body.right > SWIDTH:
			self.body.right = SWIDTH


'''Clase que representa la pelota'''
class Ball(object):

	'''Constructor parametrizado
		+ playerY: Posición vertical del jugador. Usada para colocar la pelota en la posición
			correcta.'''
	def __init__(self, playerY):
		self.body = py.Rect(SWIDTH / 2 - BSIZE / 2, playerY - BSIZE * 2, BSIZE, BSIZE)
		
		self.speed = SPEED - 2
		self.vx = self.vy = -self.speed

	'''Dibuja la pelota en la pantalla
		+ screen: Superficie donde se dibujará la pelota'''
	def render(self, screen):
		py.draw.rect(screen, (255, 255, 255), self.body)

	'''Actualiza la pelota
		+ blocks: Bloques. Necesarios para calcular las colisiones.
		+ player: Jugador. Necesario para calcular las colisiones.'''
	def update(self, blocks, player):
		self.checkPlayerCollisions(player)
		self.checkBlocksCollisions(blocks)
		self.checkBounds()
		self.move()

	'''#Comprueba las colisiones entre la pelota y el jugador
		+ player: Objetio del tipo \player\, necesario para calcular las
			colisiones entre el jugador y la pelota.'''
	def checkPlayerCollisions(self, player):
		if self.body.colliderect(player.body):
			self.body.bottom = player.body.top - 1
			self.vy *= -1

	'''#Comprueba las colisiones entre la pelota y los bloques
		+ blocks: Objeto del tipo \blocks\ usado para calcular la colisión entre
			la pelota y los bloques.'''
	def checkBlocksCollisions(self, blocks):
		for b in blocks:
			if self.body.colliderect(b.body):
				if self.body.left < b.body.right or self.body.right > b.body.left:
					self.vx *= -1
					
				self.vy *= -1
				b.dead = True

	#Comprueba que la pelota no se salga de la pantalla
	def checkBounds(self):
		if self.body.left < 0 or self.body.right > SWIDTH:
			self.vx *= -1

		if self.body.top < 0:
			self.body.top = 0
			self.vy *= -1

	#Mueve la pelota
	def move(self):
		self.body.move_ip(self.vx, self.vy)


'''Clase encargada de gestionar todos los elementos del juego'''
class Game(object):

	#Constructor por defecto
	def __init__(self):
		self.player = Player()
		self.blocks = Blocks()
		self.ball = Ball(self.player.body.top)

	#Actualiza los elementos del juego
	def update(self):
		self.blocks.update()
		self.player.update(self.ball)
		self.ball.update(self.blocks.blocks, self.player)

	'''Dibuja los elementos en la pantalla
		screen: Superficie donde se dibujarán los elementos'''
	def render(self, screen):
		self.player.render(screen)
		self.blocks.render(screen)
		self.ball.render(screen)


def main():
	py.init()

	screen = py.display.set_mode((SWIDTH, SHEIGHT))
	py.display.set_caption("BreakOut!")

	clear = (0, 0, 0)
	exit = False
	clock = py.time.Clock()

	game = Game()

	while not exit:
		for event in py.event.get():
			if event.type == QUIT:
				exit = True
		screen.fill(clear)
		game.update()
		game.render(screen)
		py.display.update()
		clock.tick(FPS)

if __name__ == '__main__':
	main()