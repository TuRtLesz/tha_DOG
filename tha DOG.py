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
    def __init__(player,spawn_x,spawn_y):
        super().__init__()
        player.image=pygame.image.load('temp.png').convert()
        player.rect=player.image.get_rect()
        player.rect.center=spawn_x,spawn_y
        player.pos=pygame.math.Vector2(player.rect.center)
        player.velocity=pygame.math.Vector2(0,0)
        player.acceleration=pygame.math.Vector2(0,0)
        player.max_velocity=200
        player.state='idle'
        player.hand=''
        player.image_frame=0
        player.run_image_list_right=[]
        player.run_image_list_left=[]
        player.run_image_spritesheet=pygame.image.load('Data/player/player_run.png').convert_alpha()
        for image_x in range(0,2625,125):
            player.import_image=pygame.Surface((125,247),pygame.SRCALPHA)
            player.import_image.blit(player.run_image_spritesheet,(0,0),(image_x,0,125,247))
            player.run_image_list_right.append(player.import_image)
            player.import_image=pygame.transform.flip(player.import_image,True,False)
            player.run_image_list_left.append(player.import_image)
    def update(player,delta_time):
        if player.state=='run_right':
            player.acceleration.x=100
            player.image_frame+=(abs(player.velocity.x)//10)*delta_time#change later?
            if round(player.image_frame)>=len(player.run_image_list_right):
                player.image_frame=5
            player.image=player.run_image_list_right[round(player.image_frame)]
        if player.state=='run_left':
            player.acceleration.x=-100
            player.image_frame+=(abs(player.velocity.x)//10)*delta_time#change later?
            if round(player.image_frame)>=len(player.run_image_list_left):
                player.image_frame=5
            player.image=player.run_image_list_left[round(player.image_frame)]
        if player.velocity.x>=player.max_velocity:
            player.velocity.x=player.max_velocity
        if player.velocity.x<=(-player.max_velocity):
            player.velocity.x=-(player.max_velocity)
        player.velocity+=player.acceleration*delta_time
        player.pos+=player.velocity*delta_time
        player.rect.center=player.pos

class apple(pygame.sprite.Sprite):
    def __init__(apple,pos_x,pos_y):
        apple.image=pygame.image.load('Data/tree/apple.png').convert()
        apple.rect=apple.image.get_rect()
        apple.rect.center=pos_x,pos_y
    def update(apple):
        for player in pygame.sprite.spritecollide(apple,player_sprite_group,dokill=False):
            if player.hand and player.state=='pick'or'jump':    
                player.hand='apple'
                apple.kill()

class camera():
    def __init__(cam):
        cam.offset=pygame.math.Vector2()
    def draw(cam,player_sprite_group,sprite_group_list):
        for player_sprite in player_sprite_group:
            cam.offset.x=player_sprite.rect.centerx-(game_window.get_width()//2)
            game_window.blit(player_sprite.image,(game_window.get_width()//2,game_window.get_height()//2))
        for sprite_group in sprite_group_list:
            for sprite in sprite_group:
                game_window.blit(sprite.image,(sprite.rect.x+cam.offset.x,sprite.rect.y+cam.offset.y))

player_sprite_group=pygame.sprite.Group()
dog_sprite_group=pygame.sprite.Group()
big_fat_guy_sprite_group=pygame.sprite.Group()
block_sprite_group=pygame.sprite.Group()

camera=camera()

prevoius_time=time.perf_counter()

player_sprite_group.add(player(0,300))
while game_mode=='in_game':
    pygame.mouse.set_visible(False)
    delta_time=time.perf_counter()-prevoius_time
    prevoius_time=time.perf_counter()
    display_window.fill((255,255,255))
    game_window.fill((255,255,255))
    player_sprite_group.update(delta_time)
    camera.draw(player_sprite_group,[block_sprite_group,dog_sprite_group,big_fat_guy_sprite_group])
    for player in player_sprite_group:
        print(player.pos,player.acceleration,player.velocity)
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
    #game_window.blit(pygame.image.load('rough.png').convert(),(0,225))#testin
    if game_settings['fullscreen']:
        display_window.blit(game_window,(0,0))
    else:
        display_window.blit(pygame.transform.smoothscale_by(game_window,0.5),(0,0))
    pygame.display.update()
    clock.tick()