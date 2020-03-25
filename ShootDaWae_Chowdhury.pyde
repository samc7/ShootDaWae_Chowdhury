'''
Title: Shoot Da Wae Thru Space
Author: Sam Chowdhury
Last Update: Jan 23 2018
BETA Testers: Marko, Michael, Rico
Debuggers: Danilo, Cole, Farees, Shashank
Description: Python game culminating
'''

#random number generator
from random import randint
#add sound library to play sound
add_library('Minim')

#initial screen variable to show on start up
screen = "menu"
#name variable
name = ""
#kill count for enemy difficulty increase counter
upcount = 0
#kill count for total enemies
deathcount = 0
#highscore variable
high = 0

#OBJECT ORIENTED PROGRAMMING
#Player class
class Player(object):
    #initialize with ship image, player name, speed, health, damage
    def __init__(self, ship, name, speed, health, damage):
        self.ship = ship
        
        self.name = name
        
        self.health = health
        
        self.damage = damage
        
        self.speed = speed
        
        #initial bounty to start with
        self.bounty = 100
        
        #initial X position of ship
        self.positionX = 270
        
        #initial Y position of ship
        self.positionY = 800
        
        #variable for going right
        self.right = 0
        
        #variable for going left
        self.left = 0
        
        #variable for going up
        self.up = 0
        
        #variable for going down
        self.down = 0
        
        #bullet array to keep track of bullets
        self.bullets = []
        
        #bullet image
        self.player_bullet = loadImage("playerbullet.png")
        
    #Function for showing ship
    def play(self):
        image(self.ship, self.positionX, self.positionY)
    
    #function for checking player state
    def is_dead(self):
        return self.health <= 1 or self.bounty <= 0
    
    #movement calculation
    #player movement code from Farees
    def move(self):
        self.positionX += (self.right - self.left) * self.speed
        
        self.positionY += (self.down - self.up) * self.speed 
    
    #bullet creator function
    def shoot(self):
        #if bullets on screen are less than 6
        if len(self.bullets) < 6:
            #create instance of Bullet and append to bullet array
            bullet = Bullet(self.positionX, self.positionY, self.player_bullet)
        
            self.bullets.append(bullet)
    
    #boundary checker
    def boundary(self):
        if self.positionX - 20 < 0:
            self.positionX = 20  
        
        elif self.positionX + 20 > 540:
            self.positionX = 520  
        
        if self.positionY - 16 < 0:
            self.positionY = 16  
            
        elif self.positionY + 16 > 810:
            self.positionY = 794 
        
    #function for when called, damages player
    def hit(self, alien):
        if self.health > 1:
            self.health -= alien
        
        elif self.health <= 1:
            self.health == 1

#bullet class
class Bullet(object):
    #initialize with position, and iamge
    def __init__(self, startX, startY, bullet_image):
        #trigger sound when created
        bullet_sound.trigger()
        
        self.bullet_image = bullet_image
        
        self.positionX = startX
        
        self.positionY = startY
        
        #health variable
        self.health = 1
        
    #function for when called, updates bullet position
    def update(self, direction):
        self.positionY -= direction
    
    #returns if the bullet hit an enemy or is off the screen
    def is_dead(self):
        return self.positionY <= 0 or self.health == 0 or self.positionY >= 850
    
    #if bullet hits, bullet will be set to 0 health
    def kill(self):
        self.health = 0

#enemy class
class Enemy(object):
    #spawn with initial health, damage, speed, steal(bounty)
    def __init__(self, health, damage, speed, steal):
        self.health = health
        
        self.damage = damage
        
        self.speed = speed
        
        self.steal = steal
        
        #spawn with random position
        self.positionX = randint(40, 500)
        
        self.positionY = 0
        
        self.death = 0
    
    #when called, update enemy position
    def update(self):
        self.positionY += self.speed
        
    #check enemy state if dead
    def is_dead(self, player):
        if self.health <= 0:
            player.bounty += self.steal / 7
            
            return True
        
        elif self.positionY >= 850:
            if player.bounty >= 1:
                player.bounty -= self.steal
        
            if player.bounty <= 0:
                player.bounty = 0
            
            return True
        
        else:
            return False
        
    #function for if player bullet hits
    def hit(self, player):
        self.health -= player.damage
        
        #knockback position change
        self.positionY -= 5
    
#Spawner variable
class Spawner(object):
    def __init__(self):
        #array for enemies
        self.aliens = []  
        
        #shield duplication checker
        self.shield = False
        
        #array for enemy bullets
        self.bullets = [] 
        
        #initial enemy health, damage, speed, steal (bounty)
        self.health = 50
        
        self.damage = 10
        
        self.speed = 1
        
        self.steal = 10 
        
        #initial max enemies on screen
        self.max_length = 3
        
        #bullet image
        self.enemy_bullet = loadImage("enemybullet.png")
        
        #powerup array
        self.powers = []
    
    #spawn enemy
    def spawn(self):
        global enemy
        
        #if not max enemies on screen
        if len(self.aliens) < self.max_length:
            #create enemy with enemy stat stuff
            enemy = Enemy(self.health, self.damage, self.speed, self.steal)
            
            #Append to enemy array
            self.aliens.append(enemy)

    #enemy upgrade when called   
    def upgrade(self):
        #upgrade enemy stats
        self.speed += 0.01
        
        self.damage += 1
        
        self.steal += 7
        
        self.max_length += 0.01
    
    #shoot variable
    def shoot(self):
        #for alien in enemy array, this will shoot a bullet for the first enemy in the array 
        for alien in self.aliens:
            #if the bullet does not exist
            if len(self.bullets) < 1:
                #create the bullet with initial values
                bullet = Bullet(alien.positionX, alien.positionY, self.enemy_bullet)
                
                #append to enemy bullet array
                self.bullets.append(bullet)    
    
    #spawn powerup variable
    def power_spawn(self, alien):
        #create powerup
        powerup = Powerup(alien)
        
        #append to powerup list
        self.powers.append(powerup)

#powerup class
class Powerup(object):
    #initialize with alien position
    def __init__(self, alien):
        #random powerup chooser
        self.select = randint(1,5)
        
        self.positionX = alien.positionX
        
        self.positionY = alien.positionY
        
        #health variable
        self.kill = 0
        
        #time variable for shield
        self.picktime = second()
    
    #update position
    def update(self):
        #if powerup alive
        if self.kill == 0:
            self.positionY += 1
    
    #check if dead
    def is_dead(self):
        return self.positionY >= 810 or self.kill == 1 
    
    #function for showing the power, depending on random selection in init    
    def power(self, spawner, player, power1, power2, power3, power4, power5):
        if self.select == 1:
            image(power1, self.positionX, self.positionY)
        
        elif self.select == 2:
            image(power2, self.positionX, self.positionY)
        
            self.power_inv = power2
        
        elif self.select == 3:
            image(power3, self.positionX, self.positionY)
            
            self.power_inv = power3
        elif self.select == 4:
            image(power4, self.positionX, self.positionY)
   
        elif self.select == 5:
            image(power5, self.positionX, self.positionY)
        
        elif self.select == 6:
            #set shield state
            spawner.shield = True
           
            #show shield 
            noFill()
                    
            stroke(255, 0, 0)
            
            ellipse(player.positionX, player.positionY, 50, 50)
            
            #once time is up, kill shield and powerup
            if self.picktime + 5 <= second():
                self.kill = 1 
                
                #reset shield state
                spawner.shield = False
            
    #function for picking up powerup 
    def pickup(self, player, spawner):
        #player health powerup
        if self.select == 1:
            self.kill = 1
            
            #add random amount of health to player health, between 25 - 50
            if player.health < 200:
                player.health += randint(25,50)
                
                if player.health >= 200:
                    player.health = 200
        
        #shield powerup, check if shield prexists
        elif self.select == 2 and spawner.shield == False:
            #change kill variable so that powerup position doesn't change (since now it's player position)
            self.kill = 2
            
            #timer for shield
            self.picktime = second()
            
            self.select = 6
        
        #kill all powerup
        elif self.select == 3:
            self.kill = 1
            
            explosion_sound.trigger()
            
            #empty alien array, doesnt count for kill count
            spawner.aliens = []
        
        #speed powerup
        elif self.select == 4:
            player.speed += 0.01
            
            self.kill = 1
        
        #damage powerup
        elif self.select == 5:
            player.damage += 2
            
            self.kill = 1
            
#intial setup funciton
def setup():
    #all the global variables for repeatedly used images and music
    global menu_font, minim, menu_music, side_music, game_music, red_ship, blue_ship, black_ship, ship, explosion_sound, spawner, bullet_sound, power1, power2, power3, power4, power5, alien_ship, highscore
    
    #window size
    size(540, 960)
    
    #smooth screen
    smooth()      
    
    #frame rate
    frameRate(120)
    
    #font for game
    menu_font = createFont("SpaceMono-Regular.ttf", 37)
    
    #powerup images
    power1 = loadImage("health.png")
    power2 = loadImage("shield.png")
    power3 = loadImage("destroy.png")
    power4 = loadImage("speed.png")
    power5 = loadImage("damage.png")
    
    #player ship images
    red_ship = loadImage("red.png")
    blue_ship = loadImage("blue.png")
    black_ship = loadImage("black.png")
    #first ship variable for start
    ship = red_ship
    
    #alien ship image
    alien_ship = loadImage("alienship.png")
    
    #minim for sounds
    minim = Minim(this)
    
    #sound files for playing depending on screen
    menu_music = minim.loadSample("Shift.mp3")
    side_music = menu_music
    game_music = minim.loadSample("Clash.mp3")        
    
    #game sounds
    bullet_sound = minim.loadSample("Pew.wav")
    explosion_sound = minim.loadSample("Explosion.wav")
    
    #highscore file for appending
    highscore = open("data/leaderboard.txt", "a")
    
    #trigger music
    menu_music.trigger()
    
    #startup spawner class
    spawner = Spawner()

#draw function
def draw(): 
    #global variables
    global name, player, upcount, screen, deathcount, high, leaderboard_list3
    
    #refresh screen so no overlap after screen change
    background(0)
    
    #menu screen 
    if screen == "menu":    
        #title
        rectMode(RADIUS)
        
        noFill()
        
        stroke(256, 0, 0)
        
        rect(270, 110, 267, 30, 10)
        
        textAlign(CENTER, CENTER)

        textFont(menu_font)
        
        fill(256, 0, 0)
        
        text("Shoot Da Wae Thru Space", 270, 100)
        #end title
        
        #play button
        rectMode(RADIUS)
        
        noFill()
        
        stroke(256, 0, 0)
        
        rect(270, 260, 140, 28, 10)
        
        textAlign(CENTER, CENTER)

        textFont(menu_font)
        
        fill(256, 0, 0)
        
        text("Play", 270, 250)
        #end play button
        
        #Tutorial button
        rectMode(RADIUS)
        
        noFill()
        
        stroke(256, 0, 0)
        
        rect(270, 360, 140, 28, 10)
        
        textAlign(CENTER, CENTER)

        textFont(menu_font)
        
        fill(256, 0, 0)
        
        text("Controls", 270, 350)
        #end Tutorial button
        
        #Leaderboard button
        rectMode(RADIUS)
        
        noFill()
        
        stroke(256, 0, 0)
        
        rect(270, 460, 160, 28, 10)
        
        textAlign(CENTER, CENTER)

        textFont(menu_font)
        
        fill(256, 0, 0)
        
        text("Recent Scores", 270, 450)
        #end Leaderboard button
        
        #credits button
        rectMode(RADIUS)
        
        noFill()
        
        stroke(256, 0, 0)
        
        rect(270, 560, 140, 28, 10)
        
        textAlign(CENTER, CENTER)

        textFont(menu_font)
        
        fill(256, 0, 0)
        
        text("Credits", 270, 550)
        #end credits button
        
        #exit button
        rectMode(RADIUS)
        
        noFill()
        
        stroke(256, 0, 0)
        
        rect(270, 760, 140, 28, 10)
        
        textAlign(CENTER, CENTER)

        textFont(menu_font)
        
        fill(256, 0, 0)

        text("Exit", 270, 750)
        #end exit button
    
    #play screen for settings before starting game    
    elif screen == "play":
        #enter name
        textAlign(CENTER, CENTER)
        
        textFont(menu_font)
        
        text("Enter your name", 270, 110)
        
        textAlign(CENTER, CENTER)
        
        textFont(menu_font)
        
        text(name, 270, 300)
        
        color(255)
        
        line(150, 330, 390, 330)
        #end name 
        
        #spaceship selector
        textAlign(CENTER, CENTER)
        
        textFont(menu_font)
        
        text("Choose your spaceship", 270, 490)
        
        imageMode(CENTER)
        
        image(ship, 270, 730)
        
        #ship selection show
        if ship == red_ship:
            textAlign(CENTER, CENTER)
        
            textFont(menu_font)
            
            textSize(30)
        
            text("Red Rider", 270, 810)
            
            textAlign(CENTER, CENTER)
        
            textFont(menu_font)
            
            textSize(30)
        
            text("Health above all", 270, 850)
        
        elif ship == blue_ship:
            textAlign(CENTER, CENTER)
        
            textFont(menu_font)
            
            textSize(30)
        
            text("Blue Rider", 270, 810)
            
            textAlign(CENTER, CENTER)
        
            textFont(menu_font)
            
            textSize(30)
        
            text("Speed above all", 270, 850)
        
        elif ship == black_ship:
            textAlign(CENTER, CENTER)
        
            textFont(menu_font)
            
            textSize(30)
        
            text("Night Rider", 270, 810)
            
            textAlign(CENTER, CENTER)
        
            textFont(menu_font)
            
            textSize(30)
        
            text("Damage above all", 270, 850)
            
        color(255)
        
        triangle(150, 715, 150, 735, 115, 725)
        
        color(255)
        
        triangle(390, 715, 390, 735, 425, 725)
        
        #end spaceship selector
        
        #hit enter text
        textAlign(CENTER, CENTER)
        
        textFont(menu_font)
    
        textSize(30)
    
        text("Hit Enter to continue", 270, 940)
        #end hit enter text
        
        #back button
        rectMode(RADIUS)
        
        noFill()
        
        stroke(256, 0, 0)
        
        rect(540, 960, 70, 28, 10)
        
        textAlign(CENTER, CENTER)

        textFont(menu_font)
        
        fill(256, 0, 0)
        
        textSize(20)
        
        text("Back", 505, 945)
        #end of back button
    
    #game screen when you actually play
    elif screen == "game":
        #game bar
        fill(255)
        
        line(0, 870, 540, 870)
        
        rectMode(CORNER)
        
        fill(255,255,255)
        
        rect(10, 885, 200, 20)
        
        fill(255,0,0)
        
        #player health rectangle
        rect(10, 885, player.health, 20)
        
        fill(255,255,0)
        
        textAlign(RIGHT,CENTER)
        
        textFont(menu_font)
        
        textSize(20)
        
        #show bounty (score)
        bounty = "Bounty: " + str(player.bounty)
        
        text(bounty, 530,880)
        
        fill(255)
        
        textAlign(RIGHT,CENTER)
        
        textSize(20)
        
        text(player.name, 530, 910)
        
        #back button
        rectMode(RADIUS)
        
        noFill()
        
        stroke(256, 0, 0)
        
        rect(540, 960, 70, 28, 10)
        
        textAlign(CENTER, CENTER)

        textFont(menu_font)
        
        fill(255,0,0)
        
        textSize(20)
        
        text("Back", 505, 945)
        # end of back button
        
        fill(255,0,0)
        
        line(0, 817, 540, 817)
        
        #player object spawning
        player.play()
        player.boundary()
        player.move()
        
        #keep trying to spawn enemies
        spawner.spawn()
        
        #list for alive bullets
        live_bullets = []      

        #for player bullets        
        for bullet in player.bullets:
            #check if not dead
            if not bullet.is_dead():
                #append to allive bullets
                live_bullets.append(bullet)
            
            #update the bullet
            bullet.update(7)
            
            #show the bullets
            image(bullet.bullet_image, bullet.positionX + 20, bullet.positionY)
            image(bullet.bullet_image, bullet.positionX - 20, bullet.positionY)
            
            #for enemies
            for alien in spawner.aliens:
                #check hitbox distance
                if dist(bullet.positionX + 20, bullet.positionY, alien.positionX, alien.positionY) < 23 or dist(bullet.positionX - 20, bullet.positionY, alien.positionX, alien.positionY) < 23:
                    #hit alien
                    alien.hit(player)
                    
                    #kill the bullet
                    bullet.kill()
                    
                    #trigger explosion sound
                    explosion_sound.trigger()
        
        #make the alive bullets array the current player bullets             
        player.bullets = live_bullets 
        
        #reset live bullets for enemy bullets
        live_bullets = []                   
        
        #for bullets in enemy array
        for bullet in spawner.bullets:
            #check if not bullet is dead
            if not bullet.is_dead():
                #append to alive bullets
                live_bullets.append(bullet)
                
            #update bullet position
            bullet.update(-4)
            
            #show bullet
            image(bullet.bullet_image, bullet.positionX + 20, bullet.positionY)
            image(bullet.bullet_image, bullet.positionX - 20, bullet.positionY)
            
            #Check if hit player
            if dist(bullet.positionX + 20, bullet.positionY, player.positionX, player.positionY) < 23 or dist(bullet.positionX - 20, bullet.positionY, player.positionX, player.positionY) < 23:
                #deal damage
                player.hit(spawner.damage)
                
                #get rid of bullet
                bullet.kill()
                
                #explosion sound
                explosion_sound.trigger()  
                
        #set alive bullets to real bullets
        spawner.bullets = live_bullets 
        
        #reset live enemies arrays for enemies
        live_enemies = []            
        
        #for enemies in enemy array
        for alien in spawner.aliens:
            #check if not alien is dead
            if not alien.is_dead(player):
                #append to live enemies
                live_enemies.append(alien)
            
            #if enemy died
            else:
                #add to upgrade counter
                upcount += 1
                
                #add to kill count
                deathcount += 1
                
                #random variable for if to spawn powerup
                do_power = randint(1, 3)
                
                #if random variable is 2 and not 3 powerups on screen
                if do_power == 2 and len(spawner.powers) < 3:
                    #create powerup
                    spawner.power_spawn(alien)
            
            #update position and shoot
            alien.update()
            spawner.shoot()    
            
            #show enemy    
            image(alien_ship, alien.positionX, alien.positionY)
            
            #if upgrade count reaches enemy array max length
            if upcount >= spawner.max_length:    
                #upgrade enemy
                spawner.upgrade()
                
                #reset upgrade count
                upcount = 0
            
            #check if player hit alien    
            if dist(alien.positionX, alien.positionY, player.positionX, player.positionY) < 40:
                #do damage to player
                player.hit(spawner.damage)
                
                #kill bullet
                bullet.kill()
                
                #trigger hit sound
                explosion_sound.trigger()
        
        #set alive enemies to current enemies
        spawner.aliens = live_enemies 

        #set live powers array        
        live_powers = []      
        
        #for powerups in power array
        for powerup in spawner.powers:
            #check if not powerup is dead
            if not powerup.is_dead():
                #append to alive powers
                live_powers.append(powerup)
            
            #show the powerup
            powerup.power(spawner, player, power1, power2, power3, power4, power5)
            
            #update the powerup
            powerup.update()
            
            #check if player touched powerup
            if dist(powerup.positionX, powerup.positionY, player.positionX, player.positionY) < 28:
                #pickup function
                powerup.pickup(player, spawner)
            
            #if the powerup is shield
            if powerup.select == 6:
                #for aliens
                for alien in spawner.aliens:
                    #if they hit player, kill them
                    if dist(player.positionX, player.positionY, alien.positionX, alien.positionY) < 80:
                        alien.health = 0
                #for enemy bullets
                for bullet in spawner.bullets:
                    #kill bullet if hit
                    if dist(player.positionX, player.positionY, bullet.positionX, bullet.positionY) < 80:
                        bullet.kill()
        
        #set alive powers to current powers                                
        spawner.powers = live_powers   
        
        #set the highest current game score to the bounty
        if player.bounty > high:
            high = player.bounty
        
        #if player dies, end game
        if player.is_dead():
            screen = "over"  
            
    #screen for if game over          
    elif screen == "over":
        #back button
        rectMode(RADIUS)
        
        noFill()
        
        stroke(256, 0, 0)
        
        rect(540, 960, 70, 28, 10)
        
        textAlign(CENTER, CENTER)

        textFont(menu_font)
        
        fill(256, 0, 0)
        
        textSize(20)
        
        text("Back", 505, 945)
        #end of back button
        
        #show score        
        textSize(40)
        
        text("GAME OVER", 270, 100)
        
        score = "Score: " + str(high - 100)
        
        #show kills
        textSize(20)
        
        text(score, 270, 300)
        
        kills = "Kills: " + str(deathcount)
        
        text(kills, 270, 500)
        
        #show final messages
        text("Score added to leaderboard", 270, 700)
        
        text("Thanks for playing!", 270, 900)
        
    elif screen == "tutorial":
        #title
        rectMode(RADIUS)
        
        noFill()
        
        stroke(256, 0, 0)
        
        rect(270, 110, 140, 28, 10)
        
        textAlign(CENTER, CENTER)

        textFont(menu_font)
        
        fill(256, 0, 0)
        
        text("Controls", 270, 100)
        #end title
        
        #back button
        rectMode(RADIUS)
        
        noFill()
        
        stroke(256, 0, 0)
        
        rect(540, 960, 70, 28, 10)
        
        textAlign(CENTER, CENTER)

        textFont(menu_font)
        
        fill(256, 0, 0)
        
        textSize(20)
        
        text("Back", 505, 945)
        #end of back button
        
        textSize(14)
        
        #show game message
        text("You have been assigned to carry precious bounty across the Universe eternally. Defend the bounty (and yourself) from aliens who are trying to take your bounty!", 270, 190, 265, 80)
        
        imageMode(CENTER)
        
        #ship images
        image(red_ship, 90, 280)
        image(blue_ship, 270, 280)
        image(black_ship, 450, 280)
        
        #explanations
        text("Choose a ship to play as and defend the bounty, shoot with \'z\'", 270, 330)
        
        #alien ship image
        image(alien_ship, 270, 375)
        
        text("Kill these aliens, avoid contact with them and their bullets", 270, 410)
        
        #powerup images
        image(power1, 90, 470)
        image(power2, 180, 470)
        image(power3, 270, 470)
        image(power4, 360, 470)
        image(power5, 450, 470)
        
        text("Health", 90, 500)
        text("Shield", 180, 500)
        text("Destroy", 270, 500)
        text("Speed", 360, 500)
        text("Damage", 450, 500)
        
        text("Powerups have a chance to spawn if an alien is killed. Speed and Damage permanently increase their respective stats.", 270, 560, 265, 50)
        
        #pass line for enemies
        line(0, 610, 540, 610)
        
        text("If an alien passes the first line, they will take your bounty! Do not let your bounty reach 0! Check your bounty in the bottom right during the game.", 270, 660, 265, 50)
        
        text("Check your health in the bottom left during the game. Stay alive!", 270, 730, 265, 50)
        
        text("Every 3 aliens you kill, the aliens will increase in difficulty", 270, 790, 265, 50)
        
        text("Basically, you must SHOOT DA WAE!", 270, 860)
        
    elif screen == "leaderboard":
        #recent scores title
        rectMode(RADIUS)
        
        noFill()
        
        stroke(256, 0, 0)
        
        rect(270, 110, 160, 28, 10)
        
        textAlign(CENTER, CENTER)

        textFont(menu_font)
        
        fill(256, 0, 0)
        
        text("Recent Scores", 270, 100)
        #end recentscores title
        
        #back button
        rectMode(RADIUS)
        
        noFill()
        
        stroke(256, 0, 0)
        
        rect(540, 960, 70, 28, 10)
        
        textAlign(CENTER, CENTER)

        textFont(menu_font)
        
        fill(256, 0, 0)
        
        textSize(20)
        
        text("Back", 505, 945)
        #end of back button
        
        #show leaderboard table headers
        textSize(30)
        textAlign(LEFT)
        text("Name", 100, 200)
        textAlign(RIGHT)
        text("Score", 440, 200)
        
        #initial x and y values for elements in highscore
        x = 100
        y = 270
        
        #for the txt high scores
        for element in leaderboard_list3:
            #split elements in each element
            cleanline = element.split(",")
            
            #show name
            textSize(20)
            textAlign(LEFT)
            text(cleanline[1], x, y)
            
            #add to x value
            x += 340
            
            #show score
            textAlign(RIGHT)
            text(cleanline[0], x, y)
            
            #reset x, add to y
            x = 100
            y += 50
    
    elif screen == "credits":
        print(mouseX, mouseY)

        #credits title
        rectMode(RADIUS)
        
        noFill()
        
        stroke(256, 0, 0)
        
        rect(270, 110, 140, 28, 10)
        
        textAlign(CENTER, CENTER)

        textFont(menu_font)
        
        fill(256, 0, 0)
        
        text("Credits", 270, 100)
        #end credits title
        
        #back button
        rectMode(RADIUS)
        
        noFill()
        
        stroke(256, 0, 0)
        
        rect(540, 960, 70, 28, 10)
        
        textAlign(CENTER, CENTER)

        textFont(menu_font)
        
        fill(256, 0, 0)
        
        textSize(20)
        
        text("Back", 505, 945)
        #end of back button
        
        #game dev section
        text("Game Developer/Designer", 270, 270)
        
        line(122, 285, 413, 285)    
            
        text("Sam Chowdhury", 270, 310) 
        
        #images section
        text("Sprite Design", 270, 370)
        
        line(122, 390, 413, 390)    
            
        text("Modified images of OpenGameArt.org origin", 270, 410) 
        
        #music section
        text("Music", 270, 470)
        
        line(122, 490, 413, 490)    
            
        text("Licensed, Various artists, 99Lives Label", 270, 510)
        
        #sound effects section
        text("Sound Effects", 270, 570)
        
        line(122, 590, 413, 590)    
            
        text("Sound effects of OpenGameArt.org origin", 270, 610)
        
        #thanks message
        text("Thanks for playing!", 270, 800)
        
#key press function
def keyPressed():
    global screen, ship, name, player
    if screen == "play":
        if key != CODED:
            #remove last character if backspace
            if key == BACKSPACE:
                name = name[0:len(name) - 1]
            
            #add to name if not any other restricted keys
            if key != BACKSPACE and key != ENTER and key != RETURN and key != ",":
                name = name + str(key)
                
                #max name legth, 10
                name = name[0:10]
            
            #check if player has name, and pressed their respective enter button
            if len(name) >= 1 and key == ENTER or key == RETURN:
                #start the game
                screen = "game"
                
                #set the ship with its respective variables 
                if ship == red_ship:
                    speed = 3
                    health = 200
                    damage = 25
                elif ship == blue_ship:
                    speed = 7
                    health = 100
                    damage = 25
                elif ship == black_ship:
                    speed = 2
                    health = 100
                    damage = 100
                
                #create player classs
                player = Player(ship, name, speed, health, damage)
        
        elif key == CODED:
            #change ship
            if keyCode == LEFT:
                if ship == red_ship:
                    ship = black_ship
                    
                elif ship == blue_ship:
                    ship = red_ship
                    
                elif ship == black_ship:
                    ship = blue_ship
                    
            #change ship
            elif keyCode == RIGHT:
                if ship == red_ship:
                    ship = blue_ship
                    
                elif ship == blue_ship:
                    ship = black_ship
                    
                elif ship == black_ship:
                    ship = red_ship
    
    #player movement code from Farees
    #game movement
    if screen == "game":
        if key == CODED:
            #check boundary
            if not player.boundary():
                #check button, move until boundary
                if keyCode == LEFT and not player.positionX <= 20:
                    player.left = 1
                elif keyCode == RIGHT and not player.positionX >= 520:
                    player.right = 1
                elif keyCode == UP and not player.positionY <= 16:
                    player.up = 1
                elif keyCode == DOWN and not player.positionY >= 794:
                    player.down = 1
        
        #shoot button
        if key != CODED:
            if key == "z":
                player.shoot()

#player movement code from Farees
#check for key release             
def keyReleased():
    #check if screen during game
    if screen == "game":
        #turn off movement varaible
        if key == CODED:
            if keyCode == LEFT:
                player.left = 0
            elif keyCode == RIGHT:
                player.right = 0
            elif keyCode == UP:
                player.up = 0
            elif keyCode == DOWN:
                player.down = 0

#if mouse pressed
def mousePressed():
    #global variables for music, and reset variables after ending game
    global screen, menu_music, game_music, side_music, red_ship, blue_ship, black_ship, ship, spawner, upcount, deathcount, high, score, spawner, name, highscore, leaderboard, leaderboard_list3
    
    #menu screen buttons
    if screen == "menu":
        #reset variables
        bounty = 0
        spawner = Spawner()
        upcount = 0
        deathcount = 0
        high = 0
        score = 0
        name = ""
        
        #buttons for menu options, stop music and trigger respective music
        if  mouseX >= 130 and mouseY >= 230 and mouseX <= 410 and mouseY <= 285:
            screen = "play"
            
            menu_music.stop()
            
            game_music.trigger()
            
        elif  mouseX >= 130 and mouseY >= 330 and mouseX <= 410 and mouseY <= 385:
            screen = "tutorial"
            
            menu_music.stop()
        
            side_music.trigger()
            
        elif  mouseX >= 130 and mouseY >= 430 and mouseX <= 410 and mouseY <= 485:
            screen = "leaderboard"
            
            menu_music.stop()
            
            #open file to read for leaderboard
            leaderboard = open("data/leaderboard.txt", "r")
            
            #readlines and create list of final readings
            leaderboard_list2 = leaderboard.readlines()
            leaderboard_list3 = []
            
            #for each element
            for element in leaderboard_list2:
                #make an element separate
                cleanline = element.replace("\n", "")
                
                #append to final list
                leaderboard_list3.append(cleanline)

            #reverse list
            leaderboard_list3 = leaderboard_list3[::-1]
            
            #keep to 10 items in list
            leaderboard_list3 = leaderboard_list3[0:10]
            
        elif  mouseX >= 130 and mouseY >= 530 and mouseX <= 410 and mouseY <= 585:
            screen = "credits"
            
            menu_music.stop()
            
            side_music.trigger()
            
        elif  mouseX >= 130 and mouseY >= 730 and mouseX <= 410 and mouseY <= 785:
            #call stop function
            stop()
    #end menu screen buttons
            
    #back button for all other screens
    elif screen =="credits" or screen == "tutorial" or screen == "game" or screen == "leaderboard":
        if mouseX >= 470 and mouseY >= 930:
            #stop music
            side_music.stop()
            game_music.stop()
            
            #set screen
            screen = "menu"
            
            #start menu music
            menu_music.trigger()
    
    #GAME OVER screen
    elif screen == "over":
        #write score to file (with format)
        highscore.write("{0},{1}\n".format(high - 100, player.name))
        
        #back button
        if mouseX >= 470 and mouseY >= 930:
            side_music.stop()
            game_music.stop()
            screen = "menu"
            menu_music.trigger() 
    
    #game setup screen        
    elif screen == "play":
        #back button
        if mouseX >= 470 and mouseY >= 930:
            game_music.stop()
            side_music.stop()
            screen = "menu"
            menu_music.trigger()
        
        #click to change ship
        elif mouseX >= 115 and mouseX <= 150 and mouseY >= 715 and mouseY <= 735:
            if ship == red_ship:
                ship = black_ship
                
            elif ship == blue_ship:
                ship = red_ship
                
            elif ship == black_ship:
                ship = blue_ship
        
        #click to change ship
        elif mouseX >= 390 and mouseX <= 425 and mouseY >= 715 and mouseY <= 735:
            if ship == red_ship:
                ship = blue_ship
                
            elif ship == blue_ship:
                ship = black_ship
                
            elif ship == black_ship:
                ship = red_ship

#stop function    
def stop():   
    #end all sound files 
    menu_music.stop()
    side_music.stop()
    game_music.stop()
    
    #close files
    menu_music.close()
    game_music.close()
    bullet_sound.close()
    explosion_sound.close()
    highscore.close()
    
    #stop music player
    minim.stop()
    
    #exit game
    exit()   