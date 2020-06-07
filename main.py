import random
import pygame
import time
pygame.init()
WIDTH, HEIGHT = 400, 720 
HW, HH = WIDTH/2, HEIGHT/2
RED = (255, 0, 0)
DARK_GREEN = (0, 102, 51)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Escape From Earth")

# Images
clock = pygame.time.Clock()
display = pygame.display.set_mode((WIDTH, HEIGHT))
bg = pygame.image.load("Images/bckg2.png")
bg = pygame.transform.scale(bg, (WIDTH,HEIGHT))
sky = pygame.image.load("Images/sky.png")
sky = pygame.transform.scale(sky, (WIDTH,HEIGHT))
menu_bg = pygame.image.load("Images/menu_bg.png")
menu_bg = pygame.transform.scale(menu_bg, (WIDTH, HEIGHT))

menu_btn1 = pygame.image.load("Images/start_btn.png")
menu_btn2 = pygame.image.load("Images/start_btn.png")

playeSprite = [pygame.image.load("Images/gemi1.png"),
pygame.image.load("Images/pckg1.png"),
pygame.image.load("Images/pckg2.png"),
pygame.image.load("Images/Shuttle.png")]

engine = [pygame.image.load(f"Images/{i}.png") for i in range(1,5)]
print(engine)
engine = [pygame.transform.scale(engine[i],(25,25)) for i in range(0,4)]

asteroid_img = pygame.image.load("Images/meteorBig.png")
asteroid_img = pygame.transform.scale(asteroid_img, (50 ,50))

# Sounds
bg_music = pygame.mixer.music.load("audio/bg_music.mp3")

pygame.display.flip()

bgWidth, bgHeight = bg.get_rect().size

class rocket:
    def __init__(self, x, y, vel):
        self.x = x
        self.y = y
        self.vel = vel
        self.hp = 100
        self.img = playeSprite[0]
        self.pckg1, self.pckg2 = playeSprite[1], playeSprite[2]
        self.shuttle = playeSprite[3]
        self.mask = pygame.mask.from_surface(self.img)
        self.health = 3
        self.pck1Posy = self.y 
        self.pck2Posy = self.y
        self.shuttlePosy=self.y
        self.engine = engine
        self.counter = 0

        #self.mask = pygame.mask.from_surface(self.img)
    def draw(self, WIN):
        WIN.blit(self.shuttle, (self.x+12, self.shuttlePosy))
        WIN.blit(self.pckg1, (self.x+25, self.pck1Posy))
        WIN.blit(self.pckg2, (self.x+5, self.pck2Posy))
        WIN.blit(self.img, (self.x, self.y))

        if self.counter + 1 >= len(self.engine) :
            self.counter = 0

        while self.counter < len(self.engine):
            WIN.blit(self.engine[self.counter], (self.x + 8, self.y + 75))
            self.counter+=1

    def get_width(self):
        return self.img.get_width()

    def get_height(self):
        return self.img.get_height()

class enemy(rocket):
    def __init__(self, x, y, vel):
        super().__init__(x, y, vel)
        self.enemy_image = asteroid_img

    def draw(self,WIN):
        WIN.blit(self.enemy_image, (self.x, self.y))

    def move(self):
        self.y += player.vel

class button:
    def __init__(self, x, y, text, image):
        self.x = x
        self.y = y
        self.txt =text
        self.img = image
        self.color = (255, 0, 0)

    def draw(self, WIN):
        WIN.blit(self.img, (self.x, self.y))
        #pygame.draw.rect(WIN, self.color, (self.x,self.y,self.width,self.height),0)
        if self.txt != "":
            btn_font = pygame.font.SysFont("Comicsans", 40)
            btn_lbl = btn_font.render(self.txt, 1, (255, 255, 255))
            WIN.blit(btn_lbl, (self.x + 20, self.y + 20))
    
    def isOver(self,pos):
        if pos[0] > self.x and pos[0] < self.x + self.img.get_width():
            if pos[1] > self.y and pos[1] < self.y + self.img.get_height():
                return True
        return False
    
def collide(obj1,obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (int(offset_x), int(offset_y))) != None

player = rocket(WIDTH/2 - 50 , HEIGHT - 200 , 2)    
MAX_SCORE = 0
def main():
    global player
    global DARK_GREEN
    pygame.mixer.music.play(-1)
    font = pygame.font.SysFont("Comicsans", 30)
    lost_font = pygame.font.SysFont("Comicsans", 60)
    restart_font = pygame.font.SysFont("Comicsans", 40)
    pause_font = pygame.font.SysFont("Comicsans", 70)
    continue_font = pygame.font.SysFont("Comicsans", 40)
    asteroids = []
    wave = 5
    move = False
    bgPosx,bgPosy = 0, 0
    run = True
    lost = False
    pause = False
    health_color = DARK_GREEN

    def reDRAW():
        global MAX_SCORE
        health_label = font.render(f"Lives : {player.health}", 1, health_color)
        distance_label = font.render(f"Distance : {bgPosy}", 1, (0, 0, 0))
        new_score_label = lost_font.render(f"New Score : {MAX_SCORE}" , 1, (255, 255, 255))
        WIN.blit(sky,(0,0))
        WIN.blit(bg,(bgPosx, bgPosy))
        player.draw(WIN)
        WIN.blit(health_label, (10,10))
        WIN.blit(distance_label, (WIDTH-150, 10))

        for asteroid in asteroids:
            asteroid.draw(WIN)

        if lost:
            if MAX_SCORE <= Distance:
                MAX_SCORE = Distance    
                WIN.blit(new_score_label, (WIDTH/2 - new_score_label.get_width() + 175, HEIGHT - 150))
            lost_label = lost_font.render(f" Your Distance {Distance} " , 1, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH/2 -lost_label.get_width()/2, 350))
            restart_label = restart_font.render("Press 'R' key To Restart", 1, (255, 255, 255))
            WIN.blit(restart_label, (WIDTH/2 - restart_label.get_width()/2, 300))
            
        if pause:
            pause_label = pause_font.render(f"PAUSE", 1, (255,255,255))
            continue_label = continue_font.render(F"Press Space to continue",1,(255,255,255))
            WIN.blit(pause_label, (WIDTH/2 - pause_label.get_width()/2, 350))
            WIN.blit(continue_label, (WIDTH/2 - continue_label.get_width()/2 , 300))
                
        pygame.display.update()

    while run:
        #rel_y = bgPosy % bg.get_rect().height
        #WIN.blit(bg,(bgPosx, rel_y - bg.get_rect().height))
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE] and pause == True:
            pause = False
            pygame.mixer.music.unpause()

        elif keys[pygame.K_ESCAPE]:
            pygame.mixer.music.pause()
            pause = True

        if player.health == 1:
            health_color = RED
            
        if player.health < 1:
            lost = True
            pygame.mixer.music.stop()
            Distance = bgPosy
           
        if keys[pygame.K_r] and lost:
            lost = False
            player.health = 3
            player = rocket(WIDTH/2 - 50 , HEIGHT - 200 , 2)    
            main_menu()

        if bgPosy > 2500:
            player.pck1Posy += 2
            player.vel = 3
        if bgPosy > 5500:
            player.pck2Posy += 2
            player.vel = 4
        if bgPosy > 8000:
            player.shuttlePosy += 2
            player.vel = 7
            move = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if lost == False:
            if pause == False:
                if keys[pygame.K_UP] and player.y > 0 + 50 and move:
                    player.y-=player.vel
                if keys[pygame.K_DOWN] and player.y < HEIGHT - 50 and move:
                    player.y+=player.vel
                if keys[pygame.K_LEFT] and player.x> 0:
                    player.x-=player.vel
                if keys[pygame.K_RIGHT] and player.x < WIDTH - 50:
                    player.x+=player.vel
                bgPosy+=player.vel

                if len(asteroids) == 0 or len(asteroids) == 5:
                    wave += 10
                    for i in range(wave):
                        asteroid = enemy(random.randrange(20,WIDTH-50),random.randrange(-1500,-100),10)
                        asteroids.append(asteroid)   

                for asteroid in asteroids[:]:
                    asteroid.move()

                    if collide(asteroid, player):
                        asteroids.pop(asteroids.index(asteroid))
                        player.health -=1
                    elif asteroid.y >= HEIGHT:
                        asteroids.pop(asteroids.index(asteroid))
        reDRAW()
        clock.tick(60)
        WIN.fill((0, 0, 0))

def main_menu():
    global MAX_SCORE
    start_buttn = button(WIDTH/2 - 60, HEIGHT/2 + 20, "START", menu_btn1)
    ext_bttn = button(WIDTH/2 - 60, HEIGHT/2 + 90, "EXIT", menu_btn2)
    title_font = pygame.font.SysFont("comicsans", 50)
    score_font = pygame.font.SysFont("COMİCSANS", 40)
    run = True
    while run:
        WIN.fill((0, 0, 0))
        WIN.blit(menu_bg, (0, 0))
        start_buttn.draw(WIN)
        ext_bttn.draw(WIN)
        title_label = title_font.render("ESCAPE FROM EARTH", 1, (255, 255, 255))

        if MAX_SCORE != 0:
            score_lbl = score_font.render(f"Max Height : {MAX_SCORE} ", 1, (255, 255, 255))
            WIN.blit(score_lbl, (WIDTH/2 - score_lbl.get_width()/2, HEIGHT - 100))
        
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 200))
        pygame.display.update()
        for event in pygame.event.get(): 
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_buttn.isOver(pos):
                    main()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ext_bttn.isOver(pos):
                    run = False
    pygame.quit()
main_menu()
    