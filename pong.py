import pygame

pygame.init()

font20 = pygame.font.Font('freesansbold.ttf', 20)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Basic parameters of the screen
WIDTH, HEIGHT = 1080, 1920
# laptop Dev size:
#WIDTH, HEIGHT = 400, 850
#screen = pygame.display.set_mode((0, 0), (pygame.FULLSCREEN | pygame.RESIZABLE))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

clock = pygame.time.Clock() 
FPS = 30

class Striker:
        # Take the initial position, dimensions, speed and color of the object
    def __init__(self, posx, posy, width, height, speed, color):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
        # Rect that is used to control the position and collision of the object
        self.geekRect = pygame.Rect(posx, posy, width, height)
        # Object that is blit on the screen
        self.geek = pygame.draw.rect(screen, self.color, self.geekRect)

    def display(self):
        self.geek = pygame.draw.rect(screen, self.color, self.geekRect)

    def update(self, xFac):
        self.posx = self.posx + self.speed*xFac

        # Restricting the striker to be below the top surface of the screen
        if self.posx <= 0:
            self.posx = 0
        # Restricting the striker to be above the bottom surface of the screen
        elif self.posx + self.width >= WIDTH:
            self.posx = WIDTH-self.width

        # Updating the rect with the new values
        self.geekRect = (self.posx, self.posy, self.width, self.height)

    def displayScore(self, text, score, x, y, color):
        text = font20.render(text+str(score), True, color)
        textRect = text.get_rect()
        textRect.center = (x, y)

        screen.blit(text, textRect)

    def getRect(self):
        return self.geekRect

# Ball class


class Ball:
    def __init__(self, posx, posy, radius, speed, color):
        self.posx = posx
        self.posy = posy
        self.radius = radius
        self.speed = speed
        self.color = color
        self.xFac = 1
        self.yFac = -1
        self.ball = pygame.draw.circle(
            screen, self.color, (self.posx, self.posy), self.radius)
        self.firstTime = 1

    def display(self):
        self.ball = pygame.draw.circle(
            screen, self.color, (self.posx, self.posy), self.radius)

    def update(self):
        self.posx += self.speed*self.xFac
        self.posy += self.speed*self.yFac
        #print(f"Ball {self.posx}, {self.posy}")

        # If the ball hits the left or right surfaces, 
        # then the sign of yFac is changed and 
        # it results in a reflection
        if self.posx <= 0 or self.posx >= WIDTH:
            self.xFac *= -1
        # if self.posy <= 0 or self.posy >= HEIGHT:
        #     self.yFac *= -1

        if self.posy <= 0 and self.firstTime:
            self.firstTime = 0
            return 1
        elif self.posy >= HEIGHT and self.firstTime:
            self.firstTime = 0
            return -1
        else:
            return 0
        #return 0

    def reset(self):
        self.posx = WIDTH//2
        self.posy = HEIGHT//2
        self.yFac *= -1
        self.firstTime = 1

    # Used to reflect the ball along the Y-axis
    def hit(self):
        self.yFac *= -1

    def getRect(self):
        return self.ball

# Game Manager


def main():
    running = True

    # Defining the objects
    geek1 = Striker(20, 40, 100, 10, 10, GREEN)
    geek2 = Striker(20, HEIGHT-30, 100, 10, 10, GREEN)
    ball = Ball(WIDTH//2, HEIGHT//2, 7, 7, WHITE)

    listOfGeeks = [geek1, geek2]

    # Initial parameters of the players
    geek1Score, geek2Score = 0, 0
    geek1XFac, geek2XFac = 0, 0

    joysticks = {}

    while running:
        screen.fill(BLACK)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.JOYDEVICEADDED:
                # This event will be generated when the program starts for every
                # joystick, filling up the list without needing to create them manually.
                joy = pygame.joystick.Joystick(event.device_index)
                joysticks[joy.get_instance_id()] = joy
                print(f"Joystick {joy.get_instance_id()} connencted")
            if event.type == pygame.JOYDEVICEREMOVED:
                del joysticks[event.instance_id]
                print(f"Joystick {event.instance_id} disconnected")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    geek2XFac = 1
                if event.key == pygame.K_LEFT:
                    geek2XFac = -1
                if event.key == pygame.K_d:
                    geek1XFac = 1
                if event.key == pygame.K_s:
                    geek1XFac = -1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    geek2XFac = 0
                if event.key == pygame.K_d or event.key == pygame.K_s:
                    geek1XFac = 0
        
        # Always read joystick if present, not event
        for index, joystick in enumerate(joysticks.values()):
            axis = joystick.get_axis(1) # left/ right
            #print(f"Axis value: {axis:>6.3f}")
            new_value = 0
            if axis > 0.01:
                new_value = 1
            elif axis < -0.01:
                new_value = -1
            else:
                new_value = 0
            if index == 0:
                geek1XFac = new_value
            elif index == 1:
                geek2XFac = new_value

        # Collision detection
        for geek in listOfGeeks:
            if pygame.Rect.colliderect(ball.getRect(), geek.getRect()):
                ball.hit()

        # Updating the objects
        geek1.update(geek1XFac)
        geek2.update(geek2XFac)
        point = ball.update()

        # -1 -> Geek_1 has scored
        # +1 -> Geek_2 has scored
        # 0 -> None of them scored
        if point == -1:
            geek1Score += 1
        elif point == 1:
            geek2Score += 1

        # Someone has scored
        # a point and the ball is out of bounds.
        # So, we reset it's position
        if point: 
            ball.reset()

        # Displaying the objects on the screen
        geek1.display()
        geek2.display()
        ball.display()

        # Displaying the scores of the players
        geek1.displayScore("Geek_1 : ", 
                        geek1Score, 100, 20, WHITE)
        geek2.displayScore("Geek_2 : ", 
                        geek2Score, WIDTH-100, 20, WHITE)

        pygame.display.update()
        clock.tick(FPS)     


if __name__ == "__main__":
    main()
    pygame.quit()
