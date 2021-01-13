#Made a mistake col and row are inversed not that big of a problem

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
        self.Cubes=[[Cube(self.board[j-1][i-1],50,i*50,j*50,i,j,False,can_modify=False if self.board[j-1][i-1]>0 else True)for j in range(1,10)]for i in range(1,10)]

    def draw_grid(self):
        for i in range(9):
            for j in range(9):
                self.Cubes[i][j].draw_cube()
                self.Cubes[i][j].if_selected()

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
    
    def is_finnished(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j]==0:
                    return (i,j)
        return False
  

    #Backtracking algorithm
    def solve(self):
        ended=self.is_finnished()
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

    def clicked(self,pos):
        if self.can_modify==True:
            if((pos[0]>=self.coord_x and pos[0]<=self.coord_x+self.size) and(pos[1]>=self.coord_y and pos[1]<=self.coord_y+self.size)):
                self.selected=True
                return True
    
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
    board.draw_grid()


num_choice=0
board=Grid()
run=True
while run:
    pg.time.delay(15)
    for event in pg.event.get():
        if event.type==pg.QUIT:
            run=False
        if event.type==pg.MOUSEBUTTONDOWN:
            pos=pg.mouse.get_pos()
            board.click(pos)
        if event.type == pg.KEYDOWN:
                if event.key == pg.K_1:
                    num_choice=1
                    board.Cubes[board.row][board.col].temp=num_choice
                if event.key == pg.K_2:
                    num_choice=2
                    board.Cubes[board.row][board.col].temp=num_choice
                if event.key == pg.K_3:
                    num_choice=3
                    board.Cubes[board.row][board.col].temp=num_choice
                if event.key == pg.K_4:
                    num_choice=4
                    board.Cubes[board.row][board.col].temp=num_choice
                if event.key == pg.K_5:
                    num_choice=5
                    board.Cubes[board.row][board.col].temp=num_choice
                if event.key == pg.K_6:
                    num_choice=6
                    board.Cubes[board.row][board.col].temp=num_choice
                if event.key == pg.K_7:
                    num_choice=7
                    board.Cubes[board.row][board.col].temp=num_choice
                if event.key == pg.K_8:
                    num_choice=8
                    board.Cubes[board.row][board.col].temp=num_choice
                if event.key == pg.K_9:
                    num_choice=9
                    board.Cubes[board.row][board.col].temp=num_choice
                if event.key == pg.K_DELETE:
                    num_choice=0
                if event.key == pg.K_KP_ENTER:
                    valid=board.if_num_is_correct(num_choice)
                    if valid:
                        board.Cubes[board.row][board.col].value=board.Cubes[board.row][board.col].temp
                        board.Cubes[board.row][board.col].temp=0
                        board.Cubes[board.row][board.col].selected=False
                        board.board[board.col][board.row]=num_choice
                        board.row=-1
                        board.col=-1
                        num_choice=0
                if event.key==pg.K_r:
                    board.solve()
                    board.row=-1
                    board.col=-1
                    num_choice=0
                    #print(board.board)

    draw_window(board)
    pg.display.update()

pg.quit()