#Sudoku game that can solve itself with backtracking algorithm
#Coded by: Iorga Florin Alexandru
#Controls : 1-9 numpad keys, enter numpad key, delete key and r so that it will solve itself 

import pygame as pg

#pygame initialization
pg.init()
pg.font.init()
pg.display.set_caption("Sudoku")
#Screen
screen_size=(550,600)
screen=pg.display.set_mode(screen_size)
#Colors
White=(255,255,255)
Black=(0,0,0)
Red=(255,0,0)
Grey=(128,128,128)


class Grid:
    col=-1
    row=-1
    board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

    """
    board = [
        [1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 2, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 3],
        [0, 4, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 5, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 6, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    """
    
    def __init__(self):
        # Made a mistake here, what i wanted to do was that the object grid will know wich cube is selected by having two variables:row and
        # col and they were supposed to be equal to the i and j from the board or the cubes array.
        # So the intent was that board[i][j] was reffering to the same cube(or value from cube) from Cubes[i][j].
        # But it's not like that, is reversed so it's board[i][j]=Cubes[j][i].value.
        # This complicated things when i wanted to make it solve itself with backtracking because the function that checks if a number can be
        # placed takes in consideration those two variables: row and col . That's why in the backtracking algorithm row and col are getting
        # modified for each iteration. It didn't destroy the program or something but truly complicated the way it solves itself through 
        # backtracking and the process to get it working.
        # Why didn't i fixed it? Simple answer: I was lazy. I coded half the program without thinking this mistake will cause some problems
        # but when i started coding the backtracking.... oh boy.
        self.Cubes=[[Cube(self.board[j-1][i-1],50,i*50,j*50,i,j,False,can_modify=False if self.board[j-1][i-1]>0 else True)for j in range(1,10)]for i in range(1,10)]

    #Function that draws the cubes and the select highlight
    def draw_grid(self):
        for i in range(9):
            for j in range(9):
                self.Cubes[i][j].draw_cube()
                self.Cubes[i][j].if_selected()

    #Checking if you are clicking on a cube and saving the coordinates so that if another cube is selected the previous cube will 
    #not be highlighted anymore
    def click(self,pos):
        for i in range(9):
            for j in range(9):
                if(self.Cubes[i][j].clicked(pos)):
                    if(self.row>=0 and self.col>=0):
                        self.Cubes[self.row][self.col].selected=False
                        self.Cubes[self.row][self.col].temp=0
                        if(self.row==i and self.col==j):
                            self.row=-1
                            self.col=-1
                        else:
                            self.row=i
                            self.col=j
                    else:
                        self.row=i
                        self.col=j

    #Function that checks if a num can be placed in the board + my 'debuggin' prints when i was coding the backtracking
    def if_num_is_correct(self,num):
        for i in range(9):
            if(num==self.board[self.col][i]):
                self.Cubes[self.row][self.col].selected=False
                self.Cubes[self.row][self.col].temp=0
                #print("I. "+str(num)+" is not good on "+str(self.col)+" "+str(self.row))
                self.row=-1
                self.col=-1
                return False
        for i in range(9):
            if(num==self.board[i][self.row]):
                self.Cubes[self.row][self.col].selected=False
                self.Cubes[self.row][self.col].temp=0
                #print("II. "+str(num)+" is not good on "+str(self.col)+" "+str(self.row))
                self.row=-1
                self.col=-1
                return False
        bo=int(self.col-self.col%3)
        foo=int(self.row-self.row%3)
        for i in range(bo,bo+3):
            for j in range(foo,foo+3):
                if(num==self.board[i][j]):
                    self.Cubes[self.row][self.col].selected=False
                    self.Cubes[self.row][self.col].temp=0
                    #print("III. "+str(num)+" is not good on "+str(self.col)+" "+str(self.row))
                    self.row=-1
                    self.col=-1
                    return False
        #print(str(num)+" worked")
        return True
    
    #Function that checks if every place in the board has been filled with a num>0 thus sudoku is finished(Didn't code a screen that say 
    # you finished tho)
    def is_finished(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j]==0:
                    return (i,j)
        return False
  

    #Backtracking algorithm and modifies every iteration the row and col variable for if_num_is_correct() function
    def solve(self):
        ended=self.is_finished()
        if not ended:
            return True
        else:
            i,j=ended
            for n in range(1,10):
                self.row=j
                self.col=i
                if self.if_num_is_correct(n):
                    self.board[i][j]=n
                    self.Cubes[j][i].value=n

                    if self.solve():
                        return True

                    #print(str(n)+" has been replaced with 0 pe "+str(i)+" "+str(j))
                    self.board[i][j]=0
                    self.Cubes[j][i].value=0
     
        return False

#The grid that is being drawn is made out of 81 objects
class Cube:

    temp=0

    def __init__(self,value,size,coord_x,coord_y,col,row,selected,can_modify):
        self.value=value
        self.size=size
        self.coord_x=coord_x
        self.coord_y=coord_y
        self.row=row
        self.col=col
        self.selected=selected
        self.can_modify=can_modify

    #Method to draw the cube with a value and if it's selected
    def draw_cube(self):
        font=pg.font.SysFont('Comic Sans MS',30)
        cube_width=4 if self.can_modify==False else 2
        if self.selected:
            if(self.value>0):
                text=font.render(str(self.value),1,(Black))
                screen.blit(text,(self.coord_x+17,self.coord_y+4))
                pg.draw.rect(screen,Red,(self.coord_x,self.coord_y,self.size,self.size), cube_width)
            else:
                pg.draw.rect(screen,Red,(self.coord_x,self.coord_y,self.size,self.size), cube_width)
        else:
            if(self.value>0):
                text=font.render(str(self.value),1,(Black))
                screen.blit(text,(self.coord_x+17,self.coord_y+4))
                pg.draw.rect(screen,Black,(self.coord_x,self.coord_y,self.size,self.size), cube_width)
            else:
                pg.draw.rect(screen,Black,(self.coord_x,self.coord_y,self.size,self.size), cube_width)

    #Method that checks if the mouse clicked on the cube 
    def clicked(self,pos):
        if self.can_modify==True:
            if((pos[0]>=self.coord_x and pos[0]<=self.coord_x+self.size) and(pos[1]>=self.coord_y and pos[1]<=self.coord_y+self.size)):
                self.selected=True
                return True
    
    #Method that draws the number choice in right corner of the cube
    def if_selected(self):
        if self.selected:
            if self.temp==0:
                pass
            else:
                font=pg.font.SysFont('Comic Sans MS',20)
                text=font.render(str(self.temp),1,(Grey))
                screen.blit(text,(self.coord_x+3,self.coord_y-4))
    


def draw_window(board):
    screen.fill(White)
    game.draw_grid()


num_choice=0
game=Grid()
run=True
while run:
    pg.time.delay(15)
    for event in pg.event.get():
        if event.type==pg.QUIT:
            run=False
        if event.type==pg.MOUSEBUTTONDOWN:
            pos=pg.mouse.get_pos()
            game.click(pos)
        #After a cube is selected it waits for a number introduced from the keyboard then it's being placed in a temp value in the cube object.
        if event.type == pg.KEYDOWN:
                if event.key == pg.K_KP1:
                    num_choice=1
                    game.Cubes[game.row][game.col].temp=num_choice
                if event.key == pg.K_KP2:
                    num_choice=2
                    game.Cubes[game.row][game.col].temp=num_choice
                if event.key == pg.K_KP3:
                    num_choice=3
                    game.Cubes[game.row][game.col].temp=num_choice
                if event.key == pg.K_KP4:
                    num_choice=4
                    game.Cubes[game.row][game.col].temp=num_choice
                if event.key == pg.K_KP5:
                    num_choice=5
                    game.Cubes[game.row][game.col].temp=num_choice
                if event.key == pg.K_KP6:
                    num_choice=6
                    game.Cubes[game.row][game.col].temp=num_choice
                if event.key == pg.K_KP7:
                    num_choice=7
                    game.Cubes[game.row][game.col].temp=num_choice
                if event.key == pg.K_KP8:
                    num_choice=8
                    game.Cubes[game.row][game.col].temp=num_choice
                if event.key == pg.K_KP9:
                    num_choice=9
                    game.Cubes[game.row][game.col].temp=num_choice
                if event.key == pg.K_DELETE:
                    num_choice=0
                #By pressing enter it modifies the values of the cube from cubes array and the value from the board (knowing the row and col of the cube)
                # with the temp value then temp will be reset and the cube will not be highlighted anymore
                if event.key == pg.K_KP_ENTER:
                    valid=game.if_num_is_correct(num_choice)
                    if valid:
                        game.Cubes[game.row][game.col].value=game.Cubes[game.row][game.col].temp
                        game.Cubes[game.row][game.col].temp=0
                        game.Cubes[game.row][game.col].selected=False
                        game.board[game.col][game.row]=num_choice
                        game.row=-1
                        game.col=-1
                        num_choice=0
                if event.key == pg.K_DELETE:
                        game.Cubes[game.row][game.col].value=0
                        game.Cubes[game.row][game.col].temp=0
                        game.Cubes[game.row][game.col].selected=False
                        game.board[game.col][game.row]=0
                        game.row=-1
                        game.col=-1
                        num_choice=0
                if event.key==pg.K_r:
                    game.solve()
                    game.row=-1
                    game.col=-1
                    num_choice=0
                    #print(board.board)

    draw_window(game)
    pg.display.update()

pg.quit()