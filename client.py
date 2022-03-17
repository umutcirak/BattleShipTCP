import pygame
from network import Network
from battleship import game
# istemcinin kodudur server üzerinden verileri , battleship py üzerinden enviromenti miras alır

def redrawWindow(screen, player1, player2): # istemci ekranına çizdirme kodu
    player1.refresh_screen(screen, player2)
    pygame.display.update()

def main(): # istemci ana kodu
    running = True
    n = Network()
    p1 = n.connection
    pygame.display.set_caption('Battleship')    # Frame Topic
    pygame.display.set_icon(pygame.image.load('images/battleshipicon.jpg'))
    screen_height = 500
    screen_width = 860
    screen = pygame.display.set_mode((screen_width, screen_height)) # create frame
    clock = pygame.time.Clock()

    while running:              # istemci main loop
        clock.tick(10)
        p2 = n.send(p1)     # data sending
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
        if running == False:
            break
        p1.check_turn(p2) # check order
        p1.get_hits(p2) # hit control
        p1.check_game_over(p2)  # game status control
        if p1.player_ready == False and p2.game_over == True:
            pass
        else:
            p1.key_press(screen, p2)
        redrawWindow(screen, p1, p2)
main()
