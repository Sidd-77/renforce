import pygame
import random

SCREEN_WIDTH = 720
SCREEN_HEIGHT = 720
INPUT_DELAY = 500
STONE_CREATION_DELAY = 600

# pygame setup
pygame.init()
screen = pygame.display.set_mode((720, 720))
clock = pygame.time.Clock()
running = True

X_POSITIONS = [120, 240, 360, 480, 600]

stones_list = []

CREATE_STONE = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_STONE, STONE_CREATION_DELAY) ## stone creation delay

ALLOW_INPUT = pygame.USEREVENT + 2
accepting_input = True

def display_score(score):
   font=pygame.font.Font(None,30)
   scoretext=font.render("Score:"+str(score), 1,(255,255,255))
   screen.blit(scoretext, (620, 20))


class stones:
    def __init__(self) -> None:
        self.y = 0
        self.x = random.choice(X_POSITIONS)

    def fall(self):
        self.y += 5

class player:
    def __init__(self) -> None:
        self.x = 360
        self.y = 600

    def moveLeft(self):
        if(self.x > 120):
            self.x -= 120
        else:
            self.x = 600


    def moveRight(self):
        if(self.x < 600):
            self.x += 120
        else:
            self.x = 120

    def collide(self, stone:stones):
        dist = (stone.x - self.x)**2 + (stone.y - self.y)**2
        ideal_dist = 40**2
        if(dist <= ideal_dist):
            return True

    def make_decision(self, stone1:stones, stone2:stones, stone3:stones):
        valid_spaces = [x for x in X_POSITIONS if x!=stone1.x and x!=stone2.x and x!=stone3.x]
        if self.x in valid_spaces:
            print("No need to move")
            return
        else:
            self.moveLeft()
            print("Moved Left")

p1 = player()

player_score = 0;

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == CREATE_STONE:
            obj1 = stones()
            stones_list.append(obj1)
            obj2 = stones()
            stones_list.append(obj2)
            obj3 = stones()
            stones_list.append(obj3)

        if event.type == ALLOW_INPUT:
            accepting_input = True


    screen.fill("black")

    # RENDER YOUR GAME HERE

    for stone in stones_list:
        stone.fall()
        stone.obj = pygame.draw.circle(screen, "red", [stone.x, stone.y], 40)
        if stone.y > 730:
            player_score += 0.5
            stones_list.remove(stone)

        if p1.collide(stone):
            print("Collided")
            print("Score: ", player_score)
            running = False

    player = pygame.draw.circle(screen, "green", [p1.x, p1.y], 40)

    keys = pygame.key.get_pressed()

    # if keys[pygame.K_a]:
    #     p1.moveLeft()
    # if keys[pygame.K_d]:
    #     p1.moveRight()

    display_score(player_score)

    if accepting_input:
        if len(stones_list) > 1:
            p1.make_decision(stones_list[0], stones_list[1], stones_list[2])
        if keys[pygame.K_a] or keys[pygame.K_d]:

            if keys[pygame.K_a]:
                p1.moveLeft()
            if keys[pygame.K_d]:
                p1.moveRight()

            accepting_input = False
            pygame.time.set_timer(ALLOW_INPUT, INPUT_DELAY)  # Allow input again after some delay


    pygame.display.flip()

    clock.tick(120)  # limits FPS to 120

pygame.quit()
