#!/usr/bin/env python
#-*- coding: utf-8 -*-
import random

from pygame.locals import *

from src.main_menu import MainMenu
from src.in_game import InGame
from src.core.application import Application
from src.game_entities import *
from src.weapon import Weapon
from src.asteroid import Asteroid

class SGame(InGame):
    def __init__(self, owner):
        super(SGame, self).__init__(owner)

        self.background = 'res/space.jpg'

        #playership
        playerShip = PlayerShip(0, 0)
        playerShip.image = 'res/Ship1.png'
        playerShip.x = self.owner.display.get_width() / 2 - playerShip.width / 2
        playerShip.y = self.owner.display.get_height() - playerShip.height
        playerShip.constraints.width = self.owner.display.get_width()
        playerShip.constraints.height = self.owner.display.get_height()

        playerShip.currentWeapon = Weapon("basicCannon")
        self._playerShip = playerShip

        self.addGameObject(playerShip)
        #test asteroidoids
        asteroid = [Asteroid(owner) for i in range(4)]
        for a in asteroid:
            a.image = 'res/asteroid{}.png'.format(random.randrange(1,3))
            a._image = pygame.transform.scale(a.image, (a.width // 4,
                                                        a.height // 4))
            a.constraints.width = None #self.owner.display.get_width()
            a.constraints.height = None #self.owner.display.get_height()
            #a.x = random.randrange(0, 800)
            #a.y = random.randrange(0, 300)
            a.spawn()
            self.addGameObject(a)
            

    def updateState(self):
        dx = 5
        dy = 5
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LSHIFT]:
            dx = 2
            dy = 2

        key_action_map = {
            K_w: lambda: self.movePlayerShip(0, -dy),
            K_a: lambda: self.movePlayerShip(-dx, 0),
            K_s: lambda: self.movePlayerShip(0,  dy),
            K_d: lambda: self.movePlayerShip(dx,  0),
            K_z: lambda: self.openFire()
        }

        for k in key_action_map:
            if pressed_keys[k]:
                key_action_map[k]()

        for i in self._gameObjects:
            i.updateState()

    def handleKeydown(self, key):
        {
            K_ESCAPE: lambda: self.owner.setState("mainMenu")
        }.get(key, lambda: None)()

    def handleKeyup(self, key):
        pass

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            self.handleKeydown(event.key)
        elif event.type == pygame.KEYUP:
            self.handleKeyup(event.key)
        else:
            pass

    def movePlayerShip(self, dx, dy):
        self._playerShip.centerx += dx
        self._playerShip.centery += dy

    def openFire(self):
        self._playerShip.currentWeapon.fire()

class SMainMenu(MainMenu):
    def __init__(self, owner):
        super(SMainMenu, self).__init__(owner)

        self.background = 'res/mainmenu/logo.png'
        self.music = 'res/runaway.ogg'
        self.play_music()
        self.addMenu("Main Menu", [
            ("Start Game", lambda: self.owner.setState("game")),
            ("Highscores", lambda: self.setCurrentMenu("High Scores")),
            ("Quit", self.owner.exitGame)
        ])

        self.addMenu("High Scores",
                     [("foo", lambda: print("foo"))])

        self.getMenu("Main Menu").menu_center_y = 320
        self.getMenu("Main Menu").caption_center_y = 250

        self.getMenu("High Scores").menu_center_y = 320
        self.getMenu("High Scores").caption_center_y = 250

        self.setCurrentMenu("Main Menu")


if __name__ == "__main__":
    App = Application("PYГAME: CTAДNЯ")
    App.addState(SGame, "game")
    App.addState(SMainMenu, "mainMenu")
    App.state = "mainMenu"
    App.start()
