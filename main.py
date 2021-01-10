import pygame
import random
from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("ToHellWithJohnny")
backgroundImg = pygame.image.load("background.png")

# rising speed
RISING_SPEED = -1.5

# background music
mixer.music.load("kid.wav")
mixer.music.play(-1)

# score
score_value = 0
font = pygame.font.Font("newfont.ttf", 32)

# game over and restart
over_font = pygame.font.Font("newfont.ttf", 64)
res_font = pygame.font.Font("newfont.ttf", 32)

# player
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 50
playerX_change = 0
playerY_change = 4.5

# icon
pygame.display.set_icon(playerImg)

# brick
brickImg = pygame.image.load("wall.png")
brickX = []
brickY = []
brickY_change = []
for i in range(2):
    brickX.append(random.randint(10, 770))
    brickY.append(600)
    brickY_change.append(RISING_SPEED)

# wood
woodImg = pygame.image.load("wood.png")
woodX = []
woodY = []
woodY_change = RISING_SPEED
wood_state = []

# conveyor
conveyorImg = pygame.image.load("conveyor.png")
conveyorX = []
conveyorY = []
conveyorY_change = RISING_SPEED
conveyor_speed = 3


def brick_generate():
    if t % 100 == 0:
        for i in range(random.randint(0, 2)):
            r = random.randint(10, 770)
            brickX.append(r)
            brickY.append(700)
            brickY_change.append(RISING_SPEED)
            generateX.append(r)

    for j in range(len(brickX) - 1, -1, -1):
        if brickY[j] <= -30:
            del brickX[j]
            del brickY[j]
            del brickY_change[j]


def wood_generate():
    if t % 100 == 0:
        for i in range(random.randint(0, 1)):
            r = random.randint(10, 770)
            valid_r = True
            for Xs in generateX:
                if Xs - 150 < r < Xs + 150:
                    valid_r = False
            if valid_r:
                woodX.append(r)
                woodY.append(700)
                wood_state.append(0)  # 0 sec for being landed
                generateX.append(valid_r)

        for j in range(len(woodX) - 1, -1, -1):
            if woodY[j] <= -30:
                del woodX[j]
                del woodY[j]


def conveyor_generate():
    if t % 100 == 0:
        for i in range(random.randint(0, 1)):
            r = random.randint(10, 770)
            valid_r = True
            for Xs in generateX:
                if Xs - 150 < r < Xs + 150:
                    valid_r = False
            if valid_r:
                conveyorX.append(r)
                conveyorY.append(700)

        for j in range(len(conveyorX) - 1, -1, -1):
            if conveyorY[j] <= -30:
                del conveyorX[j]
                del conveyorY[j]


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (65, 105, 225))
    screen.blit(score, (x, y))


def game_over():
    over = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over, (220, 250))
    res = res_font.render("Click the button below to restart", True, (255, 255, 255))
    screen.blit(res, (230, 350))


def player(x, y):
    screen.blit(playerImg, (x, y))


def brick(x, y):
    screen.blit(brickImg, (x, y))


def wood(x, y):
    screen.blit(woodImg, (x, y))


def conveyor(x, y):
    screen.blit(conveyorImg, (x, y))


# deleted landed as parameter
def land_on_brick():
    landed = False

    for i in range(len(brickX)):
        if brickY[i] - 58 <= playerY <= brickY[i] - 50 and brickX[i] - 48 <= playerX <= brickX[i] + 115:
            landed = True

    return playerY_change == 4.5 and landed, landed


def land_on_wood():
    landed = False

    for i in range(len(woodX)):
        if woodY[i] - 58 <= playerY <= woodY[i] - 50 and woodX[i] - 43 <= playerX <= woodX[i] + 115:
            landed = True
            wood_state[i] += 1

    for i in range(len(woodX)):
        if random.randint(100, 200) < wood_state[i]:
            woodY[i] = -1000
            wood_state[i] = 0
            break_sound = mixer.Sound("woodbreak.wav")
            break_sound.play()

    return playerY_change == 4.5 and landed, landed


def land_on_conveyor():
    landed = False
    for i in range(len(conveyorX)):
        if conveyorY[i] - 58 <= playerY <= conveyorY[i] - 50 and conveyorX[i] - 43 <= playerX <= conveyorX[i] + 110:
            landed = True

    return playerY_change == 4.5 and landed, landed


# button
class button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.Font('newfont.ttf', 60)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True

        return False


running = True
t = 1
restart_button = button((255, 255, 255), 320, 450, 140, 60, "Restart")

while running:
    t += 1
    screen.fill((0, 0, 0))
    screen.blit(backgroundImg, (0, 0))

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if restart_button.isOver(pos):
                # restart
                playerX = 370
                playerY = 50
                for i in range(2):
                    brickX.append(random.randint(10, 770))
                    brickY.append(600)
                    brickY_change.append(RISING_SPEED)
                score_value = 0
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            elif event.key == pygame.K_RIGHT:
                playerX_change = 5
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    if playerX >= 730:
        playerX = 730
    elif playerX <= 5:
        playerX = 5

    generateX = []
    brick_generate()
    wood_generate()
    conveyor_generate()
    generateX.clear()

    land_brick = land_on_brick()
    land_wood = land_on_wood()
    land_conveyor = land_on_conveyor()

    if land_brick[0] or land_wood[0] or land_conveyor[0]:
        score_value += 1
        bullet_sound = mixer.Sound("jump.wav")
        bullet_sound.play()
    if land_brick[1] or land_wood[1] or land_conveyor[1]:
        playerY_change = RISING_SPEED
    else:
        playerY_change = 4.5
    if land_conveyor[1]:
        playerX += 3

    for n in range(len(woodX)):
        woodY[n] += woodY_change
        wood(woodX[n], woodY[n])

    for i in range(len(brickX)):
        brickY[i] += brickY_change[i]
        brick(brickX[i], brickY[i])

    for k in range(len(conveyorX)):
        conveyorY[k] += conveyorY_change
        conveyor(conveyorX[k], conveyorY[k])

    if playerY <= -10 or playerY >= 730:
        game_over()
        restart_button.draw(screen, (0, 0, 0))
        playerY = 1000
        brickX.clear()
        brickY.clear()
        brickY_change.clear()
        woodX.clear()
        woodY.clear()
        wood_state.clear()
        conveyorX.clear()
        conveyorY.clear()

    playerX += playerX_change
    playerY += playerY_change
    player(playerX, playerY)
    show_score(10, 10)

    pygame.display.update()
