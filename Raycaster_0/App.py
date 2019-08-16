import pygame
import math

winWidth = 800
winHeight = 500

pygame.init()
window = pygame.display.set_mode((winWidth, winHeight))
pygame.display.set_caption("Raycaster_0")

run = True
clock = pygame.time.Clock()

white = (255, 255, 255)
black = (0,0,0)
grey = (50,50,50)
lightGrey = (200,200,200)
red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)

drawDistance = 20.0
minWallDistance = 2.0
minWallHeight = 20.0

class Vector2f:

	def __init__(self, x, y):

		self.x = x
		self.y = y

	def getX(self): return self.x

	def getY(self): return self.y

	def add(self, vec):

		self.x += vec.getX()
		self.y += vec.getY()

	def sub(self, vec):

		self.x -= vec.getX()
		self.y -= vec.getY()

	def getAdd(self, vec): return Vector2f(self.x + vec.getX(), self.y + vec.getY())

	def getSub(self, vec): return Vector2f(self.x - vec.getX(), self.y - vec.getY())

	def norm(self): return math.sqrt( self.x**2 + self.y**2)



class Player:

	def __init__(self, pos, velocity):

		self.pos = pos
		self.velocity = velocity
		self.direction = 0.0

	def incDirection(self, inc):
		self.direction += inc

		if self.direction > (2*math.pi):
			self.direction -= 2*math.pi

		elif self.direction < 0:
			self.direction += 2*math.pi

	def getPos(self): return self.pos

	def getVelocity(self): return self.velocity

	def getDirection(self): return self.direction



class Wall:

	def __init__(self, pos_a, pos_b, color):

		self.pos_a = pos_a
		self.pos_b = pos_b
		self.color = color

	def getPos_a(self): return self.pos_a

	def getPos_b(self): return self.pos_b

	def getColor(self): return self.color

player = Player(Vector2f(2, 2), 0.1)
wall = [Wall(Vector2f(6 , 6 ), Vector2f(6 , 7 ), red  ), 
		Wall(Vector2f(6 , 6 ), Vector2f(7 , 6 ), green),
		Wall(Vector2f(7 , 6 ), Vector2f(7 , 7 ), blue ),
		Wall(Vector2f(7 , 7 ), Vector2f(6 , 7 ), green),
		Wall(Vector2f(7 , 1 ), Vector2f(9 , 1 ), red  ),
		Wall(Vector2f(9 , 1 ), Vector2f(9 , 3 ), green),
		Wall(Vector2f(9 , 3 ), Vector2f(7 , 3 ), blue ),
		Wall(Vector2f(7 , 1 ), Vector2f(7 , 3 ), green),
		Wall(Vector2f(0 , 0 ), Vector2f(12, 0 ), red  ),
		Wall(Vector2f(0 , 0 ), Vector2f(0 , 12), green),
		Wall(Vector2f(12, 0 ), Vector2f(12, 12), blue ),
		Wall(Vector2f(0 , 12), Vector2f(12, 12), red  )]

def getIntersection(a, b, c, d):
          
	s10_x = b.getX() - a.getX()
	s10_y = b.getY() - a.getY()
	s32_x = d.getX() - c.getX()
	s32_y = d.getY() - c.getY()

	denom = s10_x * s32_y - s32_x * s10_y
	if denom == 0:
		return None 

	denomPositive = denom > 0

	s02_x = a.getX() - c.getX()
	s02_y = a.getY() - c.getY()
	s_numer = s10_x * s02_y - s10_y * s02_x
	if (s_numer < 0) == denomPositive:
		return None 

	t_numer = s32_x * s02_y - s32_y * s02_x
	if (t_numer < 0) == denomPositive:
		return None 

	if ((s_numer > denom) == denomPositive) or ((t_numer > denom) == denomPositive):
		return None 
    
	t = t_numer / denom;

	return Vector2f(a.getX() + (t * s10_x), a.getY() + (t * s10_y))	


scalar = (minWallHeight - float(winHeight)) / (1.0/float(drawDistance) - 1.0/minWallDistance)
adder = float(winHeight) - scalar/minWallDistance
def getWallHeight(wallDistance): return scalar / float(wallDistance) + adder

class Renderer:

	def __init__(self, fov, numRays):

		self.fov = fov
		self.numRays = numRays

	def render(self):

		pygame.draw.rect(window, grey, [0, winHeight/2, winWidth, winHeight/2])

		i = 0
		while  i < self.numRays:

			ray_posA = Vector2f(player.getPos().getX(), player.getPos().getY())
			alpha = self.fov / (float(self.numRays) - 1.0)
			rayDirection = (player.getDirection() + self.fov/2.0) - (i * alpha) 

			ray_posB = player.getPos().getAdd( Vector2f( (math.cos(rayDirection) * drawDistance), -(math.sin(rayDirection) * drawDistance) ) )

			intersection = None
			color = None

			for w in wall:

				vec_a = w.getPos_a().getSub(player.getPos())
				vec_b = w.getPos_b().getSub(player.getPos())

				if(vec_a.norm() <= drawDistance or vec_b.norm() <= drawDistance):

					newIntersection = getIntersection(ray_posA, ray_posB, w.getPos_a(), w.getPos_b())

					if not (newIntersection is None):

						if intersection is None:
							intersection = newIntersection
							color = w.getColor()

						else:
							intDistance = (player.getPos().getSub(intersection)).norm()
							newIntDistance = (player.getPos().getSub(newIntersection)).norm()

							if newIntDistance < intDistance:
								intersection = newIntersection
								color = w.getColor()

			if not (intersection is None):

				rectWidth = winWidth / self.numRays
				rectHeight = 0

				wallDistance = (intersection.getSub(player.getPos())).norm() * math.cos(rayDirection - player.getDirection())

				if wallDistance <= minWallDistance:
					rectHeight = winHeight

				else: rectHeight = getWallHeight(wallDistance)

				pygame.draw.rect(window, color, [i*rectWidth, (winHeight - rectHeight)/2, rectWidth, rectHeight])

			i += 1

		minMapScale = 10
		pygame.draw.rect(window, lightGrey, [0, 0, 120, 120])
		pygame.draw.rect(window, black, [ (player.getPos().getX() - 1.0/8.0)*minMapScale, (player.getPos().getY() - 1.0/8.0)*minMapScale, minMapScale/4.0, minMapScale/4.0])
		vec = player.getPos().getAdd(Vector2f(math.cos(player.getDirection()), -math.sin(player.getDirection())))
		pygame.draw.line(window, black, (player.getPos().getX()*minMapScale, player.getPos().getY()*minMapScale), (vec.getX()*minMapScale, vec.getY()*minMapScale))

		for w in wall:
			pygame.draw.line(window, black, ( w.getPos_a().getX() * minMapScale, w.getPos_a().getY() * minMapScale ), ( w.getPos_b().getX() * minMapScale, w.getPos_b().getY() * minMapScale ))


renderer = Renderer(math.pi*0.4, 200)

while run:

	for event in pygame.event.get():

		if event.type == pygame.QUIT: run = False

		if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: run = False

	pressed = pygame.key.get_pressed()

	if pressed[pygame.K_RIGHT]: player.incDirection(-math.pi/24)

	if pressed[pygame.K_LEFT]: player.incDirection(math.pi/24)

	if pressed[pygame.K_UP]:
		velocityVec = Vector2f( (math.cos(player.getDirection()) * player.getVelocity()), - (math.sin(player.getDirection()) * player.getVelocity()) )
		player.getPos().add(velocityVec)

	if pressed[pygame.K_DOWN]:
		velocityVec = Vector2f( (math.cos(player.getDirection()) * player.getVelocity()), - (math.sin(player.getDirection()) * player.getVelocity()) )
		player.getPos().sub(velocityVec)

	window.fill(white)
	renderer.render()
	pygame.display.update()

	clock.tick(30)

pygame.quit()