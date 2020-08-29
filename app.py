import pygame, os
pygame.init()

screenwidth = 800
screenheight = 480
win = pygame.display.set_mode((screenwidth, screenheight))

pygame.display.set_caption("My game!")

#Animation and background declarations
walkRight = [pygame.image.load(os.path.join('images','R1.png')), pygame.image.load(os.path.join('images','R2.png')),
pygame.image.load(os.path.join('images','R3.png')), pygame.image.load(os.path.join('images','R4.png')), pygame.image.load(os.path.join('images','R5.png')),
pygame.image.load(os.path.join('images','R6.png')), pygame.image.load(os.path.join('images','R7.png')), pygame.image.load(os.path.join('images','R8.png')),
pygame.image.load(os.path.join('images','R9.png')),]

walkLeft = [pygame.image.load(os.path.join('images','L1.png')), pygame.image.load(os.path.join('images','L2.png')),
pygame.image.load(os.path.join('images','L3.png')), pygame.image.load(os.path.join('images','L4.png')), pygame.image.load(os.path.join('images','L5.png')),
pygame.image.load(os.path.join('images','L6.png')), pygame.image.load(os.path.join('images','L7.png')), pygame.image.load(os.path.join('images','L8.png')),
pygame.image.load(os.path.join('images','L9.png')),]


bg = pygame.image.load(os.path.join('images', 'bg.jpg'))
clock = pygame.time.Clock()

class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 10
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True

    def draw(self, win):
        #Drawing a character - takes the window, color, and dimensions as
        #parameters. Now we can use win.blit to draw from the images folder
        if self.walkCount + 1 > 27:
            self.walkCount = 0

        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x,self.y)) #Example of integer division
                self.walkCount += 1

            elif myGuy.right:
                win.blit(walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1

        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))

class enemy(object):
    walkRight = [pygame.image.load(os.path.join('images','L1E.png')), pygame.image.load(os.path.join('images','L2E.png')),
    pygame.image.load(os.path.join('images','R3E.png')), pygame.image.load(os.path.join('images','R4E.png')), pygame.image.load(os.path.join('images','R5E.png')),
    pygame.image.load(os.path.join('images','R6E.png')), pygame.image.load(os.path.join('images','R7E.png')), pygame.image.load(os.path.join('images','R8E.png')),
    pygame.image.load(os.path.join('images','R9E.png')), pygame.image.load(os.path.join('images','R10E.png')), pygame.image.load(os.path.join('images','R11E.png'))]

    walkLeft = [pygame.image.load(os.path.join('images','L1E.png')), pygame.image.load(os.path.join('images','L2E.png')),
    pygame.image.load(os.path.join('images','L3E.png')), pygame.image.load(os.path.join('images','L4E.png')), pygame.image.load(os.path.join('images','L5E.png')),
    pygame.image.load(os.path.join('images','L6E.png')), pygame.image.load(os.path.join('images','L7E.png')), pygame.image.load(os.path.join('images','L8E.png')),
    pygame.image.load(os.path.join('images','L9E.png')), pygame.image.load(os.path.join('images','L10E.png')), pygame.image.load(os.path.join('images','L11E.png'))]


    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3

    def draw(self, win):
        if self.walkCount + 1 >= 33:
            self.walkCount = 0
        if self.vel > 0:
            win.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
        else:
            win.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
        self.move()
        pass

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel *= -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 10 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

def redrawGameWindow():
    win.blit(bg, (0,0))
    myGuy.draw(win)
    enemy.draw(win)
    for bullet in bullets:
        bullet.draw(win)

    pygame.display.update()

#Main loop

myGuy = player(50, 400, 64, 64)
enemy = enemy(400, 400, 64, 64, 600)
bullets = []
run = True
while run:
        clock.tick(27)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for bullet in bullets:
            if bullet.x < 800 and bullet.x > 0:
                bullet.x += bullet.vel
            else:
                bullets.pop(bullets.index(bullet))

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            if myGuy.left:
                facing = -1
            else:
                facing = 1
            if len(bullets) < 20:
                bullets.append(projectile(round(myGuy.x + myGuy.width//2),
                round(myGuy.y + myGuy.height//2), 5, (0,0,0), facing))

        if keys[pygame.K_a] and myGuy.x >= myGuy.vel:
            myGuy.x -= myGuy.vel
            myGuy.left = True
            myGuy.right = False
            myGuy.standing = False
        elif keys[pygame.K_d] and myGuy.x < screenwidth - myGuy.width - myGuy.vel:
            myGuy.x += myGuy.vel
            myGuy.left = False
            myGuy.right = True
            myGuy.standing = False
        else:
            myGuy.standing = True
            myGuy.walkCount = 0


        if not myGuy.isJump:
            if keys[pygame.K_w]:
                myGuy.isJump = True
        else:
            if myGuy.jumpCount >= -10:
                neg = 1
                if myGuy.jumpCount < 0:
                    neg = -1

                myGuy.y -= (myGuy.jumpCount ** 2 * neg) * .5
                myGuy.jumpCount -= 1

            else:
                myGuy.isJump = False
                myGuy.jumpCount = 10

        redrawGameWindow()

pygame.quit()
