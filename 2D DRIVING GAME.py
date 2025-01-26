import pygame
from pygame.locals import *
import random
import math

pygame.init()

#setting the window size
size = width,height=(800,800)
screen = pygame.display.set_mode(size)

#setting the title
pygame.display.set_caption("CAR GAME")

#dimensions of the road and the markings
road_width = int(width/1.33)
road_mark_width = int(width/120)
roadmark_unit = height/3.809 #road marking and gap
roadmark_gap = height/20

#frame settings
clock = pygame.time.Clock()
fps=120

#loading images

#player's car
car = pygame.image.load("CAR.png")
car_location = car.get_rect()
car_location.center = width/2, height*0.875

#other car 1
othercar1 = pygame.image.load("OTHER CAR 1.png")
othercar1_location = othercar1.get_rect()
##othercar1_location.center = width/2 - road_width/3, 0

#other car 2
othercar2 = pygame.image.load("OTHER CAR 2.png")
othercar2_location = othercar2.get_rect()
##othercar2_location.center = width/2, -height*2

#other car 3
othercar3 = pygame.image.load("OTHER CAR 3.png")
othercar3_location = othercar3.get_rect()
##othercar3_location.center = width/2 + road_width/3, -height*2.5

#collision effect
collision = pygame.image.load("crash.png")
collision_location = collision.get_rect()

#positions of lanes
#lane_positions = [[width/2, 0], [width/2 - road_width/3, -height*2.5], [width/2 + road_width/3, -height*4]]
lanes = [width/2, width/2 - road_width/3, width/2 + road_width/3]

#loading sounds
gameover_sound = pygame.mixer.Sound('gameover_sound.wav')
#sound = pygame.mixer.Sound('sound.wav')
pygame.mixer.music.load('sound.wav')

#playing the background music
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.32)

#animation parameter
speed = 2

# Road marking position
road_marking_y = 0
road_marking_speed = speed

counter = 0
collision_threshold = 170

othercar1_location.center = (random.choice(lanes), 0)
othercar2_location.center = (random.choice(lanes), -height * 1.5)
othercar3_location.center = (random.choice(lanes), -height * 2.5)

font = pygame.font.SysFont('Arial', 19)

game_over = False
running = True
score = 0

while running:
    clock.tick(fps)
    
    #setting the background colour
    screen.fill((239,221,111))  
    
    counter += 1
    if counter == 4000:
        speed += 0.25
        score += 1
        counter = 0
        print("LEVEL UP!", score)
    
    #moving the other vehicles
    othercar1_location[1] += speed #image_location[1] => height
    othercar2_location[1] += speed
    othercar3_location[1] += speed

    # Move the road markings
    road_marking_y += road_marking_speed
    if road_marking_y >= roadmark_unit:
        road_marking_y = 0
        


    if othercar1_location[1] > height and othercar2_location[1] > height and othercar3_location[1] > height:
        # Randomly decide the number of lanes to occupy (either 2 or 3)
        lanes_to_occupy = random.choice([2, 2, 2, 3, 3])  # Higher chance of 2 lanes being occupied

        # Random selection of lanes ensuring no overlap
        selected_lanes = random.sample(lanes, lanes_to_occupy)

        othercar1_location.center = selected_lanes[0], 0
        othercar2_location.center = selected_lanes[1], -height * 0.6

        if lanes_to_occupy == 3:
            othercar3_location.center = selected_lanes[2], -height * 1.3
        
    
    if car_location.colliderect(othercar1_location) or car_location.colliderect(othercar2_location) or car_location.colliderect(othercar3_location):

        car_center = car_location.center
        other1_center = othercar1_location.center
        other2_center = othercar2_location.center
        other3_center = othercar3_location.center

        # Calculate squared distances to avoid sqrt computation
        dist1 = math.sqrt((car_center[0] - other1_center[0]) ** 2 + (car_center[1] - other1_center[1])**2)
        dist2 = math.sqrt((car_center[0] - other2_center[0]) ** 2 + (car_center[1] - other2_center[1]) ** 2)
        dist3 = math.sqrt((car_center[0] - other3_center[0]) ** 2 + (car_center[1] - other3_center[1]) ** 2)


        if car_location.bottom == othercar1_location.top or car_location.bottom == othercar2_location.top or car_location.bottom == othercar3_location.top:
        
##            car_center = car_location.center
##            collision_location.center = car_center
##            screen.blit(collision, collision_location)
##            pygame.display.update()
##            pygame.time.delay(1000)  # Pause for 1 second on collision
            game_over = True

        elif dist1 < collision_threshold or dist2 < collision_threshold or dist3 < collision_threshold:
##            collision_location.center = car_center
##            screen.blit(collision, collision_location)
##            pygame.display.update()
##            pygame.time.delay(1000)  # Pause for 1 second on collision
            game_over = True
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type==KEYDOWN:
            if event.key in [K_a, K_LEFT]:
                if car_location.left > width/2 - road_width/2 + road_mark_width:
                    car_location = car_location.move([-int(road_width/3),0])
            if event.key in [K_d, K_RIGHT]:
                if car_location.right < width/2 + road_width/2 - road_mark_width:
                    car_location = car_location.move([int(road_width/3),0])
            if event.key == K_ESCAPE:
                running = False

    #drawing the road and the markings (inside the while loop so that the object is moved instead of being replicated)
    
    pygame.draw.rect(screen, (50,50,50), (width/2-road_width/2, 0, road_width, height)) #road: x-coordinate, y-coordinate, width, height
    
    pygame.draw.rect(screen, (255,255,255), ((width/2-road_width/2+road_mark_width), 0, road_mark_width, height)) #solid line on the left
    pygame.draw.rect(screen, (255,255,255), ((width/2+road_width/2-2*road_mark_width), 0, road_mark_width, height)) #solid line on the right


    # Broken lines
    for i in range(-1, height // int(roadmark_unit) + 2):
        offset = int(road_marking_y) + i * int(roadmark_unit)
        pygame.draw.rect(screen, (255, 255, 255), (width / 2 - road_width / 2 + road_width / 3 - road_mark_width, offset, road_mark_width, roadmark_unit - roadmark_gap))
        pygame.draw.rect(screen, (255, 255, 255), (width / 2 + road_width / 2 - road_width / 3, offset, road_mark_width, roadmark_unit - roadmark_gap))

    screen.blit(car, car_location)    
    screen.blit(othercar1, othercar1_location)
    screen.blit(othercar2, othercar2_location)
    screen.blit(othercar3, othercar3_location)

    # Render and display the speed
    speed_text = font.render('Score : ' + str(score), True, (255, 255, 255)) # render(text, antialias, color, background=None) -> Surface
    screen.blit(speed_text, (7, 10))
    
    if game_over:
        collision_location.center = car_center
        screen.blit(collision, collision_location)
        #pygame.display.update()
        #sound.stop()
        pygame.mixer.music.stop()
        pygame.time.wait(1000)
        gameover_sound.set_volume(0.32)
        gameover_sound.play()
        #pygame.mixer.music.set_volume(0.1)
        
        # Display the game over message
        font = pygame.font.Font(None, 74)
        text = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))
        pygame.display.update()
        pygame.time.wait(4000)
        running = False
    
    pygame.display.update() #only one update command per frame to avoid the issue of flickering

pygame.quit()

#adobe express
#https://www.freepik.com/
#https://www.adobe.com/express/feature/image/remove-background
#https://www.iloveimg.com/rotate-image
#https://imageresizer.com/
#https://www.iloveimg.com/
#https://pixabay.com/music/search/genre/video%20games/
