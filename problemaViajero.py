import numpy as np
import random
import matplotlib.pyplot as plt
import itertools
import numpy.ma as ma
import heapq
import collections
from IPython.display import clear_output
from IPython import display
import time

def calcularDistancia(punto1, punto2):
    ''' Esta función recibe una pareja ordenada de puntos 
        y devuelve el cuadrado de su distancia euclídea'''
    
    if (len(punto1) != 2) or (len(punto2) != 2):
        raise Exception('Alguno de los dos puntos no es una pareja ordenada')
    elif len(punto1) != len(punto2):
        raise Exception('Los puntos no tienen la misma dimensión')
    else:
        return np.sqrt((punto1[0]-punto2[0])**2 + (punto1[1]-punto2[1])**2)

class problemaViajero():
    ''' Clase de problemaViajero que consiste en la
        inicialización del problema. Se generan unos
        puntos al azar en el plano que harán las veces de
        ciudades'''
    
    def __init__(self, n):
        self.n = n
        self.x, self.y = np.random.random(size = (2, self.n))
    
    def graficoProblema(self):
        ''' Gráfica de los puntos '''
        
        plt.figure(figsize = (12, 8))
        plt.scatter(self.x, self.y, color = 'black')
        
        for i in range(self.n):
            x0 = self.x[i]
            y0 = self.y[i]
            plt.text(x0, y0 - 0.03, str(i))
        
        plt.title(f'Figura de los puntos {self.n} escogidos',
                 fontsize = 15)
        plt.show()
    
    def matrizDistancia(self):
        ''' Creación de la matriz de distancias 
            de los puntos según la norma euclídea'''
        
        filas = []
        for indice in range(self.n):
            x0 = self.x[indice], self.y[indice]
            distancias = [calcularDistancia(x0, (self.x[i], self.y[i])) for i in range(self.n)]
            filas.append(distancias)
        
        return np.matrix(filas)
    
    def dibujarTrayectoria(self, trayectoria = []):
        ''' Dibujo que une los puntos. Si no se entrega
            una trayectoria, se dibuja una aleatoriamente'''
        
        if len(trayectoria) > 0:
            permutacion = trayectoria
            strGrafica = 'Trayectoria dada'
        else:
            strGrafica = 'Trayectoria aleatoria'
            permutacion = np.random.permutation(self.n)
        
        figura, ax = plt.subplots(figsize = (12,8))
        ax.set_title(strGrafica,
                    fontsize = 15)

        for i in range(self.n):
            try:
                ejeHorizontales = [
                                   problema.x[permutacion[i]], 
                                   problema.x[permutacion[i + 1]]
                                  ]

                ejeVerticales = [
                                 problema.y[permutacion[i]], 
                                 problema.y[permutacion[i + 1]]
                                ]

                ax.plot(ejeHorizontales, ejeVerticales, 'r-')
            except IndexError:
                ejeHorizontales = [
                                   problema.x[permutacion[i]], 
                                   problema.x[permutacion[0]]
                                  ]

                ejeVerticales = [
                                 problema.y[permutacion[i]], 
                                 problema.y[permutacion[0]]
                                ]
                ax.plot(ejeHorizontales, ejeVerticales, 'r-')

        plt.scatter(problema.x, problema.y, color = 'black')
        
    
    def calcularLongitudTrayectoria(self, trayectoria):
        ''' Dada una trayectoria, se calcula
            la distancia total'''
        
        matrizDistancias = self.matrizDistancia()
        distanciaTotal = sum(matrizDistancias[trayectoria[i], trayectoria[i + 1]] for i in range(self.n))
        return distanciaTotal
        
    def trayectoriaOptimaGreedy(self):
        '''Implementación del algoritmo Codicioso
            para hallar una trayectoria'''
        
        diccionarioTrayectorias = {}

        for puntoMovil in range(self.n):
            matrizDistancias = self.matrizDistancia()
            distancias = [0]
            trayectoria = [puntoMovil]

            for _ in range(self.n):
                distanciasPuntoMovil = np.array(matrizDistancias[puntoMovil, :])[0]
                for distancia in sorted(distanciasPuntoMovil):
                    if list(distanciasPuntoMovil).index(distancia) not in trayectoria:
                        posicion = list(distanciasPuntoMovil).index(distancia)
                        break
                    else:
                        continue
                puntoMovil = posicion

                trayectoria.append(posicion)
                distancias.append(distanciasPuntoMovil[posicion])

            trayectoria[-1] = trayectoria[0]
            diccionarioTrayectorias[sum(distancias)] = trayectoria

        return diccionarioTrayectorias[min(diccionarioTrayectorias.keys())]   
    
    def compararTrayectorias(self, trayectorias, etiquetas = []):
        longitud = np.array([self.calcularLongitudTrayectoria(trayectoria) for trayectoria in trayectorias])

        if etiquetas == []:
            etiquetas = [f'Trayectoria_{i}' for i in range(len(trayectorias))]
            return dict(zip(np.array(etiquetas), longitud))
        else:
            if len(trayectorias) != len(trayectorias):
                raise Exception('La cantidad de etiquetas es diferente a la cantidad de etiquetas')
            else:
                return dict(zip(np.array(etiquetas), longitud))
    
if __name__ == '__main__':
    n = 10
    problema = problemaViajero(n)
    problema.graficoProblema()
    