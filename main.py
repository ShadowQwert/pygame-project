import pygame
# ВНИМАНИЕ! если ты ни хрена не поймешь смотри строку 140
cooldownMove = 401
cooldownAttack = 1201
class MainBoard:
    def __init__(self, width, height, widthScreen, heightScreen, image):
        self.width = width # ширина
        self.height = height # высота
        self.widthScreen = widthScreen
        self.heightScreen = heightScreen
        self.image = image
        self.board = [[['EMPTY', ''] for i in range(height)] for i in range(width)] # все клетки
        self.left = 10 # отклонение от края
        self.top = 10
        self.cell_size = 128 # размер клеток
        self.zero_cell = [4, 4]

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        img = pygame.image.load(self.image)
        img = pygame.transform.scale(img, (896, 896))
        screen.blit(img, (0, 0))

    def set_cellNew(self, pos, type):
        self.board[pos[0]][pos[1]] = type

    def remove_cellNew(self, player_pos):
        self.board[player_pos[0]][player_pos[1]] = ['EMPTY', '']

    def check_cell(self, player_pos):
        num_x = player_pos[0]
        num_y = player_pos[1]
        if self.width > num_x >= 0 and 0 <= num_y < self.height and self.board[num_x][num_y][0] == 'EMPTY':
            return True
        else:
            return False


class Player:
    def __init__(self, curX, curY, board):
        self.curX = curX
        self.curY = curY
        img = pygame.image.load('data/player.png')
        self.img = pygame.transform.scale(img, (90, 150))
        board.set_cellNew((self.curX, self.curY), ['PLAYER', self])

    def render(self, screen, x, y):
        screen.blit(self.img, (401, 336))

    def move(self, x, y, board):
        global cooldownMove, cdType
        if cooldownMove >= 400:
            cooldownMove = 0
        if cooldownMove == 0:
            if mainB.check_cell((self.curX + x, self.curY - y)):
                mainB.remove_cellNew((self.curX, self.curY))
                self.curX += x
                self.curY -= y
                mainB.set_cellNew((self.curX, self.curY), ['PLAYER', self])
                board.zero_cell[0] += x
                board.zero_cell[1] -= y
                renderAll()
                pygame.display.flip()
                cdType = 'Move'

    def atack(self, board):
        global cooldownAttack, cdType
        if cooldownAttack >= 1200:
            cooldownAttack = 0
        if cooldownAttack == 0:
            try:
                if board.board[self.curX][self.curY - 1][0] == 'ENEMY':
                    board.board[self.curX][self.curY - 1][1].gethit(1, board)
                    cdType = 'Attack'
            except IndexError:
                pass

class Enemy:
    def __init__(self, hp, x, y, board):
        self.dead = False
        self.hp = hp
        self.curX = x
        self.curY = y
        self.board = board
        img = pygame.image.load('data/SkeletEnemy.png')
        self.img = pygame.transform.scale(img, (100, 150))
        board.set_cellNew((self.curX, self.curY), ['ENEMY', self])

    def render(self, screen, x, y):
        screen.blit(self.img, (x - 128, y - 128))

    def gethit(self, hp, board):
        self.hp -= hp
        if self.hp <= 0:
            board.remove_cellNew((self.curX, self.curY))
            self.dead = True
            renderAll()
            pygame.display.flip()

class Column:
    def __init__(self, x, y, board):
        self.death = False
        self.curX = x
        self.curY = y
        img = pygame.image.load('data/Colona1.png')
        self.img = pygame.transform.scale(img, (150, 150))
        board.set_cellNew((self.curX, self.curY), ['COLUMN', self])

    def render(self, screen, x, y):
        screen.blit(self.img, (x - 128, y - 128))


def renderAll():
    mainB.render(screen)
    sX, sY = mainB.zero_cell
    posX, posY = 120, 64
    for i in range(sX, sX + mainB.widthScreen):
        for j in range(sY, sY + mainB.heightScreen):
            if mainB.board[i][j][1] != '':
                mainB.board[i][j][1].render(screen, posX, posY)
            posY += 128
        posX += 128
        posY = 64


if __name__ == '__main__':
    pygame.init()
    cdType = 'None'
    col2 = 0
    clock = pygame.time.Clock()
    cellSize = 64
    size = width, height = 1024, 896
    screen = pygame.display.set_mode(size)

    # основные объекты
    # короче - что бы создавать объекты для врага пишешь здоровье + координаты по таблице, для коллоны просто корды
    mainB = MainBoard(16, 16, 7, 7, 'data/GeenFlor.jpg')
    mainB.set_view(100, 100, 128)
    player = Player(7, 7, mainB)
    enemy1 = Enemy(1, 3, 5, mainB)
    colon1 = Column(5, 5, mainB)
    colon2 = Column(13, 13, mainB)

    # это типо границы поля
    for x in range(13):
        colon = Column(0, x, mainB)
    for x in range(13):
        colon = Column(x, 0, mainB)
    for x in range(13):
        colon = Column(13, x, mainB)
    for x in range(13):
        colon = Column(x, 13, mainB)

    # прочее
    SwordPic = pygame.transform.scale(pygame.image.load('data/sword.png'), (100, 150))
    screen.blit(SwordPic, (920, 100))
    ArroWPic = pygame.transform.scale(pygame.image.load('data/ArroW.png'), (50, 50))
    screen.blit(ArroWPic, (905, 150))
    myfont1 = pygame.font.SysFont("monospace", 15)
    myfont2 = pygame.font.SysFont("monospace", 20)
    renderAll()
    player.move(0, 0, mainB)
    isPressed = False

    running = True
    while running: # ивееентики))
        clock.tick(10)
        if cdType != 'None':
            cooldownMove += clock.get_time()
            cooldownAttack += clock.get_time()
        pygame.draw.rect(screen, 'black', ((895, 779), (1023, 892)))
        pygame.draw.rect(screen, 'black', ((906, 28), (1014, 96)))
        if cdType == 'Move':
            col2 = round(0.4 - round(cooldownMove / 1000, 2), 2)
        else:
            col2 = round(1.2 - round(cooldownAttack / 1000, 2), 2)
        if col2 < 0:
            col2 = 0
        label = myfont1.render(f"Перезарядка:", True, (255, 255, 0))
        label2 = myfont2.render(str(col2), True, (255, 255, 0))
        label3 = myfont1.render(f"Оружие:", True, (255, 255, 0))
        screen.blit(label, (900, 820))
        screen.blit(label2, (940, 850))
        screen.blit(label3, (930, 60))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)
            keyState = pygame.key.get_pressed()
            if not isPressed:
                if keyState[pygame.K_UP]:
                    player.move(0, 1, mainB)
                    isPressed = True
                    break
                elif keyState[pygame.K_DOWN]:
                    player.move(0, -1, mainB)
                    isPressed = True
                    break
                elif keyState[pygame.K_RIGHT]:
                    player.move(1, 0, mainB)
                    isPressed = True
                    break
                elif keyState[pygame.K_LEFT]:
                    player.move(-1, 0, mainB)
                    isPressed = True
                    break
                if keyState[pygame.K_SPACE]:
                    isPressed = True
                    player.atack(mainB)

            if event.type == pygame.KEYUP:
                isPressed = False
            pygame.event.pump()
    pygame.quit()




