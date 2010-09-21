#!/usr/bin/env python
# coding=latin1
#Este programa crea una pequeña animación del Sistema Solar a escala real
#This program builds a little animation of The Solar System at a real scale
import sys
import pygame
import math

pygame.init()
pygame.font.init()

fuente=pygame.font.SysFont("Arial", 12, False, False)
blanco=(255,255,255)
superficie_texto=fuente.render("Created by OGG, with PyGame and icons of Dan Wiersema", True, blanco)

#Dimensiones de la pantalla
ancho=1024
alto=768

superficie_tierra=4*3.14*6370


#Posicion del ultimo planeta
#Last planet position
num_planetas=9

#Iconos creados por DAN WIERSEMA
#ICONS CREATED BY DAN WIERSEMA
#http://www.danwiersema.com
iconos=["mercurio_1.tga", "venus_1.tga", "tierra_1.tga", "marte_1.tga", "jupiter_1.tga",
        "saturno_1.tga", "neptuno_1.tga", "urano_1.tga", "pluton_1.tga"]

nombre=["Mercurio", "Venus", "Tierra", "Marte", "Jupiter", "Saturno", "Neptuno", "Urano", "Pluton"]
#Distancias al sol de los planetas en millones de km
distancias_sol=[57.9, 108.2, 149.6, 227.9, 778.3, 1427, 2871, 4497, 5913]

#Periodo de rotacion de los planetas en dias terrestres
#Rotation period of the planets measured in Earth days
periodo_rotacion=[87.96, 224.68, 365, 687, 11.862*365, 29.456*365, 84*365, 164*365, 247.7*365 ]

#Masas de los planetas
constante_masa=5.98e24
masas=[0.06, 0.82, 1, 0.11, 318, 95.1, 14.6, 17.2, 0.002]


imagen=[]
rectangulo=[]
angulo_planeta=[]
incr_angulo=[]
escala_velocidad=2
distancias_tierra=[]
#Todos los planetas empiezan en el mismo angulo
#Cargamos las imagenes y los rectangulos de los planetas
for i in range (0,  num_planetas):
    imagen.insert(i, pygame.image.load(iconos[i]))
    rectangulo.insert(i, imagen[i].get_rect())
    angulo_planeta.insert(i, 0.0)
    incr_angulo.insert(i, escala_velocidad*math.pi*2 / periodo_rotacion[i])
    distancias_tierra.insert(i, abs(distancias_sol[i]-distancias_sol[2]))
    masas[i]=masas[i]*constante_masa

centro=[ancho/2, alto/2]

tam=(ancho, alto)

#Color de la pantalla de fondo
negro=(0,0,0)

pantalla=pygame.display.set_mode(tam)


#Posicion del sol
sol=pygame.image.load("sol_1.png")
rect_sol=sol.get_rect()
rect_sol.centerx=ancho/2
rect_sol.centery=alto/2

#Cuidado, las distancias reales son enormes. Se dividen por esta escala
#para que quepan en pantalla
escala=9.5

#Dada la distancia, nos devuelve las x y las y del planeta
def get_xy(distancia,angulo):
    x=distancia* math.cos(angulo)
    y=distancia* math.sin(angulo)
    return (x,y)

#Calcula la fuerza de atraccion
def fuerza_atraccion(masa1, masa2, distancia):
    return (6.67e-11*masa1*masa2)/(distancia*distancia)
    
#Distancia entre dos rectangulos
def distancia (rect1, rect2):
    x1=rect1.centerx
    y1=rect1.centery
    
    x2=rect2.centerx
    y2=rect2.centery
    
    x_abs=abs(x1-x2)*abs(x1-x2)
    y_abs=abs(y1-y2)*abs(y1-y2)
    distancia=math.sqrt(x_abs+y_abs)
    return distancia

#Situamos el sol en pantalla
pantalla.blit(sol, rect_sol)

centro_x=ancho/2
centro_y=alto/2
#Todos los planetas van situados con respecto al sol
offset_x_sol=centro_x
offset_y_sol=centro_y

numero_frame=0

grabar=False
superficie_pantalla=pygame.display.get_surface()
blanco=(255,255,255)
centro_pantalla=(int(centro_x), int(centro_y))
while 1:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            sys.exit()
    
    if angulo_planeta[8]>=6.28:
        sys.exit()
    pantalla.fill(negro)
    pantalla.blit (sol, rect_sol)
    
    fuerza_total=0
    #Resituamos los planetas y actualizamos sus angulos
    for i in range(0, num_planetas):
        (x_planeta, y_planeta)=get_xy(distancias_sol[i] / escala, angulo_planeta[i])
        rectangulo[i].centerx = x_planeta + offset_x_sol
        rectangulo[i].centery = y_planeta + offset_y_sol
        pygame.draw.circle(superficie_pantalla, blanco, centro_pantalla, int(distancias_sol[i]/escala),1)
        pantalla.blit (imagen[i], rectangulo[i])
        angulo_planeta[i]=angulo_planeta[i]+incr_angulo[i]
        if i!=2:
            distancia_a_la_tierra=distancia(rectangulo[i],rectangulo[2])
            fuerza_aux=fuerza_atraccion(masas[i], masas[2], distancia_a_la_tierra)
            fuerza_total=fuerza_total+fuerza_aux
        if angulo_planeta[i]>6.28:
            angulo_planeta[i]=0
            
    
    #cad_fuerza=str(fuerza_total)
    #superficie_fuerza=fuente.render(cad_fuerza, True, blanco)
    #superficie_pantalla.blit(superficie_fuerza, (5, 20))
    #superficie_pantalla.blit(superficie_texto, (5, 5))
    if grabar==True:
        #Preparamos el numero de frame    
        cad_numero_frame=str(numero_frame)
        cad_numero_alineado=cad_numero_frame.rjust(9, "0")
    
        #Cargamos la pantalla
        
        pygame.image.save(superficie_pantalla, ".\\frames\\"+cad_numero_alineado+".jpg")
        #Y despues de salvada se pasa al siguiente frame
        numero_frame=numero_frame+1
    pygame.display.flip()
    