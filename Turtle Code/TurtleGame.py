import pygame
import json
import random
import os
from pygame.locals import *

import pygame, os

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()

info = pygame.display.Info() 
screen_width,screen_height = info.current_w,info.current_h

print(info.current_w, info.current_h)

pygame.display.set_caption('Turtle!!!')

score = 0
costume = 1
multiplier = 1
prestige_cost = 250
prestige_level = 1
costume_amount = 1000
turtle_size = ((screen_width / 3.86), (screen_height / 2.16))
can_load = True

costume_list = [1, 2, 3, 4, 5, 6, 7, 8]

last_costume = 1

def get_random_costume():
    global last_costume
    
    while True:
        chosen_costume = random.choice(costume_list)
        if chosen_costume != last_costume:
            last_costume = chosen_costume
            return chosen_costume

def load_turtle_image(costume):
    image_path = f'img/Turtle{costume}.png'
    if os.path.exists(image_path):
        return pygame.image.load(image_path).convert_alpha()
    else:
        print(f"Warning: Costume image '{image_path}' not found!")
        return pygame.Surface(turtle_size)  

with open('data/save.json', 'r') as f:
    game_state = json.load(f)
    score = game_state['score']
    prestige_level = game_state['prestige_level']
    multiplier = game_state['multiplier']
    prestige_cost = game_state['prestige_cost']
    costume = game_state['costume']

screen = pygame.display.set_mode((screen_width, screen_height))
font = pygame.font.SysFont("Arial", 100)
font2 = pygame.font.SysFont("Arial", 40)
start_time = int(pygame.time.get_ticks() / 1500)
clock = pygame.time.Clock()

turtle_img = load_turtle_image(costume)  
turtle = pygame.transform.scale(turtle_img, turtle_size)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_state = {
                'score': score,
                'prestige_level': prestige_level,
                'multiplier': multiplier,
                'prestige_cost': prestige_cost,
                'costume': costume,
            }
            with open('data/save.json', 'w') as f:
                json.dump(game_state, f)
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            score += 1 * multiplier

        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_q]:
            game_state = {
                'score': score,
                'prestige_level': prestige_level,
                'multiplier': multiplier,
                'prestige_cost': prestige_cost,
                'costume': costume,
            }
            with open('data/save.json', 'w') as f:
                json.dump(game_state, f)
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if keys[pygame.K_p]:
                if score >= prestige_cost:
                    prestige_level += 1
                    multiplier += 1
                    score -= prestige_cost
                    prestige_cost = round(prestige_cost * 2.5)
                    game_state = {
                        'score': score,
                        'prestige_level': prestige_level,
                        'multiplier': multiplier,
                        'prestige_cost': prestige_cost,
                        'costume': costume,
                    }
                    with open('data/save.json', 'w') as f:
                        json.dump(game_state, f)

            if keys[pygame.K_c]:
                if score >= costume_amount:
                    score -= costume_amount
                    costume_amount = round(costume_amount * 1.1)
                    costume = get_random_costume()
                    turtle_img = load_turtle_image(costume)
                    turtle = pygame.transform.scale(turtle_img, ((screen_width / 3.86), (screen_height / 2.16)))
                    print(f'New costume: {costume}')
                    
                    game_state = {
                        'score': score,
                        'prestige_level': prestige_level,
                        'multiplier': multiplier,
                        'prestige_cost': prestige_cost,
                        'costume': costume,
                    }
                    with open('data/save.json', 'w') as f:
                        json.dump(game_state, f)

    turtle_surf = turtle
    turtle_rect = turtle_surf.get_rect(center=(screen_width // 2, (screen_height // 1.7)))

    screen.fill((17, 17, 17))

    score_surf = font.render(f'{score}', True, ('Gray'))
    score_rect = score_surf.get_rect(center=(screen_width // 2, (screen_height // 3.35)))

    if score < costume_amount:
        costume_surf = font2.render(f'{costume_amount} Turtles to Randomize Costume!', True, ('White'))
    if score >= costume_amount:
        costume_surf = font2.render(f'Press "C" To Change Costume! (this will cost {costume_amount} Turtles)', True, ('White'))
    costume_rect = costume_surf.get_rect(center=(screen_width // 2, (screen_height // 1.1)))

    if score < prestige_cost:
        prestige_surf = font2.render(f'{prestige_cost} Turtles to Prestige (lvl {prestige_level})', True, ('White'))
    if score >= prestige_cost:
        prestige_surf = font2.render(f'Press "P" to Prestige! (this will cost {prestige_cost} Turtles)', True, ('White'))
    prestige_rect = prestige_surf.get_rect(center=(screen_width // 2, (screen_height // 1.2)))

    screen.blit(score_surf, score_rect)
    screen.blit(turtle_surf, turtle_rect)
    screen.blit(score_surf, score_rect)
    screen.blit(prestige_surf, prestige_rect)
    screen.blit(costume_surf, costume_rect)

    pygame.display.update()
    clock.tick(60)
