import pygame
from pygame import K_ESCAPE, K_TAB, KEYDOWN, VIDEORESIZE
from pygame.constants import MOUSEBUTTONDOWN
import random
import time
from PIL import Image
import os
from os.path import exists
import tkinter as tk
from tkinter import filedialog
import imghdr

class Grid():
    def __init__(self):
        self.r1 = pygame.Rect(0,0,200,200)
        self.r2 = pygame.Rect(200,0,200,200)
        self.r3 = pygame.Rect(400,0,200,200)
        self.r4 = pygame.Rect(600,0,200,200)

        self.r5 = pygame.Rect(0,200,200,200)
        self.r6 = pygame.Rect(200,200,200,200)
        self.r7 = pygame.Rect(400,200,200,200)
        self.r8 = pygame.Rect(600,200,200,200)

        self.r9 = pygame.Rect(0,400,200,200)
        self.r10 = pygame.Rect(200,400,200,200)
        self.r11 = pygame.Rect(400,400,200,200)
        self.r12 = pygame.Rect(600,400,200,200)

        self.r13 = pygame.Rect(0,600,200,200)
        self.r14 = pygame.Rect(200,600,200,200)
        self.r15 = pygame.Rect(400,600,200,200)
        self.r16 = pygame.Rect(600,600,200,200)
    
        self.rectList = [self.r1, self.r2, self.r3, self.r4,
                        self.r5, self.r6, self.r7, self.r8,
                        self.r9, self.r10, self.r11, self.r12,
                        self.r13, self.r14, self.r15, self.r16]
        
        self.reference = ['0-0','0-1','0-2','0-3',
                        '1-0','1-1','1-2','1-3',
                        '2-0','2-1','2-2','2-3',
                        '3-0','3-1','3-2','3-3']
    
    def drawGrid(self):
        for rect in self.rectList:
            pygame.draw.rect(screen,(255,255,255),rect,1)

    def selectcheck(self, mouse_pos, mouse_focus):
        for rect in self.rectList:
            check = rect.collidepoint(mouse_pos)
            if check and mouse_focus:
                pygame.draw.rect(screen,(255,0,0),rect,1)
    
    def getCoord(self, mouse_pos):
        for rect in self.rectList:
            check = rect.collidepoint(mouse_pos)
            if check:
                index = self.rectList.index(rect)
                coord = self.reference[index]
                return coord

class Box():
    def __init__(self, image, row, column, num=None):
        self.image = image
        self.rightNum = num

        self.rowRight = row
        self.columnRight = column
        self.coordRight = [self.rowRight, self.columnRight]

        self.row = row
        self.column = column
        self.coord = [self.row,self.column]

        self.rect = pygame.Rect(column*200,row*200,200,200)
        self.rightNumRect = pygame.Rect(column*200,row*200,25,25)

        self.left = None
        self.right = None
        self.up = None
        self.down = None

        self.isPlayer = False
        self.isMoving = False

        self.currentX, self.currentY = column*200, row*200
        self.destinationX, self.destinationY = column*200, row*200

    def update(self):
        self.rect = pygame.Rect(self.currentX,self.currentY,200,200)
        self.rightNumRect = pygame.Rect(self.column*200,self.row*200,25,25)
        self.coord = [self.row, self.column]
        self.currentX, self.currentY = self.currentX, self.currentY
        self.destinationX, self.destinationY = self.column*200, self.row*200
        self.isMoving = False if self.currentX == self.destinationX and self.currentY == self.destinationY else True
        self.slide()
    
    def slide(self):
        if self.currentX > self.destinationX:
            self.currentX -= 12.5
        elif self.currentX < self.destinationX:
            self.currentX += 12.5
        if self.currentY > self.destinationY:
            self.currentY -= 12.5
        elif self.currentY < self.destinationY:
            self.currentY += 12.5

    def __str__(self):
        if self.isPlayer:
            return f"Player"
        else:
            return f"({self.rowRight}, {self.columnRight}), ({self.row}, {self.column})"

class Selection():
    def __init__(self):
        self.upload = pygame.transform.smoothscale(pygame.image.load("Assets/upload.png"),(180,180))
        self.boxList = []
        for i in range(0,4):
            for j in range(0,4):
                self.boxList.append(Box(pygame.transform.smoothscale(pygame.image.load(f"All_Images/original{i}-{j}.jpg"),(200,200)), i, j))
        self.boxList.pop()
    
    def drawSquares(self):
        for box in self.boxList:
            screen.blit(box.image, box.rect)
        screen.blit(self.upload,(610,610))

class Game():
    def __init__(self,boxList,coord,path = None):
        self.boxList = boxList
        self.Player = self.boxList[3][3]
        self.Player.num = None
        self.Player.isPlayer = True
        self.Player.image = pygame.image.load("Assets/playerb.png")
        self.Player.image.set_alpha(0)
        self.playerRow = 0
        self.playerColumn = 0
        self.playerCoord = [self.playerRow, self.playerColumn]
        self.playerRect =  pygame.Rect(self.playerColumn*200,self.playerRow*200,200,200)
        self.ogpg = pygame.image.load(path) if path else pygame.image.load(f"All_Images/original{coord[0]}-{coord[1]}.jpg")

    def updateBoxPositions(self):
        for rowNumber, row in enumerate(self.boxList):
            for columnNumber, box in enumerate(row):
                box.left = self.boxList[rowNumber][columnNumber-1] if columnNumber-1 in range(0,len(row)) else None
                box.right = self.boxList[rowNumber][columnNumber+1] if columnNumber+1 in range(0,len(row)) else None
                box.up = self.boxList[rowNumber-1][columnNumber] if rowNumber-1 in range(0,len(row)) else None
                box.down = self.boxList[rowNumber+1][columnNumber] if rowNumber+1 in range(0,len(row)) else None

    def shuffle(self):
        for i in range(0,200):
            options = [square for square in [self.Player.left, self.Player.right, self.Player.up, self.Player.down] if square]
            choice = random.choice(options)
            self.swap([choice.row, choice.column])

    def drawSquares(self):
        for row in self.boxList:
            for box in row:
                box.update()
                screen.blit(box.image,box.rect)

    def getRCS(self, coordinate):
        iRow, iCol = None, None
        iRP, iCP = None, None
        for index, row in enumerate(self.boxList):
            for i, box in enumerate(row): 
                if box.coord == coordinate:
                    iRow, iCol = index, i
                if box.coord == self.Player.coord:
                    iRP, iCP = index, i
        return [iRow, iCol, iRP, iCP]

    def swap(self, coordinate):
        iRow, iCol, iRP, iCP = self.getRCS(coordinate)

        self.boxList[iRow][iCol], self.boxList[iRP][iCP] = self.boxList[iRP][iCP], self.boxList[iRow][iCol]
        self.boxList[iRow][iCol].coord, self.boxList[iRP][iCP].coord = self.boxList[iRP][iCP].coord, self.boxList[iRow][iCol].coord
        self.boxList[iRow][iCol].row, self.boxList[iRow][iCol].column = self.boxList[iRow][iCol].coord
        self.boxList[iRP][iCP].row, self.boxList[iRP][iCP].column = self.boxList[iRP][iCP].coord
        
        self.updateBoxPositions()
        self.boxList[iRow][iCol].update()
        self.boxList[iRP][iCP].update()

    def moveByClick(self, coordinate, num):
        moveable = [square for square in [self.Player.left, self.Player.right, self.Player.up, self.Player.down] if square]
        if self.boxList[coordinate[0]][coordinate[1]] in moveable:
            self.swap(coordinate)
            num[0] += 1
        
    def moveByKeys(self, keys, num):
        moveable = [self.Player.left, self.Player.right, self.Player.up, self.Player.down]

        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and moveable[0] != None:
            self.swap([moveable[0].row, moveable[0].column])
            num[0] += 1
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and moveable[1] != None:
            self.swap([moveable[1].row, moveable[1].column])
            num[0] += 1
        elif (keys[pygame.K_UP] or keys[pygame.K_w]) and moveable[2] != None:
            self.swap([moveable[2].row, moveable[2].column])
            num[0] += 1
        elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and moveable[3] != None:
            self.swap([moveable[3].row, moveable[3].column])
            num[0] += 1
            
        self.updateBoxPositions()
        
    def checkCompletion(self):
        tf_list = []
        #check = [b.isMoving for a in self.boxList for b in a]
        #print(check)
        for row in self.boxList:
            for box in row:
                if box.coord == box.coordRight and not box.isMoving:
                    tf_list.append(True)
                else:
                    tf_list.append(False)
        if False in tf_list:
            return False
        else:
            return True
    
    def drawTileNumbers(self):
        for row in self.boxList:
            for box in row:
                pygame.draw.rect(screen,(255,255,255),box.rightNumRect)
                displayFont(box.rightNum, "tileNumbers", (box.column*200 + 12, box.row*200 + 12))

class Settings():
    def __init__(self, note_img):
        self.isActive = False
        self.background = pygame.image.load("Assets/settings.jpg")
        self.tileNumbers = False
        self.tileNumbersRect = pygame.Rect(200,200,50,50)
        self.tileNumbersSelect = 5
        self.timer = False
        self.timerRect = pygame.Rect(200,350,50,50)
        self.timerSelect = 5
        self.moves = False
        self.movesRect = pygame.Rect(200,500,50,50)
        self.movesSelect = 5
        self.rectColor = (194,152,119)
        self.note_img = note_img
        self.help = False
        self.help_icon = pygame.transform.smoothscale(pygame.image.load("Assets/questionMark.png"), (50,50))
        self.help_icon_rect = self.help_icon.get_rect(topleft = (10,10))
        self.exit = pygame.transform.smoothscale(pygame.image.load("Assets/exit.png"), (50,50))
        self.exit_rect_note = pygame.Rect(650,200,50,50)
        self.quit_color = (110, 84, 70)
        self.quit_rect = pygame.Rect(352, 715, 100, 50)
    
    def draw(self):
        screen.blit(self.background,(0,0))
        screen.blit(self.help_icon, self.help_icon_rect)
        pygame.draw.rect(screen, self.rectColor, self.tileNumbersRect, self.tileNumbersSelect, 5)
        pygame.draw.rect(screen, self.rectColor, self.timerRect, self.timerSelect, 5)
        pygame.draw.rect(screen, self.rectColor, self.movesRect, self.movesSelect, 5)
        pygame.draw.rect(screen, self.quit_color, self.quit_rect)
        displayFont("Tile Numbers", "tile")
        displayFont("Timer", "timer")
        displayFont("Move Counter", "moves")
        displayFont("QUIT", "quit")

        if self.help:
            screen.blit(self.note_img, (100,200))
            screen.blit(self.exit, self.exit_rect_note)
            displayFont("How to Play", "beginning_note", (340, 205))
            displayFont("__________", "beginning_note", (340, 205))
            displayFont("The objective of the game is to", "beginning_note", (210, 290))
            displayFont("arrange the tiles in their correct spot", "beginning_note", (185, 340))
            displayFont("(in numerical order). You may click", "beginning_note", (195, 390))
            displayFont("the tile you wish to move into", "beginning_note", (225, 440))
            displayFont("the blank slot.", "beginning_note", (320, 490))
    
    def checkMouse(self, mouse_pos):
        self.tileNumbersSelect = 0 if (self.tileNumbersRect.collidepoint(mouse_pos) and not self.tileNumbers) or self.tileNumbers else 5
        self.timerSelect = 0 if (self.timerRect.collidepoint(mouse_pos) and not self.timer) or self.timer else 5
        self.movesSelect = 0 if (self.movesRect.collidepoint(mouse_pos) and not self.moves) or self.moves else 5
        self.quit_color = (99, 76, 63) if self.quit_rect.collidepoint(mouse_pos) else (110, 84, 70)
    
    def select(self, mouse_pos):
        if self.tileNumbersRect.collidepoint(mouse_pos) and not self.tileNumbers:
            self.tileNumbers = True
        elif self.tileNumbersRect.collidepoint(mouse_pos) and self.tileNumbers:
            self.tileNumbers = False
        elif self.timerRect.collidepoint(mouse_pos) and not self.timer:
            self.timer = True
        elif self.timerRect.collidepoint(mouse_pos) and self.timer:
            self.timer = False
        elif self.movesRect.collidepoint(mouse_pos) and not self.moves:
            self.moves = True
        elif self.movesRect.collidepoint(mouse_pos) and self.moves:
            self.moves = False
        
        if self.help_icon_rect.collidepoint(mouse_pos):
            self.help = not self.help
        if self.exit_rect_note.collidepoint(mouse_pos) and self.help:
            self.help = False
        if self.quit_rect.collidepoint(mouse_pos):
            return True
        return None

def displayFont(toScreen, ttype, coord = None):
    if ttype == "moves":
        move_surf = settings_font.render(str(f"{toScreen}"),False,(162,124,103))
        move_rect = move_surf.get_rect(topleft = (300,500))
        screen.blit(move_surf,move_rect)
    elif ttype == "displayMoves":
        dmove_surf = move_font.render(str(f"Moves: {toScreen}"),False,(0,0,0))
        dmove_rect = dmove_surf.get_rect(topleft = coord)
        screen.blit(dmove_surf,dmove_rect)
    elif ttype == "restart":
        restart_surf = restart_font.render(str(toScreen),False,(255,255,255))
        restart_rect = restart_surf.get_rect(center = (400,650))
        screen.blit(restart_surf,restart_rect)
    elif ttype == "tile":
        tile_surf = settings_font.render((f"{toScreen}"), False, (162,124,103))
        tile_rect = tile_surf.get_rect(topleft = (300,200))
        screen.blit(tile_surf,tile_rect)
    elif ttype == "timer":
        timer_surf = settings_font.render((f"{toScreen}"), False, (162,124,103))
        timer_rect = timer_surf.get_rect(topleft = (300,350))
        screen.blit(timer_surf,timer_rect)
    elif ttype == "tileNumbers":
        tN_surf = tileNumbers_font.render((f"{toScreen}"), False, (0,0,0))
        tN_rect = tN_surf.get_rect(center = coord)
        screen.blit(tN_surf,tN_rect)
    elif ttype == "time":
        time_surf = move_font.render((f"Time: {toScreen}"), False, (0,0,0))
        time_rect = time_surf.get_rect(topleft = coord)
        screen.blit(time_surf,time_rect)
    elif ttype == "beginning_note":
        note_surf = move_font.render((f"{toScreen}"), False, (0,0,0))
        note_rect = note_surf.get_rect(topleft = coord)
        screen.blit(note_surf,note_rect)
    elif ttype == "quit":
        quit_surf = restart_font.render((f"{toScreen}"), False, (162,124,103))
        quit_rect = quit_surf.get_rect(center = (400,740))
        screen.blit(quit_surf, quit_rect)

def image_cutter(row, column, path = None):
    if path:
        infile = f"{path[0]}"
        for i in range(4):
            for j in range(4):
                with Image.open(infile) as im:
                    box = (200*i, 200*j, 200*i+200, 200*j+200)
                    new_im = im.crop(box)
                    new_im.save(str(j) + "-" + str(i)+ "." + path[1], path[1].upper())
        return path[1]
    else:
        infile = f"All_Images/original{row}-{column}" + ".jpg"
        for i in range(4):
            for j in range(4):
                with Image.open(infile) as im:
                    box = (200*i, 200*j, 200*i+200, 200*j+200)
                    new_im = im.crop(box)
                    new_im.save(str(j) + "-" + str(i)+".jpg", "JPEG")
        return "jpg"

def delete_crops(image_type):
    dir_list = ['0-0', '0-1', '0-2', '0-3', '1-0', '1-1', '1-2', '1-3', '2-0', '2-1', '2-2', '2-3', '3-0', '3-1', '3-2', '3-3']
    for photo in dir_list:
        os.remove(f"{photo}.{image_type.lower()}")

def select_user_image():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    typeOfFile = ""
    try:
        typeOfFile = imghdr.what(file_path)
    except FileNotFoundError:
        print("File not Found")
    acceptable = ["jpg", "jpeg", "png"]
    if typeOfFile in acceptable:
        return [file_path, typeOfFile]
    else:
        return None

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((800,800), pygame.RESIZABLE)

#Window Info
pygame.display.set_caption("Puzzle")

grid = Grid()

selection = Selection()

#Beginning Note
beginning_note = pygame.transform.smoothscale(pygame.image.load("Assets/BeginningNote.jpg"), (600,400))
beginning_note_bool = True

settings = Settings(beginning_note)
settings_font = pygame.font.Font(None, 64)
tileNumbers_font = pygame.font.Font(None, 32)

numOfMoves = [0]
move_font = pygame.font.Font(None, 36)

congrats = pygame.image.load("Assets/congrats.jpeg")
congrats.set_alpha(5)
restartRect = pygame.Rect(300,600,200,100)
restart_font = pygame.font.Font(None, 48)

image_type = "jpg"
canBoxlist = False
myImageInfo = None

rrow = None
ccolumn = None
ttemp = ""
ccoord = []

row = None
column = None
temp = ""
coord = []

running = True
complete = False
active_playing = False

while running:
    events = pygame.event.get()
    keys = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    mouse_focus = pygame.mouse.get_focused()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

        if event.type == KEYDOWN:
            if beginning_note_bool == False:
                if keys[pygame.K_ESCAPE]:
                    settings.isActive = not settings.isActive
        
        # if event.type == VIDEORESIZE:
        # # Perhaps, find the ratio of resize like, 1.5, 1.1, etc
        # # and also, always make sure event.w == event.h in order to keep square shape
        #     screen = pygame.display.set_mode((event.w,event.h), pygame.RESIZABLE)
    
    if active_playing:

        ticks = round((time.time()-start_time),2)

        if complete:
            screen.blit(congrats,(0,0))
            restart_collision = restartRect.collidepoint(mouse_pos)
            restartColor = (181,128,32) if restart_collision else (245,238,157)
            pygame.draw.rect(screen, restartColor, restartRect)
            displayFont("RESTART", "restart")

            for event in events:
                if event.type == MOUSEBUTTONDOWN:
                    if restart_collision:
                        numOfMoves[0] = 0
                        game.shuffle()
                        complete = False
                        active_playing = False
                        delete_crops(image_type)

        else:
            for event in events:
                if event.type == MOUSEBUTTONDOWN:
                    temp = grid.getCoord(mouse_pos)
                    row, column = temp[0], temp[2]
                    coord = [int(row), int(column)]
                    game.moveByClick(coord,numOfMoves)

                elif event.type == KEYDOWN:
                    game.moveByKeys(keys, numOfMoves)
            
            if settings.isActive:
                settings.draw()
                settings.checkMouse(mouse_pos)
            else:
                screen.fill((255,255,255))
                game.drawSquares()
                if keys[K_TAB]:
                    screen.blit(game.ogpg,(0,0))
                grid.drawGrid()
                if settings.tileNumbers:
                    game.drawTileNumbers()
                if settings.timer:
                    displayFont(ticks, "time", (game.Player.column*200 + 10, game.Player.row*200 + 90))
                if settings.moves:
                    displayFont(numOfMoves[0], "displayMoves", (game.Player.column*200 + 10, game.Player.row*200 + 50))
                grid.selectcheck(mouse_pos, mouse_focus)
                complete = game.checkCompletion()
    else:

        if settings.isActive:
            settings.draw()
            settings.checkMouse(mouse_pos)
        else:
            screen.fill((255,255,255))
            selection.drawSquares()
            grid.drawGrid()

        if beginning_note_bool:
            screen.blit(beginning_note, (100,200))
            displayFont("Note", "beginning_note", (370, 290))
            displayFont("Press TAB to view the Original Image", "beginning_note", (185,350))
            displayFont("Press ESC to view Settings", "beginning_note", (240, 390))
            displayFont("If you upload an image, please", "beginning_note", (230, 450))
            displayFont("ensure that it's 800x800", "beginning_note", (250, 490))
            displayFont("Press SPACE to continue", "beginning_note", (250, 560))
            if keys[pygame.K_SPACE]:
                beginning_note_bool = False

        elif not beginning_note_bool and not settings.isActive:
            grid.selectcheck(mouse_pos, mouse_focus)
            for event in events:
                if event.type == MOUSEBUTTONDOWN:
                    ttemp = grid.getCoord(mouse_pos)
                    rrow, ccolumn = ttemp[0], ttemp[2]
                    ccoord = [int(rrow), int(ccolumn)]

                    if ccoord != [3,3]:
                        image_type = image_cutter(ccoord[0], ccoord[1])
                        canBoxlist = True
                    else:
                        myImageInfo = select_user_image()
                        if myImageInfo:
                            image_type = image_cutter(00,00,myImageInfo)
                            canBoxlist = True

                    if canBoxlist:
                        boxList = []
                        abcdefg = 0
                        for ab in range(0,4):
                            b1 = []
                            for bc in range(0,4):
                                abcdefg += 1
                                box = Box(pygame.image.load(f'{ab}-{bc}.{image_type}'), ab, bc, abcdefg)
                                b1.append(box)
                            boxList.append(b1)

                        game = Game(boxList, ccoord) if myImageInfo == None else Game(boxList, None, myImageInfo[0])
                        game.updateBoxPositions()
                        game.shuffle()

                        active_playing = True
                        start_time = time.time()
                        canBoxlist = False
                        rrow = None
                        ccolumn = None
                        ttemp = ""
                        ccoord = []

    for event in events:
        if event.type == MOUSEBUTTONDOWN and settings.isActive:
            temp = settings.select(mouse_pos)
            if temp and active_playing:
                numOfMoves[0] = 0
                complete = False
                active_playing = False
                delete_crops(image_type)
                settings.isActive = False
            elif temp and not active_playing:
                running = False

    clock.tick(60)
    pygame.display.update()

file_exists = exists(f"0-0.{image_type}")
if file_exists:
    delete_crops(image_type)