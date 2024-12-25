import pygame
from pygame.locals import *
import time
import random
SIZE = 40
BACKGROUND_COLOR = (110, 110, 5)

class Apple:
    def __init__(self,parent_screen):
        self.image = pygame.image.load("images/images.jpeg").convert()
        self.parent_screen = parent_screen
        self.x = SIZE*3
        self.y = SIZE*3
    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()
    def move(self):
        self.x = random.randint(0,21)*SIZE
        self.y = random.randint(0,14)*SIZE

class Snake:
    def __init__(self, surface, length):
        self.length = length
        self.parent_screen = surface
        self.block = pygame.image.load("images/istockphoto-2149423184-612x612.jpg").convert()
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.direction = "down"
    def draw(self):
        self.parent_screen.fill(BACKGROUND_COLOR)
        for i in range(self.length):
          self.parent_screen.blit(self.block,(self.x[i],self.y[i]))
        pygame.display.flip()
    def walk(self):
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        if self.direction == "up":
            self.y[0] -= SIZE
        if self.direction == "down":
            self.y[0] += SIZE
        if self.direction == "left":
            self.x[0] -= SIZE
        if self.direction == "right":
            self.x[0] += SIZE
        self.draw()
    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)
    def move_left(self):
        self.direction="left"
    def move_right(self):
        self.direction="right"
    def move_up(self):
        self.direction="up"
    def move_down(self):
        self.direction="down"


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Apple game")
        pygame.mixer.init()
        self.play_background_music()
        self.surface = pygame.display.set_mode((900,600))
        self.surface.fill((110,110,5))
        self.snake = Snake(self.surface,1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()
        #colliding with apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.apple.move()
        # colliding with itself
        for i in range(1, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("metal")
                raise Exception ("Game Over")
    def show_game_over(self):
        self.surface.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont('arial', 20)
        line1 = font.render(f"Game is over! Your score is {self.snake.length}",True,(200,200,200))
        self.surface.blit(line1,(200,300))
        line2 = font.render("To play the game again press Enter. To exit press Escape!", True,(255,255,255))
        self.surface.blit(line2,(200,350))
        pygame.display.flip()
        pygame.mixer.music.pause()

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def play_sound(self,sound):
        sound = pygame.mixer.Sound(f"images/{sound}.mp3")
        pygame.mixer.Sound.play(sound)



    def is_collision(self,x1,y1,x2,y2):
        if x1 >= x2 and x1<x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def play_background_music(self):
        pygame.mixer.music.load("images/background-music-224633.mp3")
        pygame.mixer.music.play(-1)
    def display_score(self):
        font = pygame.font.SysFont('arial',20)
        score = font.render(f"Score:{self.snake.length}",True,(200,200,200))
        self.surface.blit(score,(800,10))


    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False
                        self.snake= Snake(self.surface,1)
                        self.apple = Apple(self.surface)
                    if not pause:
                      if event.key == K_UP:
                        self.snake.move_up()
                      if event.key == K_DOWN:
                        self.snake.move_down()
                      if event.key == K_LEFT:
                        self.snake.move_left()

                      if event.key == K_RIGHT:
                        self.snake.move_right()

                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                 self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()
            time.sleep(0.3)



if __name__=="__main__":
    game = Game()
    game.run()



