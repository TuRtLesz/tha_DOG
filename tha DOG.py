import pygame,sys
display_window=pygame.display.set_mode((800,450))
pygame.display.set_caption('tha_DOG')
clock=pygame.time.Clock()
game_mode='in_game'
game_settings={'fullscreen':False}
while game_mode=='in_game':
    display_window.fill((255,255,255))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_F11:
                if game_settings['fullscreen']==True:
                    display_window=pygame.display.set_mode((800,450))
                    game_settings['fullscreen']=False
                elif game_settings['fullscreen']==False:
                    display_window=pygame.display.set_mode((800,450),pygame.FULLSCREEN|pygame.SCALED)
                    game_settings['fullscreen']=True
            if event.key==pygame.K_ESCAPE:
                if game_settings['fullscreen']==True:
                    display_window=pygame.display.set_mode((800,450))
                    game_settings['fullscreen']=False
    pygame.display.update()
    clock.tick()