#def softMax(array):
#    return np.array([np.exp(x) / sum(np.exp(array))])

class AGViajero:
    def __init__(self, poblacionInicial, tasaMutacion, maxGeneraciones, tolerancia):
        self.poblacionInicial = poblacionInicial
        self.tasaMutacion = tasaMutacion
        self.maxGeneraciones = maxGeneraciones
        self.tolerancia = tolerancia

    def generarPoblacionInicial(self):
        totalNodos = self.matrizDistancias.shape[0]
        return np.array([np.random.permutation(totalNodos) for _ in range(self.poblacionInicial)])

    def fitness(self, trayectoria):
        if len(trayectoria) == self.n:
            return sum(self.matrizDistancias[trayectoria[i], trayectoria[i + 1]] for i in range(self.n - 1))
        else:
            trayectoriaCalculo = np.append(trayectoria, trayectoria[0])
            return sum(self.matrizDistancias[trayectoria[i], trayectoria[i + 1]] for i in range(self.n))
    
    def seleccionPadres(self, poblacion, pesos):
        pesosNormalizados = pesos / np.sum(pesos)
        return random.choices(population = poblacion, 
                               weights = pesosNormalizados ** 2,
                               k = 2)
    
    def mutacion(self, trayectoria):
        for nodo in trayectoria:
            puntoInicial = np.random.randint(self.n - 1)
            mutacion = random.choices(population = [0,1], weights = [1 - self.tasaMutacion, self.tasaMutacion], k = 1)[0]
            if mutacion == 1:
                longitud = np.random.randint(1, n - puntoInicial)
                subtrayectoria = trayectoria[puntoInicial : puntoInicial + longitud]
                trayectoria = np.concatenate(
                                     (trayectoria[0:puntoInicial], 
                                       np.flip(subtrayectoria),
                                       trayectoria[puntoInicial + longitud:]
                                      )
                                     ) 
                trayectoria[-1] = trayectoria[0]
                return trayectoria
            else:
                continue

        return trayectoria

    def crossover(self, padres):
        parejaAleatoria = sorted(np.random.choice(np.arange(1, self.n - 1 ), 2, replace = False))
        corte1, corte2 = parejaAleatoria
        
        padresPartes = {}
        for npadre in range(2):
            padresPartes[npadre] = [padres[npadre][0:corte1], 
                                    padres[npadre][corte1:corte2], 
                                    padres[npadre][corte2:]
                                   ]

        hijosPosibles = {}
        for nhijos in range(2):
            hijosPosibles[nhijos] = np.concatenate(
                                                 (padresPartes[1 - nhijos][0],
                                                   padresPartes[nhijos][1],
                                                   padresPartes[1 - nhijos][2])
                                                  )

        hijosFinales = []
        for nhijo in hijosPosibles.keys():
            hijoEscogido = hijosPosibles[nhijo]
            if len(hijoEscogido) > self.n:
                hijoEscogido = np.delete(hijoEscogido, -1)
            else:
                pass
            
            nodosNoVisitados = np.array(list(set(np.arange(self.n)) - set(hijoEscogido)))
            if len(nodosNoVisitados) > 0:
                i = 0
                for nodo in hijoEscogido:
                    if np.count_nonzero(hijoEscogido == nodo) > 1:
                        indice = list(hijoEscogido).index(nodo)
                        hijoEscogido[indice] = nodosNoVisitados[i]
                        i += 1
                    else:
                        continue
                
                hijosFinales.append(np.append(hijoEscogido, hijoEscogido[0]))
            else:
                hijosFinales.append(np.append(hijoEscogido, hijoEscogido[0]))

        if self.fitness(hijosFinales[0]) <= self.fitness(hijosFinales[1]):
            return self.mutacion(hijosFinales[0])
        else:
            return self.mutacion(hijosFinales[1])    
        
    def ejecutarGA(self, matrizDistancias):
        self.matrizDistancias = matrizDistancias
        self.n = matrizDistancias.shape[0]
        poblacionActual = self.generarPoblacionInicial()
        fitness = [1/self.fitness(trayectoria) for trayectoria in poblacionActual]
        
        mediasFitness = [np.mean(fitness)]
        generacion = 0
        mejora = 1000
        self.mejoresTrayectorias = []
        
        while (generacion <= self.maxGeneraciones) and (mejora > self.tolerancia):
            hijos = []
            for _ in range(self.poblacionInicial):
                padres = self.seleccionPadres(poblacion = poblacionActual,
                                              pesos = fitness)
                hijo = self.crossover(padres)
                hijos.append(hijo)
                
            generacion += 1
            poblacionActual = hijos
            
            fitness = [1/self.fitness(trayectoria) for trayectoria in poblacionActual]
            mediasFitness.append(np.mean(fitness))
            
            mejora = np.abs((mediasFitness[-2] - mediasFitness[-1])/mediasFitness[-2])
            
            idMejorTrayectoria = np.argmax([1/self.fitness(trayectoria) for trayectoria in poblacionActual])
            mejorTrayectoria = poblacionActual[idMejorTrayectoria]
                
            self.mejoresTrayectorias.append((1/self.fitness(mejorTrayectoria), mejorTrayectoria))     
            clear_output(wait = True)
            print(f'Generación {generacion}, media de adecuación: {np.mean(fitness)}')
            
        evaluacion = mediasFitness
        self.maxGeneraciones = generacion
        longitudMejores = list(zip(*self.mejoresTrayectorias))[0]
        indiceLongitudMejor = longitudMejores.index(max(longitudMejores))
        self.mejorTrayectoriaF = self.mejoresTrayectorias[indiceLongitudMejor][1]
        
        self.mejoresTrayectorias.append((1, self.mejorTrayectoriaF))
        problema.dibujarTrayectoria(self.mejorTrayectoriaF)
        return self.mejorTrayectoriaF, evaluacion
    
    def metricaEvaluacion(self, mediasFitness):
        figura, ax = plt.subplots(figsize = (12,8))
        ax.set_title('Métrica de la función de adecuación en función de la generación',
                    fontsize = 15)
        
        x = np.array(range(len(mediasFitness)))
        y = mediasFitness
                     
        plt.plot(x,y, color = 'red')
        plt.grid()
        plt.show()
        
    def mostrarEvolucion(self, mejorTrayectoriaGA, tasaRefresco = 1):
        %matplotlib inline
        for i, trayectoria in enumerate(self.mejoresTrayectorias):
            titulo = f'Mejor trayectoria - Generación {i}'
            if i % tasaRefresco == 0:
                problema.dibujarTrayectoria(trayectoria[1], titulo = titulo)
                time.sleep(0.1)
                clear_output(wait = True)
            else:
                pass
        problema.dibujarTrayectoria(self.mejorTrayectoriaF, titulo = 'Trayectoria final')
        
if __name__ == '__main__':
    pass
