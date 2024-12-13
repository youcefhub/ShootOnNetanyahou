import random
import sys
import pygame

from pygame import * #importer les cst

LARGEUR_ECRAN = 1200
HAUTEUR_ECRAN = 700

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)
JAUNE = (255, 255, 0)

# Initialisation de Pygame
pygame.init()
pygame.display.set_caption("FREE PALESTINE") #Titre de la fenetre

# Configuration de l'écran
ecran = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))
clock = pygame.time.Clock()

# Police pour les textes
police_titre = pygame.font.SysFont("arialblack", 50)
police_option = pygame.font.SysFont("Comic Sans MS", 50)

def reinitialiser_jeu():
    son_menu.play()
    son_jeu.stop()
    global tous_sprites, le_missile, les_ennemies, les_etoiles, les_explosions, le_boss, les_projectiles
    global vaisseau, score, boss_active, boss, intervall

    # Réinitialiser les groupes de sprites
    tous_sprites.empty()
    le_missile.empty()
    les_ennemies.empty()
    les_etoiles.empty()
    les_explosions.empty()
    le_boss.empty()
    les_projectiles.empty()

    # Réinitialiser les variables du jeu
    boss_active = False
    boss = None
    intervall = 500
    pygame.time.set_timer(Ajouter_ennemie, intervall)  # Redémarre l'ajout des ennemis
    pygame.time.set_timer(Ajouter_etoile, 100)  # Redémarre l'ajout des étoiles

    # Recréer les objets du jeu
    vaisseau = Vaisseau()
    score = Score()
    tous_sprites.add(vaisseau)
    tous_sprites.add(score)

    # Revenir au menu principal
    afficher_menu(ecran)

# Fonction pour dessiner un texte centré
def afficher_texte(texte, police, couleur, ecran, y):
    surface_texte = police.render(texte, True, couleur)
    rect_texte = surface_texte.get_rect(center=(LARGEUR_ECRAN // 2, y))
    ecran.blit(surface_texte, rect_texte)
def afficher_image(ecran, y):
    surface_image = pygame.image.load("DrapeauPAL.jpg").convert()
    #surface_image.set_colorkey((0,0,0))
    rect_image = surface_image.get_rect(center=(LARGEUR_ECRAN // 2, y))
    ecran.blit(surface_image, rect_image)

#CREATION DU MENU PRINCIPAL
def afficher_menu(ecran):
    menu_ouvert = True
    while menu_ouvert:
        #LES OPTIONS
        afficher_image(ecran, 400)
        afficher_texte("SHOOT ON NETANYAHOU", police_titre, JAUNE, ecran,150)
        afficher_texte("1- JOUER", police_titre, NOIR, ecran,350)
        afficher_texte("2- QUITTER", police_titre, NOIR, ecran,450)
        pygame.display.flip()

        #GESTION DU MENU
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # Touche 1 pour démarrer le jeu
                    menu_ouvert = False  # Quitte la boucle du menu
                elif event.key == pygame.K_2:  # Touche 2 pour quitter
                    pygame.quit()
                    sys.exit()

class Vaisseau(pygame.sprite.Sprite): #class vaisseau qui dérive de la classe de base "sprite"

    def __init__(self): # constructeur
        super(Vaisseau, self).__init__() #fonction super appelle la class mère
        self.surf = pygame.image.load('drapeau.png')# "convert()" sert a convertir le png en surface
        self.surf.set_colorkey((0, 0, 0))# on remplace le fond noir par un couleur transparente
        self.rect = self.surf.get_rect()
        son_menu.play()
        #DEPLACEMENT DU VAISSEAU
    def update(self, pressed_key): #la méthode update met à jour le vaisseau à chaque tour de boucle
        if pressed_key[K_UP]: # vers le haut
            self.rect.move_ip(0, -5)# 5 pixels
#REMARQUE : les valeurs min sont au coin sup gauche et max au coin inf droit
        if pressed_key[K_DOWN]:
            self.rect.move_ip(0,  5)
        if pressed_key[K_RIGHT]:
            self.rect.move_ip(5, 0)
        if pressed_key[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_key[K_SPACE]:
            if len(le_missile.sprites()) < 1 :  # la fonction len determine la taille du sprite
              missile = Missile(self.rect.center) # centre du vaisseau
              tous_sprites.add(missile) # ajoute aux groupes de sprites
              le_missile.add(missile) # ajoute au gorupe du missile
        if pressed_key[K_RETURN]:
           reinitialiser_jeu()
#LES LIMITES DE L'ECRAN
        if self.rect.left <0:
            self.rect.left = 0
        if self.rect.right > LARGEUR_ECRAN:
            self.rect.right = LARGEUR_ECRAN
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= HAUTEUR_ECRAN:
            self.rect.bottom = HAUTEUR_ECRAN

#CREATION DES MISSILES
class Missile(pygame.sprite.Sprite): #class missile qui dérive de la classe de base "sprite"

    def __init__(self, center_missile): # constructeur
        super(Missile, self).__init__() #fonction super appelle la class mère
        self.surf = pygame.image.load('SAROUKH2.png').convert() # "convert()" sert a convertir le png en surface
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)# on remplace le fond noir par un couleur transparente
        self.rect = self.surf.get_rect(center = center_missile) # son centre sera le centre du vaisseau
        son_missile.play()
     # METHODE UPDATE POUR LE MISSILE
    def update(self):
         self.rect.move_ip(15, 0)  # 15 pix/cycle
         if self.rect.left > LARGEUR_ECRAN:
                self.kill() # si le missile sort de l'ecran il n'existera plus

#CREATION DE L'ENNEMIE
class Ennemie(pygame.sprite.Sprite):

    def __init__(self):  # constructeur
        super(Ennemie, self).__init__()  # fonction super appelle la class mère
        self.surf = pygame.image.load('Netanyahou.jpg') # "convert()" sert a convertir le png en surface
        self.surf.set_colorkey((0, 0, 0))  # on remplace le fond blanc par une couleur transparente
        # Les ennemies apparaissent sur la droite de l'ecran à une hauteur au hazard
        self.rect = self.surf.get_rect(
            center=(
                LARGEUR_ECRAN + 50, # sur la droite
                random.randint(0, HAUTEUR_ECRAN), #  hauteur au hazard
            )
        )
        # VITESSE DE L'ENNEMIE
        self.speed = random.randint(5, 20)  # Vitesse prise au hazard

    # METHODE UPDATE POUR L'ENNEMIE
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()  # si l'ennemie sort de l'ecran il n'existera plus

#CREATION DES ETOILES
class Etoile(pygame.sprite.Sprite):
    def __init__(self):
        super(Etoile, self).__init__()
        self.surf = pygame.image.load("Etoile.png")
        self.surf.set_colorkey((0, 0, 0))
        self.rect = self.surf.get_rect(
            center=(
                LARGEUR_ECRAN + 20,
                random.randint(0 , HAUTEUR_ECRAN),
            )
        )
   # METHODE UPDATE POUR L'ETOILE
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()  # si l'etoile sort de l'ecran elle n'existera plus

#PROJECTILE DU BOSS
class Projectile(pygame.sprite.Sprite):
    def __init__(self, center_projectiles):
        super(Projectile, self).__init__()
        self.surf = pygame.image.load("bouledefeux.JPG").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)  # Rouge pour les projectiles du boss
        self.rect = self.surf.get_rect(center = center_projectiles) # son centre sera le centre du vaisseau

    def update(self):
        self.rect.move_ip(-20, 0)  # 15 pix/cycle
        if self.rect.left > LARGEUR_ECRAN:
            self.kill()  # si le missile sort de l'ecran il n'existera plus


#CREATION DU BOSS
class Boss(pygame.sprite.Sprite):
    def __init__(self):  # constructeur
        super(Boss, self).__init__()
        self.surf = pygame.image.load('BOSS1.jpg').convert()
        self.surf.set_colorkey((0, 0, 0))
        self.rect = self.surf.get_rect(
            center=(
                LARGEUR_ECRAN + 200, # sur la droite
                HAUTEUR_ECRAN//2
            )
        )
        self.hp = 5 # Points de vie
        self.speed_x = -30 # Vitesse horizontale initiale
        self.speed_y = 0  # Vitesse verticale initiale
        self.direction_change_cooldown = 0  # Timer pour limiter les changements de direction
        self.max_speed_y =  10  # Vitesse maximale verticale
        self.shoot_cooldown = 20  # Temps entre chaque tir (en frames)
        self.shoot_timer = 0  # Timer pour le tir
        son_jeu.play()
        son_menu.stop()
    def update(self):
        # Déplacement horizontal
        if self.rect.right > LARGEUR_ECRAN - 50:
            self.rect.x += self.speed_x
        else:
            # Timer pour limiter les changements de direction
            if self.direction_change_cooldown > 0:
                self.direction_change_cooldown -= 1

            # Changer de direction verticalement si le cooldown est écoulé
            if self.direction_change_cooldown <= 0:
                self.speed_y = random.uniform(-self.max_speed_y, self.max_speed_y)  # Nouvelle vitesse verticale
                self.direction_change_cooldown = 150  # Temps avant le prochain changement (en frames)

            # Appliquer la vitesse verticale
            self.rect.y += self.speed_y
            # Empêcher le boss de sortir de l'écran verticalement
            if self.rect.top < 0:
                self.rect.top = 0
                self.speed_y = abs(self.speed_y)  # Rebond vers le bas
            elif self.rect.bottom > HAUTEUR_ECRAN:
                self.rect.bottom = HAUTEUR_ECRAN
                self.speed_y = -abs(self.speed_y)  # Rebond vers le haut
         # Gestion du tir
        if self.shoot_timer <= 0:
            # Créer un projectile
            projectile = Projectile(self.rect.center)
            tous_sprites.add(projectile)  # Ajouter le projectile aux groupes
            les_projectiles.add(projectile)  # Ajouter le projectile au groupe de projectiles
            self.shoot_timer = self.shoot_cooldown  # Réinitialiser le timer de tir
        else:
            self.shoot_timer -= 1  # Décrémenter le timer à chaque frame

    # Fonction pour infliger des dégâts au boss
    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.kill()
            # Affiche l'écran de victoire
            victoire = Victoire()
            tous_sprites.add(victoire)

#CREATION DES EXPLOSIONS
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center_vaisseau):
        self._compteur = 10 # on affiche l'explosion pendant 10 cycles
        super(Explosion, self).__init__()
        self.surf = pygame.image.load("EXPLOSION2.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = center_vaisseau )
        son_explosion.play()
   # METHODE UPDATE POUR L'EXPLOSION
    def update(self):
        self._compteur = self._compteur - 1 # decrémentation du compteur
        if self._compteur == 0 :
            self.kill()
#AFFICHAGE SCORE
class Score(pygame.sprite.Sprite):
    def __init__(self):
        super(Score, self).__init__()
        self.scoreInit = 0
        self._setText()
    def _setText(self):
        self.surf = police_score.render(
            'Score : '+ str(self.scoreInit), False, (255,255,255))
        self.rect = self.surf.get_rect(
            center = (LARGEUR_ECRAN / 2, 15)
        )
# METHODE UPDATE POUR LE TEXT
    def update(self):
        self._setText()
# INCREMENTATION DU SCORE
    def increment(self, valeur):
        self.scoreInit = self.scoreInit + valeur

#GAME OVER
class Gameover(pygame.sprite.Sprite):
    def __init__(self):
        super(Gameover, self).__init__()
        self.surf = pygame.image.load("GAMEOVER.png").convert()
        self.surf.set_colorkey((0, 0, 0))
        self.rect = self.surf.get_rect( center = ( LARGEUR_ECRAN // 2,
                                                   HAUTEUR_ECRAN // 2))
        son_menu.stop()
        son_fin.play()
        son_defaite.play()

#VICTOIRE
class Victoire(pygame.sprite.Sprite):
    def __init__(self):
        super(Victoire, self).__init__()
        self.surf = pygame.image.load("VICTOIRE.jpg").convert()
        self.surf.set_colorkey((0, 0, 0))
        self.rect = self.surf.get_rect(center=(LARGEUR_ECRAN // 2,
                                               HAUTEUR_ECRAN // 2))

pygame.font.init()
police_score = pygame.font.SysFont('Comic sans MS', 30)

#REGLAGE SON
pygame.mixer.init() #intitialisation du mixer qui gère tout les sons du jeu
son_jeu = pygame.mixer.Sound("Star Wars - The Imperial March.mp3")
son_missile = pygame.mixer.Sound("Missile.ogg")
son_explosion = pygame.mixer.Sound("Crie.ogg")
son_fin = pygame.mixer.Sound("game-over-160612.mp3")
son_levelup = pygame.mixer.Sound("fade-in-pitch-up-space-82425.mp3")
son_defaite = pygame.mixer.Sound("failure-1-89170.mp3")
son_menu = pygame.mixer.Sound("Palestine.mp3")

clock = pygame.time.Clock() # On appel l'horloge


# On genere des évennements à intervale régulier
intervall = 500
Ajouter_ennemie = pygame.USEREVENT + 1 # nouvel evennement
pygame.time.set_timer(Ajouter_ennemie, intervall) # chaque 500 ms
Ajouter_etoile = pygame.USEREVENT + 2
pygame.time.set_timer(Ajouter_etoile, 100)

#LES GROUPES DE SPRITES
tous_sprites = pygame.sprite.Group()
#Missile
le_missile = pygame.sprite.Group() # groupe qui contient que le missile
#Boss de fin
le_boss = pygame.sprite.Group()
#Ennemie
les_ennemies =  pygame.sprite.Group()
#Etoile
les_etoiles = pygame.sprite.Group()
#Explosion
les_explosions = pygame.sprite.Group()
#Projectile boss
les_projectiles = pygame.sprite.Group()

#OBJET
vaisseau = Vaisseau() # création du vaisseau
tous_sprites.add(vaisseau) # on ajoute notre vaisseau au groupe
score = Score()
tous_sprites.add(score)
boss_active = False  # Indique si le boss est présent
boss = None  # Référence au boss
#GAME LOOP
afficher_menu(ecran)
continuer = True
while continuer:
    for event in pygame.event.get(): #on recupère les evennements
        if event.type == pygame.QUIT:
            continuer = False
        elif event.type == Ajouter_ennemie:
            if not boss_active:
            #Cree un nouvel ennemie et on l'ajoute à la classe ennemie
               nouvel_ennemie = Ennemie()
            #Rendre le jeu plus difficile en augumentant la fréquence d'ajout des ennemies
               if intervall > 100 :
                  intervall -= 3
                  pygame.time.set_timer(Ajouter_ennemie, intervall)
             #On l'ajoute aussi au groupe de sprite
               les_ennemies.add(nouvel_ennemie)
               tous_sprites.add(nouvel_ennemie) # pour qu'il soit dessiner

        elif event.type == Ajouter_etoile:
            #Cree une nouvelle etoile et on l'ajoute à la classe etoile
             nouvelle_etoile = Etoile()
             #On l'ajoute aussi au groupe de sprite
             les_etoiles.add(nouvelle_etoile)
             tous_sprites.add(nouvelle_etoile) # pour qu'il soit dessiner

        if score.scoreInit >= 5 and not boss_active:  # Le boss apparaît à un score de 50
             boss = Boss()
             le_boss.add(boss)
             tous_sprites.add(boss)
             boss_active = True

    ecran.fill((0, 0, 0)) # ecran noir

   #DETECTION DES COLLISIONS ENTRE ENNEMIE ET VAISSEAU
    if pygame.sprite.spritecollideany(vaisseau, les_ennemies) or pygame.sprite.spritecollideany(vaisseau, les_projectiles):
        vaisseau.kill()
        explosion = Explosion(vaisseau.rect.center) # au centre du vaisseau
        les_explosions.add(explosion)
        tous_sprites.add(explosion)
        gameover = Gameover()
        tous_sprites.add(gameover)
        # Pause pour afficher l'écran de défaite
        for _ in range(150):
            ecran.fill(NOIR)
            tous_sprites.update()
            for mon_sprite in tous_sprites:
                ecran.blit(mon_sprite.surf, mon_sprite.rect)
            pygame.display.flip()
            clock.tick(40)
        reinitialiser_jeu()

    # DÉTECTION DES COLLISIONS ENTRE MISSILE ET BOSS
    if boss_active:  # Si le boss est présent
        for missile in le_missile:
            boss_touche = pygame.sprite.spritecollide(missile, le_boss, False) # Collision avec le boss
            if len(boss_touche)>0:
                missile.kill()  # Détruire le missile
                boss.take_damage(1)  # Infliger 1 point de dégâts
                score.increment(len(boss_touche))  # Augmenter le score
                for boss in boss_touche:
                    explosion = Explosion(boss.rect.center)
                    les_explosions.add(explosion)
                    tous_sprites.add(explosion)

    # DETECTION DES COLLISIONS ENTRE ENNEMIE ET MISSILE
    for missile in le_missile :  # pour chaque missile contenu dans le groupe de missile
        ennemie_touché = pygame.sprite.spritecollide(missile, les_ennemies, True)
        if len(ennemie_touché)>0:
            missile.kill()
            score.increment(len(ennemie_touché))
        for ennemi in ennemie_touché :
            explosion = Explosion(ennemi.rect.center)
            les_explosions.add(explosion)
            tous_sprites.add(explosion)

    touche_appuyer = pygame.key.get_pressed() #on récupère la touche

#LES MISES A JOURS DES GROUPES DE SPRITES
    vaisseau.update(touche_appuyer) # et on update les touche au vaisseau
    le_missile.update() # On met à jour le groupe du missile aussi
    le_boss.update()
    les_ennemies.update()
    les_etoiles.update()
    les_explosions.update()
    score.update()
    les_projectiles.update()

#BLIT de tous les éléments contenue dans tous_sprites
    for mon_sprite in tous_sprites:
       ecran.blit(mon_sprite.surf, mon_sprite.rect)# block transfert "blit" recopier sur l'ecran ce qui est dessiner sur le vaisseau

    pygame.display.flip() # flip du display pour afficher ce qu'on a créer sur la fenetre

    clock.tick(35) # On indique a pygame de ne pas réaliser cette boucle plus de 32 fois/sec

pygame.time.delay(4000)
pygame.quit()
