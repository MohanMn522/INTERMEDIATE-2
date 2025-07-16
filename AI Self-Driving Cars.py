import pygame
import numpy as np
import math
import sys

pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Self-Driving Car Simulation")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ROAD_COLOR = (50, 50, 50)

# Clock
clock = pygame.time.Clock()

# Car class
class Car:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 100
        self.angle = 0
        self.speed = 2
        self.length = 40
        self.width = 20
        self.color = (0, 255, 0)

    def draw(self, screen):
        rotated_car = pygame.Surface((self.length, self.width))
        rotated_car.fill(self.color)
        rotated_car = pygame.transform.rotate(rotated_car, self.angle)
        rect = rotated_car.get_rect(center=(self.x, self.y))
        screen.blit(rotated_car, rect.topleft)

    def update(self, sensors):
        # Basic AI: if left sensor sees road, turn right; if right sees road, turn left
        if sensors['left'] and not sensors['right']:
            self.angle += 5
        elif sensors['right'] and not sensors['left']:
            self.angle -= 5

        # Move car forward
        rad = math.radians(self.angle)
        self.x += self.speed * math.sin(rad)
        self.y -= self.speed * math.cos(rad)

    def get_sensors(self):
        left_x = int(self.x - 15)
        right_x = int(self.x + 15)
        forward_y = int(self.y - 20)

        try:
            left_color = screen.get_at((left_x, forward_y))[:3]
            right_color = screen.get_at((right_x, forward_y))[:3]
        except IndexError:
            left_color = right_color = (255, 255, 255)

        return {
            'left': left_color == ROAD_COLOR,
            'right': right_color == ROAD_COLOR
        }

# Draw a road
def draw_road():
    screen.fill(WHITE)
    pygame.draw.rect(screen, ROAD_COLOR, pygame.Rect(WIDTH//3, 0, WIDTH//3, HEIGHT))

def main():
    car = Car()
    running = True

    while running:
        clock.tick(30)
        draw_road()
        sensors = car.get_sensors()
        car.update(sensors)
        car.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
