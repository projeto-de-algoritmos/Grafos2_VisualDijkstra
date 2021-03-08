import pygame, sys, random, math
from collections import deque
from tkinter import messagebox, Tk
size = (width, height) = 640, 480
pygame.init()
win = pygame.display.set_mode(size)
pygame.display.set_caption("Dijkstra Visual")
relogio = pygame.time.Clock()
cols, rows = 64, 48
w = width // cols
h = height // rows
grid = []
queue, visitado = deque(), []
path = []
class Ponto:
    def __init__(self, i, j):
        self.x, self.y = i, j
        self.f, self.g, self.h = 0, 0, 0
        self.vizinhos = []
        self.anterior = None
        self.parede = False 
        self.visitado = False
        if random.randint(0, 100) < 20:
            self.parede = True ## Caso deseje testar o programa sem nenhuma parede, mudar essa variavel para True

    def show(self, win, col, shape=1):
        if self.parede == True:
            col = (0, 0, 0)
        if shape == 1:
            pygame.draw.rect(win, col, (self.x * w, self.y * h, w - 1, h - 1))
        else:
            pygame.draw.circle(win, col, (self.x * w + w // 2, self.y * h + h // 2), w // 3)

    def add_vizinho(self, grid):
        if self.x < cols - 1:
            self.vizinhos.append(grid[self.x + 1][self.y])
        if self.x > 0:
            self.vizinhos.append(grid[self.x - 1][self.y])
        if self.y < rows - 1:
            self.vizinhos.append(grid[self.x][self.y + 1])
        if self.y > 0:
            self.vizinhos.append(grid[self.x][self.y - 1])
def clickParede(pos, state):
    i = pos[0] // w
    j = pos[1] // h
    grid[i][j].parede = state
def place(pos):
    i = pos[0] // w
    j = pos[1] // h
    return w, h
for i in range(cols):
    arr = []
    for j in range(rows):
        arr.append(Ponto(i, j))
    grid.append(arr)

for i in range(cols):
    for j in range(rows):
        grid[i][j].add_vizinho(grid)

start = grid[cols // 2][rows // 2]
end = grid[cols - 50][rows - cols // 2]
start.parede = False
end.parede = False

queue.append(start)
start.visitado = True


def main():
    flag = False
    noflag = True
    startflag = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if pygame.mouse.get_pressed(3):
                    clickParede(pygame.mouse.get_pos(), True)
                if pygame.mouse.get_pressed(5):
                    clickParede(pygame.mouse.get_pos(), False)
            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    clickParede(pygame.mouse.get_pos(), True)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    startflag = True

        if startflag:
            if len(queue) > 0:
                current = queue.popleft()
                if current == end:
                    temp = current
                    while temp.anterior:
                        path.append(temp.anterior)
                        temp = temp.anterior
                    if not flag:
                        flag = True
                        messagebox.showinfo("Caminho encontrado!", "O caminho foi encontrado :D")
                        print("Achou!")
                    elif flag:
                        continue
                if flag == False:
                    for i in current.vizinhos:
                        if not i.visitado and not i.parede:
                            i.visitado = True
                            i.anterior = current
                            queue.append(i)
            else:
                if noflag and not flag:
                    Tk().wm_withdraw()
                    messagebox.showinfo("Não foi achado nenhum caminho", "Não foi achado nenhum caminho D=")
                    noflag = False
                else:
                    continue

        win.fill((0, 20, 20))
        for i in range(cols):
            for j in range(rows):
                ponto = grid[i][j]
                ponto.show(win, (44, 62, 80))
                if ponto in path:
                    ponto.show(win, (192, 57, 43))
                elif ponto.visitado:
                    ponto.show(win, (39, 174, 96))
                if ponto in queue:
                    ponto.show(win, (44, 62, 80))
                    ponto.show(win, (39, 174, 96), 0)
                if ponto == start:
                    ponto.show(win, (0, 255, 200))
                if ponto == end:
                    ponto.show(win, (0, 120, 255))
        pygame.display.flip()
main()