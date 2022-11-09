# -*- coding: utf-8 -*-
"""
Dannz Editor

This is a temporary script file.
"""

from tkinter import *
import pygame, sys, random
from fontTools.ttLib import TTFont
from PIL import Image, ImageTk

#Tạo hàm cho trò chơi

pygame.init()
def draw_floor():
    screen.blit(floor,(floor_x_pos,650))
    screen.blit(floor,(floor_x_pos+432,650))
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop =(500,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop =(500,random_pipe_pos-750))
    return bottom_pipe, top_pipe
def move_pipe(pipes):
	for pipe in pipes :
		pipe.centerx -= 5
	return pipes
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600 : 
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rect.top <= -900 or bird_rect.bottom >= 900:
            return False
    return True 
def rotate_bird(bird1):
	new_bird = pygame.transform.rotozoom(bird1,-bird_movement*3,1)
	return new_bird
def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
    return new_bird, new_bird_rect
def score_display(game_state):
    if game_state == 'main game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (216,100))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}',True,(255,255,255))
        score_rect = score_surface.get_rect(center = (216,100))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}',True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (216,630))
        screen.blit(high_score_surface,high_score_rect)
def update_score(score,high_score):
    if score > high_score:
        high_score = score
    return high_score
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)

screen=pygame.display.set_mode((432,768))
pygame.display.set_caption('Flappy Bird')
root=Tk()
root.title('Flappy Bird')
root.geometry("500x600")
root.iconbitmap('icon.ico')

load=Image.open('background.png').convert()
render=ImageTk.PhotoImage(load)
img=Label(root,image=render)
img.place(x=0,y=0)

font = TTFont('C:/Users/TTC/Documents/Code/Code/04B_19.ttf')
name=Label(root,text="Keys uses",fg="#FFFFFF",bd=0,bg="#03152D")
name.config(font=("Transformers Movie",20))
name.pack(pady=10)

name=Label(root,text="Play again: Enter (just run when game over)",fg="#FFFFFF",bd=0,bg="#03152D")
name.config(font=("Transformers Movie",15))
name.pack(pady=15)

name=Label(root,text="Out game: Esc",fg="#FFFFFF",bd=0,bg="#03152D")
name.config(font=("Transformers Movie",15))
name.pack(pady=20)

name=Label(root,text="Fly up: spacebar or arrow up",fg="#FFFFFF",bd=0,bg="#03152D")
name.config(font=("Transformers Movie",15))
name.pack(pady=25)

name=Label(root,text="Fly down: arrow down",fg="#FFFFFF",bd=0,bg="#03152D")
name.config(font=("Transformers Movie",15))
name.pack(pady=30)

name=Label(root,text="Creator, Dev, Designer: Dannz",fg="#FFFFFF",bd=0,bg="#03152D")
name.config(font=("Transformers Movie",10))
name.pack(pady=35)


name=Label(root,text="Flappy Bird",fg="#FFFFFF",bd=0,bg="#03152D")
name.config(font=("04B_19",20))
name.pack(pady=40)

clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf',35)
#Tạo các biến cho trò chơi
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0
#chèn background
bg = pygame.image.load('bkn.png').convert()
bg = pygame.transform.scale2x(bg)
#chèn sàn
floor = pygame.image.load('floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0
#tạo chim
bird_down = pygame.transform.scale2x(pygame.image.load('yellowbird-downflap.png').convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load('yellowbird-midflap.png').convert_alpha())
bird_up = pygame.transform.scale2x(pygame.image.load('yellowbird-upflap.png').convert_alpha())
bird_list= [bird_down,bird_mid,bird_up] #0 1 2
bird_index = 0
bird = bird_list[bird_index]
#bird= pygame.image.load('assets/yellowbird-midflap.png').convert_alpha()
#bird = pygame.transform.scale2x(bird)
bird_rect = bird.get_rect(center = (100,384))

#tạo timer cho bird
birdflap = pygame.USEREVENT + 1
pygame.time.set_timer(birdflap,200)
#tạo ống
pipe_surface = pygame.image.load('pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list =[]
#tạo timer
spawnpipe= pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1200)
pipe_height = [200,300,400]
#Tạo màn hình kết thúc
game_over_surface = pygame.transform.scale2x(pygame.image.load('message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(216,384))
#Chèn âm thanh
flap_sound = pygame.mixer.Sound('5_Flappy_Bird_sound_sfx_wing.wav')
hit_sound = pygame.mixer.Sound('5_Flappy_Bird_sound_sfx_hit.wav')
score_sound = pygame.mixer.Sound('5_Flappy_Bird_sound_sfx_point.wav')
score_sound_countdown = 100
#while loop của trò chơi
while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_active:
                    bird_movement = 0
                    bird_movement =-11
                    flap_sound.play()
                if event.key == pygame.K_DOWN and game_active:
                    bird_movement = 0
                if event.key == pygame.K_UP and game_active:
                    bird_movement =-11
                if event.key == pygame.K_RETURN and game_active==False:
                    game_active = True 
                    pipe_list.clear()
                    bird_rect.center = (100,384)
                    bird_movement = 0 
                    score = 0 

                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                       pygame.event.post(pygame.event.Event(pygame.QUIT))
 
            if event.type == spawnpipe:
                pipe_list.extend(create_pipe())
            if event.type == birdflap:
                if bird_index < 2:
                    bird_index += 1
                else:
                    bird_index =0 
                bird, bird_rect = bird_animation()    
                
        screen.blit(bg,(0,0))
        if game_active:
            #chim
            bird_movement += gravity
            rotated_bird = rotate_bird(bird)       
            bird_rect.centery += bird_movement
            screen.blit(rotated_bird,bird_rect)
            game_active= check_collision(pipe_list)
            #ống
            pipe_list = move_pipe(pipe_list)
            draw_pipe(pipe_list)
            score += 0.01
            score_display('main game')
            score_sound_countdown -= 1
            if score_sound_countdown <= 0:
                score_sound.play()
                score_sound_countdown = 100
        else:
            screen.blit(game_over_surface,game_over_rect)
            high_score = update_score(score,high_score)
            score_display('game_over')
        #sàn
        floor_x_pos -= 1
        draw_floor()
        if floor_x_pos <= -432:
            floor_x_pos =0
        
        pygame.display.update()

        clock.tick(120)

        pygame.display.flip()