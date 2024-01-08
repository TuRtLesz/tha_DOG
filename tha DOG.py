import pygame,sys,time,csv,numpy
pygame.init()
pygame.mixer.init()
display_size=[pygame.display.Info().current_w,pygame.display.Info().current_h]
game_window=pygame.Surface((display_size[0],display_size[1]))
display_window=pygame.display.set_mode((display_size[0]//2,display_size[1]//2))
pygame.display.set_caption('tha_DOG')
pygame.display.set_icon(pygame.image.load('Data/icon/DOG.png').convert())
clock=pygame.time.Clock()

save_data={'high_score':0}#add lsat check point?

game_settings={'fullscreen':False,'negative_screen':False,'mode':'game_complete'}

def load_spritesheet(spritesheet_image,sprite_list,frames=2,alpha_sur=True,image_scale=1):
    sprite_list.clear()
    for image_x in range(0,spritesheet_image.get_width(),spritesheet_image.get_width()//frames):
        if alpha_sur:
            sprite_image=pygame.Surface((spritesheet_image.get_width()//frames,spritesheet_image.get_height()),pygame.SRCALPHA)
        else:
            sprite_image=pygame.Surface((spritesheet_image.get_width()//frames,spritesheet_image.get_height()))
        sprite_image.blit(spritesheet_image,(0,0),(image_x,0,sprite_image.get_width(),sprite_image.get_height()))
        if image_scale!=1:
            sprite_image=pygame.transform.scale_by(sprite_image,image_scale)
        sprite_list.append(sprite_image)
    return sprite_list
def load_spritesheet_2dir(spritesheet_image,sprite_list,sprite_list_fliped,frames=2,image_scale=1,alpha_sur=True):
    sprite_list.clear()
    sprite_list_fliped.clear()
    for image_x in range(0,spritesheet_image.get_width(),spritesheet_image.get_width()//frames):
        if alpha_sur:
            sprite_image=pygame.Surface((spritesheet_image.get_width()//frames,spritesheet_image.get_height()),pygame.SRCALPHA)
        else:
            sprite_image=pygame.Surface((spritesheet_image.get_width()//frames,spritesheet_image.get_height()))
        sprite_image.blit(spritesheet_image,(0,0),(image_x,0,sprite_image.get_width(),sprite_image.get_height()))
        if image_scale!=1:
            sprite_image=pygame.transform.scale_by(sprite_image,image_scale)
        sprite_list.append(sprite_image)
        sprite_list_fliped.append(pygame.transform.flip(sprite_image,True,False))
    return sprite_list,sprite_list_fliped

menu_image_frame=0
exit_image=pygame.image.load('Data/menu_buttons/exit.png').convert()
exit_image=pygame.transform.scale2x(exit_image)
game_over_image=pygame.image.load('Data/menu_buttons/game_over.png').convert()
game_over_image=pygame.transform.scale2x(game_over_image)
paused_image=pygame.image.load('Data/menu_buttons/paused.png').convert()
paused_image=pygame.transform.scale2x(paused_image)
high_score_image=pygame.image.load('Data/menu_buttons/high_score.png').convert_alpha()
score_image=pygame.Surface((72,28),pygame.SRCALPHA)
score_image.blit(high_score_image,(0,0),(62,0,72,28))
exit_game_complete_list=[]
game_complete_list=[]
play_list=[]
retry_list=[]
replay_list=[]
cookie_list=[]
cookie_image_frame=0
load_spritesheet(pygame.image.load('Data/menu_buttons/exit_game_complete.png').convert(),exit_game_complete_list,alpha_sur=False,image_scale=2)
load_spritesheet(pygame.image.load('Data/menu_buttons/replay.png').convert(),replay_list,alpha_sur=False,image_scale=2)
load_spritesheet(pygame.image.load('Data/menu_buttons/retry.png').convert(),retry_list,alpha_sur=False,image_scale=2)
load_spritesheet(pygame.image.load('Data/menu_buttons/play.png').convert(),play_list,alpha_sur=False,image_scale=2)
load_spritesheet(pygame.image.load('Data/menu_buttons/game_complete.png').convert(),game_complete_list,alpha_sur=False,image_scale=3)
load_spritesheet(pygame.image.load('Data/menu_buttons/cookie.png').convert(),cookie_list,frames=7,alpha_sur=False,image_scale=2)
exit_rect=exit_image.get_rect(topleft=(display_size[0]//2-exit_image.get_width()//2,display_size[1]-200))
exit_game_complete_rect=exit_game_complete_list[1].get_rect(topleft=(display_size[0]//2+(200+exit_game_complete_list[0].get_width()//2),display_size[1]-200))
cookie_rect=cookie_list[0].get_rect(topleft=(display_size[0]//2-(retry_list[1].get_width()//2),100+game_complete_list[0].get_height()))
play_rect=play_list[1].get_rect(topleft=(display_size[0]//2-(retry_list[1].get_width()//2),display_size[1]//2-retry_list[1].get_height()//2))
retry_rect=retry_list[1].get_rect(topleft=(display_size[0]//2-(retry_list[1].get_width()//2),display_size[1]//2-retry_list[1].get_height()//2))
replay_rect=replay_list[0].get_rect(topleft=(display_size[0]//2-(200+replay_list[0].get_width()//2),display_size[1]-200))
new_life_image_list=[]
life_death_image_list=[]
load_spritesheet(pygame.image.load('Data/life/new_life.png').convert_alpha(),new_life_image_list,5,image_scale=2)
load_spritesheet(pygame.image.load('Data/life/life_death.png').convert_alpha(),life_death_image_list,6,image_scale=2)

def text(text,color,size,text_pos):
        font=pygame.font.Font('Data/font/font.ttf',int(size))
        text_data=font.render(text,False,color)
        game_window.blit(text_data,text_pos)

class player(pygame.sprite.Sprite):
    def __init__(player,spawn_x,spawn_y):
        super().__init__()
        player.fat_guy_pan=0
        player.score=0
        player.velocity=pygame.math.Vector2(0,0)
        player.acceleration=pygame.math.Vector2(0,0)
        player.max_velocity=pygame.math.Vector2(200,5000)
        player.life=40#change later
        player.life_image_frame=0
        player.prev_life=player.life
        player.explode_timer=0
        player.stamina=1000
        player.state='idle'
        player.throw_angle=0
        player.throw_power=150
        player.idle_timer=0
        player.water=False
        player.jump=False
        player.jump_counter=0
        player.direction='right'
        player.hand=''
        player.dog_collide=False
        player.jump_height=spawn_y
        player.prev_flower_count=0
        player.flower_count=0
        player.flower_timer=2
        player.image_frame=0
        player.run_image_list_right=[]
        player.run_image_list_left=[]
        player.swim_image_list_right=[]
        player.swim_image_list_left=[]
        player.pant_image_list_right=[]
        player.pant_image_list_left=[]
        player.jump_image_list_right=[]
        player.jump_image_list_left=[]
        player.throw_image_list_right=[]
        player.throw_image_list_left=[]
        player.dodge_image_list_right=[]
        player.dodge_image_list_left=[]
        player.explode_image_list_right=[]
        player.explode_image_list_left=[]
        load_spritesheet_2dir(pygame.image.load('Data/player/player_run.png').convert_alpha(),player.run_image_list_right,player.run_image_list_left,frames=21)
        load_spritesheet_2dir(pygame.image.load('Data/player/player_swim.png').convert_alpha(),player.swim_image_list_right,player.swim_image_list_left,frames=17)
        load_spritesheet_2dir(pygame.image.load('Data/player/player_pant.png').convert_alpha(),player.pant_image_list_right,player.pant_image_list_left,frames=7)
        load_spritesheet_2dir(pygame.image.load('Data/player/player_jump.png').convert_alpha(),player.jump_image_list_right,player.jump_image_list_left,frames=11)
        load_spritesheet_2dir(pygame.image.load('Data/player/player_throw.png').convert_alpha(),player.throw_image_list_right,player.throw_image_list_left,frames=7)
        load_spritesheet_2dir(pygame.image.load('Data/player/player_dodge.png').convert_alpha(),player.dodge_image_list_right,player.dodge_image_list_left,frames=14)
        load_spritesheet_2dir(pygame.image.load('Data/player/player_explode.png').convert_alpha(),player.explode_image_list_right,player.explode_image_list_left,frames=7)
        player.image=player.run_image_list_right[0]
        player.rect=player.image.get_rect()
        player.rect.center=spawn_x,spawn_y
        player.mask=pygame.mask.from_surface(player.image)
        player.pos=pygame.math.Vector2(player.rect.center)
        player.rock_throw_sound=pygame.mixer.Sound('Data/player/rock_throw.wav')
    def update(player,delta_time):#player states- explode run sprint swim swim_fast pick interact aim throw 
        for check_point in check_point_list:
            if player.pos.x>=check_point.right:
                player.last_check_point=check_point
        player.water=False
        for water_rect in water_blocks_rect_list:
            if not player.water:
                if player.rect.colliderect(water_rect):
                    player.water=True
            else:
                break
        for dog in pygame.sprite.spritecollide(player,dog_sprite_group,dokill=False,collided=pygame.sprite.collide_mask):
            if not player.dog_collide:
                if player.state!='grass' and player.state!='dodge' and dog.state!='bite' and dog.stun_timer<=0:
                    player.life-=1
                    player.score-=250
                    player.velocity.xy=0,0
                    player.state='idle'
                    dog.bite_timer=3
                    dog.image_frame=0
                else:
                    if player.state=='dodge':
                        player.score+=500
                player.dog_collide=True
        if player.stamina<1000 and not player.water:
                if player.state=='idle' and not player.jump:
                    player.state='pant'
                    player.image_frame=0
        elif player.stamina>=1000:
            player.stamina=1000
            if player.state=='pant':
                player.state='idle'
        if player.state=='idle':
            player.idle_timer+=delta_time
            if not player.jump:
                player.image_frame=0
            if player.direction=='right':
                player.image=player.run_image_list_right[0]
            elif player.direction=='left':
                player.image=player.run_image_list_left[0]
        if player.state!='pant'and player.state!='aim' and player.state!='throw' and player.state!='idle' and player.state!='pick':
            player.idle_timer=0
        if player.state=='explode':
            player.velocity.x=0
            player.stamina+=200*delta_time
            if player.image_frame>=len(player.explode_image_list_left)-1:
                player.image_frame=len(player.explode_image_list_left)-1
                if player.explode_timer>1:
                    player.state='idle'
                    player.explode_timer=0
                else:
                    player.explode_timer+=delta_time
            if player.direction=='right':
                player.image=player.explode_image_list_right[round(player.image_frame)]
            elif player.direction=='left':
                player.image=player.explode_image_list_left[round(player.image_frame)]
            player.image_frame+=10*delta_time
        if player.state=='grass':player.stamina+=200*delta_time
        if player.state=='dodge':
            if int(player.image_frame)>=len(player.dodge_image_list_left)-1:
                player.state='run'
                player.stamina-=100
                player.image_frame=0
                player.dodge=False
                player.dog_collide=False
                if player.direction=='left':
                    player.rect.x-=12
                else:
                    player.rect.x+=12
                player.pos.xy=player.rect.center
            if player.direction=='left':
                player.velocity.x=-550
                player.image=player.dodge_image_list_left[int(player.image_frame)]
            elif player.direction=='right':
                player.velocity.x=550
                player.image=player.dodge_image_list_right[int(player.image_frame)]
            player.image_frame+=10*delta_time
        if player.state=='pant':
            player.idle_timer+=delta_time
            player.stamina+=200*delta_time
            if player.image_frame>=len(player.pant_image_list_left)-1:
                player.image_frame=len(player.pant_image_list_left)-1
            if player.direction=='right':
                player.image=player.pant_image_list_right[round(player.image_frame)]
            elif player.direction=='left':
                player.image=player.pant_image_list_left[round(player.image_frame)]
            player.image_frame+=10*delta_time
        elif player.state=='aim':
            print(player.throw_angle,player.throw_power)
            player.idle_timer+=delta_time
            if player.image_frame>=3:
                player.image_frame=3
            if player.direction=='left':
                player.image=player.throw_image_list_left[int(player.image_frame)]
            elif player.direction=='right':
                player.image=player.throw_image_list_right[int(player.image_frame)]
            player.image_frame+=5*delta_time
            if player.throw_angle>=45:
                player.throw_angle=45
                player.throw_power+=40*delta_time
            else:
                if player.throw_power>=300:
                    player.throw_angle+=10*delta_time
                else:
                    player.throw_power+=100*delta_time
            player.arc_eq_a=numpy.tan(numpy.deg2rad(player.throw_angle))
            player.arc_eq_b=250/((numpy.cos(numpy.deg2rad(player.throw_angle)**2)*(player.throw_power**2)))
            if player.direction=='right':
                for x in range(0,300,10):#change later
                    pygame.draw.line(game_window,(0,0,0),(x-game.player_offset.x+(display_size[0]//2)+50,550-player.arc_eq_a*x+player.arc_eq_b*x**2-game.player_offset.y),(x+5-game.player_offset.x+(display_size[0]//2)+50,550-player.arc_eq_a*x+player.arc_eq_b*(x+5)**2-game.player_offset.y))
            elif player.direction=='left':
                for x in range(0,300,10):
                    pygame.draw.line(game_window,(0,0,0),(game.player_offset.x+(display_size[0]//2)-50-x,550-player.arc_eq_a*x+player.arc_eq_b*x**2-game.player_offset.y),(game.player_offset.x+(display_size[0]//2)-50-x-5,550-player.arc_eq_a*x+player.arc_eq_b*(x+5)**2-game.player_offset.y))
        elif player.state=='throw':
            player.idle_timer+=delta_time
            if player.image_frame>len(player.throw_image_list_left):
                if player.direction=='left':
                    player.rock_obj=little_rock(player.rect.left+19,player.rect.top+28)
                else:
                    player.rock_obj=little_rock(player.rect.right-19,player.rect.top+28)
                player.hand=''
                player.rock_obj.velocity.from_polar((player.throw_power,player.throw_angle))
                player.throw_angle,player.throw_power=0,150
                player.rock_obj.velocity.y=-player.rock_obj.velocity.y
                if player.direction=='left':
                    player.rock_obj.velocity.x=-player.rock_obj.velocity.x
                player.rock_obj.acceleration.y=300
                player.rock_obj.initial_velocity=player.rock_obj.velocity
                print(player.rock_obj.velocity)
                reactive_block_sprite_group.add(player.rock_obj)
                player.state='idle'
                player.rock_throw_sound.play()
            else:
                if player.direction=='left':
                    player.image=player.throw_image_list_left[int(player.image_frame)]
                elif player.direction=='right':
                    player.image=player.throw_image_list_right[int(player.image_frame)]
                player.image_frame+=10*delta_time
        elif player.state=='run':
            player.max_velocity.x=200
            player.image_frame+=(abs(player.velocity.x)//10)*delta_time
            if round(player.image_frame)>=len(player.run_image_list_right)-1:
                player.image_frame=5
            if player.direction=='right':    
                player.acceleration.x=50
                player.image=player.run_image_list_right[round(player.image_frame)]
            elif player.direction=='left':
                player.acceleration.x=-50
                player.image=player.run_image_list_left[round(player.image_frame)]
        elif player.state=='sprint':
            player.max_velocity.x=350
            player.stamina-=100*delta_time
            player.image_frame+=(abs(player.velocity.x)//10)*delta_time
            if round(player.image_frame)>=len(player.run_image_list_right)-1:
                player.image_frame=5
            if player.direction=='right':
                player.acceleration.x=100
                player.image=player.run_image_list_right[round(player.image_frame)]
            elif player.direction=='left':
                player.acceleration.x=-100
                player.image=player.run_image_list_left[round(player.image_frame)]
        elif player.state=='swim_fast':
            if player.stamina<=0:
                player.state='swim'
            else:
                player.max_velocity.x=300
                player.stamina-=150*delta_time
                player.image_frame+=15*delta_time#change later?
                if round(player.image_frame)>=len(player.swim_image_list_right)-1:
                    player.image_frame=6
                if player.direction=='right':
                    player.acceleration.x=100
                    player.image=player.swim_image_list_right[round(player.image_frame)]
                elif player.direction=='left':
                    player.acceleration.x=-100
                    player.image=player.swim_image_list_left[round(player.image_frame)]
        if player.state=='swim':
            player.max_velocity.x=150
            player.image_frame+=10*delta_time
            if round(player.image_frame)>=len(player.swim_image_list_right)-1:
                player.image_frame=6
            if player.direction=='right':    
                player.acceleration.x=50
                player.image=player.swim_image_list_right[round(player.image_frame)]
            elif player.direction=='left':
                player.acceleration.x=-50
                player.image=player.swim_image_list_left[round(player.image_frame)]
        if player.velocity.x>=player.max_velocity.x:
            player.velocity.x=player.max_velocity.x
        if player.velocity.x<=(-player.max_velocity.x):
            player.velocity.x=-(player.max_velocity.x)
        #if player.velocity.y>=player.max_velocity.y:
        #    player.velocity.y=player.max_velocity.y
        if player.stamina<=0:
            player.stamina=0
        if player.state!='idle'and player.state!='pant' and player.state!='interact' and player.state!='fall' and player.state!='aim' and player.state!='throw' and player.state!='explode' and player.state!='pick' and player.state!='grass':
            player.velocity+=player.acceleration*delta_time
            player.pos+=player.velocity*delta_time
            player.rect=player.image.get_rect(center=player.pos.xy)
            player.mask=pygame.mask.from_surface(player.image)
        else:
            if player.state!='pick':
                player.velocity.x=0
        if not player.jump or abs(player.pos.y-player.jump_height)>=150:
            player.jump_counter+=1
            if player.water or player.state=='swim' or player.state=='siwm_fast':
                player.pos.y+=5*delta_time
                player.rect.center=player.pos
                player.jump=False
            else:
                player.pos.y+=400*delta_time
                player.rect.center=player.pos
                player.jump=False
        for block in pygame.sprite.spritecollide(player,block_sprite_instance_group,dokill=False):
            player.jump_height=player.pos.y
            player.jump_counter=0
            game.draw_rect.centery=player.jump_height-300#?
            if block.id=='0' or block.id=='1' or block.id=='2' or block.id=='64' or block.id=='65' or block.id == '66' or block.id == '116' or block.id == '117' or block.id == '118':
                player.rect.bottom=block.rect.top
            elif block.id=='68':
                if block.rect.x<player.rect.x:
                    player.rect.left=block.rect.right
                elif block.rect.x>player.rect.x:
                    player.rect.right=block.rect.left
                player.rect.bottom=block.rect.top
            elif block.id=='10':
                player.rect.bottom=block.rect.top+4
            elif block.id=='12':
                player.rect.bottom=block.rect.top+30
            elif block.id=='13':
                player.rect.bottom=block.rect.top+30
            elif block.id=='70':
                player.rect.bottom=block.rect.top
            elif block.id=='3':#ramps
                player.rect.bottom=round(0.3488603*(block.rect.x-player.pos.x))+block.rect.bottom-52#ramp_up
            elif block.id=='4':
                player.rect.bottom=round(0.3488603*(block.rect.x-player.pos.x))+block.rect.bottom-37
            elif block.id=='5':
                player.rect.bottom=round(0.3488603*(block.rect.x-player.pos.x))+block.rect.bottom-22
            elif block.id=='92':
                player.rect.bottom=16-(round(0.3488603*abs(player.pos.x-block.rect.x)))+block.rect.bottom-52#ramp_down
            elif block.id=='93':
                player.rect.bottom=16-(round(0.3488603*abs(player.pos.x-block.rect.x)))+block.rect.bottom-37
            elif block.id=='94':
                player.rect.bottom=16-(round(0.3488603*abs(player.pos.x-block.rect.x)))+block.rect.bottom-22
            #rock
            elif block.id=='35' or block.id=='87':
                if block.rect.collidepoint(player.rect.centerx,player.rect.centery+85) and player.direction=='right':
                    player.rect.right=block.rect.left+53
                    player.velocity.xy=0,0
                    player.state='idle'
            elif block.id=='37' or block.id=='91':
                if block.rect.collidepoint(player.rect.centerx,player.rect.centery+85) and player.direction=='left':
                    player.rect.left=block.rect.right-53
                    player.velocity.xy=0,0
                    player.state='idle'
            elif block.id=='7' or block.id=='59':
                if block.rect.collidepoint(player.rect.centerx,player.rect.bottom):
                    player.rect.bottom=block.rect.top+26
            elif block.id == '6' or block.id == '58':#top curve right
                if player.pos.x-block.rect.x>18:
                    player.rect.bottom=block.rect.top+26
                    #player.rect.bottom=round(1.320033*(player.pos.x-block.rect.x)-(0.0099421*((player.pos.x-block.rect.x)**2)))+block.rect.bottom-26
            elif block.id == '8':#top curve left
                if player.pos.x-block.rect.x<=23:
                    player.rect.bottom=block.rect.top+26
                    #player.rect.bottom= 21-round(0.8659639*(player.pos.x-block.rect.x))+block.rect.bottom-26
            #elif block.id == '35':#sideleft
            #    if pygame.sprite.collide_mask(player,block):
            #        if player.rect.bottom!=block.rect.bottom+1:
            #            print('test')
            #            player.rect.bottom= 48-(1.743497*(player.pos.x-block.rect.x))+block.rect.bottom
            #        else:
            #            if player.state=='run_right':
            #                player.rect.right=block.rect.left+48
            #elif block.id == '37':#side right
            #    if player.pos.x-block.rect.x>23:
            #        player.rect.bottom= -1.145418*(player.pos.x-block.rect.x) + 26.91235+block.rect.bottom
            player.pos.xy=player.rect.center
        if player.jump:
            if abs(player.pos.y-player.jump_height)<150:
                if player.jump_counter<=0:
                    player.image_frame+=5*delta_time
                    if round(player.image_frame)>=len(player.jump_image_list_right)-1:
                        player.image_frame=len(player.jump_image_list_right)-1
                    if player.direction=='right':  
                        player.image=player.jump_image_list_right[round(player.image_frame)]
                    elif player.direction=='left':  
                        player.image=player.jump_image_list_left[round(player.image_frame)] 
                    player.stamina-=50*delta_time
                    player.pos.y-=300*delta_time
                    if player.velocity.x<100 and player.direction=='right':
                        player.velocity.x=150
                    elif player.velocity.x<-100 and player.direction=='left':
                        player.velocity.x=-150
                    player.rect.center=player.pos
                else:
                    player.jump=False
        for water_line in water_hitlines:
            if player.rect.clipline(water_line)!=():
                if player.state=='run' or player.state=='sprint':
                    if numpy.random.randint(0,7)==1:
                        bubble_sprite_group.add(bubble(numpy.random.randint(player.rect.x,player.rect.x+player.image.get_width()),numpy.random.randint(water_line[1][1],player.rect.bottom),round(numpy.random.uniform(0.1,1.5),ndigits=1)))


                #add waves hereee

class dog(pygame.sprite.Sprite):
    dog_run_image_list_right=[]
    dog_run_image_list_left=[]
    dog_death_image_list_right=[]
    dog_death_image_list_left=[]
    dog_bite_image_list_right=[]
    dog_bite_image_list_left=[]
    load_spritesheet_2dir(pygame.image.load('Data/dog/dog_run.png').convert_alpha(),dog_run_image_list_left,dog_run_image_list_right,21)
    load_spritesheet_2dir(pygame.image.load('Data/dog/dog_death.png').convert_alpha(),dog_death_image_list_left,dog_death_image_list_right,5)
    load_spritesheet_2dir(pygame.image.load('Data/dog/dog_bite.png').convert_alpha(),dog_bite_image_list_left,dog_bite_image_list_right,4)
    tut_end=0
    def __init__(dog_instance,x,y):
        super().__init__()
        dog_instance.velocity=pygame.math.Vector2(0,0)
        dog_instance.acceleration=pygame.math.Vector2(0,100)
        dog_instance.max_velocity=pygame.math.Vector2(250,100)
        dog_instance.life=3
        dog_instance.state='idle'
        dog_instance.direction='right'
        dog_instance.prev_direction=dog_instance.direction
        dog_instance.dodge_counter=3
        dog_instance.player_collide=False
        dog_instance.image_frame=0
        dog_instance.image=dog.dog_run_image_list_right[0]
        dog_instance.rect=dog_instance.image.get_rect(topleft=(x*48,y*48-16))
        dog_instance.pos=pygame.math.Vector2(dog_instance.rect.center)
        dog_instance.mask=pygame.mask.from_surface(dog_instance.image)
        dog_instance.stun_timer=0
        dog_instance.bite_timer=0
    def update(dog_instance,delta_time):
        if dog_instance.pos.x<dog.tut_end:#tutoiral side
            dog_instance.max_velocity.x=150
        else:
            dog_instance.max_velocity.x=250
        if dog_instance.life<=0:
            dog_instance.state='dead'
        if dog_instance.state!='dead':
            if dog_instance.bite_timer<=0:
                if dog_instance.stun_timer<=0:
                    for water_rect in water_blocks_rect_list:
                        if dog_instance.state!='swim':
                            if dog_instance.rect.colliderect(water_rect):
                                for bomb_rect in bomb_rect_list:
                                    if bomb_rect.x<dog_instance.rect.centerx<bomb_rect.right:
                                        for reactive_block in reactive_block_sprite_instance_group:
                                            if bomb_rect.colliderect(reactive_block) and type(reactive_block)==bomb and reactive_block.explode:
                                                dog_instance.life=0
                                                dog_instance.image_frame=0
                                if dog_instance.state!='idle':
                                    dog_instance.state='swim'
                        else:
                            break
                    if dog_instance.state=='swim' or dog_instance.state=='run':
                        if dog_instance.prev_direction!=dog_instance.direction:#reducing drag while switching dirtections
                            if dog_instance.prev_direction=='right':
                                dog_instance.velocity.x=100
                            elif dog_instance.prev_direction=='left':
                                dog_instance.velocity.x=-100
                            dog_instance.prev_direction=dog_instance.direction
                    for player in player_sprite_group:
                        if player.state!='grass':
                            if dog_instance.state!='stomp_rat' or dog_instance.state!='chase_rat':
                                dog_instance.state='run'
                            if player.rect.x-dog_instance.rect.centerx<0:
                                dog_instance.direction='left'
                            elif player.rect.x-dog_instance.rect.centerx>0:
                                dog_instance.direction='right'
                    for rat in pygame.sprite.spritecollide(dog_instance,rat_sprite_group,dokill=False,collided=pygame.sprite.collide_circle):
                        dog_instance.state='chase_rat'
                        if rat.pos.x-dog_instance.pos.x>0:
                            dog_instance.direction='right'
                        elif rat.pos.x-dog_instance.pos.x<0:
                            dog_instance.direction='left'
                        if rat.rect.colliderect(dog_instance.rect):
                            if not rat.dead:
                                rat.dead=True
                                rat.frame=0
                                dog_instance.state='stomp_rat'
                    if dog_instance.state=='run':
                        dog_instance.max_velocity.y=100
                        dog_instance.image_frame+=10*delta_time
                        if dog_instance.image_frame>=len(dog_instance.dog_run_image_list_left)-1:
                            dog_instance.image_frame=12
                        if dog_instance.direction=='right':
                            dog_instance.acceleration.x=100
                            dog_instance.image=dog_instance.dog_run_image_list_right[round(dog_instance.image_frame)]
                        elif dog_instance.direction=='left':
                            dog_instance.acceleration.x=-100
                            dog_instance.image=dog_instance.dog_run_image_list_left[round(dog_instance.image_frame)]
                    elif dog_instance.state=='swim' or dog_instance.state=='chase_rat':
                        dog_instance.velocity.y=0
                        dog_instance.image_frame+=15*delta_time
                        if dog_instance.image_frame>=11:
                            dog_instance.image_frame=0
                        if dog_instance.direction=='right':
                            dog_instance.acceleration.x=80
                            dog_instance.image=dog_instance.dog_run_image_list_right[round(dog_instance.image_frame)]
                        elif dog_instance.direction=='left':
                            dog_instance.acceleration.x=-80
                            dog_instance.image=dog_instance.dog_run_image_list_left[round(dog_instance.image_frame)]
                    elif dog_instance.state=='stop_rat':
                        dog_instance.state='idle'#edit later
                    dog_instance.mask=pygame.mask.from_surface(dog_instance.image)
                    if dog_instance.velocity.x>=dog_instance.max_velocity.x:
                        dog_instance.velocity.x=dog_instance.max_velocity.x
                    if dog_instance.velocity.x<=(-dog_instance.max_velocity.x):
                        dog_instance.velocity.x=-(dog_instance.max_velocity.x)
                    if dog_instance.velocity.y>=dog_instance.max_velocity.y:
                        dog_instance.velocity.y=dog_instance.max_velocity.y
                    dog_instance.velocity+=dog_instance.acceleration*delta_time
                    dog_instance.pos+=dog_instance.velocity*delta_time
                    dog_instance.rect.center=dog_instance.pos.xy
                    for block in pygame.sprite.spritecollide(dog_instance,block_sprite_instance_group,dokill=False):
                        if block.id == '0':
                            dog_instance.rect.bottom=block.rect.top
                            dog_instance.pos.xy=dog_instance.rect.center
                        elif block.id == '1':
                            dog_instance.rect.bottom=block.rect.top
                            dog_instance.pos.xy=dog_instance.rect.center
                        elif block.id == '2':
                            dog_instance.rect.bottom=block.rect.top
                            dog_instance.pos.xy=dog_instance.rect.center
                        elif block.id == '10':
                            dog_instance.rect.bottom=block.rect.top+4
                            dog_instance.pos.xy=dog_instance.rect.center
                        elif block.id == '12':
                            dog_instance.rect.bottom=block.rect.top+30
                            dog_instance.pos.xy=dog_instance.rect.center
                        elif block.id == '13':
                            dog_instance.rect.bottom=block.rect.top+30
                            dog_instance.pos.xy=dog_instance.rect.center
                        elif block.id == '70':
                            dog_instance.rect.bottom=block.rect.top
                            dog_instance.pos.xy=dog_instance.rect.center
                        elif block.id == '3':#ramps
                            dog_instance.rect.bottom=round(0.3488603*(block.rect.x-dog_instance.pos.x))+block.rect.bottom-52#ramp_up
                            dog_instance.pos.xy=dog_instance.rect.center
                        elif block.id == '4':
                            dog_instance.rect.bottom=round(0.3488603*(block.rect.x-dog_instance.pos.x))+block.rect.bottom-37
                            dog_instance.pos.xy=dog_instance.rect.center
                        elif block.id == '5':
                            dog_instance.rect.bottom=round(0.3488603*(block.rect.x-dog_instance.pos.x))+block.rect.bottom-22
                            dog_instance.pos.xy=dog_instance.rect.center
                        elif block.id == '92':
                            dog_instance.rect.bottom=16-(round(0.3488603*abs(dog_instance.pos.x-block.rect.x)))+block.rect.bottom-52#ramp_down
                            dog_instance.pos.xy=dog_instance.rect.center
                        elif block.id == '93':
                            dog_instance.rect.bottom=16-(round(0.3488603*abs(player.pos.x-block.rect.x)))+block.rect.bottom-37
                            dog_instance.pos.xy=dog_instance.rect.center
                        elif block.id == '94':
                            dog_instance.rect.bottom=16-(round(0.3488603*abs(dog_instance.pos.x-block.rect.x)))+block.rect.bottom-22
                            dog_instance.pos.xy=dog_instance.rect.center
                else:
                    if dog_instance.stun_timer<=0:
                        dog_instance.state='idle'
                        dog_instance.stun_timer=0
                        for player in player_sprite_group:player.dog_collide=False
                    else:
                        dog_instance.stun_timer-=delta_time
            else:
                dog_instance.bite_timer-=delta_time
                if int(dog_instance.image_frame)>=len(dog.dog_bite_image_list_left)-1:
                    dog_instance.image_frame=len(dog.dog_bite_image_list_left)-1
                else:dog_instance.image_frame+=5*delta_time
                if dog_instance.direction=='left':
                    dog_instance.image=dog.dog_bite_image_list_left[int(dog_instance.image_frame)]
                else:
                    dog_instance.image=dog.dog_bite_image_list_right[int(dog_instance.image_frame)]
        else:
            if int(dog_instance.image_frame)>=len(dog.dog_death_image_list_left):
                dog_instance.kill()
            else:
                if dog_instance.direction=='left':
                    dog_instance.image=dog.dog_death_image_list_left[int(dog_instance.image_frame)]
                else:
                    dog_instance.image=dog.dog_death_image_list_right[int(dog_instance.image_frame)]
                dog_instance.image_frame+=10*delta_time
        dog_instance.pos=pygame.math.Vector2(dog_instance.rect.center)

        #for dog in dog_sprite_group:
        #    print(dog.pos,dog.velocity,dog.state,'\033c',end='')
class bird(pygame.sprite.Sprite):
    fly_image_list_left=[]
    death_image_list_left=[]
    fly_image_list_right=[]
    death_image_list_right=[]
    load_spritesheet_2dir(pygame.image.load('Data/bird/bird_fly.png').convert_alpha(),fly_image_list_left,fly_image_list_right,3)
    load_spritesheet_2dir(pygame.image.load('Data/bird/bird_death.png').convert_alpha(),death_image_list_left,death_image_list_right,5)
    def __init__(bird_instance,x,y):
        super().__init__()
        bird_instance.velocity=pygame.math.Vector2()
        bird_instance.image=bird.fly_image_list_left[0]
        bird_instance.rect=bird_instance.image.get_rect(center=(x,y))
        bird_instance.dead=False
        bird_instance.image_frame=0
    def update(bird_instance,delta_time):
        if bird_instance.dead:
            for block in pygame.sprite.spritecollide(bird_instance,block_sprite_instance_group,dokill=False):
                bird_instance.kill()
            else:
                if int(bird_instance.image_frame)>=len(bird.death_image_list_left):
                    bird_instance.image_frame=len(bird.death_image_list_left)
                else:
                    bird_instance.image_frame+=10*delta_time
                    if int(bird_instance.image_frame)>=2:
                        bird_instance.image_frame=2
                bird_instance.rect.centery+=100*delta_time
            if bird_instance.velocity.x<0:
                bird_instance.image=bird.death_image_list_right[int(bird_instance.image_frame)]
            else:
                bird_instance.image=bird.death_image_list_left[int(bird_instance.image_frame)]
        else:
            for player in player_sprite_group:
                for reactive_block in pygame.sprite.spritecollide(bird_instance,reactive_block_sprite_instance_group,dokill=False):
                    if type(reactive_block)==little_rock:
                        player.score+=550
                        bird_instance.dead=True
                if player.rect.centerx-bird_instance.rect.centerx<-200:
                    bird_instance.velocity.x=-350
                    if player.rect.centerx-bird_instance.rect.centerx<-100:
                        if bird_instance.rect.centery<player.rect.centery:
                            bird_instance.velocity.y=250
                        else:
                            bird_instance.velocity.y=-250
                    else:bird_instance.velocity.y=0
                else:bird_instance.velocity.y=0
                if player.rect.centerx-bird_instance.rect.centerx>200:
                    bird_instance.velocity.x=350
                    if player.rect.centerx-bird_instance.rect.centerx>100:
                        if bird_instance.rect.centery<player.rect.centery:
                            bird_instance.velocity.y=250
                        else:
                            bird_instance.velocity.y=-250
                    else:bird_instance.velocity.y=0
                else:bird_instance.velocity.y=0
                bird_instance.rect.center+=bird_instance.velocity*delta_time
                if player.rect.colliderect(bird_instance.rect) and player.state!='dodge':
                    player.score-=100
                    player.life-=1
                    bird_instance.dead=True
                    bird_instance.image_frame=0
                if int(bird_instance.image_frame)>=len(bird.fly_image_list_left):
                    bird_instance.image_frame=0
                if bird_instance.velocity.x>0:
                    bird_instance.image=bird.fly_image_list_right[int(bird_instance.image_frame)]
                else:
                    bird_instance.image=bird.fly_image_list_left[int(bird_instance.image_frame)]
                bird_instance.image_frame+=10*delta_time
class ostrich(pygame.sprite.Sprite):
    run_image_list_left=[]
    death_image_list_left=[]
    run_image_list_right=[]
    death_image_list_right=[]
    load_spritesheet_2dir(pygame.image.load('Data/ostrich/ostrich_run.png').convert_alpha(),run_image_list_left,run_image_list_right,9)
    load_spritesheet_2dir(pygame.image.load('Data/ostrich/ostrich_death.png').convert_alpha(),death_image_list_left,death_image_list_right,5)
    def __init__(ostrich_instance,x,y,direction):
        super().__init__()
        ostrich_instance.image=ostrich.run_image_list_left[0]
        ostrich_instance.rect=ostrich_instance.image.get_rect(midbottom=(x*48,((y+1)*48)+5))
        ostrich_instance.velocity=pygame.math.Vector2()
        ostrich_instance.acceleration=pygame.math.Vector2()
        if direction=='left':
            ostrich_instance.acceleration.x=50
        else:
            ostrich_instance.acceleration.x=-50
        ostrich_instance.life=4
        ostrich_instance.image_frame=0
        ostrich_instance.stun_timer=0
    def update(ostrich_instance,delta_time):
        if ostrich_instance.life>0:
            if ostrich_instance.stun_timer==0:
                for player in player_sprite_group:
                    if player.pos.x-ostrich_instance.rect.left<-500:
                        ostrich_instance.acceleration.x=-50
                    elif player.pos.x-ostrich_instance.rect.right>500:
                        ostrich_instance.acceleration.x=50
                    for block in pygame.sprite.spritecollide(ostrich_instance,block_sprite_instance_group,dokill=False):
                        if block.id=='87' or block.id=='35':
                            if ostrich_instance.acceleration.x==50:
                                ostrich_instance.velocity.x=0
                                ostrich_instance.acceleration.x=-50
                                ostrich_instance.image_frame=0
                        elif block.id=='37' or block.id=='91':
                            if ostrich_instance.acceleration.x==-50:
                                ostrich_instance.velocity.x=0
                                ostrich_instance.acceleration.x=50
                                ostrich_instance.image_frame=0
                    if int(ostrich_instance.image_frame)>=len(ostrich.run_image_list_left):
                        ostrich_instance.image_frame=0
                    if ostrich_instance.acceleration.x>0:
                        ostrich_instance.image=ostrich.run_image_list_right[int(ostrich_instance.image_frame)]
                    elif ostrich_instance.acceleration.x<0:
                        ostrich_instance.image=ostrich.run_image_list_left[int(ostrich_instance.image_frame)]
                    ostrich_instance.velocity+=ostrich_instance.acceleration*delta_time
                    ostrich_instance.rect.center+=ostrich_instance.velocity*delta_time
                    ostrich_instance.image_frame+=10*delta_time
                    for player in pygame.sprite.spritecollide(ostrich_instance,player_sprite_group,dokill=False,collided=pygame.sprite.collide_mask):
                        if player.state!='dodge':
                            player.life-=1
                            player.score-=500
                            player.velocity.x=0
                            player.state='idle'
                            ostrich_instance.stun_timer=2
                    for dog in pygame.sprite.spritecollide(ostrich_instance,dog_sprite_group,dokill=False):
                        if dog.life>0:
                            if ostrich_instance.acceleration.x<0 and ostrich_instance.rect.centerx-dog.rect.centerx>0:
                                dog.image_frame=0
                                dog.life=0
                                player.score+=50
                            elif ostrich_instance.acceleration.x>0 and ostrich_instance.rect.centerx-dog.rect.centerx<0:
                                dog.image_frame=0
                                dog.life=0
                                player.score+=50
                    for reactive_block in pygame.sprite.spritecollide(ostrich_instance,reactive_block_sprite_instance_group,dokill=False):
                        if type(reactive_block)==bomb_land:
                            if ostrich_instance.rect.collidepoint(reactive_block.rect.center):
                                ostrich_instance.life=0
                                ostrich_instance.image_frame=0
                                reactive_block.explode=True
                        elif type(reactive_block)==little_rock:
                            if reactive_block.velocity.x!=0:
                                ostrich_instance.stun_timer=4
                                ostrich_instance.life-=1
                                if ostrich_instance.life<=0:ostrich_instance.image_frame=0
                                player.score+=450
            else:
                if ostrich_instance.stun_timer<0:
                    ostrich_instance.stun_timer=0
                else:
                    ostrich_instance.stun_timer-=delta_time
        else:
            if int(ostrich_instance.image_frame)>=len(ostrich.death_image_list_left)-1:
                ostrich_instance.kill()
            if ostrich_instance.acceleration.x>0:
                ostrich_instance.image=ostrich.death_image_list_right[int(ostrich_instance.image_frame)]
            elif ostrich_instance.acceleration.x<0:
                ostrich_instance.image=ostrich.death_image_list_left[int(ostrich_instance.image_frame)]
            ostrich_instance.image_frame+=5*delta_time
class big_fat_guy(pygame.sprite.Sprite):
    whack_image_list_left=[]
    run_image_list_left=[]
    rope_image_list_left=[]
    whack_image_list_right=[]
    run_image_list_right=[]
    rope_image_list_right=[]
    death_image_list_left=[]
    death_image_list_right=[]
    load_spritesheet(pygame.image.load('Data/big_fat_guy/big_fat_guy_whack.png').convert(),whack_image_list_left,frames=32,alpha_sur=False)
    load_spritesheet(pygame.image.load('Data/big_fat_guy/big_fat_guy_whack_right.png').convert(),whack_image_list_right,frames=32,alpha_sur=False)
    load_spritesheet_2dir(pygame.image.load('Data/big_fat_guy/big_fat_guy_run.png').convert(),run_image_list_left,run_image_list_right,frames=17,alpha_sur=False)
    load_spritesheet_2dir(pygame.image.load('Data/big_fat_guy/big_fat_guy_rope.png').convert(),rope_image_list_left,rope_image_list_right,frames=20,alpha_sur=False)
    load_spritesheet_2dir(pygame.image.load('Data/big_fat_guy/big_fat_guy_death.png').convert(),death_image_list_left,death_image_list_right,frames=14,alpha_sur=False)
    hook_image=pygame.image.load('Data/big_fat_guy/hook.png').convert_alpha()
    hook_image_right=pygame.transform.flip(hook_image,True,False)
    def __init__(fat_guy,x,y):
        super().__init__()
        fat_guy.right_rope_limit=0
        fat_guy.left_rope_limit=0
        fat_guy.start_fight=False
        fat_guy.image_frame=0
        fat_guy.direction='left'
        fat_guy.bat='left'
        fat_guy.state='idle'
        fat_guy.life=2#tweak later
        fat_guy.hook_offset=pygame.math.Vector2()
        fat_guy.hook_throw=False
        fat_guy.whack_hit=False
        fat_guy.player_caught=False
        fat_guy.player_collide=False
        if fat_guy.direction=='left':
            fat_guy.image=big_fat_guy.whack_image_list_left[10]
        elif fat_guy.direction=='right':
            fat_guy.image=big_fat_guy.whack_image_list_right[10]
        fat_guy.rect=fat_guy.image.get_rect(midbottom=((x+1)*48,(y+1)*48))
        fat_guy.body_rect=pygame.Rect(fat_guy.rect.left+149,fat_guy.rect.top+119,94,160)
        fat_guy.pos=pygame.math.Vector2(fat_guy.body_rect.center)
        fat_guy.head_rect=pygame.Rect(fat_guy.rect.centerx,fat_guy.rect.centery,49,32)
        fat_guy.hook_rect=big_fat_guy.hook_image.get_rect(midright=(fat_guy.rect.left,fat_guy.rect.top+35))
        fat_guy.whack_rect=pygame.Rect(fat_guy.rect.left,fat_guy.rect.top,102,48)#whack impact rect
    def update(fat_guy,delta_time):
        if fat_guy.state!='dead':
            if fat_guy.life<=0:
                if int(fat_guy.image_frame)>=len(big_fat_guy.death_image_list_left)-1:
                    game_settings['negative_screen']=False
                    fat_guy.state='dead'
                    for player in player_sprite_group:player.score+=2500
                else:
                    if fat_guy.direction=='left':
                        fat_guy.rect.topleft=fat_guy.body_rect.x-195,fat_guy.body_rect.y-81
                        fat_guy.image=big_fat_guy.death_image_list_left[int(fat_guy.image_frame)]
                    else:
                        fat_guy.rect.topleft=fat_guy.body_rect.x-77,fat_guy.body_rect.y-81
                        fat_guy.image=big_fat_guy.death_image_list_right[int(fat_guy.image_frame)]
                    fat_guy.image_frame+=7*delta_time
            else:
                for player in player_sprite_group:
                    if fat_guy.start_fight:#whakc and stuff only if fight started
                        game_settings['negative_screen']=True
                        if player.pos.x<=fat_guy.left_rope_limit or player.pos.x>=fat_guy.right_rope_limit:
                            fat_guy.state='rope'
                        if fat_guy.state!='rope':
                            if abs(player.pos.x-fat_guy.body_rect.centerx)>142:
                                    fat_guy.state='run'
                            else:
                                    fat_guy.state='whack'
                        if player.pos.x>fat_guy.pos.x:
                            fat_guy.direction='right'
                        else:
                            fat_guy.direction='left'
                    else:
                        if player.rect.colliderect(fat_guy.body_rect):
                            fat_guy.start_fight=True
                            game.fat_guy_hit=True
                            player.velocity.xy=0,0
                    if fat_guy.state=='whack':
                        if int(fat_guy.image_frame)>=len(big_fat_guy.whack_image_list_left):
                            fat_guy.image_frame=0
                            game.earthquake=True
                            fat_guy.whack_hit=False
                        if fat_guy.bat=='left':
                            if fat_guy.image_frame==0:
                                fat_guy.image_frame=11
                            elif fat_guy.image_frame>=26:
                                fat_guy.bat='right'
                        if int(fat_guy.image_frame)>=26 and not fat_guy.whack_hit:#fatguy impact rect
                            if fat_guy.direction=='left':
                                if int(fat_guy.image_frame)==26:
                                    fat_guy.whack_rect.topleft=fat_guy.rect.x+36,fat_guy.rect.y+79
                                elif int(fat_guy.image_frame)==27:
                                    fat_guy.whack_rect.topleft=fat_guy.rect.x+23,fat_guy.rect.y+169
                                elif int(fat_guy.image_frame)==28:
                                    fat_guy.whack_rect.topleft=fat_guy.rect.x+26,fat_guy.rect.y+232
                                elif int(fat_guy.image_frame)==29 or int(fat_guy.image_frame)==30 or int(fat_guy.image_frame)==31:
                                    fat_guy.whack_rect.topleft=fat_guy.rect.x+21,fat_guy.rect.y+274
                            else:
                                if int(fat_guy.image_frame)==26:#330
                                    fat_guy.whack_rect.topleft=fat_guy.rect.x+294,fat_guy.rect.y+79
                                elif int(fat_guy.image_frame)==27:
                                    fat_guy.whack_rect.topleft=fat_guy.rect.x+307,fat_guy.rect.y+169
                                elif int(fat_guy.image_frame)==28:
                                    fat_guy.whack_rect.topleft=fat_guy.rect.x+304,fat_guy.rect.y+232
                                elif int(fat_guy.image_frame)==29 or int(fat_guy.image_frame)==30 or int(fat_guy.image_frame)==31:
                                    fat_guy.whack_rect.topleft=fat_guy.rect.x+309,fat_guy.rect.y+274
                            if player.rect.colliderect(fat_guy.whack_rect) and player.state!='dodge':
                                player.life-=2
                                fat_guy.whack_hit=True
                        if fat_guy.direction=='left':
                            fat_guy.head_rect=pygame.Rect(fat_guy.rect.centerx,fat_guy.rect.centery,49,32)
                            fat_guy.image=big_fat_guy.whack_image_list_left[int(fat_guy.image_frame)]
                        elif fat_guy.direction=='right':
                            fat_guy.head_rect=pygame.Rect(fat_guy.rect.centerx,fat_guy.rect.centery,49,32)
                            fat_guy.image=big_fat_guy.whack_image_list_right[int(fat_guy.image_frame)]
                        fat_guy.image_frame+=10*delta_time
                        fat_guy.rect=fat_guy.image.get_rect(topleft=(fat_guy.body_rect.left-149,fat_guy.body_rect.top-119))
                    elif fat_guy.state=='run':#50 37 offset-left 29,37?-right
                        if fat_guy.image_frame>=len(big_fat_guy.run_image_list_left)-1:
                            fat_guy.image_frame=9
                        if fat_guy.direction=='left':
                            if fat_guy.bat=='left':
                                if int(fat_guy.image_frame)<9:
                                    fat_guy.image_frame=9
                            fat_guy.pos.x-=100*delta_time
                            fat_guy.image=big_fat_guy.run_image_list_left[int(fat_guy.image_frame)]
                        elif fat_guy.direction=='right':
                            if fat_guy.bat=='right':
                                if int(fat_guy.image_frame)<9:
                                    fat_guy.image_frame=9
                            fat_guy.pos.x+=100*delta_time
                            fat_guy.image=big_fat_guy.run_image_list_right[int(fat_guy.image_frame)]
                        fat_guy.body_rect.center=fat_guy.pos#fox offset issue
                        fat_guy.rect=fat_guy.image.get_rect(topleft=(fat_guy.body_rect.left-98,fat_guy.body_rect.top-81))
                        fat_guy.image_frame+=10*delta_time
                    elif fat_guy.state=='rope':
                        if fat_guy.image_frame>=12:
                            if not fat_guy.player_collide:
                                if fat_guy.direction=='left':
                                    if player.pos.x>fat_guy.hook_rect.x:
                                        fat_guy.player_caught=True
                                elif fat_guy.direction=='right':
                                    if fat_guy.hook_rect.x>player.pos.x:
                                        fat_guy.player_caught=True
                                if pygame.sprite.spritecollideany(fat_guy,player_sprite_group):
                                    fat_guy.player_collide=True
                                if fat_guy.player_caught:
                                    player.state='idle'
                                    if fat_guy.direction=='left':
                                        player.rect.topleft=fat_guy.hook_rect.midright
                                        player.pos.xy=player.rect.center
                                        fat_guy.hook_rect.x+=1100*delta_time
                                    elif fat_guy.direction=='right':
                                        player.rect.topright=fat_guy.hook_rect.midleft
                                        player.pos.xy=player.rect.center
                                        fat_guy.hook_rect.x-=1100*delta_time
                                else:
                                    if fat_guy.direction=='left':
                                        fat_guy.hook_rect.x-=1100*delta_time
                                    elif fat_guy.direction=='right':
                                        fat_guy.hook_rect.x+=1100*delta_time
                                fat_guy.hook_rect.y+=50*delta_time
                                if int(fat_guy.image_frame)==12 and not fat_guy.hook_throw:#first time?
                                    if fat_guy.direction=='left':
                                        fat_guy.hook_rect.midright=(fat_guy.rect.left,fat_guy.rect.top+35)
                                    else:
                                        fat_guy.hook_rect.midleft=(fat_guy.rect.right,fat_guy.rect.top+35)
                                    fat_guy.hook_throw=True
                                fat_guy.image_frame=12
                                if fat_guy.direction=='left':
                                    game_window.blit(fat_guy.hook_image,(fat_guy.hook_rect.x-fat_guy.hook_offset.x,fat_guy.hook_rect.y-fat_guy.hook_offset.y))
                                    pygame.draw.line(game_window,(0,0,0),(fat_guy.hook_rect.right-fat_guy.hook_offset.x,fat_guy.hook_rect.midright[1]-fat_guy.hook_offset.y),(fat_guy.rect.left-fat_guy.hook_offset.x,fat_guy.rect.top+41-fat_guy.hook_offset.y))
                                else:
                                    game_window.blit(fat_guy.hook_image_right,(fat_guy.hook_rect.x-fat_guy.hook_offset.x,fat_guy.hook_rect.y-fat_guy.hook_offset.y))
                                    pygame.draw.line(game_window,(0,0,0),(fat_guy.hook_rect.left-fat_guy.hook_offset.x,fat_guy.hook_rect.midright[1]-fat_guy.hook_offset.y),(fat_guy.rect.right-fat_guy.hook_offset.x,fat_guy.rect.top+41-fat_guy.hook_offset.y))
                            else:
                                fat_guy.player_caught=False
                                if fat_guy.image_frame>=len(fat_guy.rope_image_list_left)-1:
                                    fat_guy.player_collide=False
                                    fat_guy.hook_throw=False
                                    fat_guy.image_frame=0
                                    fat_guy.state='idle'
                        if fat_guy.direction=='left':
                            fat_guy.image=big_fat_guy.rope_image_list_left[int(fat_guy.image_frame)]
                        elif fat_guy.direction=='right':
                            fat_guy.image=big_fat_guy.rope_image_list_right[int(fat_guy.image_frame)]
                        fat_guy.rect=fat_guy.image.get_rect(topleft=(fat_guy.body_rect.left-98,fat_guy.body_rect.top-81))
                        fat_guy.image_frame+=10*delta_time
                    for reactive_block in reactive_block_sprite_instance_group:
                        if type(reactive_block)==little_rock and reactive_block.velocity.x!=0:#change velocity cpa later?
                            if reactive_block.rect.colliderect(fat_guy.head_rect):
                                fat_guy.life-=2
                                player.score+=750
                                reactive_block.kill()#make it reflect later?
                                if fat_guy.life<=0:
                                    fat_guy.image_frame=0
                                    if fat_guy.direction=='left':
                                        fat_guy.rect.topleft=(fat_guy.body_rect.x-195,fat_guy.body_rect.y-81)
                                    else:
                                        fat_guy.rect.topleft=(fat_guy.body_rect.x+77,fat_guy.body_rect.y-81)
                            elif reactive_block.rect.colliderect(fat_guy.body_rect):
                                fat_guy.life-=1
                                player.score+=450
                                reactive_block.kill()#make it reflect later?
                                if fat_guy.life<=0:
                                    fat_guy.image_frame=0
                                    if fat_guy.direction=='left':
                                        fat_guy.rect.topleft=(fat_guy.body_rect.x-195,fat_guy.body_rect.y-81)
                                    else:
                                        fat_guy.rect.topleft=(fat_guy.body_rect.x+77,fat_guy.body_rect.y-81)
class rat(pygame.sprite.Sprite):
    death_sound=pygame.mixer.Sound('Data/rat/rat_death.wav')
    rat_run_right_list=[]
    rat_death_right_list=[]
    rat_run_left_list=[]
    rat_death_left_list=[]
    load_spritesheet_2dir(pygame.image.load('Data/rat/rat_run.png').convert_alpha(),rat_run_left_list,rat_run_right_list,frames=4)
    load_spritesheet_2dir(pygame.image.load('Data/rat/rat_death.png').convert_alpha(),rat_death_left_list,rat_death_right_list,frames=7)
    def __init__(rat_instance,x,y):
        super().__init__()
        rat_instance.image=rat.rat_run_left_list[0]
        rat_instance.rect=rat_instance.image.get_rect(topleft=(x*48,(y*48)+16))
        rat_instance.mask=pygame.mask.from_surface(rat_instance.image)
        rat_instance.frame=0
        rat_instance.dead=False
        rat_instance.velocity=pygame.math.Vector2(-10,0)
        rat_instance.pos=pygame.math.Vector2(rat_instance.rect.center)
    def update(rat_instance,delta_time):
        if rat_instance.dead:
            if rat_instance.frame>len(rat.rat_death_right_list)-1:
                rat_instance.kill()
            elif rat_instance.frame==0:
                rat.death_sound.play()
            if rat_instance.velocity.x>0:
                rat_instance.image=rat.rat_death_right_list[int(rat_instance.frame)]
            elif rat_instance.velocity.x<0:
                rat_instance.image=rat.rat_death_left_list[int(rat_instance.frame)]
            rat_instance.frame+=8*delta_time
        else:
            for player in pygame.sprite.spritecollide(rat_instance,player_sprite_group,dokill=False,collided=pygame.sprite.collide_mask):
                if player.state!='pant' and player.state!='idle' and player.state!='aim' and player.state!='interact' and player.state!='throw':
                    rat_instance.dead=True
                    rat_instance.frame=0
            for block in pygame.sprite.spritecollide(rat_instance,block_sprite_instance_group,dokill=False):
                if block.id=='41':#rat_hole
                    rat_instance.velocity.x=-70
                elif block.id=='37':#rock
                    rat_instance.velocity.x=70
                elif block.id=='91':#rock_long
                    rat_instance.velocity.x=70
            rat_instance.pos.x+=rat_instance.velocity.x*delta_time
            rat_instance.rect.center=rat_instance.pos
            if rat_instance.frame>len(rat.rat_run_right_list)-1:
                rat_instance.frame=0
            if rat_instance.velocity.x>0:
                rat_instance.image=rat.rat_run_right_list[round(rat_instance.frame)]
            elif rat_instance.velocity.x<0:
                rat_instance.image=rat.rat_run_left_list[round(rat_instance.frame)]
            if not rat_instance.dead:rat_instance.frame+=10*delta_time
class fish(pygame.sprite.Sprite):#fishes are not the bad guys
    fish_swim_imagelist_right=[]
    fish_swim_imagelist_left=[]
    fish_death_imagelist_right=[]
    fish_death_imagelist_left=[]
    load_spritesheet_2dir(pygame.image.load('Data/fish/fish_swim.png').convert_alpha(),fish_swim_imagelist_left,fish_swim_imagelist_right,frames=4)
    load_spritesheet_2dir(pygame.image.load('Data/fish/fish_death.png').convert_alpha(),fish_death_imagelist_left,fish_death_imagelist_right,frames=3)
    def __init__(fish_instance,x,y,direction):
        super().__init__()
        fish_instance.death=False
        fish_instance.player_bite=False
        if direction=='left':
            fish_instance.direction='left'
            fish_instance.image=fish.fish_swim_imagelist_left[0]
        elif direction=='right':
            fish_instance.direction='right'
            fish_instance.image=fish.fish_swim_imagelist_right[0]
        fish_instance.mask=pygame.mask.from_surface(fish_instance.image)
        fish_instance.image_frame=0
        fish_instance.rect=fish_instance.image.get_rect(center=(x*48,y*48))
        fish_instance.pos=pygame.math.Vector2(fish_instance.rect.center)
        fish_instance.velocity=pygame.math.Vector2()
    def update(fish_instance,delta_time):
        if fish_instance.death:
            if not fish_instance.image_frame>=len(fish.fish_death_imagelist_left):
                if fish_instance.direction=='left':
                    fish_instance.image=fish.fish_death_imagelist_left[int(fish_instance.image_frame)]
                elif fish_instance.direction=='right':
                    fish_instance.image=fish.fish_death_imagelist_right[int(fish_instance.image_frame)]
                fish_instance.image_frame+=10*delta_time
                fish_instance.velocity.xy=0,10
            for block in pygame.sprite.spritecollide(fish_instance,block_sprite_instance_group,dokill=False):
                if block.id=='10':
                    fish_instance.velocity.y=0
                    fish_instance.rect.bottom=block.rect.top
                    fish_instance.pos.xy=fish_instance.rect.center
                elif block.id=='0' or block.id=='1' or block.id=='2':
                    fish_instance.velocity.y=0
                    fish_instance.rect.bottom=block.rect.top
                    fish_instance.pos.xy=fish_instance.rect.center
        else:
            fish_instance.water=False
            for water_rect in water_blocks_rect_list:
                if not fish_instance.water:
                    if water_rect.colliderect(fish_instance.rect):
                        fish_instance.water=True
                        break
            for block in pygame.sprite.spritecollide(fish_instance,block_sprite_instance_group,dokill=False):
                if block.id=='145' or block.id=='174' or block.id=='204' or block.id=='147' or block.id=='177' or block.id=='206' or block.id=='149' or block.id=='178' or block.id=='207' or block.id=='92' or block.id=='93' or block.id=='94' or block.id=='9':
                    if fish_instance.direction=='left':
                        fish_instance.direction='right'
                elif block.id=='154' or block.id=='183' or block.id=='211' or block.id=='209' or block.id=='180' or block.id=='152' or block.id=='150' or block.id=='179' or block.id=='208' or block.id=='67' or block.id=='3' or block.id=='4' or block.id=='5':
                    if fish_instance.direction=='right':
                        fish_instance.direction='left'
            for player in player_sprite_group:
                if player.water:
                    if fish_instance.player_bite:
                        fish_instance.velocity.xy=0,0
                        if player.state=='swim' or player.state=='swim_fast':
                            if player.direction=='right':
                                fish_instance.pos.xy=player.rect.left,player.rect.bottom-19
                            else:
                                fish_instance.pos.xy=player.rect.right,player.rect.bottom-19
                        else:
                            fish_instance.pos.xy=player.rect.centerx,player.rect.bottom-19
                        if fish_instance.direction=='left':
                            fish_instance.image=fish.fish_death_imagelist_left[1]
                        elif fish_instance.direction=='right':
                            fish_instance.image=fish.fish_death_imagelist_right[1]
                    else:
                        for player_obj in pygame.sprite.spritecollide(fish_instance,player_sprite_group,dokill=False,collided=pygame.sprite.collide_mask):
                            fish_instance.player_bite=True
                            player_obj.life-=1
                            player_obj.score-=100
                        if player.pos.x>fish_instance.pos.x:
                            fish_instance.velocity.x=150
                            fish_instance.direction='right'
                        else:
                            fish_instance.velocity.x=-150
                            fish_instance.direction='left'
                        if player.pos.y>fish_instance.pos.y:
                            fish_instance.velocity.y=50
                        else:
                            fish_instance.velocity.y=-50
                        fish_instance.image_frame+=10*delta_time
                        if fish_instance.image_frame>=len(fish.fish_swim_imagelist_left)-1:
                            fish_instance.image_frame=0
                        if fish_instance.direction=='left':
                            fish_instance.image=fish.fish_swim_imagelist_left[int(fish_instance.image_frame)]
                        elif fish_instance.direction=='right':
                            fish_instance.image=fish.fish_swim_imagelist_right[int(fish_instance.image_frame)]
                        if fish_instance.velocity.y<0:
                            if player.rect.bottom<fish_instance.rect.top:
                                if fish_instance.direction=='right':
                                    fish_instance.image=pygame.transform.rotate(fish_instance.image,45)
                                else:
                                    fish_instance.image=pygame.transform.rotate(fish_instance.image,-45)
                else:   
                    fish_instance.image_frame+=5*delta_time
                    if fish_instance.image_frame>=len(fish.fish_swim_imagelist_left):
                        fish_instance.image_frame=0
                    if fish_instance.direction=='left':
                        fish_instance.image=fish.fish_swim_imagelist_left[int(fish_instance.image_frame)]
                        fish_instance.velocity.xy=-20,0
                    elif fish_instance.direction=='right':
                        fish_instance.image=fish.fish_swim_imagelist_right[int(fish_instance.image_frame)]
                        fish_instance.velocity.xy=20,0
                    if not fish_instance.water:
                        fish_instance.velocity.y=30
            for water_line in water_hitlines:
                if fish_instance.rect.clipline(water_line)!=():
                    if water_line[1][1]<=fish_instance.rect.top:
                        fish_instance.velocity.y=0
                #add wavess?? if 
        fish_instance.pos+=fish_instance.velocity*delta_time
        fish_instance.rect.center=fish_instance.pos

class block(pygame.sprite.Sprite):
    sprite_sheet=pygame.image.load('Data/blocks/blocks.png').convert()
    block_list=[]
    for block_y in range(0,sprite_sheet.get_height()//48):
        for block_x in range(0,sprite_sheet.get_width()//48):
            image=pygame.Surface((48,48))
            image.blit(sprite_sheet,(0,0),(block_x*48,block_y*48,48,48))
            block_list.append(image)
    def __init__(block_instance,block_id,x,y):
        super().__init__()
        block_instance.id=block_id
        block_instance.image=block.block_list[int(block_id)]
        block_instance.rect=block_instance.image.get_rect(topleft=(x*48,y*48))

class grass(pygame.sprite.Sprite):
    image=pygame.image.load('Data/blocks/reactive_blocks/grass.png').convert_alpha()
    mask=pygame.mask.from_surface(image)
    def __init__(grass_instance,x,y):
        super().__init__()
        grass_instance.image=grass.image
        grass_instance.mask=grass.mask
        grass_instance.rect=grass_instance.image.get_rect(topleft=(x*48,y*48-23))
    def update(grass_instance,delta_time):
        for player in pygame.sprite.spritecollide(grass_instance,player_sprite_group,dokill=False,collided=pygame.sprite.collide_mask):
            if player.state!='throw':
                player.state='grass'   
                if player.direction=='left':
                    player.image=player.pant_image_list_left[-1]
                else:
                    player.image=player.pant_image_list_right[-1]
class apple(pygame.sprite.Sprite):
    image=pygame.image.load('Data/blocks/reactive_blocks/apple.png').convert_alpha()
    def __init__(apple_instance,x,y):
        super().__init__()
        apple_instance.image=apple.image
        apple_instance.rect=apple_instance.image.get_rect(topleft=(x*48,(y*48)+22))
    def update(apple_instance,delta_time):
        for player in pygame.sprite.spritecollide(apple_instance,player_sprite_group,dokill=False):#recover heath here
            player.life+=2
            player.score+=200
            player.stamina+=1000
            apple_instance.kill()
class flower(pygame.sprite.Sprite):
    image=pygame.image.load('Data/blocks/reactive_blocks/flower.png').convert_alpha()
    def __init__(flower_instance,x,y):
        super().__init__()
        flower_instance.image=flower.image
        flower_instance.rect=flower_instance.image.get_rect(topleft=(x*48,y*48))
    def update(flower_instance,delta_time):
        for player in pygame.sprite.spritecollide(flower_instance,player_sprite_group,dokill=False):
            if player.state=='pick':
                player.flower_count+=1
                player.score+=600
                flower_instance.kill()
                player.stamina+=500
                player.state='idle'
class spike(pygame.sprite.Sprite):
    image_1=pygame.image.load('Data/blocks/reactive_blocks/spike_1.png').convert_alpha()
    mask_1=pygame.mask.from_surface(image_1)
    image_2=pygame.image.load('Data/blocks/reactive_blocks/spike_2.png').convert_alpha()
    mask_2=pygame.mask.from_surface(image_2)
    def __init__(spike_instance,x,y,variant):
        super().__init__()
        spike_instance.player_collide=False
        if variant==1:
            spike_instance.image=spike.image_1
            spike_instance.rect=spike_instance.image.get_rect(topleft=(x*48,((y+1)*48)-28))
        else:
            spike_instance.image=spike.image_2
            spike_instance.rect=spike_instance.image.get_rect(topleft=(x*48,((y+1)*48)-22))
    def update(spike_instance,delta_time):
        for player in pygame.sprite.spritecollide(spike_instance,player_sprite_group,dokill=False,collided=pygame.sprite.collide_mask):
            if not spike_instance.player_collide:
                spike_instance.rect.top=player.rect.bottom
                player.life-=1
                player.score-=350
                game.spike_shake_timer=1
                spike_instance.player_collide=True
class bomb(pygame.sprite.Sprite):
    image_list=[]
    load_spritesheet(pygame.image.load('Data/blocks/reactive_blocks/bomb.png').convert_alpha(),image_list,frames=8)
    def __init__(bomb_instance,x,y):
        super().__init__()
        bomb_instance.bomb_image_list=bomb.image_list
        bomb_instance.image=bomb_instance.bomb_image_list[0]
        bomb_instance.rect=bomb_instance.image.get_rect(topleft=(x*48-117,y*48-96))
        bomb_instance.frame=0
        bomb_instance.mask=pygame.mask.from_surface(bomb_instance.image)
        bomb_instance.explode=False
    def update(bomb_instance,delta_time):
        for player in pygame.sprite.spritecollide(bomb_instance,player_sprite_group,dokill=False,collided=pygame.sprite.collide_mask): 
            if not bomb_instance.explode:
                player.life-=1
                player.score-=300
            bomb_instance.explode=True
            player.image_frame=0
            player.state='explode'
        if bomb_instance.explode:
            bomb_instance.frame+=4*delta_time
            if bomb_instance.frame>len(bomb_instance.bomb_image_list)-1:
                for bubble_count in range(numpy.random.randint(5,10)):
                    bubble_sprite_group.add(bubble(numpy.random.randint(bomb_instance.rect.x,bomb_instance.rect.x+bomb_instance.image.get_width()),numpy.random.randint(bomb_instance.rect.y,bomb_instance.rect.bottom),round(numpy.random.uniform(0.1,2),ndigits=1)))
                bomb_instance.kill()
            else:
                bomb_instance.image=bomb_instance.bomb_image_list[int(bomb_instance.frame)]
class bomb_land(pygame.sprite.Sprite):
    image_list=[]
    load_spritesheet(pygame.image.load('Data/blocks/reactive_blocks/bomb_land.png').convert_alpha(),image_list,frames=8)
    def __init__(bomb_instance,x,y):
        super().__init__()
        bomb_instance.image=bomb_land.image_list[0]
        bomb_instance.rect=bomb_instance.image.get_rect(topleft=((x-2)*48,(y-2)*48))
        bomb_instance.frame=0
        bomb_instance.mask=pygame.mask.from_surface(bomb_instance.image)
        bomb_instance.explode=False
        bomb_instance.radius=30
    def update(bomb,delta_time):
        if bomb.explode:
            bomb.frame+=4*delta_time
            if bomb.frame>len(bomb_land.image_list)-1:
                bomb.kill()
            else:
                bomb.image=bomb_land.image_list[int(bomb.frame)]
                bomb.mask=pygame.mask.from_surface(bomb.image)
            for dog in pygame.sprite.spritecollide(bomb,dog_sprite_group,dokill=False):
                if dog.life>0:
                    dog.image_frame=0
                    dog.life=0
            for reactive_block in pygame.sprite.spritecollide(bomb,reactive_block_sprite_instance_group,dokill=False,collided=pygame.sprite.collide_circle):
                if type(reactive_block)==bomb_land:
                    reactive_block.explode=True
        else:
            for player in pygame.sprite.spritecollide(bomb,player_sprite_group,dokill=False,collided=pygame.sprite.collide_mask): 
                if player.state!='dodge':
                    if not bomb.explode:
                        player.life-=2
                        player.score-=500
                    bomb.explode=True
                    player.image_frame=0
                    player.state='explode'
                
class chain(pygame.sprite.Sprite):
    image=pygame.image.load('Data/blocks/reactive_blocks/chain.png').convert_alpha()
    def __init__(chain_instance,x,y):
        super().__init__()
        chain_instance.image=chain.image
        chain_instance.rect=chain_instance.image.get_rect(topleft=(x*48-17,y*48))
    def update(chain_instance,delta_time):
        pass
class rock(pygame.sprite.Sprite):
    image=pygame.image.load('Data/blocks/reactive_blocks/rock.png').convert_alpha()
    def __init__(rock_instance,x,y):
        super().__init__()
        rock_instance.origin_image=rock.image
        rock_instance.image=rock_instance.origin_image
        rock_instance.rect=rock_instance.image.get_rect(topleft=((x-1)*48,(y-1)*48))
        rock_instance.angle=0
        rock_instance.roll=False
    def update(rock_instance,delta_time):
        if rock_instance.angle<=-360:
            rock_instance.angle+=360
        rock_instance.image=pygame.transform.rotate(rock_instance.origin_image,rock_instance.angle)
        if rock_instance.roll:
            rock_instance.rect.x+=100*delta_time
            rock_instance.rect.y+=400*delta_time
            rock_instance.angle-=40*delta_time
            for block in pygame.sprite.spritecollide(rock_instance,block_sprite_instance_group,dokill=False):
                if block.id=='10':
                    rock_instance.roll=False
                    rock_instance.rect.midbottom=block.rect.midtop
                else:
                    if block.id=='145':
                        if rock_instance.rect.left-block.rect.left<=17:
                            rock_instance.rect.bottom=48-(3.4*(rock_instance.rect.left-block.rect.x)+block.rect.bottom)-18 #y = 3.399023*x - 6.511401
                    elif block.id=='174':
                        if rock_instance.rect.left-block.rect.left>=14:
                            rock_instance.rect.bottom=1.655*(rock_instance.rect.left-block.rect.x)+block.rect.bottom-18
                    elif block.id=='177':
                        if rock_instance.rect.left-block.rect.left<=32:
                            rock_instance.rect.bottom=48-(-1.7*(rock_instance.rect.left-block.rect.x))+block.rect.bottom-18
                    elif block.id=='206':
                        if rock_instance.rect.left-block.rect.left>=29:
                            rock_instance.rect.bottom=48-(-2.38*(rock_instance.rect.left-block.rect.x))+block.rect.bottom-18
                    elif block.id=='149':
                        if rock_instance.rect.left-block.rect.left<=11:
                            rock_instance.rect.bottom=48-(-5.56*(rock_instance.rect.left-block.rect.x))+block.rect.bottom-18
                    elif block.id=='178':
                        if rock_instance.rect.left-block.rect.left<=25:
                            rock_instance.rect.bottom=48-(-3.5*(rock_instance.rect.left-block.rect.x))+block.rect.bottom-18
                    elif block.id=='207':
                        if rock_instance.rect.left-block.rect.left>=22:
                            rock_instance.rect.bottom=48-(-1.9*(rock_instance.rect.left-block.rect.x))+block.rect.bottom-18
                    elif block.id=='204' or block.id=='147':#45degreethingy
                        rock_instance.rect.bottom=0.5*(rock_instance.rect.left-block.rect.x)+block.rect.bottom-18
                    if block.id=='154':
                        if rock_instance.rect.left-block.rect.left>=31:
                            rock_instance.rect.bottom=3.4*(rock_instance.rect.left-block.rect.x)+block.rect.bottom-18 #y = 3.399023*x - 6.511401
                    elif block.id=='183':
                        if rock_instance.rect.left-block.rect.left<=33:
                            rock_instance.rect.bottom=-1.655*(rock_instance.rect.left-block.rect.x)+block.rect.bottom-18#y = -1.655013*x + 54.31424
                    elif block.id=='180':#y = -1.7*x + 74.49683
                        if rock_instance.rect.left-block.rect.left>=16:
                            rock_instance.rect.bottom=-1.7*(rock_instance.rect.left-block.rect.x)+block.rect.bottom-18
                    elif block.id=='209':#y = -2.38*x + 42.61518
                        if rock_instance.rect.left-block.rect.left<=19:
                            rock_instance.rect.bottom=-2.38*(rock_instance.rect.left-block.rect.x)+block.rect.bottom-18
                    elif block.id=='150':#y = -5.56*x + 265.5725
                        if rock_instance.rect.left-block.rect.left>=37:
                            rock_instance.rect.bottom=-5.56*(rock_instance.rect.left-block.rect.x)+block.rect.bottom-18
                    elif block.id=='179':#y = -3.5*x + 137.3384
                        if rock_instance.rect.left-block.rect.left>=23:
                            rock_instance.rect.bottom=-3.5*(rock_instance.rect.left-block.rect.x)+block.rect.bottom-18
                    elif block.id=='208':#y = -1.9*x + 47.14072
                        if rock_instance.rect.left-block.rect.left<=26:
                            rock_instance.rect.bottom=-1.9*(rock_instance.rect.left-block.rect.x)+block.rect.bottom-18
                    elif block.id=='211' or block.id=='152':
                        rock_instance.rect.bottom=48-(0.5*(rock_instance.rect.left-block.rect.x))+block.rect.bottom-18
                    elif block.id=='203' or block.id=='176' or block.id=='205' or block.id=='181' or block.id=='210' or block.id=='212' or block.id=='0' or block.id=='1' or block.id=='2':#203 176 205 181 210 212
                        rock_instance.rect.bottom=block.rect.top
        else:
            for reactive_block in pygame.sprite.spritecollide(rock_instance,reactive_block_sprite_instance_group,dokill=False):
                if type(reactive_block)==little_rock:
                    rock_instance.roll=True
class little_rock(pygame.sprite.Sprite):
    image_list=[]
    load_spritesheet(pygame.image.load('Data/blocks/reactive_blocks/little_rock.png').convert_alpha(),image_list,3)
    mask=pygame.mask.from_surface(image_list[0])
    water_resistance=pygame.math.Vector2(0,100)
    water_jump_sound=pygame.mixer.Sound('Data/blocks/reactive_blocks/little_rock_water.wav')
    def __init__(rock_instance,x,y):
        super().__init__()
        rock_instance.life=3
        rock_instance.image_frame=0
        rock_instance.image=little_rock.image_list[0]
        rock_instance.mask=little_rock.mask
        rock_instance.rect=rock_instance.image.get_rect(topleft=(x+17,y))
        rock_instance.pos=pygame.math.Vector2(rock_instance.rect.center)
        rock_instance.velocity=pygame.math.Vector2()
        rock_instance.acceleration=pygame.math.Vector2()
    def update(rock_instance,delta_time):
        if rock_instance.life>0:
            for player in pygame.sprite.spritecollide(rock_instance,player_sprite_group,dokill=False):
                if player.state=='pick' and player.hand=='':
                    player.hand='rock'
                    rock_instance.kill()
            for player in player_sprite_group:
                if rock_instance.velocity.x!=0:
                    for dog in pygame.sprite.spritecollide(rock_instance,dog_sprite_group,dokill=False):
                        dog.stun_timer=5
                        dog.life-=1
                        dog.image_frame=0
                        rock_instance.velocity.x=0
                        rock_instance.life-=1
                        player.score+=200
                if rock_instance.velocity.y!=0:
                    for reactive_block in pygame.sprite.spritecollide(rock_instance,reactive_block_sprite_instance_group,dokill=False,collided=pygame.sprite.collide_mask):
                        if type(reactive_block)==bomb or type(reactive_block)==bomb_land:
                            reactive_block.explode=True
                            rock_instance.life-=1
                        elif type(reactive_block)==spike:
                            reactive_block.rect.top=rock_instance.rect.bottom
                rock_instance.velocity+=rock_instance.acceleration*delta_time
                rock_instance.pos+=rock_instance.velocity*delta_time
                rock_instance.rect.center=rock_instance.pos.xy
                for block in pygame.sprite.spritecollide(rock_instance,block_sprite_instance_group,dokill=False):
                    rock_instance.velocity.xy=0,0
                    rock_instance.acceleration.xy=0,0
                    if block.id=='0' or block.id=='1' or block.id=='2':
                        rock_instance.rect.bottom=block.rect.top+24
                    rock_instance.pos.xy=rock_instance.rect.center
                for water_line in water_hitlines:
                    if rock_instance.rect.clipline(water_line)!=():
                        rock_instance.acceleration.y=300
                        if rock_instance.velocity.y>little_rock.water_resistance.y:
                            rock_instance.velocity-=little_rock.water_resistance
                            rock_instance.velocity.y=-rock_instance.velocity.y
                            rock_instance.water_jump_sound_channel=pygame.mixer.find_channel()
                            if rock_instance.water_jump_sound==None:
                                rock_instance.water_jump_sound_channel=pygame.mixer.Channel(pygame.mixer.get_num_channels+1)
                            if abs(rock_instance.rect.x-player.pos.x)<=50:
                                rock_instance.water_jump_sound_channel.set_volume(1,1)
                            else:
                                if player.pos.x>rock_instance.rect.x:
                                    rock_instance.water_jump_sound_channel.set_volume(0.9,0.1)#set volue acoddin to how close rokc slpashlater
                                else:
                                    rock_instance.water_jump_sound_channel.set_volume(0.1,0.9)#set volue acoddin to how close rokc slpashlater
                            rock_instance.water_jump_sound_channel.play(little_rock.water_jump_sound)
        else:
            if int(rock_instance.image_frame)>=len(little_rock.image_list):
                rock_instance.kill()
            else:
                rock_instance.image=little_rock.image_list[int(rock_instance.image_frame)]
                rock_instance.image_frame+=10*delta_time
class rock_pile(pygame.sprite.Sprite):
    image=pygame.image.load('Data/blocks/reactive_blocks/rock_pile.png').convert_alpha()
    def __init__(rock_pile_instance,x,y):
        super().__init__()
        rock_pile_instance.image=rock_pile.image
        rock_pile_instance.rect=rock_pile_instance.image.get_rect(midbottom=(x,y))
    def update(rock_pile_instance,delta_time):
        for player in pygame.sprite.spritecollide(rock_pile_instance,player_sprite_group,dokill=False):
            if player.state=='pick':
                player.hand='rock'
class switch(pygame.sprite.Sprite):
    image_list=[]
    load_spritesheet(pygame.image.load('Data/blocks/reactive_blocks/switch.png').convert_alpha(),image_list,frames=8)
    switch_rotate_sound=pygame.mixer.Sound('Data/blocks/reactive_blocks/switch_rotate.wav')
    def __init__(switch_instance,x,y):
        super().__init__()
        switch_instance.switch_image_list=switch.image_list
        switch_instance.image=switch_instance.switch_image_list[0]
        switch_instance.rect=switch_instance.image.get_rect(bottomright=((x+1)*48+3,(y+1)*48+3))
        switch_instance.frame=0
        switch_instance.prev_frame=0
        switch_instance.connected=False
    def update(switch_instance,delta_time):
        for player in pygame.sprite.spritecollide(switch_instance,player_sprite_group,dokill=False):
            if player.state=='interact':
                if switch_instance.frame>=len(switch_instance.switch_image_list)-1:
                    switch_instance.image=switch_instance.switch_image_list[len(switch_instance.switch_image_list)-1]
                    for bomb_rect in bomb_rect_list:
                        if bomb_rect.colliderect(switch_instance.rect):
                            for reative_block in reactive_block_sprite_group:
                                if type(reative_block)==bomb or type(reative_block)==bomb_land:
                                    if bomb_rect.collidepoint(reative_block.rect.center):
                                        switch_instance.connected=True
                                        reative_block.explode=True
                                elif type(reative_block)==chain:
                                    if reative_block.rect.colliderect(bomb_rect):
                                        reative_block.kill()
                            if switch_instance.connected:
                                for fish in fish_sprite_group:
                                    if bomb_rect.colliderect(fish.rect):
                                        fish.death=True
                                        fish.image_frame=0
                else:
                    switch_instance.image=switch_instance.switch_image_list[round(switch_instance.frame)]
                    if int(switch_instance.frame)!=switch_instance.prev_frame and int(switch_instance.frame)%2==0:
                        switch.switch_rotate_sound.play()
                    switch_instance.prev_frame=int(switch_instance.frame)
                    switch_instance.frame+=15*delta_time
class pressure_switch(pygame.sprite.Sprite):
    image_list=[]
    load_spritesheet(pygame.image.load('Data/blocks/reactive_blocks/pressure_switch.png').convert_alpha(),image_list)
    switch_press_sound=pygame.mixer.Sound('Data/blocks/reactive_blocks/switch_press.wav')
    def __init__(switch_instance,x,y):
        super().__init__()
        switch_instance.switch_image_list=pressure_switch.image_list
        switch_instance.image=switch_instance.switch_image_list[0]
        switch_instance.rect=switch_instance.image.get_rect(bottomright=((x+1)*48+3,(y+1)*48+3))
        switch_instance.connected=False
        switch_instance.clicked=False
    def update(switch_instance,delta_time):
        for trig_reactive_block in pygame.sprite.spritecollide(switch_instance,reactive_block_sprite_group,dokill=False):
            if type(trig_reactive_block)==rock:
                switch_instance.image=switch_instance.switch_image_list[1]
                if not switch_instance.clicked:
                    pressure_switch.switch_press_sound.play()
                    switch_instance.clicked=True
                for bomb_rect in bomb_rect_list:
                        if bomb_rect.colliderect(switch_instance.rect):
                            for reative_block in reactive_block_sprite_instance_group:
                                if type(reative_block)==bomb or type(reative_block)==bomb_land:
                                    if bomb_rect.collidepoint(reative_block.rect.center):
                                        switch_instance.connected=True
                                        reative_block.explode=True
                                elif type(reative_block)==chain:
                                    if reative_block.rect.colliderect(bomb_rect):
                                        reative_block.kill()
                            if switch_instance.connected:
                                for fish in fish_sprite_group:
                                    if bomb_rect.colliderect(fish.rect):
                                        fish.death=True
                                        fish.image_frame=0
class nest(pygame.sprite.Sprite):
    image_list=[]
    load_spritesheet(pygame.image.load('Data/blocks/reactive_blocks/nest.png').convert_alpha(),image_list,7)
    def __init__(nest_instance,x,y):
        super().__init__()
        nest_instance.timer=10
        nest_instance.fall=False
        nest_instance.image=nest.image_list[0]
        nest_instance.image_frame=0
        nest_instance.bird_count=5#no of birds in a nest
        nest_instance.rect=nest_instance.image.get_rect(topleft=(x*48,y*48))
    def update(nest_instance,delta_time):
        if nest_instance.bird_count>0:
            if not nest_instance.fall:
                if nest_instance.timer>=10:
                    nest_instance.timer=0
                    bird_sprite_group.add(bird(nest_instance.rect.centerx,nest_instance.rect.centery))
                    nest_instance.bird_count-=1
                else:
                    nest_instance.timer+=delta_time
            for reactive_block in pygame.sprite.spritecollide(nest_instance,reactive_block_sprite_instance_group,dokill=False):
                if type(reactive_block)==little_rock:
                    nest_instance.fall=True
                    for player in player_sprite_group:player.score+=650 
        else:
            for block in pygame.sprite.spritecollide(nest_instance,block_sprite_instance_group,dokill=False):
                nest_instance.rect.bottom=block.rect.top
                if int(nest_instance.image_frame)+1>=7:
                    nest_instance.kill()
                else:
                    nest_instance.image=nest.image_list[int(nest_instance.image_frame)]
                    nest_instance.image_frame+=10*delta_time
            else:
                nest_instance.rect.y+=100*delta_time

class tree(pygame.sprite.Sprite):
    tree_image=pygame.image.load('Data/tree.png').convert_alpha()
    cut_tree_image=pygame.image.load('Data/cut_tree.png').convert_alpha()
    dry_tree_image=pygame.image.load('Data/dry_tree.png').convert_alpha()
    def __init__(tree_instance,x,y,variant):
        super().__init__()
        if variant=='0':
            tree_instance.image=tree.tree_image
        elif variant=='1':
            tree_instance.image=tree.cut_tree_image
        elif variant=='2':
            tree_instance.image=tree.dry_tree_image
        tree_instance.rect=tree_instance.image.get_rect(bottomleft=((x+1)*48,(y+1)*48))
class bubble(pygame.sprite.Sprite):
    bubble_image=pygame.image.load('Data/bubble.png').convert_alpha()
    def __init__(bubble_instance,x,y,bubble_size):
        super().__init__()
        bubble_instance.size=bubble_size
        bubble_instance.image=pygame.transform.scale_by(bubble.bubble_image,bubble_size)
        bubble_instance.rect=bubble_instance.image.get_rect(center=(x,y))
    def update(bubble_instance,delta_time):
        game_window.blit(bubble_instance.image,bubble_instance.rect)
        bubble_instance.rect.centery=bubble_instance.rect.centery-20*delta_time
        for water_line in water_hitlines:
            if bubble_instance.rect.clipline(water_line)!=():
                #add waves herhee



                bubble_instance.kill()
class tutorial_block(pygame.sprite.Sprite):
    def __init__(tut_block,x_image_len,name,x,y):
        super().__init__()
        tut_block.image_list=[]
        tut_block.spirte_sheet=pygame.image.load(f'Data/blocks/tut_blocks/{name}.png').convert_alpha()
        for image_x in range(0,tut_block.spirte_sheet.get_width()//x_image_len):
            image=pygame.Surface((x_image_len,tut_block.spirte_sheet.get_height()),pygame.SRCALPHA)
            final_image=pygame.Surface((x_image_len*2,tut_block.spirte_sheet.get_height()*2),pygame.SRCALPHA)
            image.blit(tut_block.spirte_sheet,(0,0),(image_x*x_image_len,0,x_image_len,tut_block.spirte_sheet.get_height()))
            final_image=pygame.transform.scale2x(image,final_image)
            tut_block.image_list.append(final_image)
        tut_block.image_frame=0
        tut_block.image=tut_block.image_list[tut_block.image_frame]
        tut_block.rect=tut_block.image.get_rect(center=(x*48,y*48))
    def update(tut_block,delta_time):
        if tut_block.image_frame>=len(tut_block.image_list):
            tut_block.image_frame=0
        tut_block.image=tut_block.image_list[int(tut_block.image_frame)]
        tut_block.image_frame+=5*delta_time

class game():
    def __init__(game):
        game.offset=pygame.math.Vector2()#offest of objects
        game.player_offset=pygame.math.Vector2()#offset of player from scren center
        game.screen_shake=pygame.math.Vector2()
        game.draw_rect=pygame.Rect(0,0,display_size[0]+40,display_size[1]+40)
        game.update_rect=pygame.Rect(0,0,display_size[0]*2,display_size[1]+400)
        game.earthquake=False
        game.earthquake_timer=0
        game.spike_shake_timer=0
        game.pressure_switch_pan=False
        game.fat_guy_hit=False
    def draw(cam,delta_time,above_player_sprite_group_list,player_sprite_group,below_player_sprite_group_list):
        for player_sprite in player_sprite_group:
            if player.state=='explode':
                cam.screen_shake.xy=(numpy.random.randint(-10,10),numpy.random.randint(-10,10))
            else:
                cam.screen_shake.xy=(0,0)
                if cam.spike_shake_timer>0:
                    cam.spike_shake_timer-=delta_time
                    cam.screen_shake.x=numpy.random.randint(-15,15)
            if cam.earthquake:
                if cam.earthquake_timer>=30:#1/2 min
                    cam.earthqake_timer=0
                    cam.earthquake=False
                    cam.screen_shake.xy=(0,0)
                else:
                    if cam.earthquake_timer==0:
                        cam.screen_shake.y=20
                    else:
                        cam.screen_shake.y=numpy.random.randint(-15,15)
                    cam.earthquake_timer+=delta_time
            if not cam.fat_guy_hit and player_sprite.pos.x>player.fat_guy_pan:#fat_guy pan loc
                cam.player_offset.x-=100*delta_time
                if cam.player_offset.x<=-(display_size[1]//2-50):
                    cam.player_offset.x=-(display_size[1]//2-50)
                cam.offset.x=player_sprite.pos.x-(game_window.get_width()//2)+cam.player_offset.x
            else:
                if cam.pressure_switch_pan:
                    if cam.player_offset.x>=(display_size[1]//2+150):
                        cam.player_offset.x=(display_size[1]//2+150)
                    else:
                        cam.player_offset.x+=300*delta_time
                else:
                    if player_sprite.idle_timer>=2:
                        if cam.player_offset.x>=display_size[1]//2-50:
                            cam.player_offset.x-=100*delta_time
                            if cam.player_offset.x<display_size[1]//2-50:cam.player_offset.x=display_size[1]//2-50
                        else:
                            if cam.player_offset.x<=-(display_size[1]//2-50):
                                cam.player_offset.x=-(display_size[1]//2-50)
                            else:
                                if player_sprite.direction=='right':
                                    cam.player_offset.x+=100*delta_time#pan speed for idle pan
                                else:
                                    cam.player_offset.x-=100*delta_time#pan speed for idle pan
                    else:
                        if cam.player_offset.x>0:
                            cam.player_offset.x-=100*delta_time
                            if cam.player_offset.x<0:cam.player_offset.x=0
                        elif cam.player_offset.x<0:
                            cam.player_offset.x+=100*delta_time
                            if cam.player_offset.x>0:cam.player_offset.x=0
                if player_sprite.pos.x<display_size[1]//2:
                    cam.player_offset.x=display_size[1]//2-player_sprite.pos.x
                    cam.offset.x=0
                else:
                    cam.offset.x=player_sprite.pos.x-(game_window.get_width()//2)+cam.player_offset.x
            if player_sprite.pos.y>game_window.get_height()-300:
                cam.player_offset.y=player_sprite.pos.y-(game_window.get_height()-300)
                cam.offset.y=player_sprite.pos.y-(game_window.get_height()-300)
            else:
                cam.offset.y=0
                cam.player_offset.y=0
            cam.draw_rect.center=player_sprite.rect.center
            cam.draw_rect.centerx+=cam.player_offset.x
            #cam.draw_rect.centery+=player_sprite.rect.top-cam.player_offset.y-((display_size[1]//2)-300)-player_sprite.image.get_height()//2
            for sprite_group in below_player_sprite_group_list:
                for sprite in sprite_group:
                    if cam.draw_rect.colliderect(sprite.rect):
                        game_window.blit(sprite.image,(sprite.rect.x-cam.offset.x+cam.screen_shake.x,sprite.rect.y-cam.offset.y+cam.screen_shake.y))
                        if type(sprite)==big_fat_guy and sprite.state=='rope':
                            sprite.hook_offset=cam.offset
            game_window.blit(player_sprite.image,((game_window.get_width()//2)-player_sprite.image.get_width()//2-cam.player_offset.x+cam.screen_shake.x,player_sprite.rect.top-cam.player_offset.y+cam.screen_shake.y))
            for sprite_group in above_player_sprite_group_list:
                for sprite in sprite_group:
                    if cam.draw_rect.colliderect(sprite.rect):
                        game_window.blit(sprite.image,(sprite.rect.x-cam.offset.x+cam.screen_shake.x,sprite.rect.y-cam.offset.y+cam.screen_shake.y))
    def update(update_instance,update_sprite_group_list,delta_time):
        for player in player_sprite_group:
            player.update(delta_time)
            update_instance.update_rect.center=player.rect.center
            block_sprite_instance_group.empty()
            for block in block_sprite_group:
                if block.rect.colliderect(update_instance.update_rect):
                    block_sprite_instance_group.add(block)
            for sprite_group in update_sprite_group_list:
                for sprite in sprite_group:
                    if update_instance.update_rect.colliderect(sprite.rect):
                        sprite.update(delta_time)
            reactive_block_sprite_instance_group.empty()
            for reactive_block in reactive_block_sprite_group:
                if reactive_block.rect.colliderect(update_instance.update_rect):
                    reactive_block_sprite_instance_group.add(reactive_block)
            update_instance.pressure_switch_pan=False
            for reactive_instance_block in reactive_block_sprite_instance_group:
                reactive_instance_block.update(delta_time)
                if type(reactive_instance_block)==pressure_switch and update_instance.pressure_switch_pan_x<player.pos.x<update_instance.pressure_switch_pan_x+1152 and not reactive_instance_block.clicked:
                    update_instance.pressure_switch_pan=True

player_sprite_group=pygame.sprite.Group()

fish_sprite_group=pygame.sprite.Group()
rat_sprite_group=pygame.sprite.Group()
dog_sprite_group=pygame.sprite.Group()
ostrich_sprite_group=pygame.sprite.Group()
bird_sprite_group=pygame.sprite.Group()
big_fat_guy_sprite_group=pygame.sprite.Group()

block_sprite_group=pygame.sprite.Group()
reactive_block_sprite_group=pygame.sprite.Group()
tree_sprite_group=pygame.sprite.Group()
bubble_sprite_group=pygame.sprite.Group()

block_sprite_instance_group=pygame.sprite.Group()
reactive_block_sprite_instance_group=pygame.sprite.Group()

tutorial_block_sprite_group=pygame.sprite.Group()

bomb_rect_list=[]
water_blocks_rect_list=[]
water_hitlines=[]

#loading map
with open('Data/worlds/0/0_blocks.csv') as map:
    world_reader=csv.reader(map,delimiter=',')
    for row_number,row in enumerate(world_reader):
        for block_number,block_id in enumerate(row):
            if block_id!='-1':
                block_sprite_group.add(block(block_id,block_number,row_number))
bomb_rect_load_list=[]
with open('Data/worlds/0/0_bomb_rects.csv') as map:
    world_reader=csv.reader(map,delimiter=',')
    for row in world_reader:
        bomb_rect_load_list.append(row)#transfose bombrect-map list here
bomb_rect_load_list=[[row[i] for row in bomb_rect_load_list] for i in range(len(bomb_rect_load_list[0]))]
bomb_rect_list.clear()
bomb_rect_topright=[]
for row_number,row in enumerate(bomb_rect_load_list):  
    for rect_number,block_id in enumerate(row):
        if block_id=='0':
            bomb_rect_topright=[(rect_number-1)*48,(row_number-1)*48]
        if block_id=='1':
            bomb_rect_list.append(pygame.Rect(bomb_rect_topright[1],bomb_rect_topright[0],((row_number+1)*48)-bomb_rect_topright[1],((rect_number+1)*48)-bomb_rect_topright[0]))
with open('Data/worlds/0/0_trees.csv') as map:
    world_reader=csv.reader(map,delimiter=',')
    for row_number,row in enumerate(world_reader):
        for tree_number,tree_id in enumerate(row):    
            if tree_id!='-1': 
                tree_sprite_group.add(tree(tree_number,row_number,tree_id))
with open('Data/worlds/0/0_water_blocks.csv') as map:
    world_reader=csv.reader(map,delimiter=',')
    for row_number,row in enumerate(world_reader):
        for block_number,block_id in enumerate(row):
            if block_id=='0':
                water_blocks_rect_list.append(pygame.Rect(block_number*48,row_number*48,48,48))
with open('Data/worlds/0/0_tut_blocks.csv') as map:
    world_reader=csv.reader(map,delimiter=',')
    for row_number,row in enumerate(world_reader):
        for block_number,block_id in enumerate(row):    
            if block_id=='0':
                tutorial_block_sprite_group.add(tutorial_block(151,'move_right',block_number,row_number))
            elif block_id=='1':
                tutorial_block_sprite_group.add(tutorial_block(151,'move_left',block_number,row_number))
            elif block_id=='2':
                tutorial_block_sprite_group.add(tutorial_block(221,'move_up',block_number,row_number))
            elif block_id=='3':
                tutorial_block_sprite_group.add(tutorial_block(183,'pick_up',block_number,row_number))
            elif block_id=='4':
                tutorial_block_sprite_group.add(tutorial_block(178,'interact',block_number,row_number))
            elif block_id=='5':
                tutorial_block_sprite_group.add(tutorial_block(381,'rock_throw',block_number,row_number))
            elif block_id=='6':
                tutorial_block_sprite_group.add(tutorial_block(158,'sniff',block_number,row_number))
            elif block_id=='7':
                tutorial_block_sprite_group.add(tutorial_block(185,'rock_roll',block_number,row_number))
            elif block_id=='8':
                tutorial_block_sprite_group.add(tutorial_block(101,'squishy',block_number,row_number))
            elif block_id=='9':
                tutorial_block_sprite_group.add(tutorial_block(324,'dodge',block_number,row_number))
                tut_end=block_number*48+500
            elif block_id=='10':
                tutorial_block_sprite_group.add(tutorial_block(301,'sprint',block_number,row_number))
            elif block_id=='11':
                tutorial_block_sprite_group.add(tutorial_block(100,'shiny',block_number,row_number))
            elif block_id=='12':
                tutorial_block_sprite_group.add(tutorial_block(81,'ninja_time',block_number,row_number))
            elif block_id=='13':
                tutorial_block_sprite_group.add(tutorial_block(196,'apple_tut',block_number,row_number))
with open('Data/worlds/0/0_checkpoints.csv') as map:
    world_reader=csv.reader(map,delimiter=',')
    check_point_list=[]
    for row_number,row in enumerate(world_reader):
        for number,id in enumerate(row):    
            if id!='-1': 
                check_point_list.append(pygame.Rect(number*48,row_number*48,48,48))

game=game()

player_sprite_group.add(player(2067,560))#2067,560,30111,75984,960,boss-109968

def map_load():
    reactive_block_sprite_group.empty()
    with open('Data/worlds/0/0_reactive_blocks.csv') as map:
        world_reader=csv.reader(map,delimiter=',')
        for row_number,row in enumerate(world_reader):
            for block_number,block_id in enumerate(row):    
                if block_id=='0': 
                    reactive_block_sprite_group.add(grass(block_number,row_number))
                elif block_id=='1':
                    reactive_block_sprite_group.add(apple(block_number,row_number))
                elif block_id=='2':
                    reactive_block_sprite_group.add(bomb(block_number,row_number))
                elif block_id=='3':
                    reactive_block_sprite_group.add(bomb_land(block_number,row_number))
                elif block_id=='4':
                    reactive_block_sprite_group.add(chain(block_number,row_number))
                elif block_id=='5':
                    reactive_block_sprite_group.add(rock(block_number,row_number))
                elif block_id=='6':
                    reactive_block_sprite_group.add(switch(block_number,row_number))
                elif block_id=='7':
                    reactive_block_sprite_group.add(flower(block_number,row_number))
                elif block_id=='8':
                    for x_pos in range(block_number*48,(block_number+1)*48,16):
                        pass

                    #import water springs pos
                elif block_id=='9':
                    reactive_block_sprite_group.add(pressure_switch(block_number,row_number))
                elif block_id=='10':
                    reactive_block_sprite_group.add(little_rock(block_number*48,(row_number+1)*48-12))#x*48,(y+1)*48-12
                elif block_id=='11':
                    reactive_block_sprite_group.add(rock_pile(block_number*48,(row_number+2)*48-39))
                elif block_id=='12':
                    reactive_block_sprite_group.add(spike(block_number,row_number,1))
                elif block_id=='13':
                    reactive_block_sprite_group.add(spike(block_number,row_number,2))
                elif block_id=='14':
                    reactive_block_sprite_group.add(nest(block_number,row_number))
    rat_sprite_group.empty()
    fish_sprite_group.empty()
    big_fat_guy_sprite_group.empty()
    dog_sprite_group.empty()
    fish_sprite_group.empty()
    with open('Data/worlds/0/0_mobs.csv') as map:
        world_reader=csv.reader(map,delimiter=',')
        for mob_y,row in enumerate(world_reader):
            for mob_x,mob_id in enumerate(row):  
                if mob_id=='0':
                    rat_sprite_group.add(rat(mob_x,mob_y))
                elif mob_id=='1':
                    fish_sprite_group.add(fish(mob_x,mob_y,'right'))
                elif mob_id=='2':
                    big_fat_guy_sprite_group.add(big_fat_guy(mob_x,mob_y))
                elif mob_id=='3':
                    dog_sprite_group.add(dog(mob_x,mob_y))
                elif mob_id=='4':
                    fish_sprite_group.add(fish(mob_x,mob_y,'left'))
                elif mob_id=='5':
                    fish_sprite_group.add(ostrich(mob_x,mob_y,'left'))
                elif mob_id=='6':
                    fish_sprite_group.add(ostrich(mob_x,mob_y,'right'))
    for fat_guy in big_fat_guy_sprite_group:
        for player in player_sprite_group:
            with open('Data/worlds/0/0_fat_guy_effects.csv') as map:
                world_reader=csv.reader(map,delimiter=',')
                for row_number,row in enumerate(world_reader):
                    for x,id in enumerate(row):    
                        if id=='0': 
                            player.fat_guy_pan=x*48
                        elif id=='1':
                            fat_guy.left_rope_limit=x*48
                        elif id=='2':
                            fat_guy.right_rope_limit=x*48
                        elif id=='3':
                            game.pressure_switch_pan_x=x*48

map_load()
dog.tut_end=tut_end

prevoius_time=time.perf_counter()
while True:
    delta_time=time.perf_counter()-prevoius_time
    prevoius_time=time.perf_counter()
    game_window.fill((255,255,255))
    for player in player_sprite_group:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.mixer.quit()
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
                    if game_settings['mode']=='in_game':
                        game_settings['mode']='paused'
                    elif game_settings['mode']=='paused':
                        game_settings['mode']='in_game'
                if event.key==pygame.K_w:
                    if player.state!='explode' and player.state!='dodge':
                        player.jump=True
                        player.image_frame=0
                        player.state='sprint'
    if game_settings['mode']=='in_game':
        pygame.mouse.set_visible(False)
        for player in player_sprite_group:
            if player.life<=0:
                game_settings['mode']='game_over'
            if player.state!='aim':
                game.update([fish_sprite_group,rat_sprite_group,dog_sprite_group,ostrich_sprite_group,bird_sprite_group,big_fat_guy_sprite_group,bubble_sprite_group,tutorial_block_sprite_group],
                            delta_time)
            elif player.state=='aim' or player.state=='throw':
                player.update(delta_time)
                big_fat_guy_sprite_group.update(delta_time)
        game.draw(delta_time,[reactive_block_sprite_instance_group,fish_sprite_group,rat_sprite_group,dog_sprite_group,ostrich_sprite_group,bird_sprite_group,bubble_sprite_group],
                    player_sprite_group,
                    [big_fat_guy_sprite_group,tree_sprite_group,block_sprite_instance_group,tutorial_block_sprite_group])
        
        for player in player_sprite_group:
            print(str(player.pos),str(player.stamina)+player.state+'\033c',end='')
        keys_pressed=pygame.key.get_pressed()
            #elif event.type==pygame.KEYUP:
            #    if event.key==pygame.K_w:
            #        for player in player_sprite_group:
            #            player.image_frame=0
            #            #player.jump_counter=0
        for player in player_sprite_group:
            if player.prev_flower_count!=player.flower_count:
                player.prev_flower_count=player.flower_count
                player.flower_timer=4
            text(str(player.flower_count),(0,0,0),30+player.flower_timer*10,(display_size[0]-100,30))
            if player.flower_timer>2:
                player.flower_timer-=2*delta_time
                game_window.blit(pygame.transform.scale_by(flower.image,player.flower_timer),(display_size[0]-150-player.flower_timer*24,10))
            else:
                player.flower_timer=2
                game_window.blit(pygame.transform.scale2x(flower.image),(display_size[0]-150-48,10))
            if player.hand=='rock':
                game_window.blit(pygame.transform.scale2x(little_rock.image_list[0]),(display_size[0]-100,120))
            if game_settings['negative_screen']:#when hit fat_guy
                white_screen=pygame.Surface(game_window.get_size())
                white_screen.fill((255,255,255))
                white_screen.blit(game_window,(0,0),special_flags=pygame.BLEND_SUB)
                game_window=white_screen
            if player.prev_life>player.life:
                for life_count in range(player.prev_life-1):
                    game_window.blit(new_life_image_list[-1],(display_size[0]-230-30*life_count,30))
                if player.life_image_frame>=len(life_death_image_list):
                    player.life_image_frame=0
                    player.prev_life=player.life
                else:
                    game_window.blit(life_death_image_list[int(player.life_image_frame)],(display_size[0]-230-30*player.life,24))
                    player.life_image_frame+=9*delta_time#chnage to 10 later?
            elif player.prev_life<player.life:
                for life_count in range(player.prev_life):
                    game_window.blit(new_life_image_list[-1],(display_size[0]-230-30*life_count,30))
                if player.life_image_frame>=len(new_life_image_list):
                    player.life_image_frame=0
                    game_window.blit(new_life_image_list[-1],(display_size[0]-230-30*player.life+30,30))
                    player.prev_life=player.life
                else:
                    game_window.blit(new_life_image_list[int(player.life_image_frame)],(display_size[0]-230-30*player.life+30,30))
                    player.life_image_frame+=5*delta_time#chnage to 10 later?
            else:
                for life_count in range(player.prev_life):
                    game_window.blit(new_life_image_list[-1],(display_size[0]-230-30*life_count,30))
            if player.state!='explode'and player.state!='dodge':
                if keys_pressed[pygame.K_d]:
                    if player.direction=='left':
                        player.velocity.x=0
                    player.direction='right'
                    if player.water:
                        if player.state!='swim_fast':
                            player.state='swim'
                    else:
                        if player.state!='sprint' and player.state!='dodge':
                            player.state='run'
                    if keys_pressed[pygame.K_LSHIFT]:
                        if player.water:
                            player.state='swim_fast'
                        else:
                            player.state='sprint'
                    if keys_pressed[pygame.K_SPACE]:
                        if not player.water:
                            if player.stamina>=100:
                                player.state='dodge'
                            else:
                                player.state='run'
                        else:
                            player.state='swim'
                if keys_pressed[pygame.K_a]:
                    if player.direction=='right':
                        player.velocity.x=0
                    player.direction='left'
                    if player.water:
                        if player.state!='swim_fast':
                            player.state='swim'
                    else:
                        if player.state!='sprint' and player.state!='dodge':
                            player.state='run'
                    if keys_pressed[pygame.K_LSHIFT]:
                        if player.water:
                            player.state='swim_fast'
                        else:
                            player.state='sprint'
                    if keys_pressed[pygame.K_SPACE]:
                        if not player.water:
                            if player.stamina>=100:
                                player.state='dodge'
                            else:
                                player.state='run'
                        else:
                            player.state='swim'
                if keys_pressed[pygame.K_SPACE] and player.state!='dodge':
                    if player.hand=='rock':
                        player.state='aim'
                    else:
                        player.state='interact'
                if keys_pressed[pygame.K_s] and not player.water:
                    player.state='pick'
                if not (keys_pressed[pygame.K_a] or keys_pressed[pygame.K_d] or keys_pressed[pygame.K_s] or keys_pressed[pygame.K_w] or keys_pressed[pygame.K_SPACE] or player.state=='pant'):
                    if player.state=='aim' or player.state=='throw':
                        player.state='throw'
                    else:
                        if player.state!='pant' and player.state!='explode' and player.state!='grass':
                            player.state='idle'
        pygame.draw.rect(game_window,(0,0,0),(display_size[0]//2-game.player_offset.x-(((player.stamina/1000)*200)//2),player.rect.top-game.player_offset.y-50,(player.stamina/1000)*200,6))
        if player.stamina>0:
            pygame.draw.circle(game_window,(0,0,0),(display_size[0]//2-game.player_offset.x-(((player.stamina/1000)*200)//2),player.rect.top-game.player_offset.y-47),3)
            pygame.draw.circle(game_window,(0,0,0),(display_size[0]//2-game.player_offset.x+(((player.stamina/1000)*200)//2),player.rect.top-game.player_offset.y-47),3)
        #game_window.blit(pygame.image.load('rough.png').convert(),(0,225))#testin
        #print(str(clock.get_fps()))
        clock.tick()
    elif game_settings['mode']=='game_over':
        pygame.mouse.set_visible(True)
        game_window.blit(game_over_image,(display_size[0]//2-game_over_image.get_width()//2,100))
        game_window.blit(exit_image,(exit_rect.topleft))
        if round(menu_image_frame)>1:
            menu_image_frame=0
        else:
            menu_image_frame+=5*delta_time
        game_window.blit(retry_list[int(menu_image_frame)],(retry_rect.topleft))
        if any(pygame.mouse.get_pressed()):
            mouse_pos=pygame.mouse.get_pos()
            if game_settings['fullscreen']:
                if retry_rect.collidepoint(mouse_pos):
                    game_settings['mode']='in_game'
                    for player in player_sprite_group:
                        try:
                            player.rect.midbottom=player.last_check_point.midbottom
                        except:
                            player.rect.center=(2067,560)
                        player.pos.xy=player.rect.center
                        player.life=3
                        player.score=0
                        player.hand=''
                        player.state='idle'
                        player.flower_count=0
                        player.stamina=1000
                    map_load()
                elif exit_rect.collidepoint(mouse_pos):
                    pygame.mixer.quit()
                    pygame.quit()
                    sys.exit()
            else:
                if retry_rect.collidepoint(mouse_pos[0]*2,mouse_pos[1]*2):
                    game_settings['mode']='in_game'
                    game.earthquake=False
                    for player in player_sprite_group:
                        try:
                            player.rect.midbottom=player.last_check_point.midbottom
                        except:
                            player.rect.center=(2067,560)
                        player.pos.xy=player.rect.center
                        player.life=3
                        player.score=0
                        player.hand=''
                        player.state='idle'
                        player.flower_count=0
                        player.stamina=1000
                    map_load()
                elif exit_rect.collidepoint(mouse_pos[0]*2,mouse_pos[1]*2):
                    pygame.mixer.quit()
                    pygame.quit()
                    sys.exit()
    elif game_settings['mode']=='paused':
        pygame.mouse.set_visible(True)
        game_window.blit(paused_image,(display_size[0]//2-paused_image.get_width()//2,100))
        game_window.blit(exit_image,(exit_rect.topleft))
        if round(menu_image_frame)>1:
            menu_image_frame=0
        else:
            menu_image_frame+=5*delta_time
        game_window.blit(play_list[int(menu_image_frame)],(play_rect.topleft))
        if game_settings['negative_screen']:#when hit fat_guy
            white_screen=pygame.Surface(game_window.get_size())
            white_screen.fill((255,255,255))
            white_screen.blit(game_window,(0,0),special_flags=pygame.BLEND_SUB)
            game_window=white_screen
        if any(pygame.mouse.get_pressed()):
            mouse_pos=pygame.mouse.get_pos()
            if game_settings['fullscreen']:
                if exit_rect.collidepoint(mouse_pos):
                    pygame.mixer.quit()
                    pygame.quit()
                    sys.exit()
                elif play_rect.collidepoint(mouse_pos):
                    game_settings['mode']='in_game'
            else:
                if exit_rect.collidepoint(mouse_pos[0]*2,mouse_pos[1]*2):
                    pygame.mixer.quit()
                    pygame.quit()
                    sys.exit()
                elif play_rect.collidepoint(mouse_pos[0]*2,mouse_pos[1]*2):
                    game_settings['mode']='in_game'
    elif game_settings['mode']=='game_complete':
        if player.score>save_data['high_score']:
            save_data['high_score']=player.score
        if round(menu_image_frame)>1:
            menu_image_frame=0
        game_window.blit(game_complete_list[int(menu_image_frame)],(display_size[0]//2-game_complete_list[0].get_width()//2,50))
        if int(cookie_image_frame)<=6:
            game_window.blit(cookie_list[int(cookie_image_frame)],cookie_rect.topleft)
        game_window.blit(replay_list[int(menu_image_frame)],replay_rect.topleft)
        game_window.blit(exit_game_complete_list[int(menu_image_frame)],exit_game_complete_rect.topleft)
        text('thanguu for playin the game!! here is a cookie <3',(0,0,0),30,(display_size[0]//2-441,50+game_complete_list[0].get_height()))
        menu_image_frame+=5*delta_time
        if any(pygame.mouse.get_pressed()):
            mouse_pos=pygame.mouse.get_pos()
            if game_settings['fullscreen']:
                if exit_game_complete_rect.collidepoint(mouse_pos):
                    pygame.mixer.quit()
                    pygame.quit()
                    sys.exit()
                elif replay_rect.collidepoint(mouse_pos):
                    player.score=0
                    player.hand=''
                    player.pos.xy=(check_point_list[0])
                    player.life=3
                    game_settings['mode']='in_game'
                elif cookie_rect.collidepoint(mouse_pos):
                    cookie_image_frame+=1
            else:
                if exit_game_complete_rect.collidepoint(mouse_pos[0]*2,mouse_pos[1]*2):
                    pygame.mixer.quit()
                    pygame.quit()
                    sys.exit()
                elif replay_rect.collidepoint(mouse_pos[0]*2,mouse_pos[1]*2):
                    player.score=0
                    player.hand=''
                    player.pos.xy=(check_point_list[0])
                    player.life=3
                    game_settings['mode']='in_game'
                elif cookie_rect.collidepoint(mouse_pos[0]*2,mouse_pos[1]*2):
                    cookie_image_frame+=1
    game_window.blit(high_score_image,(10,10))
    text(str(save_data['high_score']),(0,0,0),40,(156,5))
    game_window.blit(score_image,(10,50))
    if player.score<0:player.score=0
    text(str(player.score),(0,0,0),40,(92,45))
    if game_settings['fullscreen']:
        display_window.blit(game_window,(0,0))
    else:
        display_window.blit(pygame.transform.smoothscale_by(game_window,0.5),(0,0))
    pygame.display.update()