import pygame
from Saskes.constants import WIDTH, HEIGHT, SQUARE_SIZE, WHITE
from Saskes.game import Game
from minimax.algorithm import minimax
import mysql.connector
from ftplib import FTP
import os

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Saskes")
pygame.init()


def mouse_coordinates():  # grazina peles koordinates C:\Users\PC\AppData\Local\Programs\Python\Python38
    x, y = pygame.mouse.get_pos()

    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE

    return int(row), int(col)


def take_data_from_database():
    name = input("Iveskite vartotojo varda")

    if name != '':
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="dbaze"
        )
        dbcursor = db.cursor()

        dbcursor.execute("SELECT pirktosPrekes FROM vartotojai WHERE vartotojaiVardas=%s", (name,))
        result = dbcursor.fetchone()

        resultString = ""
        if result is not None:
            if all(result):
                for k in result:
                    resultString += k
        boughtProducts = list(filter(None, resultString.rsplit("*")))
        return list(dict.fromkeys(boughtProducts))

    else:
        return ''

def take_img_from_ftp(boughtProducts):
    host = "localhost"
    user = "rejus"
    password = "123"
    with FTP(host) as ftp:
        ftp.login(user=user, passwd=password)
        print(ftp.getwelcome())
        ftp.encoding = 'utf-8'

        for i in range(len(boughtProducts)):
            try:
                with open('assets/' + boughtProducts[i], 'wb') as f:
                    ftp.retrbinary("RETR " + boughtProducts[i], f.write, 1024)
            except:
                print("Nuotrauka nerasta " + str(i))
                os.remove('assets/' + boughtProducts[i])
                boughtProducts[i] = None

        ftp.quit()
        return list(filter(None, boughtProducts))


def main():
    run = True
    clock = pygame.time.Clock()
    boughtProducts = take_data_from_database() # grazina nupurktu produktu lista
    if boughtProducts != '':
        boughtProducts = take_img_from_ftp(boughtProducts) # grazina galimus produktus
    game = Game(WIN, boughtProducts)

    while run:
        clock.tick(FPS)

        if game.turn == WHITE: # kompiuterio ejimas
            value, new_board = minimax(game.get_board(), 2, WHITE) # grazina nauja lenta kuri turi irasyta geriausia judesi
            game.ai_move(new_board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                row, col = mouse_coordinates()
                game.select(row, col) # paiima saske

        game.update() #atnaujina zaidima/lenta

    for product in boughtProducts: # istrina nuotraukas assets folderyje
        if os.path.exists('assets/' + product):
            os.remove('assets/' + product)
    pygame.quit()


main()
