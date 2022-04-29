
from cmath import sin
from tkinter import LEFT, RIGHT
import arcade
import time
import math
import random

WIDTH=600
HEIGHT=400

class Space_craft(arcade.Sprite):
    def __init__(self):
        super().__init__(':resources:images/space_shooter/playerShip1_blue.png')
        self.height=35
        self.width=35
        self.center_x=WIDTH/2
        self.center_y=50
        self.angle=0
        self.change_angle=0
        self.bullet_list=[]
    def rotat(self):
        self.angle -=self.change_angle

    def fire(self):
        self.bullet_list.append(Bullet(self))
        laser_sound=arcade.load_sound(':resources:sounds/laser4.wav')
        arcade.play_sound(laser_sound)
    def pop(self):
        self.bullet_list.pop(0)

class Enemy(arcade.Sprite):
    def __init__(self):
        super().__init__(':resources:images/space_shooter/playerLife1_orange.png')
        self.height=25
        self.width=25
        self.center_x=random.randint(25,575)
        self.center_y=390
        self.angle=180
        self.speed=1.5
    def move(self):
        self.center_y-=self.speed

    def explode(self):
        expload_sound=arcade.load_sound(':resources:sounds/explosion1.wav')
        arcade.play_sound(expload_sound,0.5)
        
class Bullet(arcade.Sprite):
    def __init__(self,host):
        super().__init__(':resources:images/space_shooter/laserRed01.png')
        self.center_x=host.center_x
        self.center_y=host.center_y
        self.angle=host.angle
        self.speed=4
    
    def move(self):
        self.x=math.radians(self.angle)
        self.center_x -= self.speed * math.sin(self.x)
        self.center_y += self.speed * math.cos(self.x)

class Ghule(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.height=75
        self.width=75


class Health(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.center_x=0
        self.center_y=10
        self.health_image=arcade.load_texture('images.jpg')
        self.tedad_joon=3
    def draw(self):
        for i in range(self.tedad_joon):
            arcade.draw_lrwh_rectangle_textured(self.center_x,self.center_y,25,25,self.health_image)
            self.center_x+=30
        self.center_x=0
class Gameover(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.flag=0
    def draw(self):
        arcade.draw_text('GAME OVER',150,100,arcade.color.RED,40)

class Score(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.record=0
    def draw(self):
        arcade.draw_text('record: '+str(self.record),WIDTH-100,HEIGHT-375,arcade.color.BLUE_GREEN,10)
class Game(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, 'space craft')
        arcade.set_background_color(arcade.color.BLACK)
        self.background_image=arcade.load_texture(':resources:images/backgrounds/stars.png')
        self.t1=time.time()
        self.me=Space_craft()
        self.enemy=[Enemy()]
        self.score=Score()
        self.health=Health()
        self.ghul=Ghule()
        self.gameover=Gameover()
    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0,0,WIDTH,HEIGHT,self.background_image)
        self.t3=time.time()
        if self.gameover.flag==1:
            self.gameover.draw()
            if self.t3 - self.t1 >2:
                arcade.exit()
        self.me.draw()
        for enemy in self.enemy:
            enemy.draw()
        for bulet in self.me.bullet_list:
            bulet.draw()
        self.score.draw()
        self.health.draw()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol==arcade.key.RIGHT:
            self.me.change_angle+=2.25
        elif symbol==arcade.key.LEFT:
            self.me.change_angle-=2.25
        if symbol==arcade.key.SPACE:
            self.me.fire()
    def on_key_release(self, symbol: int, modifiers: int):
            self.me.change_angle=0

    def on_update(self, delta_time: float):
        self.me.rotat()
        for enemy in self.enemy:
            enemy.move()
            if enemy.center_y<0:
                self.enemy.pop(0)
                self.health.tedad_joon-=1
                if self.health.tedad_joon==0:
                    self.gameover.flag=1
        self.t2=time.time()
        r=random.randint(4,7)
        if self.t2 - self.t1 > r:
            self.enemy.append(Enemy())
            self.t1=time.time()
        for bulet in self.me.bullet_list:
            for enemy in self.enemy:
                    if arcade.check_for_collision(enemy,bulet):
                        enemy.explode()
                        self.enemy.remove(enemy)
                        self.score.record+=1
                        
            bulet.move()
            if bulet.center_x < 0 or bulet.center_y<0 or bulet.center_x>WIDTH or bulet.center_y> HEIGHT:
                self.me.pop()
        
Game()
arcade.run()
