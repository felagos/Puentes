#Librerias a utilizar
#https://github.com/cran/metaheuristicOpt/blob/master/R/DA.Algorithm.R
#install scipy: pip install scipy

from Solution import Solution
import random
import math
import copy
from Constantes import DATOS_TESADO, DATOS_MH
from random import shuffle
from itertools import permutations
from random import randint
import numpy as np
from random import uniform
import time
import os
import shutil
from scipy.spatial import distance
from scipy.special import gamma
from math import pi, sin


class Meta:
    iteraciones = None
    poblacion = None
    solutions = []
    deltaSolution = []
    MT = None
    permutaciones = None

    def __init__(self, pob, iter):
        self.poblacion = pob
        self.iteraciones = iter
        npend = DATOS_TESADO["NumPendolas"]
        orden = list(permutations(range(1, npend + 1)))
        self.permutaciones = orden

    def Metaheuristic(self,modelo):

        '''***INICIALIZACIoN POBLACION***'''
        self.poblacionInicial(modelo, False) # SE CREAN LA POBLACIoN INICIAL (ORDEN Y MAGNITUDES).
        #self.poblacionInicial(modelo, True) # SE CREA UNA SEGUNDA POBLACION NECESARIO PARA LA MH.
        solutions = self.solutions # SE GUARDAN LA POBLACIoN CREADA EN solutions.
        deltaSolutions = self.deltaSolution
        N = len(solutions) # N DEFINE EL NUMERO DE NIDOS.

        ub = np.ones(3) * DATOS_MH["ub"]
        lb = np.ones(3) * DATOS_MH["lb"]
        initialRadius = (ub - lb) / 10
        print("initialRadius: ", initialRadius)
        Delta_max= (np.ones(3) * ub - np.ones(3) * lb) / 10
        print("delta max: ", Delta_max)

        foodFitness = float("inf")
        foodPos = np.zeros(3)

        enemyFitness = -float("inf")
        enemyPos = np.zeros(3)

        fitness = np.array([])

        DragonFlies = [np.zeros(7) for x in range(self.poblacion)]
        DeltaDragonFlies = [np.zeros(7) for x in range(self.poblacion)]
        
        for w in range(0, N): #SE RELLENA EL NIDO CON EL ORDEN Y LAS MAGNITUDES DE LAS solutions CREADAS.
            mag2 = solutions[w].magnitud
            orden2 = solutions[w].orden

            deltamag2 = solutions[w].magnitud
            deltaorden2 = solutions[w].orden

            for e in range (3):
                DragonFlies[w][e] = orden2[e]
                DragonFlies[w][e + 3] = mag2[e]

                DeltaDragonFlies[w][e] = deltamag2[e]
                DeltaDragonFlies[w][e + 3] = deltaorden2[e]
        
        modelo.cerrarSap2000()  # Cerrar SAP2000 el cual contenia el Puente Original
        modelo.abrirSAP()

        Registro = open("Registro.txt", "w")  # CREA EL ARCHIVO DE REGISTRO

        cont1 = 0
        while cont1 < self.poblacion:
            star_time = time.time()  # Iniciamos variable para registrar tiempo en cada iteracion
            Registro.write("CALCULO POBLACIoN:" + "," + str(cont1) + ",")  # Registro para el .txt
            # Mostramos en consola en la iteracion a ejecutar
            print("***POBLACIoN***:  " + str(cont1))
            modelo.cargarPuenteModificado()  # Cargamos Puente Modificado
            # SE APLICA TESADO A LA solution i
            modelo.aplicarTesado([solutions[cont1]])
            #modelo.aplicarTesado([deltaSolutions[cont1]])
            # GUARDO EL VALOR DE FITNESS DE solution i  EN NIDOS i
            DragonFlies[cont1][6] = solutions[cont1].calcularFitness(modelo)
            #DeltaDragonFlies[cont1][6] = deltaSolutions[cont1].calcularFitness(modelo)
            if DragonFlies[cont1][6] == -1:
                self.regenerarSolution(modelo, solutions, cont1)
                cont1 = cont1 - 1
                continue
            '''
            if DragonFlies[cont1][6] < foodFitness:
                foodFitness = DragonFlies[cont1][6]
                foodPos = DragonFlies[cont1]
            
            if DragonFlies[cont1][6] > enemyFitness:
                if True:
                    enemyFitness = DragonFlies[cont1][6]
                    enemyPos = DragonFlies[cont1]
            '''
            arrayFitness = np.array(DragonFlies)
            fitness = list(arrayFitness[:, 6])

            foodFitness = np.min(fitness)
            indexMin = np.argmin(fitness)
            foodPos = DragonFlies[indexMin][3:6]

            arrDF = np.array(DragonFlies)
            enemyPos = list(arrDF[len(arrDF) - 1, ])[3:6]
            enemyFitness = fitness[len(fitness) - 1]

            '''REMUEVO Y CAMBIO ARCHIVOS CORRESPONDIENTES PARA EVITAR TIEMPOS DE CALCULOS EXPONENCIALES'''
            os.remove('C:\Puentes\Modificado\PuenteMod.Y08')
            os.remove('C:\Puentes\Modificado\PuenteMod.Y09')
            os.remove('C:\Puentes\Modificado\PuenteMod.msh')
            os.remove('C:\Puentes\Modificado\PuenteMod.K~0')
            os.remove('C:\Puentes\Modificado\PuenteMod.Y~')

            os.remove('C:\Puentes\Modificado\PuenteMod.Y')
            os.remove('C:\Puentes\Modificado\PuenteMod.Y00')
            os.remove('C:\Puentes\Modificado\PuenteMod.Y03')
            os.remove('C:\Puentes\Modificado\PuenteMod.Y07')
            os.remove('C:\Puentes\Modificado\PuenteMod.Y05')

            os.remove('C:\Puentes\Modificado\PuenteMod.Y06')
            os.remove('C:\Puentes\Modificado\PuenteMod.Y04')
            os.remove('C:\Puentes\Modificado\PuenteMod.Y01')
            os.remove('C:\Puentes\Modificado\PuenteMod.Y02')
            os.remove('C:\Puentes\Modificado\PuenteMod.K~J')

            os.remove('C:\Puentes\Modificado\PuenteMod.K~M')
            os.remove('C:\Puentes\Modificado\PuenteMod.K~I')
            os.remove('C:\Puentes\Modificado\PuenteMod.y~2')
            os.remove('C:\Puentes\Modificado\PuenteMod.Y$$')
            os.remove('C:\Puentes\Modificado\PuenteMod.Y~1')

            os.remove('C:\Puentes\Modificado\PuenteMod.log')
            os.remove('C:\Puentes\Modificado\PuenteMod.$2K')
            os.remove('C:\Puentes\Modificado\PuenteMod.OUT')

            '''GUARDO LA INFORMACIoN OBTENIDA EN "Registro.txt"'''
            Registro.write("ITERACION:" + "," + str(cont1) + ",")
            Registro.write("P1" + "," + str(DragonFlies[cont1][0]) + ",")
            Registro.write("P2" + "," + str(DragonFlies[cont1][1]) + ",")
            Registro.write("P3" + "," + str(DragonFlies[cont1][2]) + ",")
            Registro.write("T1" + "," + str(DragonFlies[cont1][3]) + ",")
            Registro.write("T2" + "," + str(DragonFlies[cont1][4]) + ",")
            Registro.write("T3" + "," + str(DragonFlies[cont1][5]) + ",")
            Registro.write("FIT" + "," + str(DragonFlies[cont1][6]) + ",")

            # Registro de tiempo por calculo de cada individuo de la poblacion
            tiempototaliteracion = time.time() - star_time
            # Mostramos Tiempo del calculo de cada individuo de la poblacion
            print('EL TIEMPO DE POBLACIoN ' + str(cont1) + ' FUE: ' + str(tiempototaliteracion))
            # Guardamos en el .txt del tiempo por calculo de cada individuo de la poblacion
            Registro.write("Tiempo de Poblacion" + "," + str(tiempototaliteracion) + ",\n")

            cont1 = cont1 + 1

        #print("total filas: ", len(self.solutions), " - total columnas: ",len(self.solutions[0].orden+self.solutions[0].magnitud))


        mag = [0,0,0]
        orden = [0,0,0]
        
        '''LOOP ALGORITMO'''
        i = 1
        while i <= self.iteraciones:
            min = modelo.tesadoMinimo
            star_time = time.time() #Registro de tiempo
            modelo.cargarPuenteModificado()

            r = (ub - lb) / 4 + (( ub - lb) * ( i / self.iteraciones ) * 2)

            w = float(0.9 - i * ((0.9-0.4) / self.iteraciones))

            my_c = float(0.1 - i * (( 0.1 - 0) / (self.iteraciones / 2)))
            my_c = 0 if my_c < 0 else my_c
            
            s = 2 * random.uniform(0, 1) * my_c # Seperation weight
            a = 2 * random.uniform(0, 1) * my_c # Alignment weight
            c = 2 * random.uniform(0, 1) * my_c # Cohesion weight
            f = 2 * random.uniform(0, 1)     # Food attraction weight
            e = my_c        # Enemy distraction weight

            totalDragonFlies = len(DragonFlies)

            print("total dragonflies: ", totalDragonFlies)
   
            for iDragonFly in range(totalDragonFlies):
                index = 0
                neighboursNo = 0

                orden = [DragonFlies[iDragonFly][0], DragonFlies[iDragonFly][1], DragonFlies[iDragonFly][2]]
                mag = [DragonFlies[iDragonFly][3], DragonFlies[iDragonFly][4], DragonFlies[iDragonFly][5]]

                ordenDelta = [DeltaDragonFlies[iDragonFly][0], DeltaDragonFlies[iDragonFly][1], DeltaDragonFlies[iDragonFly][2]]
                magDelta = [DeltaDragonFlies[iDragonFly][3], DeltaDragonFlies[iDragonFly][4], DeltaDragonFlies[iDragonFly][5]]

                neighboursDelta = [np.zeros(3) for x in range(totalDragonFlies)]
                neighboursDragonfly = [np.zeros(3) for x in range(totalDragonFlies)]


                for j in range(totalDragonFlies):
                    subMag = [DragonFlies[j][3], DragonFlies[j][4], DragonFlies[j][5]]
                    subMagDelta = [DeltaDragonFlies[j][3], DeltaDragonFlies[j][4], DeltaDragonFlies[j][5]]

                    distanceEc = distance.euclidean(mag, subMag)
                    if all(distanceEc <= r) and distanceEc is not 0:
                        neighboursDelta[index] = subMag
                        neighboursDragonfly[index] = mag

                        index = index + 1
                        neighboursNo = neighboursNo + 1
                
                #Separation
                S = np.zeros(3)
                if neighboursNo > 1:
                    for k in range(neighboursNo):
                       S = S + (np.array(neighboursDragonfly[k])-np.array(mag))
                    S = -1 * S

                #Alignment
                A = magDelta
                if neighboursNo > 1:
                    A = np.array(neighboursDragonfly).sum(axis=0) / neighboursNo
                    #A = np.squeeze(np.asarray(A))
                
                #Cohesion
                C = magDelta
                if neighboursNo > 1:
                    C = np.array(neighboursDragonfly).sum(axis=0) / neighboursNo
                    #C = np.squeeze(np.asarray(C))
                C = np.array(C) - np.array(mag)

                #Attraction to food
                distance2Food = distance.euclidean(mag, foodPos)
                F = 0
                if all(distance2Food <= r):
                    F = np.array(foodPos) - np.array(mag)

                distance2Enemy = distance.euclidean(mag, enemyPos)
                E = np.zeros(3)
                if all(distance2Enemy <= r):
                    E = np.array(enemyPos) + np.array(mag)
                
                
                #print("S: ", S)
                #print("A: ", A)
                #print("C: ", C)
                #print("F: ", F)
                #print("E: ", E)
                
                if any(distance2Food > r):
                    if neighboursNo > 1:
                        for j in range(3):
                            #print("levy: ", self.levy(3))
                            mov = w * magDelta[j] + random.uniform(0, 1) * A[j] + random.uniform(0, 1) * C[j] + random.uniform(0, 1) * S[j]
                            magDelta[j] = mov
                            if magDelta[j] > Delta_max[j]:
                                magDelta[j] = Delta_max[j]

                            if magDelta[j] < -1 * Delta_max[j]:
                                magDelta[j] = -1 * Delta_max[j]

                            mag[j] = np.array(mag[j]) + np.array(magDelta[j])
                            if mag[j] > modelo.tesadoMaximo[j]: #Si la nueva mag es mayor al max, utilizamos la minima
                                mag[j] = min
                    else:
                        mag = np.array(mag) + self.levy(3) * np.array(mag)

                        #DragonFlies[iDragonFly][3] = mag[0]
                        #DragonFlies[iDragonFly][4] = mag[1]
                        #DragonFlies[iDragonFly][5] = mag[2]

                        magDelta = np.zeros(3)
                else:
                    for j in range(3):
                        magDelta[j] = (a*A[j]+c*C[j]+s*S[j]+f*F[j]+e*E[j]) + w*magDelta[j]
                        if magDelta[j] > Delta_max[j]:
                            magDelta[j] = Delta_max[j]

                        if magDelta[j] < -1 * Delta_max[j]:
                            magDelta[j] = -1 * Delta_max[j]
                        
                        mag[j] = np.array(mag[j]) + np.array(magDelta[j])

                        if mag[j] > modelo.tesadoMaximo[j]: #Si la nueva mag es mayor al max, utilizamos la minima
                            mag[j] = min

                #mag = self.checkBounds(mag, lb, ub)
            
                #DragonFlies[iDragonFly][3] = mag[0]
                #DragonFlies[iDragonFly][4] = mag[1]
                #DragonFlies[iDragonFly][5] = mag[2]

                solution = Solution(orden, mag)

                modelo.aplicarTesado([solution])  #Se aplica tension en la nueva solution con vuelo de Levy
                newFitness = solution.calcularFitness(modelo)

                if newFitness == -1:
                    iDragonFly = iDragonFly - 1
                    continue

                if newFitness < DragonFlies[iDragonFly][6]:
                    for j in range(3):
                        DragonFlies[iDragonFly][j] = orden[j] 
                        DragonFlies[iDragonFly][j + 3] = mag[j]
                    DragonFlies[iDragonFly][6] = newFitness

            #Ordenamos la Poblacion de menos a mayor
            DragonFlies= sorted(DragonFlies, key=lambda x: x[6], reverse= False) 

            #se incrementa el indice de las iteraciones

            '''REMUEVO Y CAMBIO ARCHIVOS CORRESPONDIENTES PARA EVITAR TIEMPOS DE CALCULOS EXPONENCIALES'''
            os.remove('C:\Puentes\Modificado\PuenteMod.Y08')
            os.remove('C:\Puentes\Modificado\PuenteMod.Y09')
            os.remove('C:\Puentes\Modificado\PuenteMod.msh')
            os.remove('C:\Puentes\Modificado\PuenteMod.K~0')
            os.remove('C:\Puentes\Modificado\PuenteMod.Y~')

            os.remove('C:\Puentes\Modificado\PuenteMod.Y')
            os.remove('C:\Puentes\Modificado\PuenteMod.Y00')
            os.remove('C:\Puentes\Modificado\PuenteMod.Y03')
            os.remove('C:\Puentes\Modificado\PuenteMod.Y07')
            os.remove('C:\Puentes\Modificado\PuenteMod.Y05')

            os.remove('C:\Puentes\Modificado\PuenteMod.Y06')
            os.remove('C:\Puentes\Modificado\PuenteMod.Y04')
            os.remove('C:\Puentes\Modificado\PuenteMod.Y01')
            os.remove('C:\Puentes\Modificado\PuenteMod.Y02')
            os.remove('C:\Puentes\Modificado\PuenteMod.K~J')

            os.remove('C:\Puentes\Modificado\PuenteMod.K~M')
            os.remove('C:\Puentes\Modificado\PuenteMod.K~I')
            os.remove('C:\Puentes\Modificado\PuenteMod.y~2')
            os.remove('C:\Puentes\Modificado\PuenteMod.Y$$')
            os.remove('C:\Puentes\Modificado\PuenteMod.Y~1')

            os.remove('C:\Puentes\Modificado\PuenteMod.log')
            os.remove('C:\Puentes\Modificado\PuenteMod.$2K')
            os.remove('C:\Puentes\Modificado\PuenteMod.OUT')

            print("EL MEJOR NIDO DE ESTA ITERACION ES: " + str(DragonFlies[0][6]))
            print(DragonFlies[0]) 

            tiempototaliteracion = time.time() - star_time #Registro de tiempo por calculo de cada Iteracion
            print('EL TIEMPO DE ESTA ITERACIoN ' + str(i) + ' FUE: ' + str(tiempototaliteracion))
        
            '''GUARDO LA INFORMACIoN OBTENIDA EN "Registro.txt"'''
            Registro.write("ITERACION:" + "," + str(i) + ",")
            Registro.write("P1" + "," + str(DragonFlies[0][0]) + ",")
            Registro.write("P2" + "," + str(DragonFlies[0][1]) + ",")
            Registro.write("P3" + "," + str(DragonFlies[0][2]) + ",")
            Registro.write("T1" + "," + str(DragonFlies[0][3]) + ",")
            Registro.write("T2" + "," + str(DragonFlies[0][4]) + ",")
            Registro.write("T3" + "," + str(DragonFlies[0][5]) + ",")
            Registro.write("FIT" + "," + str(DragonFlies[0][6]) + ",")
            Registro.write("Tiempo de iteracion" + "," + str(tiempototaliteracion) + ",\n")

            print("iteracion: ", i)

            i = i + 1
        

    def getSolution(self, min, npend, modelo, mag):
        for j in range(npend):
            mag.append(random.uniform(min, modelo.tesadoMaximo[j]))
        
        z = randint(0, npend-1)
        orden = self.permutaciones[z]
        solution = Solution(orden, mag)
        return solution


    '''CREACIoN DE LA POBLACIoN'''
    def poblacionInicial(self, modelo, forDelta):
        #self.solutions = []
        npend = DATOS_TESADO["NumPendolas"] #Obtener el numero de pendolas de nuestra instancia
        min = modelo.tesadoMinimo #Obtenemos nuestro valor de tensado minimo
        #Se crean magnitudes Random
        print("Total poblacion: "+str(self.poblacion))
        for i in range(self.poblacion):
            mag = []
            mag2 = []
            #for j in range (npend):
            #    mag.append(random.uniform(min, modelo.tesadoMaximo[j])) #La magnitud esta entre min y max

            #Se crean orden por permutaciones
            #z = randint(0, npend-1)
            #orden = self.permutaciones[z]
            #solution = Solution(orden, mag)     #Solution
            solution = self.getSolution(min, npend, modelo, [])
            self.solutions.append(solution)

            solutionDelta = self.getSolution(min, npend, modelo, [])
            self.deltaSolution.append(solutionDelta)

            ##if forDelta is False:
            #    self.solutions.append(solution)     #Solutions
            #else:
            #    self.deltaSolution.append(solution)

    def regenerarSolution(self, modelo, solutions, cont1):
        npend = DATOS_TESADO["NumPendolas"] #Obtener el numero de pendolas de nuestra instancia
        min = modelo.tesadoMinimo #Obtenemos nuestro valor de tensado minimo
        #Se crean magnitudes Random
        mag = []
        for j in range (npend):
            mag.append(random.uniform(min, modelo.tesadoMaximo[j])) #La magnitud esta entre min y max

        #Se crean orden por permutaciones
        z = randint(0, npend-1)
        orden = self.permutaciones[z]
        solution = Solution(orden, mag)     #Solution
        solutions [cont1] = solution     #Solutions
    
    def levy(self, dim):
        beta = 3/2
        sigma = (gamma(1+beta)*sin(pi*beta/2)/(gamma((1+beta)/2)*beta*2**((beta-1)/2)))**(1/beta)
        u = np.random.randn(1, 3)[0] * sigma
        v = np.random.randn(1, 3)[0]
        step = u/abs(v)**(1/beta)
        return 0.01 * step

    def checkBounds(self, position, lowerBound, upperBound):
        position = np.array(position)
        upperBound = np.array(upperBound)
        lowerBound = np.array(lowerBound)

        check1 = position > upperBound
        check2 = position < lowerBound

        for i in range(len(check1)):
            check1[i] = 1 if check1[i] is True else 0
            check2[i] = 1 if check1[i] is True else 0
        
        temp = check1 + check2
        for i in range(len(temp)):
            temp[i] = 1 if temp[i] is 0 else 1
        
        result = (position * temp) + upperBound * check1 + lowerBound * check2

        return result