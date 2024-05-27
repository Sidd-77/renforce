import pygame
import random

SCREEN_WIDTH = 720
SCREEN_HEIGHT = 720


# pygame setup
pygame.init()
screen = pygame.display.set_mode((720, 720))
clock = pygame.time.Clock()
running = True

X_POSITIONS = [120, 240, 360, 480, 600]

stones_list = []

CREATE_STONE = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_STONE, 1000)

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


    def moveRight(self):
        if(self.x < 600):
            self.x += 120

    def collide(self, stone:stones):
        dist = (stone.x - self.x)**2 + (stone.y - self.y)**2
        ideal_dist = 40**2
        if(dist <= ideal_dist):
            return True

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
        if keys[pygame.K_a] or keys[pygame.K_d]:

            if keys[pygame.K_a]:
                p1.moveLeft()
            if keys[pygame.K_d]:
                p1.moveRight()

            accepting_input = False
            pygame.time.set_timer(ALLOW_INPUT, 300)  # Allow input again after some delay


    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
