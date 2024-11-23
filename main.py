import pygame
import time
import random

snake_speed = 15

#la taille de la fenetre
window_x = 480
window_y = 480

#definition des couleurs
noir = pygame.Color(0, 0, 0)
blanc = pygame.Color(255, 255, 255)
rouge = pygame.Color(255, 0, 0)
vert = pygame.Color(0, 255, 0)
bleu = pygame.Color(0, 0, 255)
fond = pygame.Color(48, 213, 200)

#initialisation de la fenetre
pygame.init()

pygame.display.set_caption("Snake")
fenetre = pygame.display.set_mode((window_x, window_y))

#controle du fps
fps = pygame.time.Clock()

#la position du serpent
position_serpent = [100, 50]

#le corps du serpent
corps = [
    [100, 50],
    [90, 50],
    [80, 50],
    [70, 50],
]

#la position du fruit
position_fruit = [random.randrange(1, window_x // 10) * 10,
                  random.randrange(1, window_y // 10) * 10]
parution_fruit = True

#le positionnement du serpent par deffaut
direction = "RIGHT"
change_to = direction

#la gestion du score
score = 0

#la fonction pour changer le score
def changer_score(couleur, polis, taille) -> None:
    score_polis = pygame.font.SysFont(polis, taille)
    score_surface = score_polis.render("Score: " + str(score), True, couleur)

    #creation du rectangle pour le score
    score_rect = score_surface.get_rect()

    fenetre.blit(score_surface, score_rect)

#la fonction qui affiche le score en cas de defaite
def defaite() -> None:
    defaite_polis = pygame.font.SysFont('times new roman', 50)
    defaite_surface = defaite_polis.render("Votre score est: " + str(score), True, rouge)

    defaite_rect = defaite_surface.get_rect()

    #specifier la position du text
    defaite_rect.midtop = (window_x/2, window_y/4)

    #affichage du text sur l'ecran
    fenetre.blit(defaite_surface, defaite_rect)
    pygame.display.flip()

    #3 secondes de delai avnt de quiter le jeu
    time.sleep(3)

    pygame.quit()

    quit()

if __name__ == "__main__":
    while True:

        # handling key events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'

        # If two keys pressed simultaneously
        # we don't want snake to move into two
        # directions simultaneously
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        # Moving the snake
        if direction == 'UP':
            position_serpent[1] -= 10
        if direction == 'DOWN':
            position_serpent[1] += 10
        if direction == 'LEFT':
            position_serpent[0] -= 10
        if direction == 'RIGHT':
            position_serpent[0] += 10

        #mecanism de croissance du serpent
        #si le serpent mange le fruit on augmante le score par 10

        corps.insert(0, list(position_serpent))
        if position_serpent[0] == position_fruit[0] and position_serpent[1] == position_fruit[1]:
            score += 10
            parution_fruit = False

        else:
            corps.pop()

        if not parution_fruit:
            position_fruit = [random.randrange(1, window_x // 10) * 10,
                              random.randrange(1, window_y // 10) * 10]

        parution_fruit = True
        fenetre.fill(fond)

        for partie in corps:
            pygame.draw.rect(fenetre, rouge, pygame.Rect(partie[0], partie[1], 10, 10))

        pygame.draw.rect(fenetre, blanc, pygame.Rect(position_fruit[0], position_fruit[1], 10, 10))

        #les conditions de defaite
        if position_serpent[0] < 0 or position_serpent[0] > (window_x - 10):
            defaite()


        if position_serpent[1] < 0 or position_serpent[1] > (window_y - 10):
            defaite()

        for block in corps[1:]:
            if position_serpent[0] == block[0] and position_serpent[1] == block[1]:
                defaite()

        #affichage du score
        changer_score(bleu, "times new roman", 20)

        #mise a jour de la fenetre
        pygame.display.update()
        fps.tick(snake_speed)
