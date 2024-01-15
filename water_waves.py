import pygame
from pygame.locals import *
# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 400
CAPTION = "Waves Simulation with Pygame"
BLUE = (0, 103, 247)
WHITE = (255, 255, 255)





screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(CAPTION)
clock = pygame.time.Clock()  


class water_spring:
    tension = 0.025
    dampening = 0.020
    spread = 0.25
    def __init__(water_spring_instance, x, target_height):
        water_spring_instance.x = x
        water_spring_instance.y = 0
        water_spring_instance.speed = 0
        water_spring_instance.height = target_height
        water_spring_instance.target_height=target_height
        water_spring_instance.bottom = 400
    def update(water_spring_instance):
        water_spring_instance.y = water_spring_instance.target_height - water_spring_instance.height
        water_spring_instance.speed += water_spring.tension * water_spring_instance.y - water_spring_instance.speed * water_spring.dampening
        water_spring_instance.height += water_spring_instance.speed

# Max wave height and stable point
target_height = 200
# First position
init_position_x = 0
# Second position
final_position_x = 1000

water_spring_list = []

"""Create the water_spring list"""
for x in range(init_position_x, final_position_x, 2):
    water_spring_list.append(water_spring(x, target_height))


        



def wave_update():
    for water_spring in water_spring_list:
        water_spring.update()
    lDeltas = list(water_spring_list)
    rDeltas = list(water_spring_list)
    for j in range(5):# Number of loop round // Warning with a too hight value on this variable, the script will be very slower
        for i in range(len(water_spring_list)): 
            if i > 0:
                lDeltas[i] = water_spring.spread * (water_spring_list[i].height - water_spring_list[i - 1].height)
                water_spring_list[i - 1].speed += lDeltas[i]
            if i < len(water_spring_list) - 1:
                rDeltas[i] = water_spring.spread * (water_spring_list[i].height - water_spring_list[i + 1].height)
                water_spring_list[i + 1].speed += rDeltas[i]
        for i in range(len(water_spring_list)):
            if i > 0:
                water_spring_list[i - 1].height += lDeltas[i]
            if i < len(water_spring_list) - 1:
                water_spring_list[i + 1].height += rDeltas[i]
    count = 0
    for i in range(len(water_spring_list)):
        if not int(water_spring_list[i].speed) and not int(water_spring_list[i].y):
            count += 1
    if count == len(water_spring_list):
        for i in range(len(water_spring_list)):
            water_spring_list[i].speed = 0
            water_spring_list[i].height = water_spring_list[i].target_height
            water_spring_list[i].y = 0 

     
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == MOUSEBUTTONUP:



            #if counter.done == True:
            pos = pygame.mouse.get_pos()
            water_spring_list[int(pos[0] / final_position_x * (abs(int((init_position_x - final_position_x) / 2))))].speed = 200
            


    screen.fill(WHITE)
    wave_update()

    for water_spring in water_spring_list:
        pygame.draw.line(screen, BLUE, (water_spring.x, water_spring.height), (water_spring.x, water_spring.height), 2)

    #water_spring_last_pos=[0,0]
    #for water_spring in water_spring_list:
    #    if water_spring.x-water_spring_last_pos[0]<16:#change number later
    #        pygame.draw.line(screen, BLUE, (water_spring.x, water_spring.height), (water_spring.x, water_spring.height), 2)
    #        water_spring_last_pos[0]=water_spring.x
    #        water_spring_last_pos[1]=water_spring.height
    #    else:
    #        water_spring_last_pos[0]=water_spring.x
    #        water_spring_last_pos[1]=water_spring.height
        
    clock.tick(60)
    pygame.display.flip()   