import pygame,sys,time,csv,numpy
from scipy.interpolate import interp1d
pygame.init()
display_size=[pygame.display.Info().current_w,pygame.display.Info().current_h]
game_window=pygame.Surface((display_size[0],display_size[1]))
display_window=pygame.display.set_mode((display_size[0]//2,display_size[1]//2))
pygame.display.set_caption('tha_DOG')
pygame.display.set_icon(pygame.image.load('Data/icon/DOG.png').convert())
clock=pygame.time.Clock()
game_mode='in_game'

save_data={'world':0}

game_settings={'fullscreen':False}
game_varibles={'current_world':save_data['world']}

class player(pygame.sprite.Sprite):
    def __init__(player,spawn_x,spawn_y):
        super().__init__()
        player.velocity=pygame.math.Vector2(0,0)
        player.acceleration=pygame.math.Vector2(0,0)
        player.max_velocity=pygame.math.Vector2(200,5000)
        player.health=300
        player.stamina=1000
        player.state='idle'
        player.throw_angle=10
        player.throw_power=10
        player.idle_timer=0
        player.water=False
        player.jump=False
        player.jump_counter=0
        player.direction='right'
        player.hand=''
        player.jump_height=spawn_y
        player.flower_count=0
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
        player.run_image_spritesheet=pygame.image.load('Data/player/player_run.png').convert_alpha()
        player.swim_image_spritesheet=pygame.image.load('Data/player/player_swim.png').convert_alpha()
        player.pant_image_spritesheet=pygame.image.load('Data/player/player_pant.png').convert_alpha()
        player.jump_image_spritesheet=pygame.image.load('Data/player/player_jump.png').convert_alpha()
        player.throw_image_spritesheet=pygame.image.load('Data/player/player_throw.png').convert_alpha()
        for image_x in range(0,player.run_image_spritesheet.get_width(),107):
            player.import_image=pygame.Surface((107,211),pygame.SRCALPHA)
            player.import_image.blit(player.run_image_spritesheet,(0,0),(image_x,0,107,211))
            player.run_image_list_right.append(player.import_image)
            player.run_image_list_left.append(pygame.transform.flip(player.import_image,True,False))
        for image_x in range(0,player.pant_image_spritesheet.get_width(),109):
            player.import_image=pygame.Surface((109,210),pygame.SRCALPHA)
            player.import_image.blit(player.pant_image_spritesheet,(0,0),(image_x,0,109,210))
            player.pant_image_list_right.append(player.import_image)
            player.pant_image_list_left.append(pygame.transform.flip(player.import_image,True,False))
        for image_x in range(0,player.swim_image_spritesheet.get_width(),230):
            player.import_image=pygame.Surface((230,211),pygame.SRCALPHA)
            player.import_image.blit(player.swim_image_spritesheet,(0,0),(image_x,0,230,211))
            player.swim_image_list_right.append(player.import_image)
            player.swim_image_list_left.append(pygame.transform.flip(player.import_image,True,False))
        for image_x in range(0,player.jump_image_spritesheet.get_width(),108):
            player.import_image=pygame.Surface((108,212),pygame.SRCALPHA)
            player.import_image.blit(player.jump_image_spritesheet,(0,0),(image_x,0,108,212))
            player.jump_image_list_right.append(player.import_image)
            player.jump_image_list_left.append(pygame.transform.flip(player.import_image,True,False))
        for image_x in range(0,player.throw_image_spritesheet.get_width(),111):
            player.import_image=pygame.Surface((111,210),pygame.SRCALPHA)
            player.import_image.blit(player.throw_image_spritesheet,(0,0),(image_x,0,111,210))
            player.throw_image_list_right.append(player.import_image)
            player.throw_image_list_left.append(pygame.transform.flip(player.import_image,True,False))
        player.image=player.run_image_list_right[0]
        player.import_image=pygame.Surface((107,211),pygame.SRCALPHA)
        player.player_grass_image=player.import_image.blit(player.image,(0,100),player.image.get_rect())
        player.rect=player.image.get_rect()
        player.rect.center=spawn_x,spawn_y
        player.pos=pygame.math.Vector2(player.rect.center)
    def update(player,delta_time):
        player.water=False
        for water_rect in water_blocks_rect_list:
            if not player.water:
                if player.rect.colliderect(water_rect):
                    player.water=True
            else:
                break
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
        else:
            if player.state!='pant'or player.state!='aim':
                player.idle_timer=0
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
        elif player.state=='grass':
            player.image=player.player_grass_image
        elif player.state=='aim':#make projetile path here
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
                player.throw_power+=30*delta_time
            else:
                player.throw_angle+=20*delta_time
        elif player.state=='throw':
            if player.image_frame>len(player.throw_image_list_left):
                if player.direction=='left':
                    player.rock_obj=little_rock(player.rect.left+19,player.rect.top+28)
                else:
                    player.rock_obj=little_rock(player.rect.right-19,player.rect.top+28)
                player.rock_obj.velocity.from_polar((player.throw_power,player.throw_angle))
                player.throw_angle,player.throw_power=10,10
                player.rock_obj.velocity.y=-player.rock_obj.velocity.y
                if player.direction=='left':
                    player.rock_obj.velocity.x=-player.rock_obj.velocity.x
                player.rock_obj.acceleration.y=10
                player.rock_obj.initial_velocity=player.rock_obj.velocity
                print(player.rock_obj.velocity)
                reactive_block_sprite_group.add(player.rock_obj)
                player.state='idle'
            else:
                if player.direction=='left':
                    player.image=player.throw_image_list_left[int(player.image_frame)]
                elif player.direction=='right':
                    player.image=player.throw_image_list_right[int(player.image_frame)]
                player.image_frame+=10*delta_time
        elif player.state=='run':
            player.max_velocity.x=200
            player.image_frame+=(abs(player.velocity.x)//10)*delta_time#change later?
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
            player.image_frame+=(abs(player.velocity.x)//10)*delta_time#change later?
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
        if player.state!='idle'and player.state!='pant'and player.state!='pick' and player.state!='interact' and player.state!='fall' and player.state!='aim' and player.state!='throw':
            player.velocity+=player.acceleration*delta_time
            player.pos+=player.velocity*delta_time
            player.rect=player.image.get_rect(center=player.pos.xy)
        else:
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
        for block in pygame.sprite.spritecollide(player,block_sprite_group,dokill=False):
            player.jump_height=player.pos.y
            player.jump_counter=0
            if block.id == '0' or block.id == '1' or block.id == '2':
                player.rect.bottom=block.rect.top
                player.pos.xy=player.rect.center
            elif block.id == '10':
                player.rect.bottom=block.rect.top+4
                player.pos.xy=player.rect.center
            elif block.id == '12':
                player.rect.bottom=block.rect.top+30
                player.pos.xy=player.rect.center
            elif block.id == '13':
                player.rect.bottom=block.rect.top+30
                player.pos.xy=player.rect.center
            elif block.id == '70':
                player.rect.bottom=block.rect.top
                player.pos.xy=player.rect.center
            #if pygame.sprite.collide_mask(player,block):
            elif block.id == '3':#ramps
                player.rect.bottom=round(0.3488603*(block.rect.x-player.pos.x))+block.rect.bottom-52#ramp_up
                player.pos.xy=player.rect.center
            elif block.id == '4':
                player.rect.bottom=round(0.3488603*(block.rect.x-player.pos.x))+block.rect.bottom-37
                player.pos.xy=player.rect.center
            elif block.id == '5':
                player.rect.bottom=round(0.3488603*(block.rect.x-player.pos.x))+block.rect.bottom-22
                player.pos.xy=player.rect.center
            elif block.id == '92':
                player.rect.bottom=16-(round(0.3488603*abs(player.pos.x-block.rect.x)))+block.rect.bottom-52#ramp_down
                player.pos.xy=player.rect.center
            elif block.id == '93':
                player.rect.bottom=16-(round(0.3488603*abs(player.pos.x-block.rect.x)))+block.rect.bottom-37
                player.pos.xy=player.rect.center
            elif block.id == '94':
                player.rect.bottom=16-(round(0.3488603*abs(player.pos.x-block.rect.x)))+block.rect.bottom-22
                player.pos.xy=player.rect.center
            #rock
            #elif block.id == '6':#top curve right
            #    if player.pos.x-block.rect.x>18:
            #        player.rect.bottom=round(1.320033*(player.pos.x-block.rect.x)-(0.0099421*((player.pos.x-block.rect.x)**2)))+block.rect.bottom-26
            #        player.pos.xy=player.rect.center
            #elif block.id == '7':
            #    player.rect.bottom=block.rect.top+23
            #    player.pos.xy=player.rect.center
            #elif block.id == '8':#top curve left
            #    if player.pos.x-block.rect.x<=23:
            #        player.rect.bottom= 21-round(0.8659639*(player.pos.x-block.rect.x))+block.rect.bottom-26
            #        player.pos.xy=player.rect.center
            #elif block.id == '35':#sideleft
            #    if pygame.sprite.collide_mask(player,block):
            #        if player.rect.bottom!=block.rect.bottom+1:
            #            print('test')
            #            player.rect.bottom= 48-(1.743497*(player.pos.x-block.rect.x))+block.rect.bottom
            #        else:
            #            if player.state=='run_right':
            #                player.rect.right=block.rect.left+48
            #        player.pos.xy=player.rect.center
            #elif block.id == '37':#side right
            #    if player.pos.x-block.rect.x>23:
            #        player.rect.bottom= -1.145418*(player.pos.x-block.rect.x) + 26.91235+block.rect.bottom
            #        player.pos.xy=player.rect.center
        if player.jump:
            if abs(player.pos.y-player.jump_height)<150:
                if player.jump_counter<=0:
                    player.image_frame+=10*delta_time
                    if round(player.image_frame)>=len(player.jump_image_list_right)-1:
                        player.image_frame=len(player.jump_image_list_right)-1
                    if player.direction=='right':  
                        player.image=player.jump_image_list_right[round(player.image_frame)]
                        player.pos.x+=100*delta_time
                    elif player.direction=='left':  
                        player.image=player.jump_image_list_left[round(player.image_frame)]
                        player.pos.x-=100*delta_time   
                    player.stamina-=50*delta_time
                    player.pos.y-=300*delta_time
                    player.rect.center=player.pos
                else:
                    player.jump=False
        for water_line in water_hitlines:
            if player.rect.clipline(water_line)!=():
                if player.state=='run' or player.state=='sprint':
                    if numpy.random.randint(0,7)==1:
                        bubble_sprite_group.add(bubble(numpy.random.randint(player.rect.x,player.rect.x+player.image.get_width()),numpy.random.randint(water_line[1][1],player.rect.bottom),round(numpy.random.uniform(0.1,1.5),ndigits=1)))
                for water_dot in water_dot_sprite_group:
                    if player.rect.centerx-15<water_dot.dest_pos.x<player.rect.centerx+15:
                        water_dot.force=30

class dog(pygame.sprite.Sprite):
    dog_run_image_sprite_sheet=pygame.image.load('Data/dog/dog_run.png').convert_alpha()
    dog_run_image_list_right=[]
    dog_run_image_list_left=[]
    for image_x in range(0,dog_run_image_sprite_sheet.get_width(),116):
            import_image=pygame.Surface((116,71),pygame.SRCALPHA)
            import_image.blit(dog_run_image_sprite_sheet,(0,0),(image_x,0,116,71))
            dog_run_image_list_left.append(import_image)
            dog_run_image_list_right.append(pygame.transform.flip(import_image,True,False))
    def __init__(dog_instance,x,y):
        super().__init__()
        dog_instance.velocity=pygame.math.Vector2(0,0)
        dog_instance.acceleration=pygame.math.Vector2(0,100)
        dog_instance.max_velocity=pygame.math.Vector2(250,100)
        dog_instance.health=500
        dog_instance.state='idle'
        dog_instance.direction='right'
        dog_instance.prev_direction=dog_instance.direction
        dog_instance.lose_sight_timer=0
        dog_instance.image_frame=0
        dog_instance.image=dog.dog_run_image_list_right[0]
        dog_instance.rect=dog_instance.image.get_rect(topleft=(x*48,y*48-16))
        dog_instance.pos=pygame.math.Vector2(dog_instance.rect.center)
        dog_instance.vission_line=[list(dog_instance.rect.topright),[0,0]]
        dog_instance.mask=pygame.mask.from_surface(dog_instance.image)
    def update(dog_instance,delta_time):
        for water_rect in water_blocks_rect_list:
            if dog_instance.state!='swim':
                if dog_instance.rect.colliderect(water_rect):
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
            if player.rect.x-dog_instance.rect.centerx<0:
                dog_instance.vission_line=[(dog_instance.rect.topright),(player.rect.topright)]
                if player.state!='grass':
                    dog_instance.direction='left'
            elif player.rect.x-dog_instance.rect.centerx>0:
                dog_instance.vission_line=[(dog_instance.rect.topleft),(player.rect.topleft)]
                if player.state!='grass':
                    dog_instance.direction='right'
            if abs(player.rect.x-dog_instance.rect.centerx)<800:
                for block in pygame.sprite.spritecollide(dog_instance,block_sprite_group,dokill=False,collided=pygame.sprite.collide_circle):
                    if block.rect.clipline(dog_instance.vission_line[0],dog_instance.vission_line[1]):
                        dog_instance.lose_sight_timer+=1*delta_time
                    else:
                        dog_instance.state='run'
                        if player.state!='grass':
                            dog_instance.lose_sight_timer=0
                if player.state=='grass':
                    dog_instance.lose_sight_timer+=1*delta_time
            else:
                dog_instance.lose_sight_timer+=1*delta_time
        for rat in pygame.sprite.spritecollide(dog_instance,rat_sprite_group,dokill=False,collided=pygame.sprite.collide_circle):
            dog_instance.state='chase_rat'
            if rat.pos.x-dog_instance.pos.x>0:
                dog_instance.direction='right'
            elif rat.pos.x-dog_instance.pos.x<0:
                dog_instance.direction='left'
            if rat.rect.colliderect(dog_instance.rect):
                rat.dead=True
                dog_instance.state='stomp_rat'
        if dog_instance.lose_sight_timer>=4 and dog_instance.state!='chase_rat':
            dog_instance.state='idle'
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
            dog_instance.max_velocity.y=0
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
        if dog_instance.velocity.x>=dog_instance.max_velocity.x:
            dog_instance.velocity.x=dog_instance.max_velocity.x
        if dog_instance.velocity.x<=(-dog_instance.max_velocity.x):
            dog_instance.velocity.x=-(dog_instance.max_velocity.x)
        if dog_instance.velocity.y>=dog_instance.max_velocity.y:
            dog_instance.velocity.y=dog_instance.max_velocity.y
        dog_instance.velocity+=dog_instance.acceleration*delta_time
        dog_instance.pos+=dog_instance.velocity*delta_time
        dog_instance.rect.center=dog_instance.pos.xy
        for block in pygame.sprite.spritecollide(dog_instance,block_sprite_group,dokill=False):
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
        dog_instance.pos=pygame.math.Vector2(dog_instance.rect.center)

        #for dog in dog_sprite_group:
        #    print(dog.pos,dog.velocity,dog.state,'\033c',end='')
class rat(pygame.sprite.Sprite):
    rat_run_sprite_sheet=pygame.image.load('Data/rat/rat_run.png').convert_alpha()
    rat_dead_sprite_sheet=pygame.image.load('Data/rat/rat_death.png').convert_alpha()
    rat_run_right_list=[]
    rat_death_right_list=[]
    rat_run_left_list=[]
    rat_death_left_list=[]
    for image_x in range(0,rat_run_sprite_sheet.get_width()//66):
        image=pygame.Surface((66,37),pygame.SRCALPHA)
        image.blit(rat_run_sprite_sheet,(0,0),(image_x*66,0,66,37))
        rat_run_left_list.append(image)
        rat_run_right_list.append(pygame.transform.flip(image,True,False))
    for image_x in range(0,rat_dead_sprite_sheet.get_width()//66):
        image=pygame.Surface((66,37),pygame.SRCALPHA)
        image.blit(rat_dead_sprite_sheet,(0,0),(image_x*66,0,66,37))
        rat_death_left_list.append(image)
        rat_death_right_list.append(pygame.transform.flip(image,True,False))
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
        for player in pygame.sprite.spritecollide(rat_instance,player_sprite_group,dokill=False,collided=pygame.sprite.collide_mask):
            if player.state=='jump':
                rat_instance.dead=True
            elif player.state=='jump_right':
                rat_instance.dead=True
            elif player.state=='jump_left':
                rat_instance.dead=True
        if rat_instance.dead:
            if rat_instance.frame>len(rat.rat_death_right_list)-1:
                rat_instance.kill()
            if rat_instance.velocity.x>0:
                rat_instance.image=rat.rat_death_right_list[int(rat_instance.frame)]
            elif rat_instance.velocity.x<0:
                rat_instance.image=rat.rat_death_left_list[int(rat_instance.frame)]
            rat_instance.frame+=8*delta_time
        else:
            for block in pygame.sprite.spritecollide(rat_instance,block_sprite_group,dokill=False):
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
            rat_instance.frame+=10*delta_time
class fish(pygame.sprite.Sprite):#fishes are not the bad guys
    fish_swim_spritesheet=pygame.image.load('Data/fish/fish_swim.png').convert_alpha()
    fish_death_spritesheet=pygame.image.load('Data/fish/fish_death.png').convert_alpha()
    fish_swim_imagelist_right=[]
    fish_swim_imagelist_left=[]
    fish_death_imagelist_right=[]
    fish_death_imagelist_left=[]
    for image_x in range(0,fish_swim_spritesheet.get_width()//49):
        image=pygame.Surface((49,21),pygame.SRCALPHA)
        image.blit(fish_swim_spritesheet,(0,0),(image_x*49,0,49,21))
        fish_swim_imagelist_left.append(image)
        fish_swim_imagelist_right.append(pygame.transform.flip(image,True,False))
    for image_x in range(0,fish_death_spritesheet.get_width()//47):
        image=pygame.Surface((47,19),pygame.SRCALPHA)
        image.blit(fish_death_spritesheet,(0,0),(image_x*47,0,47,19))
        fish_death_imagelist_left.append(image)
        fish_death_imagelist_right.append(pygame.transform.flip(image,True,False))
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
            for block in pygame.sprite.spritecollide(fish_instance,block_sprite_group,dokill=False):
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
            for block in pygame.sprite.spritecollide(fish_instance,block_sprite_group,dokill=False):
                if block.id=='147' or block.id=='177' or block.id=='206' or block.id=='145' or block.id=='174' or block.id=='204':
                    if fish_instance.direction=='left':
                        fish_instance.direction='right'
                elif block.id=='152' or block.id=='180' or block.id=='209' or block.id=='154' or block.id=='183' or block.id=='211':
                    if fish_instance.direction=='right':
                        fish_instance.direction='left'
            for player in player_sprite_group:
                if player.water:#fix fish goin thru land whne playyer not in same pond
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
                        if player.pos.x>fish_instance.pos.x:
                            fish_instance.velocity.x=35
                            fish_instance.direction='right'
                        else:
                            fish_instance.velocity.x=-35
                            fish_instance.direction='left'
                        if player.pos.y>fish_instance.pos.y:
                            fish_instance.velocity.y=8
                        else:
                            fish_instance.velocity.y=-8
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
                        fish_instance.velocity.xy=-15,0
                    elif fish_instance.direction=='right':
                        fish_instance.image=fish.fish_swim_imagelist_right[int(fish_instance.image_frame)]
                        fish_instance.velocity.xy=15,0
                    if not fish_instance.water:
                        fish_instance.velocity.y=30
            for water_line in water_hitlines:
                if fish_instance.rect.clipline(water_line)!=():
                    if water_line[1][1]<=fish_instance.rect.top:
                        fish_instance.velocity.y=0
        fish_instance.pos+=fish_instance.velocity*delta_time
        fish_instance.rect.center=fish_instance.pos

class block(pygame.sprite.Sprite):
    sprite_sheet=pygame.image.load('Data/blocks/blocks.png').convert_alpha()
    block_list=[]
    for block_y in range(0,sprite_sheet.get_height()//48):
        for block_x in range(0,sprite_sheet.get_width()//48):
            image=pygame.Surface((48,48),pygame.SRCALPHA)
            image.blit(sprite_sheet,(0,0),(block_x*48,block_y*48,48,48))
            block_list.append(image)
    def __init__(block_instance,block_id,x,y):
        super().__init__()
        block_instance.id=block_id
        block_instance.image=block.block_list[int(block_id)]
        block_instance.rect=block_instance.image.get_rect(topleft=(x*48,y*48))

class grass(pygame.sprite.Sprite):
    image=pygame.image.load('Data/blocks/reactive_blocks/grass.png').convert_alpha()
    def __init__(grass_instance,x,y):
        super().__init__()
        grass_instance.image=grass.image
        grass_instance.rect=grass_instance.image.get_rect(topleft=(x*48,y*48-23))
    def update(grass_instance,delta_time):
            for player in pygame.sprite.spritecollide(grass_instance,player_sprite_group,dokill=False):
                if player.state!='grass':
                    for dog in pygame.sprite.spritecollide(player,dog_sprite_group,dokill=False,collided=pygame.sprite.collide_circle):
                        pass
                    else:
                        player.state='grass'   
class apple(pygame.sprite.Sprite):
    image=pygame.image.load('Data/blocks/reactive_blocks/apple.png').convert_alpha()
    def __init__(apple_instance,x,y):
        super().__init__()
        apple_instance.image=apple.image
        apple_instance.rect=apple_instance.image.get_rect(topleft=(x*48,y*48))
    def update(apple_instance,delta_time):
        for player in pygame.sprite.spritecollide(apple_instance,player_sprite_group,dokill=False):
            player.hand='apple'
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
                flower_instance.kill()
class bomb(pygame.sprite.Sprite):
    image_list=[]
    bomb_sprite_sheet=pygame.image.load('Data/blocks/reactive_blocks/bomb.png').convert_alpha()
    for image_x in range(0,bomb_sprite_sheet.get_width()//249):
        image=pygame.Surface((249,248),pygame.SRCALPHA)
        image.blit(bomb_sprite_sheet,(0,0),(image_x*249,0,249,248))
        image_list.append(image)
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
            bomb_instance.explode=True
            if player.state=='run_right':#does not work
                player.velocity.xy=150,100
                player.state='idle'
            elif player.state=='run_left':
                player.velocity.xy=-150,100
                player.state='idle'
            elif player.state=='jump_right':
                player.velocity.xy=150,100
                player.state='idle'
            elif player.state=='jump_left':
                player.velocity.xy=-150,100
                player.state='idle'
            elif player.state=='jump':
                player.velocity.y=150
                player.state='idle'
            elif player.state=='idle':
                player.velocity.y=150
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
    bomb_land_sprite_sheet=pygame.image.load('Data/blocks/reactive_blocks/bomb_land.png').convert_alpha()
    for image_x in range(0,bomb_land_sprite_sheet.get_width()//249):
        image=pygame.Surface((249,201),pygame.SRCALPHA)
        image.blit(bomb_land_sprite_sheet,(0,0),(image_x*249,0,249,201))
        image_list.append(image)
    def __init__(bomb,x,y):
        super().__init__()
        bomb.bomb_image_list=bomb_land.image_list
        bomb.image=bomb.bomb_image_list[0]
        bomb.rect=bomb.image.get_rect(topleft=((x-2)*48,(y-2)*48))
        bomb.frame=0
        bomb.mask=pygame.mask.from_surface(bomb.image)
        bomb.explode=False
    def update(bomb,delta_time):
        for player in pygame.sprite.spritecollide(bomb,player_sprite_group,dokill=False,collided=pygame.sprite.collide_mask): 
            bomb.explode=True
            if player.state=='run_right':
                player.velocity.xy=150,100
                player.state='idle'
            elif player.state=='run_left':
                player.velocity.xy=-150,100
                player.state='idle'
            elif player.state=='jump_right':
                player.velocity.xy=150,100
                player.state='idle'
            elif player.state=='jump_left':
                player.velocity.xy=-150,100
                player.state='idle'
            elif player.state=='jump':
                player.velocity.y=150
                player.state='idle'
            elif player.state=='idle':
                player.velocity.y=150
        if bomb.explode:
            bomb.frame+=4*delta_time
            if bomb.frame>len(bomb.bomb_image_list)-1:
                bomb.kill()
            else:
                bomb.image=bomb.bomb_image_list[int(bomb.frame)]
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
    def update(rock_instance,delta_time):
        rock_instance.image=pygame.transform.rotate(rock_instance.image,rock_instance.angle)#add colision and stuff later
class little_rock(pygame.sprite.Sprite):
    image=pygame.image.load('Data/blocks/reactive_blocks/little_rock.png').convert_alpha()
    water_resistance=pygame.math.Vector2(5,0)
    def __init__(rock_instance,x,y):
        super().__init__()
        rock_instance.image=little_rock.image
        rock_instance.angle=0
        rock_instance.rect=rock_instance.image.get_rect(topleft=(x,y))
        rock_instance.pos=pygame.math.Vector2(rock_instance.rect.center)
        rock_instance.initial_velocity=pygame.math.Vector2()#for collsions
        rock_instance.velocity=pygame.math.Vector2()
        rock_instance.acceleration=pygame.math.Vector2()
    def update(rock_instance,delta_time):
        if rock_instance.angle>=360:
            rock_instance.angle-=360
        rock_instance.image=pygame.transform.rotate(little_rock.image,rock_instance.angle)
        for player in pygame.sprite.spritecollide(rock_instance,player_sprite_group,dokill=False):
            if player.state=='pick':
                player.hand='little_rock'
                rock_instance.kill()
        rock_instance.velocity+=rock_instance.acceleration*delta_time*2# for increaing the speed of rock falling
        rock_instance.pos+=rock_instance.velocity*delta_time*2# for increaing the speed of rock falling
        rock_instance.rect.center=rock_instance.pos.xy
        for block in pygame.sprite.spritecollide(rock_instance,block_sprite_group,dokill=False):
            rock_instance.velocity.xy=0,0
            rock_instance.acceleration.xy=0,0
            if block.id=='0' or block.id=='1' or block.id=='2':
                rock_instance.rect.bottom=block.rect.top+12
            rock_instance.pos.xy=rock_instance.rect.center
        for water_line in water_hitlines:
            if rock_instance.rect.clipline(water_line)!=():
                if rock_instance.velocity.x>10:
                    rock_instance.velocity=rock_instance.initial_velocity-little_rock.water_resistance
                    rock_instance.initial_velocity=rock_instance.velocity
                    rock_instance.velocity.y=-rock_instance.velocity.y//2
class switch(pygame.sprite.Sprite):
    image_list=[]
    switch_sprite_sheet=pygame.image.load('Data/blocks/reactive_blocks/switch.png').convert_alpha()
    for image_x in range(0,switch_sprite_sheet.get_width()//58):
        image=pygame.Surface((58,40),pygame.SRCALPHA)
        image.blit(switch_sprite_sheet,(0,0),(image_x*58,0,58,40))
        image_list.append(image)
    def __init__(switch_instance,x,y):
        super().__init__()
        switch_instance.switch_image_list=switch.image_list
        switch_instance.image=switch_instance.switch_image_list[0]
        switch_instance.rect=switch_instance.image.get_rect(bottomright=((x+1)*48+3,(y+1)*48+3))
        switch_instance.frame=0
        switch_instance.connected=False
    def update(switch_instance,delta_time):
        for player in pygame.sprite.spritecollide(switch_instance,player_sprite_group,dokill=False):
            if player.state=='interact':
                if switch_instance.frame>=len(switch_instance.switch_image_list)-1:
                    switch_instance.image=switch_instance.switch_image_list[len(switch_instance.switch_image_list)-1]
                    for bomb_rect in bomb_rect_list:
                        if bomb_rect.colliderect(switch_instance.rect):
                            for reative_block in reactive_block_sprite_group:
                                if type(reative_block)==bomb:
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
                    switch_instance.frame+=5*delta_time
class pressure_switch(pygame.sprite.Sprite):
    image_list=[]
    switch_sprite_sheet=pygame.image.load('Data/blocks/reactive_blocks/pressure_switch.png').convert_alpha()
    for image_x in range(0,switch_sprite_sheet.get_width()//42):
        image=pygame.Surface((42,20),pygame.SRCALPHA)
        image.blit(switch_sprite_sheet,(0,0),(image_x*42,0,42,20))
        image_list.append(image)
    def __init__(switch_instance,x,y):
        super().__init__()
        switch_instance.switch_image_list=pressure_switch.image_list
        switch_instance.image=switch_instance.switch_image_list[0]
        switch_instance.rect=switch_instance.image.get_rect(bottomright=((x+1)*48+3,(y+1)*48+3))
        switch_instance.connected=False
    def update(switch_instance,delta_time):
        for trig_reactive_block in pygame.sprite.spritecollide(switch_instance,reactive_block_sprite_group,dokill=False):
            if type(trig_reactive_block)==rock:
                rock.velocity.xy=0,0
                switch_instance.image=switch_instance.switch_image_list[1]
                for bomb_rect in bomb_rect_list:
                        if bomb_rect.colliderect(switch_instance.rect):
                            for reative_block in reactive_block_sprite_group:
                                if type(reative_block)==bomb:
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

class tree(pygame.sprite.Sprite):
    tree_image=pygame.image.load('Data/tree.png').convert_alpha()
    def __init__(tree_instance,x,y):
        super().__init__()
        tree_instance.image=tree.tree_image
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
                for water_dot in water_dot_sprite_group:
                    if bubble_instance.rect.centerx-15<water_dot.dest_pos.x<bubble_instance.rect.centerx+15:
                        water_dot.force=bubble_instance.size*10
                bubble_instance.kill()
class water_dot(pygame.sprite.Sprite):
    def __init__(water_dot,pos):
        super().__init__()
        water_dot.dest_pos=pygame.math.Vector2(pos)
        water_dot.pos=pos[1]
        water_dot.force=0
        water_dot.damping=1
        #water_dot.spread_dir=None
        #water_dot.spread_resistence=0.5
    def update(water_dot):
        #if water_dot.spread_dir=='left':
        #    for fellow_water_dot in water_dot_sprite_group:
        #        if fellow_water_dot.dest_pos.x==water_dot.dest_pos.x-15:
        #            fellow_water_dot.force=water_dot.force-water_dot.spread_resistence
        #            fellow_water_dot.spread_dir='left'
        #    water_dot.spread_dir=None
        #elif water_dot.spread_dir=='right':
        #    for fellow_water_dot in water_dot_sprite_group:
        #        if fellow_water_dot.dest_pos.x==water_dot.dest_pos.x+15:
        #            fellow_water_dot.force=water_dot.force-water_dot.spread_resistence
        #            fellow_water_dot.spread_dir='left'
        #    water_dot.spread_dir=None
        if water_dot.pos-water_dot.dest_pos.y>0:
            water_dot.pos-=water_dot.force
        elif water_dot.pos-water_dot.dest_pos.y<=0:
            water_dot.pos+=water_dot.force
        if abs(water_dot.force)>0:
            if water_dot.force>0:
                water_dot.force=water_dot.force-water_dot.damping
            else:
                water_dot.force=water_dot.force+water_dot.damping

class game():
    def __init__(game):
        game.offset=pygame.math.Vector2()
        game.player_offset=pygame.math.Vector2()
        game.draw_rect=pygame.Rect(0,0,display_size[0]+200,display_size[1]+400)
        game.update_rect=pygame.Rect(0,0,display_size[0]*2,display_size[1]+200)
    def draw(cam,delta_time,above_player_sprite_group_list,player_sprite_group,below_player_sprite_group_list,water_dot_sprite_group):
        for player_sprite in player_sprite_group:
            if player_sprite.idle_timer>=2:
                if cam.player_offset.x>=game_window.get_width()//2-50:
                    cam.player_offset.x=game_window.get_width()//2-50
                else:
                    if cam.player_offset.x<=-(game_window.get_width()//2-50):
                        cam.player_offset.x=-(game_window.get_width()//2-50)
                    else:
                        if player_sprite.direction=='right':
                            cam.player_offset.x+=100*delta_time#pan speed for idle pan
                        else:
                            cam.player_offset.x-=100*delta_time#pan speed for idle pan
            else:
                if cam.player_offset.x>0:
                    cam.player_offset.x-=100*delta_time#pan speed for idle pan
                    if cam.player_offset.x<0:cam.player_offset.x=0
                elif cam.player_offset.x<0:
                    cam.player_offset.x+=100*delta_time#pan speed for idle pan
                    if cam.player_offset.x>0:cam.player_offset.x=0
            if player_sprite.pos.x<game_window.get_width()//2:
                cam.player_offset.x=game_window.get_width()//2-player_sprite.pos.x
                cam.offset.x=0
            else:
                cam.offset.x=player_sprite.pos.x-(game_window.get_width()//2)+cam.player_offset.x
                #cam.player_offset.x=0
            if player_sprite.pos.y>game_window.get_height()-300:
                cam.player_offset.y=player_sprite.pos.y-(game_window.get_height()-300)
                cam.offset.y=player_sprite.pos.y-(game_window.get_height()-300)
            else:
                cam.offset.y=0
                cam.player_offset.y=0
            cam.draw_rect.center=player_sprite.rect.center
            cam.draw_rect.centerx+=cam.player_offset.x
            cam.draw_rect.centery+=cam.player_offset.y
            for sprite_group in below_player_sprite_group_list:
                for sprite in sprite_group:
                    if cam.draw_rect.colliderect(sprite.rect):
                        game_window.blit(sprite.image,(sprite.rect.x-cam.offset.x,sprite.rect.y-cam.offset.y))
            game_window.blit(player_sprite.image,((game_window.get_width()//2)-player_sprite.image.get_width()//2-cam.player_offset.x,player_sprite.rect.top-cam.player_offset.y))
            #rendering waves?
            cam.water_bodies_list_counter=0
            cam.water_bodies={}
            cam.prev_water_dot_xpos=0
            for water_dot in water_dot_sprite_group:#making seprate lists for serpate water bodies
                if water_dot.dest_pos.x-cam.prev_water_dot_xpos>17:
                    cam.water_bodies_list_counter+=1
                cam.prev_water_dot_xpos=water_dot.dest_pos.x
                try:
                    cam.water_bodies[cam.water_bodies_list_counter].append(pygame.math.Vector2(water_dot.dest_pos.x,water_dot.pos))
                except:
                    cam.water_bodies[cam.water_bodies_list_counter]=[]
                    cam.water_bodies[cam.water_bodies_list_counter].append(pygame.math.Vector2(water_dot.dest_pos.x,water_dot.pos))
            for key in cam.water_bodies:
                cam.water_dot_list=cam.water_bodies[key]
                cam.water_dot_xpos=[water_dot.x for water_dot in cam.water_dot_list]
                cam.x_array=numpy.array([water_dot.x for water_dot in cam.water_dot_list[:-1]])
                cam.y_array=numpy.array([water_dot.y for water_dot in cam.water_dot_list[:-1]])
                cam.funtion=interp1d(cam.x_array,cam.y_array,kind='cubic',fill_value='extrapolate')
                cam.water_dot_ypos=cam.funtion(cam.water_dot_xpos)
                cam.water_dot_x_list=list(cam.water_dot_xpos)
                cam.water_dot_y_list=list(cam.water_dot_ypos)
                cam.water_dot_list_final=[(round(cam.water_dot_x_list[water_dot]),round(cam.water_dot_y_list[water_dot])) for water_dot in range(len(cam.water_dot_x_list))]
                cam.prev_water_dot_pos=pygame.math.Vector2(0,0)
                for water_dot_x,water_dot_y in cam.water_dot_list_final:
                    if cam.prev_water_dot_pos.x==0:
                        cam.prev_water_dot_pos.xy=water_dot_x,water_dot_y
                    else:
                        pygame.draw.line(game_window,(0,0,0),cam.prev_water_dot_pos-cam.offset,(water_dot_x-cam.offset.x,water_dot_y-cam.offset.y))
                        cam.prev_water_dot_pos.xy=water_dot_x,water_dot_y
            for sprite_group in above_player_sprite_group_list:
                for sprite in sprite_group:
                    if cam.draw_rect.colliderect(sprite.rect):
                        game_window.blit(sprite.image,(sprite.rect.x-cam.offset.x,sprite.rect.y-cam.offset.y))
    def update(update_instance,update_sprite_group_list,delta_time,water_dot_sprite_group):
        for player in player_sprite_group:
            player.update(delta_time)
            update_instance.update_rect.center=player.rect.center
        for sprite_group in update_sprite_group_list:
            for sprite in sprite_group:
                if update_instance.update_rect.colliderect(sprite.rect):
                    sprite.update(delta_time)
        for water_dot in water_dot_sprite_group:
            if abs(player.rect.centerx-water_dot.dest_pos.x)<display_size[0]:
                water_dot.update()

player_sprite_group=pygame.sprite.Group()

fish_sprite_group=pygame.sprite.Group()
rat_sprite_group=pygame.sprite.Group()
dog_sprite_group=pygame.sprite.Group()
big_fat_guy_sprite_group=pygame.sprite.Group()

block_sprite_group=pygame.sprite.Group()
reactive_block_sprite_group=pygame.sprite.Group()
tree_sprite_group=pygame.sprite.Group()
bubble_sprite_group=pygame.sprite.Group()

water_dot_sprite_group=pygame.sprite.Group()

bomb_rect_list=[]
water_blocks_rect_list=[]
water_hitlines=[]

world_maps={'reactive_blocks':{0:[]},'water_blocks':{0:[]},'blocks':{0:[]},'bomb_rects':{0:[]},'trees':{0:[]},'mobs':{0:[]}}#importing worlds
for world_name in range(0,1):
    with open(f'Data/worlds/{world_name}/{world_name}_reactive_blocks.csv') as map:
        world_reader=csv.reader(map,delimiter=',')
        for row in world_reader:
            world_maps['reactive_blocks'][world_name].append(row)
    with open(f'Data/worlds/{world_name}/{world_name}_blocks.csv') as map:
        world_reader=csv.reader(map,delimiter=',')
        for row in world_reader:
            world_maps['blocks'][world_name].append(row)
    with open(f'Data/worlds/{world_name}/{world_name}_bomb_rects.csv') as map:
        world_reader=csv.reader(map,delimiter=',')
        for row in world_reader:
            world_maps['bomb_rects'][world_name].append(row)#transfose bombrect-map list here
    world_maps['bomb_rects'][world_name]=[[row[i] for row in world_maps['bomb_rects'][world_name]] for i in range(len(world_maps['bomb_rects'][world_name][0]))]
    with open(f'Data/worlds/{world_name}/{world_name}_trees.csv') as map:
        world_reader=csv.reader(map,delimiter=',')
        for row in world_reader:
            world_maps['trees'][world_name].append(row)
    with open(f'Data/worlds/{world_name}/{world_name}_mobs.csv') as map:
        world_reader=csv.reader(map,delimiter=',')
        for row in world_reader:
            world_maps['mobs'][world_name].append(row)
    with open(f'Data/worlds/{world_name}/{world_name}_water_blocks.csv') as map:
        world_reader=csv.reader(map,delimiter=',')
        for row in world_reader:
            world_maps['water_blocks'][world_name].append(row)

game=game()

player_sprite_group.add(player(5130,560))#550,1311

#loading map
for row_number,row in enumerate(world_maps['blocks'][game_varibles['current_world']]):
    for block_number,block_id in enumerate(row):
        if block_id!='-1':
            block_sprite_group.add(block(block_id,block_number,row_number))
for row_number,row in enumerate(world_maps['water_blocks'][game_varibles['current_world']]):
    for block_number,block_id in enumerate(row):
        if block_id=='0':
            water_blocks_rect_list.append(pygame.Rect(block_number*48,row_number*48,48,48))
for row_number,row in enumerate(world_maps['reactive_blocks'][game_varibles['current_world']]):
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
                water_dot_sprite_group.add(water_dot((x_pos,row_number*48)))
        elif block_id=='9':
            reactive_block_sprite_group.add(pressure_switch(block_number,row_number))
        elif block_id=='10':
            reactive_block_sprite_group.add(little_rock(block_number*48,(row_number+1)*48-12))#x*48,(y+1)*48-12
bomb_rect_list.clear()
bomb_rect_topright=[]
for row_number,row in enumerate(world_maps['bomb_rects'][game_varibles['current_world']]):  
    for rect_number,block_id in enumerate(row):
        if block_id=='0':
            bomb_rect_topright=[(rect_number-1)*48,(row_number-1)*48]
        if block_id=='1':
            bomb_rect_list.append(pygame.Rect(bomb_rect_topright[1],bomb_rect_topright[0],((row_number+1)*48)-bomb_rect_topright[1],((rect_number+1)*48)-bomb_rect_topright[0]))
for row_number,row in enumerate(world_maps['trees'][game_varibles['current_world']]):
    for tree_number,tree_id in enumerate(row):    
        if tree_id!='-1': 
            tree_sprite_group.add(tree(tree_number,row_number))
for mob_y,row in enumerate(world_maps['mobs'][game_varibles['current_world']]):
    for mob_x,mob_id in enumerate(row):  
        if mob_id=='0':
            rat_sprite_group.add(rat(mob_x,mob_y))
        elif mob_id=='1':
            fish_sprite_group.add(fish(mob_x,mob_y,'right'))
        #elif mob_id=='2':
        #    big_fat_guy_sprite_group.add(big_fat_guy(mob_x,mob_y))
        elif mob_id=='3':
            dog_sprite_group.add(dog(mob_x,mob_y))
        elif mob_id=='4':
            fish_sprite_group.add(fish(mob_x,mob_y,'left'))
#water_hitline
water_bodies_list_counter=0
water_bodies={}
prev_water_dot_xpos=0
for water_dot in water_dot_sprite_group:#making seprate lists for serpate water bodiesS
    if water_dot.dest_pos.x-prev_water_dot_xpos>17:
        water_bodies_list_counter+=1
    prev_water_dot_xpos=water_dot.dest_pos.x
    try:
        water_bodies[water_bodies_list_counter].append(pygame.math.Vector2(water_dot.dest_pos))
    except:
        water_bodies[water_bodies_list_counter]=[]
        water_bodies[water_bodies_list_counter].append(pygame.math.Vector2(water_dot.dest_pos))
for key in water_bodies:
    water_bodies_list=water_bodies[key]
    water_hitlines.append((water_bodies_list[0],water_bodies_list[-1]))

prevoius_time=time.perf_counter()

while game_mode=='in_game':
    if game_varibles['current_world']!=save_data['world']:#loading map for new worlds
        block_sprite_group.clear()
        reactive_block_sprite_group.clear()
        tree_sprite_group.clear()
        for row_number,row in enumerate(world_maps['blocks'][game_varibles['current_world']]):
            for block_number,block_id in enumerate(row):
                if block_id!='-1':
                    block_sprite_group.add(block(block_id,block_number,row_number))
        for row_number,row in enumerate(world_maps['water_blocks'][game_varibles['current_world']]):
            for block_number,block_id in enumerate(row):
                if block_id=='0':
                    water_blocks_rect_list.append(pygame.Rect(block_number*48,row_number*48,48,48))
        for row_number,row in enumerate(world_maps['reactive_blocks'][game_varibles['current_world']]):
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
                        water_dot_sprite_group.add(water_dot((x_pos,row_number*48)))
                elif block_id=='9':
                    reactive_block_sprite_group.add(pressure_switch(block_number,row_number))
                elif block_id=='10':
                    reactive_block_sprite_group.add(little_rock(block_number*48,(row_number+1)*48-12))
        bomb_rect_list.clear()
        bomb_rect_topright=[]
        for row_number,row in enumerate(world_maps['bomb_rects'][game_varibles['current_world']]):  
            for rect_number,block_id in enumerate(row):
                if block_id=='0':
                    bomb_rect_topright=[(rect_number-1)*48,(row_number-1)*48]
                if block_id=='1':
                    bomb_rect_list.append(pygame.Rect(bomb_rect_topright[1],bomb_rect_topright[0],((row_number+1)*48)-bomb_rect_topright[1],((rect_number+1)*48)-bomb_rect_topright[0]))
        for row_number,row in enumerate(world_maps['trees'][game_varibles['current_world']]):
            for tree_number,tree_id in enumerate(row):    
                if tree_id!='-1': 
                    tree_sprite_group.add(tree(tree_number,row_number))
        for mob_y,row in enumerate(world_maps['mobs'][game_varibles['current_world']]):
            for mob_x,mob_id in enumerate(row):  
                if mob_id=='0':
                    rat_sprite_group.add(rat(mob_x,mob_y))
                elif mob_id=='1':
                    fish_sprite_group.add(fish(mob_x,mob_y,'right'))
                #elif mob_id=='2':
                #    big_fat_guy_sprite_group.add(big_fat_guy(mob_x,mob_y))
                elif mob_id=='3':
                    dog_sprite_group.add(dog(mob_x,mob_y))
                elif mob_id=='4':
                    fish_sprite_group.add(fish(mob_x,mob_y,'left'))
        #water_hitline
        water_bodies_list_counter=0
        water_bodies={}
        prev_water_dot_xpos=0
        for water_dot in water_dot_sprite_group:#making seprate lists for serpate water bodies
            if water_dot.dest_pos.x-prev_water_dot_xpos>17:
                water_bodies_list_counter+=1
            prev_water_dot_xpos=water_dot.dest_pos.x
            try:
                player.water_bodies[water_bodies_list_counter].append(pygame.math.Vector2(water_dot.dest_pos.x,water_dot.pos))
            except:
                water_bodies[water_bodies_list_counter]=[]
                water_bodies[water_bodies_list_counter].append(pygame.math.Vector2(water_dot.dest_pos.x,water_dot.pos))
        for key in water_bodies:
            water_bodies_list=water_bodies[key]
            water_hitlines.append((water_bodies_list[0],water_bodies_list[-1]))
        save_data['world']=game_varibles['current_world']
    pygame.mouse.set_visible(False)
    delta_time=time.perf_counter()-prevoius_time
    prevoius_time=time.perf_counter()
    display_window.fill((255,255,255))
    game_window.fill((255,255,255))
    for player in player_sprite_group:
        if player.state!='aim':
            game.update([fish_sprite_group,rat_sprite_group,dog_sprite_group,reactive_block_sprite_group,bubble_sprite_group],delta_time,water_dot_sprite_group)
    game.draw(delta_time,[reactive_block_sprite_group,fish_sprite_group,rat_sprite_group,dog_sprite_group,bubble_sprite_group],
                player_sprite_group,
                [tree_sprite_group,block_sprite_group],
                water_dot_sprite_group)
    
    #for player in player_sprite_group:
    #    print(str(player.pos),str(player.acceleration),str(player.velocity),str(player.stamina)+'     deltatime'+str(delta_time)+player.state+'\033c',end='')
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
            if event.key==pygame.K_w:
                for player in player_sprite_group:
                    player.jump=True
                    player.image_frame=0
        #elif event.type==pygame.KEYUP:
        #    if event.key==pygame.K_w:
        #        for player in player_sprite_group:
        #            player.image_frame=0
        #            #player.jump_counter=0
    for player in player_sprite_group:
        if keys_pressed[pygame.K_d]:
            if player.direction=='left':
                player.velocity.x=0
            if player.state!='sprint':
                if player.water:
                    player.state='swim'
                    player.direction='right'
                else:
                    player.state='run'
                    player.direction='right'
            if keys_pressed[pygame.K_LSHIFT]:
                if player.water:
                    player.state='swim_fast'
                    player.direction='right'
                else:
                    player.state='sprint'
                    player.direction='right'
        if keys_pressed[pygame.K_a]:
            if player.direction=='right':
                player.velocity.x=0
            if player.state!='sprint':
                if player.water:
                    player.state='swim'
                    player.direction='left'
                else:
                    player.state='run'
                    player.direction='left'
            if keys_pressed[pygame.K_LSHIFT]:
                if player.water:
                    player.state='swim_fast'
                    player.direction='left'
                else:
                    player.state='sprint'
                    player.direction='left'
        if keys_pressed[pygame.K_SPACE]:
            if player.hand=='little_rock':
                player.state='aim'
            else:
                player.state='interact'
        if keys_pressed[pygame.K_s]:
            player.state='pick'
        if not (keys_pressed[pygame.K_a] or keys_pressed[pygame.K_d] or keys_pressed[pygame.K_s] or keys_pressed[pygame.K_w] or keys_pressed[pygame.K_SPACE] or player.state=='pant'):
                if player.state=='aim' or player.state=='throw':
                    player.state='throw'
                else:
                    player.state='idle'
    #game_window.blit(pygame.image.load('rough.png').convert(),(0,225))#testin
    if game_settings['fullscreen']:
        display_window.blit(game_window,(0,0))
    else:
        display_window.blit(pygame.transform.smoothscale_by(game_window,0.5),(0,0))
    pygame.display.update()
    print(str(clock.get_fps()))
    clock.tick()