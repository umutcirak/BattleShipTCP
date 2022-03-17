import pygame
pygame.init() # Initialize

# Implement game sounds
pygame.mixer.music.load("sounds/theme.mp3")
pygame.mixer.music.play(-1) # Firstly not singing
miss_sound = pygame.mixer.Sound("sounds/miss.wav")
explosion_sound = pygame.mixer.Sound("sounds/explosion.wav")
error_sound = pygame.mixer.Sound("sounds/error.wav")

# Implement game pngs
background = pygame.image.load('images/water.png')
destroyer_h = pygame.image.load('images/destroyer_horizontal.png')
destroyer_v = pygame.image.load('images/destroyer_vertical.png')
submarine_h = pygame.image.load('images/submarine_horizontal.png')
submarine_v = pygame.image.load('images/submarine_vertical.png')

# Implement ship pngs
battleship_h = pygame.image.load('images/battleship_horizontal.png')
battleship_v = pygame.image.load('images/battleship_vertical.png')
carrier_h = pygame.image.load('images/carrier_horizontal.png')
carrier_v = pygame.image.load('images/carrier_vertical.png')
explosion = pygame.image.load('images/explosion.png')


class game: # main game class
    def __init__(self, id):     # initial parameters
        self.id = id
        self.player_ready = False
        self.destroyer = [[0,0], [0,1]]
        self.destroyer_status = [False, 'Horizontal', 'destroyer']
        self.submarine = [[1,0], [1,1], [1,2]]
        self.submarine_status = [False, 'Horizontal', 'submarine']
        self.battleship = [[3,0], [3,1], [3,2], [3,3]]
        self.battleship_status = [False, 'Horizontal', 'battleship']
        self.carrier = [[4,0], [4,1], [4,2], [4,3], [4,4]]
        self.carrier_status = [False, 'Horizontal', 'carrier']
        self.hits = []
        self.misses = []
        self.opponent_hits = []
        self.turn = False if self.id % 2 == 1 else True
        self.grid = []
        self.strikes = 0
        self.game_over = False
        self.display_strikes = False

    def reset(self):                                             # reset all parameters function.
        self.turn = False if self.id % 2 == 1 else True
        self.strikes = 0
        self.game_over = False
        self.player_ready = False
        # Delete all hits and misses, clear grid.
        del self.hits[:]
        del self.misses[:]
        del self.opponent_hits[:]
        del self.grid[:]
        self.destroyer = [[0,0], [0,1]]
        self.destroyer_status = [False, 'Horizontal', 'destroyer']
        self.submarine = [[1,0], [1,1], [1,2]]
        self.submarine_status = [False, 'Horizontal', 'submarine']
        self.battleship = [[3,0], [3,1], [3,2], [3,3]]
        self.battleship_status = [False, 'Horizontal', 'battleship']
        self.carrier = [[4,0], [4,1], [4,2], [4,3], [4,4]]
        self.carrier_status = [False, 'Horizontal', 'carrier']
        self.display_strikes = False

    def check_display_strikes(self, player2):                               # strike control function
        if self.game_over == False and player2.game_over == False:
            self.display_strikes = True

    def get_hits(self, p2):                                                 # get hit control function
        if self.game_over == False:
            self.opponent_hits = p2.hits

    def check_turn(self, p2):                                                # check order function(sırani kontrol et)
        if self.id % 2 != 0:
            if self.strikes < p2.strikes:
                self.turn = True
        else:
            if self.strikes == p2.strikes:
                self.turn = True

    def overlapping(self, ship, _type):                                     #gride yerleştirme fonsk.
        for location in ship:
            if type(self.grid[location[0]][location[1]]) != tuple:
                if self.grid[location[0]][location[1]] != _type:
                    return True
        return False

    def adjust_location(self, ship, _type):                                   #gride yerleştirme fonsk.
        while self.overlapping(ship, _type) == True:
            for location in ship:
                if ship[len(ship)-1][0] != 9:
                    location[0] += 1
                else:
                    location[1] += 1
        return ship

    def update_grid(self):
        grid = [[(255,255,255) for x in range(10)] for y in range(10)]  # 10 a 10 grid built.
        for location in self.destroyer:
           grid[location[0]][location[1]] = "destroyer"

        if self.destroyer_status[0] == True:
            self.submarine = self.adjust_location(self.submarine, "submarine")      # sırayla uygun gemiyi ilgili seçilen koordinata yerlestirme fonksiyonu
            for location in self.submarine:
                grid[location[0]][location[1]] = "submarine"


        if self.submarine_status[0] == True:
            self.battleship = self.adjust_location(self.battleship, "battleship")
            for location in self.battleship:
               grid[location[0]][location[1]] = "battleship"

        if self.battleship_status[0] == True:
            self.carrier = self.adjust_location(self.carrier, "carrier")
            for location in self.carrier:
                grid[location[0]][location[1]] = "carrier"
        return grid

    def refresh_screen(self, screen, player2):          # ekranı yenileme yenilikleri çizdirme fonks.
        screen.fill((0,0,0))
        screen.blit(background,(20,10))
        #gridi ve gemi lokasyonlarını günceller
        self.grid = self.update_grid()
        #gemileri çizer
        self.draw_boats(screen)
        #vuruşları çizer
        self.draw_explosions(screen)
        #player 2 yi çizer
        self.draw_player2(screen, player2)
        #alttaki bilgilendirme yazılarını çizdirme
        if self.game_over == True:
            self.draw_game_over_text(screen)
        else:
            self.draw_text(screen, player2)

        self.check_display_strikes(player2)

    def draw_game_over_text(self, screen):   # oyun biti mi menüsü ve yazıları
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        if len(self.opponent_hits) == 14:
            text1 = font.render("You Lost! ...", True, (255,255,255))
        else:
            text1 = font.render("You Won! ...", True, (255,255,255))
        text2 = font.render("(Press enter to play again.)", True, (255,255,255))
        screen.blit(text1, (430-(text1.get_width()/2), 430))
        screen.blit(text2, (430-(text2.get_width()/2), 452))

    def draw_player2(self, screen, player2):        # karşı oyuncu bildirimleri
        if self.player_ready == True and player2.player_ready == True:
            screen.blit(background,(440,10))
            y_coordinate = -30
            #gridleri çizer
            for item in player2.grid:
                x_coordinate = 440
                y_coordinate += 40
                for color in item:
                    pygame.draw.rect(screen, (255,255,255), (x_coordinate, y_coordinate, 40, 40), 1)
                    x_coordinate += 40
            #ıskalama durumları hesabını burada yapıyoruz
            for location in self.misses:
                x_coordinate = 440+(location[0]*40)
                y_coordinate = 10+(location[1]*40)
                pygame.draw.rect(screen, (255,0,0), (x_coordinate, y_coordinate, 40, 40), 1)
                pygame.draw.line(screen, (255,0,0), (x_coordinate, y_coordinate), (x_coordinate+40, y_coordinate+40), 1)
                pygame.draw.line(screen, (255,0,0), (x_coordinate+40, y_coordinate),(x_coordinate, y_coordinate+40), 1)
            #vuruşları burada çizdiriyoruz
            for location in self.hits:
                x_coordinate = 440+(location[0]*40)
                y_coordinate = 10+(location[1]*40)
                screen.blit(explosion,(x_coordinate, y_coordinate))
        else:
            font1 = pygame.font.Font(pygame.font.get_default_font(), 48)
            text1 = font1.render("Player 2", True, (255,255,255))
            screen.blit(text1, (640-(text1.get_width()/2), 200))

    def draw_text(self, screen, player2):                                               # ekrana bilgilendirme yazılarını ayarladığımız fonks.
        font2 = pygame.font.Font(pygame.font.get_default_font(), 16)
        text3 = None
        if self.player_ready == False and player2.game_over == True:
            text2 = font2.render("Waiting for player 2's reset...", True, (255,255,255))
        elif self.player_ready == False and player2.player_ready == False:
            text2 = font2.render("Locate the ships ...", True, (255,255,255))
            text3 = font2.render("(Arrows: Locate / Space: Spin/ Enter: Confirm)", True, (255,255,255))
        elif self.player_ready == True and player2.player_ready == False:
            text2 = font2.render("Waiting for player 2 ...", True, (255,255,255))
        elif self.player_ready == False and player2.player_ready == True:
            text2 = font2.render("Player 2 is ready...", True, (255,255,255))
        else:
            if self.turn == True:
                text2 = font2.render("Fire with left click...", True, (255,255,255))
            else:
                text2 = font2.render("Waiting for player 2's shoot...", True, (255,255,255))

        if text3 == None:
            screen.blit(text2, (430-(text2.get_width()/2), 445))
        else:
            screen.blit(text2, (430-(text2.get_width()/2), 430))
            screen.blit(text3, (430-(text3.get_width()/2), 452))

    def draw_boats(self, screen):       # draw ships function.
        destroyer_switch = False
        submarine_switch = False
        battleship_switch  = False
        carrier_switch = False
        y_coordinate = -30
        for item in self.grid:
            x_coordinate = 20
            y_coordinate += 40
            for color in item:
                if color == "destroyer" and destroyer_switch == False:
                    if self.destroyer_status[1] == 'Horizontal':
                        screen.blit(destroyer_h,(x_coordinate, y_coordinate))
                    else:
                        screen.blit(destroyer_v,(x_coordinate, y_coordinate))
                    destroyer_switch = True
                if color == "submarine" and submarine_switch == False:
                    if self.submarine_status[1] == 'Horizontal':
                        screen.blit(submarine_h,(x_coordinate, y_coordinate))
                    else:
                        screen.blit(submarine_v,(x_coordinate, y_coordinate))
                    submarine_switch = True
                if color == "battleship" and battleship_switch == False:
                    if self.battleship_status[1] == 'Horizontal':
                        screen.blit(battleship_h,(x_coordinate, y_coordinate))
                    else:
                        screen.blit(battleship_v,(x_coordinate, y_coordinate))
                    battleship_switch = True
                if color == "carrier" and carrier_switch == False:
                    if self.carrier_status[1] == 'Horizontal':
                        screen.blit(carrier_h,(x_coordinate, y_coordinate))
                    else:
                        screen.blit(carrier_v,(x_coordinate, y_coordinate))
                    carrier_switch = True
                x_coordinate += 40

    def draw_explosions(self, screen):      #patlamaları çizdirir
        if self.display_strikes == True:
            for location in self.opponent_hits:
                x_coordinate = 20+(location[0]*40)
                y_coordinate = 10+(location[1]*40)
                screen.blit(explosion,(x_coordinate, y_coordinate))

    def check_hit_miss(self, coords, x, y):     #ıskalı vuruşları çizdirir
        if type(coords) == str:
            if [x, y] not in self.hits:
                self.hits.append([x,y])
                self.turn = False
                self.strikes += 1
                pygame.mixer.Sound.play(explosion_sound)

        elif type(coords) == tuple:
            if [x, y] not in self.misses:
                self.misses.append([x,y])
                self.turn = False
                self.strikes += 1
                pygame.mixer.Sound.play(miss_sound)

    def check_game_over(self, player2):     # check if game is over
        if self.game_over == False and player2.game_over == False:
            if len(self.hits) == 17:
                self.game_over = True
            elif len(self.opponent_hits) == 17:
                self.game_over = True

    def boundary_adjust(self, ship):
        if ship[len(ship)-1][1] > 9:
            if len(ship) == 2:
                ship = [[ship[0][0],8], [ship[1][0],9]]
            elif len(ship) == 3:
                ship = [[ship[0][0],7], [ship[1][0],8], [ship[2][0],9]]
            elif len(ship) == 4:
                ship = [[ship[0][0],6], [ship[1][0],7], [ship[2][0],8], [ship[3][0],9]]
            elif len(ship) == 5:
                ship = [[ship[0][0],5], [ship[1][0],6], [ship[2][0],7], [ship[3][0],8], [ship[4][0],9]]

        if ship[len(ship)-1][0] > 9:
            if len(ship) == 2:
                ship = [[8,ship[0][1]], [9,ship[1][1]]]
            elif len(ship) == 3:
                ship = [[7,ship[0][1]], [8,ship[1][1]], [9,ship[2][1]]]
            elif len(ship) == 4:
                ship = [[6,ship[0][1]], [7,ship[1][1]], [8,ship[2][1]], [9,ship[3][1]]]
            elif len(ship) == 5:
                ship = [[5,ship[0][1]], [6,ship[1][1]], [7,ship[2][1]], [8,ship[3][1]], [9,ship[4][1]]]
        return ship

    def left_adjust(self, boat, boat_type):
        for x in boat:
            if type(self.grid[x[0]][x[1]-1]) != tuple:
                if boat_type != self.grid[x[0]][x[1]-1]:
                    return False
        return True

    def right_adjust(self, boat, boat_type):
        for x in boat:
            if type(self.grid[x[0]][x[1]+1]) != tuple:
                if boat_type != self.grid[x[0]][x[1]+1]:
                    return False
        return True

    def up_adjust(self, boat, boat_type):
        for x in boat:
            if type(self.grid[x[0]-1][x[1]]) != tuple:
                if boat_type != self.grid[x[0]-1][x[1]]:
                    return False
        return True

    def down_adjust(self, boat, boat_type):
        for x in boat:
            if type(self.grid[x[0]+1][x[1]]) != tuple:
                if boat_type != self.grid[x[0]+1][x[1]]:
                    return False
        return True

    def save_old_location(self, ship):
        old_location = []
        for x in ship:
            old_location.append(x)
        return old_location

    def check_overlap(self, ship, _type):
        for x in ship:
            if type(self.grid[x[0]][x[1]]) == str:
                if self.grid[x[0]][x[1]] != _type:
                    pygame.mixer.Sound.play(error_sound)
                    return True
        return False

    def rotate_boat(self, ship, old_direction, _type):
        old_location = self.save_old_location(ship)
        for num in range(1, len(ship)):
            if old_direction == 'Horizontal':
                ship[num] = [ship[0][0]+num, ship[0][1]]
            else:
                ship[num] = [ship[0][0], ship[0][1]+num]
        new_location = self.boundary_adjust(ship)
        overlapping = self.check_overlap(new_location, _type)
        if overlapping == False:
            direction = 'Horizontal' if old_direction == 'Vertical' else 'Vertical'
            location = new_location
        else:
            direction = old_direction
            location = old_location
        return location, direction

    def move_left(self, x_axis, ship, _type):       # grid üzerinde gemi koordinat bilgisini bir sola taşır
        if x_axis != 0:
            if self.left_adjust(ship, _type) == True:
                for y in ship:
                    y[1] -=1
        return ship

    def move_right(self, x_axis, ship, _type):      # grid üzerinde gemi koordinat bilgisini bir sağa taşır
        if x_axis != 9:
            if self.right_adjust(ship, _type) == True:
                for y in ship:
                    y[1] +=1
        return ship

    def move_up(self, y_axis, ship, _type):     # grid üzerinde gemi koordinat bilgisini bir yukarı taşır
        if y_axis != 0:
            if self.up_adjust(ship, _type) == True:
                for y in ship:
                    y[0] -=1
        return ship

    def move_down(self, y_axis, ship, _type):       # grid üzerinde gemi koordinat bilgisini bir aşağı taşır
        if y_axis != 9:
            if self.down_adjust(ship, _type) == True:
                for y in ship:
                    y[0] +=1
        return ship

    def launch_missle(self, position, player2):
        # füze fırlatma kısımı pozisyon hesabına
        # göre ilgili exenlere fırlatılan füzenin atımı orada gemi olup olmadığı vuruş kontrolü burada gerçekleşiyor
        x_axises = [[440, 480], [480, 520], [520, 560], [560, 600], [600, 640], [640, 680], [680, 720], [720, 760], [760, 800], [800, 840]]
        y_axises = [[10, 50], [50,90], [90, 130], [130, 170], [170, 210], [210, 250], [250,290], [290, 330], [330, 370], [370, 410]]
        for x, x_coords in enumerate(x_axises):
            for y, y_coords in enumerate(y_axises):
                if position[0] > x_coords[0] and position[0] < x_coords[1]:
                    if position[1] > y_coords[0] and position[1] < y_coords[1]:
                        self.check_hit_miss(player2.grid[y][x], x, y)

    def set_ship(self):
        if self.destroyer_status[0] == False:
            self.destroyer_status[0] = True
        elif self.submarine_status[0] == False:
            self.submarine_status[0] = True
        elif self.battleship_status[0] == False:
            self.battleship_status[0] = True
        elif self.carrier_status[0] == False:
            self.carrier_status[0] = True
            self.player_ready = True
        else:
            pass

    def left_arrow_pressed(self):
        if self.destroyer_status[0]  == False:
            self.destroyer = self.move_left(self.destroyer[0][1], self.destroyer, self.destroyer_status[2])
        elif self.submarine_status[0] == False:
            self.submarine = self.move_left(self.submarine[0][1], self.submarine, self.submarine_status[2])
        elif self.battleship_status[0] == False:
            self.battleship = self.move_left(self.battleship[0][1], self.battleship, self.battleship_status[2])
        elif self.carrier_status[0] == False:
            self.carrier = self.move_left(self.carrier[0][1], self.carrier, self.carrier_status[2])
        else:
            pass

    def right_arrow_pressed(self):
        if self.destroyer_status[0]  == False:
            self.destroyer = self.move_right(self.destroyer[1][1], self.destroyer, self.destroyer_status[2])
        elif self.submarine_status[0] == False:
            self.submarine = self.move_right(self.submarine[2][1], self.submarine, self.submarine_status[2])
        elif self.battleship_status[0] == False:
            self.battleship = self.move_right(self.battleship[3][1], self.battleship, self.battleship_status[2])
        elif self.carrier_status[0] == False:
            self.carrier = self.move_right(self.carrier[4][1], self.carrier, self.carrier_status[2])
        else:
            pass

    def up_arrow_pressed(self):
        if self.destroyer_status[0]  == False:
            self.destroyer = self.move_up(self.destroyer[0][0], self.destroyer, self.destroyer_status[2])
        elif self.submarine_status[0] == False:
            self.submarine = self.move_up(self.submarine[0][0], self.submarine, self.submarine_status[2])
        elif self.battleship_status[0] == False:
            self.battleship = self.move_up(self.battleship[0][0], self.battleship, self.battleship_status[2])
        elif self.carrier_status[0] == False:
            self.carrier = self.move_up(self.carrier[0][0], self.carrier, self.carrier_status[2])
        else:
            pass

    def down_arrow_pressed(self):
        if self.destroyer_status[0]  == False:
            self.destroyer = self.move_down(self.destroyer[1][0], self.destroyer, self.destroyer_status[2])
        elif self.submarine_status[0] == False:
            self.submarine = self.move_down(self.submarine[2][0], self.submarine, self.submarine_status[2])
        elif self.battleship_status[0] == False:
            self.battleship = self.move_down(self.battleship[3][0], self.battleship, self.battleship_status[2])
        elif self.carrier_status[0] == False:
            self.carrier = self.move_down(self.carrier[4][0], self.carrier, self.carrier_status[2])
        else:
            pass

    def spacebar_pressed(self):
        if self.destroyer_status[0] == False:
            self.destroyer, self.destroyer_status[1] = self.rotate_boat(self.destroyer, self.destroyer_status[1], 'destroyer')
        elif self.submarine_status[0] == False:
            self.submarine, self.submarine_status[1] = self.rotate_boat(self.submarine, self.submarine_status[1], 'submarine')
        elif self.battleship_status[0] == False:
            self.battleship, self.battleship_status[1] = self.rotate_boat(self.battleship, self.battleship_status[1], 'battleship')
        elif self.carrier_status[0] == False:
            self.carrier, self.carrier_status[1] = self.rotate_boat(self.carrier, self.carrier_status[1], 'carrier')
        else:
            pass

    def enter_key_pressed(self):
        if self.game_over == False:
            self.set_ship()
        else:
            self.reset()

    def key_press(self, screen, player2):           # kullanıcı klavye girdileri burada alınır
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        #sol ok tuşu
        if keys[pygame.K_LEFT]:
            self.left_arrow_pressed()
        #sağ ok tuşu
        if keys[pygame.K_RIGHT]:
            self.right_arrow_pressed()
        #yukarı ok
        if keys[pygame.K_UP]:
            self.up_arrow_pressed()
        #aşağı ok
        if keys[pygame.K_DOWN]:
            self.down_arrow_pressed()
        # gemi lokasyonunu onaylama inputu
        if keys[pygame.K_RETURN]:
            self.enter_key_pressed()
        #gemi döndürme inputu
        if keys[pygame.K_SPACE]:
            self.spacebar_pressed()
        #füze fırlatma kısımı
        if mouse[0] and (self.game_over == False and player2.game_over == False):
            if self.turn == True and (self.player_ready and player2.player_ready):
                position = pygame.mouse.get_pos()
                self.launch_missle(position, player2)
