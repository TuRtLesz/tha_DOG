import pygame,sys,time,random
pygame.init()
display_size=[pygame.display.Info().current_w,pygame.display.Info().current_h]
game_window=pygame.Surface((display_size[0],display_size[1]))
display_window=pygame.display.set_mode((display_size[0]//2,display_size[1]//2))
pygame.display.set_caption('tha_DOG')
pygame.display.set_icon(pygame.image.load('Data/icon/DOG.png').convert())
clock=pygame.time.Clock()
game_mode='in_game'
game_settings={'fullscreen':False}

class player(pygame.sprite.Sprite):
    def __init__(player):
        super().__init__()
        player.image=pygame.image.load('temp.png').convert()
        player.rect=player.image.get_rect()
        player.pos=pygame.math.Vector2(player.rect.center)
        player.velocity=pygame.math.Vector2(0,0)
        player.acceleration=pygame.math.Vector2(0,0)
        player.max_velocity=70
        player.state='idle'
    def update(player,delta_time):
        if player.state=='run_right':
            player.acceleration.x=30
        if player.state=='run_left':
            player.acceleration.x=-30
        if player.velocity.x>player.max_velocity:
            player.velocity.x=player.max_velocity
        if player.velocity.x<-player.max_velocity:
            player.velocity.x=-(player.max_velocity)
        player.velocity+=player.acceleration*delta_time
        player.pos+=player.velocity*delta_time
        player.rect.center=player.pos

player_sprite_group=pygame.sprite.Group()
dog_sprite_group=pygame.sprite.Group()
big_fat_guy_sprite_group=pygame.sprite.Group()
block_sprite_group=pygame.sprite.Group()
prevoius_time=time.perf_counter()

player_sprite_group.add(player())
while game_mode=='in_game':
    delta_time=time.perf_counter()-prevoius_time
    prevoius_time=time.perf_counter()
    display_window.fill((255,255,255))
    game_window.fill((255,255,255))
    player_sprite_group.update(delta_time)
    player_sprite_group.draw(game_window)
    keys_pressed=pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_F11:
                if game_settings['fullscreen']==True:
                    display_window=pygame.display.set_mode((display_size[0]//2,display_size[1]//2))
                    game_settings['fullscreen']=False
                elif game_settings['fullscreen']==False:
                    display_window=pygame.display.set_mode((display_size[0],display_size[1]),pygame.FULLSCREEN|pygame.SCALED)
                    game_settings['fullscreen']=True
            if event.key==pygame.K_ESCAPE:
                if game_settings['fullscreen']==True:
                    display_window=pygame.display.set_mode((display_size[0]//2,display_size[1]//2))
                    game_settings['fullscreen']=False
    for player in player_sprite_group:
        if keys_pressed[pygame.K_d]:
            player.state='run_right'
        if keys_pressed[pygame.K_a]:
            player.state='run_left'
        if keys_pressed[pygame.K_w]:
            player.state='jump'
            if keys_pressed[pygame.K_d]:
                player.state='jump_right'
            elif keys_pressed[pygame.K_a]:
                player.state='jump_left'
        if keys_pressed[pygame.K_SPACE]:
            player.state='throw'
        if keys_pressed[pygame.K_s]:
            player.state='pick'
    game_window.blit(pygame.image.load('rough.png').convert(),(0,450))#testin
    if game_settings['fullscreen']:
        display_window.blit(game_window,(0,0))
    else:
        display_window.blit(pygame.transform.smoothscale_by(game_window,0.5),(0,0))
    pygame.display.update()
    clock.tick()