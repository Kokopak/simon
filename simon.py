#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *

import random
import pickle
import os
from termcolor import colored

class Simon:
    def __init__(self, size_carre):
        pygame.init()

        screen_dim = size_carre * 4

        self.screen = pygame.display.set_mode((screen_dim, screen_dim))
        pygame.display.set_caption("Simon")

        self.size_carre = size_carre

        #===COULEURS===#

        self.bleu = pygame.Color(0,0,255)
        self.jaune = pygame.Color(255,255,0)
        self.rouge = pygame.Color(255,0,0)
        self.vert = pygame.Color(0,255,0)

        self.eclair= pygame.Color(255,255,255)

        fond = pygame.Color(220,150,15)

        #===SONS===#
        pygame.mixer.init()

        self.bleuSound = pygame.mixer.Sound("sound/bleu.wav")
        self.jauneSound = pygame.mixer.Sound("sound/jaune.wav")
        self.rougeSound = pygame.mixer.Sound("sound/rouge.wav")
        self.vertSound = pygame.mixer.Sound("sound/vert.wav")

        #Coordonées des couleurs

        self.x_bleu, self.y_bleu = (self.size_carre, 0)
        self.x_jaune, self.y_jaune = (self.size_carre * 2, 0)
        self.x_rouge, self.y_rouge = (self.size_carre, self.size_carre)
        self.x_vert, self.y_vert = (self.size_carre * 2, self.size_carre)

        #On les dessine
        pygame.draw.rect(self.screen, fond, pygame.Rect(0,0,self.size_carre*4, self.size_carre*4))

        self.carre_bleu = pygame.draw.rect(self.screen, self.bleu, pygame.Rect(self.x_bleu, self.y_bleu,size_carre, self.size_carre))
        self.carre_jaune = pygame.draw.rect(self.screen, self.jaune, pygame.Rect(self.x_jaune, self.y_jaune, self.size_carre, self.size_carre))
        self.carre_rouge = pygame.draw.rect(self.screen, self.rouge, pygame.Rect(self.x_rouge, self.y_rouge, self.size_carre, self.size_carre))
        self.carre_vert = pygame.draw.rect(self.screen, self.vert, pygame.Rect(self.x_vert, self.y_vert, self.size_carre, self.size_carre))

        
        self.c_choix = [] #==> Choix générés
        self.c_choix_util = [] #==> Choix de l'utilisateur

        self.font = pygame.font.Font(None, 17)
        spaceText = self.font.render("Appuyez sur la barre d'espace pour commencer !", True, (0,0,0), (159,182,205))
        spaceTextRec = spaceText.get_rect()
        spaceTextRec.centerx = self.screen.get_rect().centerx
        spaceTextRec.centery = self.screen.get_rect().centery + 50
        self.screen.blit(spaceText, spaceTextRec)

        pygame.display.update()

    def genChoix(self):
        choix_dispo = "BLEU, JAUNE, ROUGE, VERT".split(", ")
        choix = random.choice(choix_dispo)
        #Si la liste est vide
        if self.c_choix == []:
            #On append le choix
            choix = random.choice(choix_dispo)
            self.c_choix.append(choix)
        else:
            #Pour éviter que ce soit 2 fois la même couleur
            while choix == self.c_choix[-1]:
                choix = random.choice(choix_dispo)
            self.c_choix.append(choix)
        return choix

    def eclaircieCouleurs(self):
        eclaircie = {
                "BLEU": ((self.x_bleu, self.y_bleu), self.bleu),
                "JAUNE": ((self.x_jaune, self.y_jaune), self.jaune),
                "ROUGE": ((self.x_rouge, self.y_rouge), self.rouge),
                "VERT": ((self.x_vert, self.y_vert), self.vert)
        }

        #Permet de dessiner un petit flash (blanc) sur les couleurs générés
        for couleur in self.c_choix:
            x, y = eclaircie[couleur][0]
            self.playStopSoundColor(couleur)
            pygame.draw.rect(self.screen, self.eclair, pygame.Rect(x, y, self.size_carre, self.size_carre))
            pygame.display.update()
            pygame.time.wait(450)
            self.playStopSoundColor(couleur, "stop")
            pygame.draw.rect(self.screen, eclaircie[couleur][1], pygame.Rect(x, y, self.size_carre, self.size_carre))
            pygame.display.update()

    def playStopSoundColor(self, couleur, mode="play"):
        soundColor = {
                "BLEU": self.bleuSound,
                "JAUNE": self.jauneSound,
                "ROUGE": self.rougeSound,
                "VERT": self.vertSound
        }

        if mode == "play":
            soundColor[couleur].play()
        elif mode == "stop":
            soundColor[couleur].stop()
        else:
            print "Mode inconnue !"


    def checkListes(self):
        return self.c_choix == self.c_choix_util

    def getScore(self):
        return len(self.c_choix_util)
    
    def getScoreFile(self):
        with open("scores.txt", "r") as f:
            depickler = pickle.Unpickler(f)
            score = depickler.load()
        return score

    def saveScoreFile(self):
        score = self.getScore()
        if os.path.isfile("scores.txt"):
            scoreRecupe = self.getScoreFile()
            if score > scoreRecupe: 
                with open("scores.txt", "w") as f:
                    pickler = pickle.Pickler(f)
                    pickler.dump(score)
                print "Score enregistré car votre ancien score était plus petit !"
            else:
                print "Score non enregistré car votre ancien score était plus grand !"
        else:
            with open("scores.txt", "w") as f:
                pickler = pickle.Pickler(f)
                pickler.dump(score)
                print "Fichier scores.txt créer ! Score enregistré !"
        
    def mainLoop(self):
        ok = True
        while ok:
            event = pygame.event.wait()
            if event.type == QUIT:
                ok = False
            elif event.type == KEYDOWN and event.key == K_SPACE:
                if self.c_choix == []:
                    choix = self.genChoix()
                    self.eclaircieCouleurs()
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                if self.c_choix != []:
                    mx, my = pygame.mouse.get_pos()
                    mx = (mx / self.size_carre) * self.size_carre
                    my = (my / self.size_carre) * self.size_carre 
                    pos_carre = {
                            (self.x_bleu, self.y_bleu) : "BLEU",
                            (self.x_jaune, self.y_jaune) : "JAUNE",
                            (self.x_rouge, self.y_rouge) : "ROUGE",
                            (self.x_vert, self.y_vert) : "VERT"
                    }
                    if (mx, my) in pos_carre:
                        couleur = pos_carre[mx,my]
                        self.c_choix_util.append(couleur)
                        self.playStopSoundColor(couleur)

                    #Si la taille des 2 listes est la même, on les compares.
                    if len(self.c_choix_util) == len(self.c_choix):
                        pygame.time.wait(500)
                        self.playStopSoundColor(couleur, "stop")
                        #Pas pareil on sort 
                        if not self.checkListes():
                            termcolor_carre = {
                                    "BLEU": "blue",
                                    "JAUNE": "yellow",
                                    "ROUGE": "red",
                                    "VERT": "green"
                            }
                            print "Perdu !"
                            print "Le bon ordre était : %s" % "-->".join(colored("%s" % el, termcolor_carre[el]) for el in self.c_choix)
                            print "Le votre           : %s" % "-->".join(colored("%s" % el, termcolor_carre[el]) for el in self.c_choix_util)
                            print "SCORE : %d" % self.getScore()
                            self.saveScoreFile()
                            ok = False
                        else :
                            choix = self.genChoix()
                            self.eclaircieCouleurs()
                            self.c_choix_util = []
                        
if __name__ == '__main__':
    simon = Simon(128)
    simon.mainLoop()
