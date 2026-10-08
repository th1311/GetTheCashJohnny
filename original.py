from turtle import delay

import pygame
import time
import random
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1000, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

BG = pygame.transform.scale(pygame.image.load("figures\X-Jóhann í gjaldkera.jpg"), (WIDTH, HEIGHT))
ENDIMG = pygame.transform.scale(pygame.image.load("figures/Johann.jpg"), (WIDTH, HEIGHT))



PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50

STAR_WIDTH = 40
STAR_HEIGHT = 40

SVEPPS_WIDTH = 30
SVEPPS_HEIGHT = 20

player_image = pygame.transform.scale(pygame.image.load("figures/Johann.jpg"), (PLAYER_WIDTH, PLAYER_HEIGHT))
gussi = pygame.transform.scale(pygame.image.load("figures/lgbt.png"), (STAR_WIDTH, STAR_HEIGHT))
cash = pygame.transform.scale(pygame.image.load("figures/cash.jpg"), (1+SVEPPS_WIDTH, 2+2*SVEPPS_HEIGHT))




# Create a player rectangle
PLAYER_NEW_HEIGHT = 60
PLAYER_VEL = 5 

HLIDAR_BOX_HEIGHT = 1000
HLIDAR_BOX_WIDTH = 20

NIDRI_BOX_HEIGHT = 20
NIDRI_BOX_WIDTH = 1400

FONT = pygame.font.SysFont("comicsans", 30)

#Background music
pygame.mixer.music.load('audio/JohannTheme.mp3')
pygame.mixer.music.play(-1, 177.0)

#Soud fx

def draw(player, stars, svepps, HLIDAR_BOX, HLIDAR_BOX2, NIDRI_BOX, UPPI_BOX, counter, elapsed_time):
    WIN.blit(BG, (0, 0))
    

    pygame.draw.rect(WIN, "red", HLIDAR_BOX)
    
    pygame.draw.rect(WIN, "red", HLIDAR_BOX2)

    pygame.draw.rect(WIN, "red", NIDRI_BOX)

    pygame.draw.rect(WIN, "red", UPPI_BOX)

    pygame.draw.rect(WIN, "blue", player)

    counter2 = FONT.render(f"$: {round(counter)}", 1, "white")
    WIN.blit(counter2, (10,10))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10,50))

    for star in stars:
        pygame.draw.rect(WIN, "red", star)
        WIN.blit(gussi, (star.x,star.y))

    for svepp in svepps:
        pygame.draw.rect(WIN, "white", svepp)
        WIN.blit(cash, (svepp.x-1,svepp.y-SVEPPS_HEIGHT/2 -1))

    WIN.blit(player_image, (player.x,player.y))

   

    pygame.display.update()




def main(): 
    run = True

    
    player = pygame.Rect(WIDTH/2-PLAYER_WIDTH/2, HEIGHT/2-PLAYER_HEIGHT/2, PLAYER_WIDTH, PLAYER_HEIGHT)
   
    


    x_change = 0       
    y_change = 0

    counter = 0

    HLIDAR_BOX = pygame.Rect(0-HLIDAR_BOX_WIDTH, 0, HLIDAR_BOX_WIDTH, HLIDAR_BOX_HEIGHT)
    HLIDAR_BOX2 = pygame.Rect(1000, 0, HLIDAR_BOX_WIDTH, HLIDAR_BOX_HEIGHT)
    NIDRI_BOX = pygame.Rect(0, 700, NIDRI_BOX_WIDTH, NIDRI_BOX_HEIGHT)
    UPPI_BOX = pygame.Rect(0, 0-NIDRI_BOX_HEIGHT, NIDRI_BOX_WIDTH, NIDRI_BOX_HEIGHT)

    clock = pygame.time.Clock()

    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_count = 0
    stars = []

    svepp_add_increment = 2000
    svepp_count = 0
    svepps = []

    hit = False

    while run:
        star_count += clock.tick(60)
        svepp_count = star_count
        elapsed_time = time.time() - start_time
        

        if star_count > star_add_increment:
            for _ in range(1):
                star_x = random.randint(0+SVEPPS_WIDTH, WIDTH-SVEPPS_WIDTH)
                star_y = random.randint(0+SVEPPS_HEIGHT, HEIGHT-SVEPPS_HEIGHT)
                star = pygame.Rect(star_x, star_y, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)

            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0    

        if svepp_count > svepp_add_increment:
            for _ in range(2):
                svepp_x = random.randint(0+SVEPPS_WIDTH, WIDTH-SVEPPS_WIDTH)
                svepp_y = random.randint(0+SVEPPS_HEIGHT, HEIGHT-SVEPPS_HEIGHT)
                svepp = pygame.Rect(svepp_x, svepp_y, SVEPPS_WIDTH, SVEPPS_HEIGHT)
                svepps.append(svepp)

            svepp_add_increment = max(200, svepp_add_increment - 50)
            svepp_count = 0  



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            x_change = -PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + PLAYER_WIDTH <= WIDTH:
            x_change = PLAYER_VEL
        if keys[pygame.K_UP] and player.y - PLAYER_VEL >= 0:
            y_change = -PLAYER_VEL
        if keys[pygame.K_DOWN] and player.y + PLAYER_VEL + PLAYER_HEIGHT <= HEIGHT:
            y_change = PLAYER_VEL

        player.x += x_change
        player.y += y_change
        clock.tick(100)
        
        
        for star in stars[:]:
            if star.colliderect(player):
                hit = True
                break
            if len(stars) > 8:
                stars.remove(star)
            
        

        if player.colliderect(HLIDAR_BOX):
            hit = True
        if player.colliderect(HLIDAR_BOX2):
            hit = True
        if player.colliderect(NIDRI_BOX):
            hit = True
        if player.colliderect(UPPI_BOX):
            hit = True

        for svepp in svepps[:]:
            if svepp.colliderect(player):
                svepps.remove(svepp)
                counter += 1
                break
                

             

        if hit:
            lost_text = FONT.render("You Lost!", 1, "white")
            #WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_width()/2))
            WIN.blit(ENDIMG, (0, 0))
            pygame.display.update()
            pygame.time.delay(1000)
            break

        draw(player, stars, svepps , HLIDAR_BOX, HLIDAR_BOX2, NIDRI_BOX, UPPI_BOX, counter, elapsed_time)
         
   
    pygame.quit()

if __name__ ==  "__main__":
    main()