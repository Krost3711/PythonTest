import pygame
import random
import math
from pygame import mixer

# Inicializamos todos los metodos de pygame
pygame.init()

#Crear Pantalla Principal
pantalla = pygame.display.set_mode((800,600))

# Titulo he Icono
pygame.display.set_caption("Invasion Espacial")
icono = pygame.image.load("nave-espacial.png")
pygame.display.set_icon(icono)
fondo = pygame.image.load("Fondo.jpg")

# Agregar Musica
mixer.music.load('MusicaFondo.mp3')
mixer.music.set_volume(0.1)
mixer.music.play(-1) # -1 Significa que se va a repetir cada vez que termine

#AGREGADO (Variable de Formato Texto)
# Se define el formato del texto
font = pygame.font.SysFont("Arial",16)

#AGREGADO Variables Agregadas
leyendas_app = pygame.font

# Texto Final de Juego
fuente_final = pygame.font.Font('freesansbold.ttf', 42)

# Puntaje
puntaje = 0
fuente = pygame.font.Font("freesansbold.ttf", 32)
texto_x = 10
texto_y = 10

# Variables del Jugador
img_jugador = pygame.image.load("nave-espacial2.png")
jugador_x = 368
jugador_y = 500
jugador_x_cambio = 0

# Variables Enemigos para mas de un Enemigo
#Conjunto de Listas Vacias
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 8

# Variables del Enemigo
for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load("enemigos.png"))
    enemigo_x.append(random.randint(0,736))
    enemigo_y.append(random.randint(50,200))
    enemigo_x_cambio.append(0.2)  # Al estar en 0.2 genera el movimiento
    enemigo_y_cambio.append(15)

# Variables de la bala
balas = []
img_bala= pygame.image.load("bala.png")
bala_x = 0
bala_y = 500
bala_x_cambio = 0
bala_y_cambio = 1 # Velocidad, cuantos pixeles por iteracion
bala_visible = False

#---------------------------------------------
#AGREGADO Variables de Explosion
img_explosion = pygame.image.load("explosion.png")
x_explosion = 0
y_explosion = 0

def explosion_enemigo(x, y): # blit siginifica arrojar
    pantalla.blit(img_explosion,(x,y))# Espera la Ubicacion para mostrar la Explosion
    pygame.display.update()
    pygame.time.delay(50)
#---------------------------------------------

#AGREGADO
def agregar_texto_en_pantalla(texto, font, color, surface,x,y):
    obj_texto = font.render(texto, True, color)
    format_text = obj_texto.get_rect()
    format_text.topleft = (x,y)
    surface.blit(obj_texto,format_text)

# Funcion del Jugador
def jugador(x, y): # blit significa arrojar
    pantalla.blit(img_jugador,(x, y))

# Funcion del Enemigo
def enemigo(x, y, ene):  # blit significa arrojar
    pantalla.blit(img_enemigo[ene], (x, y))

# Funcion Disparar Bala
def disparar_bala(x,y):
    global bala_visible # Variable Global
    bala_visible = True
    pantalla.blit(img_bala,(x + 16,y + 10)) # Con esto +16 y +16 hacemos que la bala aparezca en el centro de la nave

# Detectar Coliciones
def hay_colisiones(x_1,y_1,x_2,y_2):
    distancia = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_2 - y_1,2))
    if distancia < 27:
        return True
    else:
        return False

# Funcion mostrar puntaje
def mostrar_puntaje(x,y):
    texto = fuente.render(f"Puntaje: {puntaje}",True,(255,255,255))
    pantalla.blit(texto,(x, y))

#
def texto_final():
    mi_fuente_final = fuente_final.render("JUEGO TERMINADO", True, (255,255,255))
    pantalla.blit(mi_fuente_final,(200, 200))

# Cabeza Principal del Programa
# Este se esta ejecutando constantemente por medio del While
se_ejecuta = True
while se_ejecuta:

    #RGB
    #pantalla.fill((45, 54, 59))
    # Fondo de Pantalla
    pantalla.blit(fondo,(0,0))

    # Para que se ejecute cada ves que el sistema inicia
    agregar_texto_en_pantalla("Krost Game",font,(255,255,255), pantalla,728,580)

    #Interar Eventos
    for evento in pygame.event.get():

        #Evento para cerrar
        if evento.type == pygame.QUIT:
            se_ejecuta = False

        # Evento Presiona Teclas  # key down es cuando se presiona una tecla.
        if evento.type == pygame.KEYDOWN:

            # Va dictando cuanto debe moverse
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -0.5
            # Va dictando cuanto debe moverse
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0.5
            if evento.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound("disparo.mp3")
                sonido_bala.set_volume(0.1)
                sonido_bala.play()
                nueva_bala = {
                    "x": jugador_x,
                    "y": jugador_y,
                    "velocidad": -1
                }
                balas.append(nueva_bala)

        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0

    # Para que tome un valor mas igual lo que contenga o que halle como valor de cambio, en jugador x cambio

    # 1-Modifica la Ubicacion del Jugador
    jugador_x += jugador_x_cambio

    # 1-Mantener dentro de bordes al Jugador
    if jugador_x <= -10:
        jugador_x = -10
    elif jugador_x >= 748:
        jugador_x = 748

    # 2-Modifica la Ubicacion del Enemigo
    for e in range(cantidad_enemigos):

        #fin de juego
        if enemigo_y[e] > 455:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            texto_final()
            break

        enemigo_x[e] += enemigo_x_cambio[e]

    # 2-Mantener dentro de bordes al enemigo
        if enemigo_x[e] <= -10:
            enemigo_x_cambio[e] = 0.9 # Cambia Velocidad del Enemigo
            enemigo_y[e] += enemigo_y_cambio[e]
        elif enemigo_x[e] >= 748:
            enemigo_x_cambio[e] = -0.9 # Cambia Velocidad del Enemigo
            enemigo_y[e] += enemigo_y_cambio[e]

        # Colision

        for bala in balas:
            colision_bala_enemigo = hay_colisiones(enemigo_x[e], enemigo_y[e], bala["x"], bala["y"])

            if colision_bala_enemigo:
                sonido_colision = mixer.Sound("Golpe.mp3")
                sonido_colision.play()
                sonido_colision.set_volume(0.1)

                puntaje += 1

                # AGREGADO
                x_explosion = enemigo_x[e]
                y_explosion = enemigo_y[e]
                # AGREGADO
                # Llama a Mostrar la Explosion
                explosion_enemigo(x_explosion, y_explosion)

                # Desaparece al Enemigo y lo Vuleve a Colocar en otro Lugar como Enemigo Nuevo
                enemigo_x[e] = random.randint(0, 736)
                enemigo_y[e] = random.randint(50, 200)
                break

            # Llamada al Enemigo
        enemigo(enemigo_x[e], enemigo_y[e], e)

    # Movimiento de la Bala
    for bala in balas:
        bala["y"] += bala["velocidad"]
        pantalla.blit(img_bala, (bala["x"] + 16, bala["y"] + 10))
        if bala["y"] < 0:
            balas.remove(bala)

    # Llamada al Jugador
    jugador(jugador_x,jugador_y)

    mostrar_puntaje(texto_x, texto_y)

    #Actualizar
    pygame.display.update()
