import pygame
import random

SCREEN_WIDTH = 720
SCREEN_HEIGHT = 720
X_POSITIONS = [120, 240, 360, 480, 600]

pygame.init()
CREATE_STONE = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_STONE, 1000)

ALLOW_INPUT = pygame.USEREVENT + 2
accepting_input = True


class Stones:
    def __init__(self) -> None:
        self.y = 0
        self.x = random.choice(X_POSITIONS)

    def fall(self):
        self.y += 5


class Player:
    def __init__(self) -> None:
        self.x = 360
        self.y = 600

    def moveLeft(self):
        if(self.x > 120):
            self.x -= 120
        pygame.time.set_timer(ALLOW_INPUT, 300)


    def moveRight(self):
        if(self.x < 600):
            self.x += 120
        pygame.time.set_timer(ALLOW_INPUT, 300)

    def collide(self, stone:Stones):
        dist = (stone.x - self.x)**2 + (stone.y - self.y)**2
        ideal_dist = 40**2
        if(dist <= ideal_dist):
            return True


class GameAI:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((720, 720))
        self.clock = pygame.time.Clock()
        self.running = True
        self.reset()
        # self.stones_list = []
        # self.player = Player()
        # self.score = 0
        # self.create_stone()
        # self.accepting_input = True

    def reset(self):
        self.stones_list = []
        self.player = Player()
        self.score = 0
        self.create_stone()
        self.create_stone()
        self.accepting_input = True
        self.frame_iteration = 0


    def create_stone(self):
        self.stones_list.append(Stones())
        self.stones_list.append(Stones())

    def display_score(self):
        font=pygame.font.Font(None,30)
        scoretext=font.render("Score:"+str(self.score/3), 1,(255,255,255))
        self.screen.blit(scoretext, (620, 20))

    def play_step(self, action):
        self.frame_iteration = 0
        game_over = False
        reward = 0

        if action == [1, 0, 0]:
            self.player.moveLeft()
        elif action == [0, 0, 1]:
            self.player.moveRight()
        else:
            pass

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False


            if event.type == CREATE_STONE:
                obj1 = Stones()
                self.stones_list.append(obj1)
                obj2 = Stones()
                self.stones_list.append(obj2)
                obj3 = Stones()
                self.stones_list.append(obj3)

            if event.type == ALLOW_INPUT:
                self.accepting_input = True

        for stone in self.stones_list:
            stone.fall()
            if stone.y > 720:
                self.stones_list.remove(stone)
                self.score += 1
                reward = 1

            if self.player.collide(stone):
                print("Collided")
                print("Score: ", self.score)
                self.running = False

        reward = reward/3

        if self.is_collision():
            game_over = True
            reward = -10

        return reward, game_over, self.score

    def is_collision(self):
        for stone in self.stones_list:
            if self.player.collide(stone):
                return True
        return False

    def update_ui(self):
        self.screen.fill("black")
        for stone in self.stones_list:
            pygame.draw.circle(self.screen, "red", [stone.x, stone.y], 40)

        pygame.draw.circle(self.screen, "green", [self.player.x, self.player.y], 40)
        pygame.display.flip()



# if __name__ == "__main__":
#     game = GameAI()
#     while game.running:
#         game.play_step()
#         game.update_ui()
#         game.display_score()
#         # pygame.display.update()
#         game.clock.tick(60)
#     pygame.quit()