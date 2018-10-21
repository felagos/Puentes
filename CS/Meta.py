#Librerias a utilizar
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


class Meta:
    iteraciones = None
    poblacion = None
    solutions = []
    MT = None
    permutaciones = None

    def __init__(self, pob, iter):
        self.poblacion = pob
        self.iteraciones = iter
        npend = DATOS_TESADO["NumPendolas"]
        orden = list(permutations(range(1, npend + 1)))
        self.permutaciones = orden

    def Metaheuristic(self,modelo):

        '''***INICIALIZACIÓN POBLACIÓN***'''
        self.poblacionInicial(modelo) # SE CREAN LA POBLACIÓN INICIAL (ORDEN Y MAGNITUDES).
        solutions = self.solutions # SE GUARDAN LA POBLACIÓN CREADA EN solutions.
        N = len(solutions) # N DEFINE EL NUMERO DE NIDOS.

        #Utilizaremos el arreglo Nido para de tamaño 7 en el caso particular de esta MH ya que ordenaremos los resultados en función al fitness
        Nidos = [np.zeros(7) for x in range(self.poblacion)] #SE CREAN LOS Población + Iteración NIDOS EN DONDE ESTARAN EL ORDEN(0,1,2), LAS MAGNITUDES(3,4,5), Y EL REGISTRO DE FITNESS(6).
        for w in range(0, N): #SE RELLENA EL NIDO CON EL ORDEN Y LAS MAGNITUDES DE LAS solutions CREADAS.
            mag2 = solutions[w].magnitud
            orden2 = solutions[w].orden
            for e in range (3):
                Nidos[w][e] = orden2[e]
                Nidos[w][e+3] = mag2[e]

        #CARGA DEL PUENTE MODIFICADO A SAP2000.
        modelo.cerrarSap2000() #Cerrar SAP2000 el cual contenia el Puente Original
        modelo.abrirSAP()
        
        Registro = open("Registro.txt", "w") #CREA EL ARCHIVO DE REGISTRO
        
        cont1 = 0 #Inicializamos contador del While para generar población inicial

        #Evaluamos la población
        while cont1 <  self.poblacion:# Se genera la población.
            star_time = time.time() #Iniciamos variable para registrar tiempo en cada iteración
            Registro.write("CALCULO POBLACIÓN:" + "," + str(cont1) + ",") #Registro para el .txt
            print("***POBLACIÓN***:  " + str(cont1)) #Mostramos en consola en la iteración a ejecutar
            modelo.cargarPuenteModificado() #Cargamos Puente Modificado
            modelo.aplicarTesado([solutions[cont1]])  # SE APLICA TESADO A LA solution i
            Nidos[cont1][6] = solutions[cont1].calcularFitness(modelo) #GUARDO EL VALOR DE FITNESS DE solution i  EN NIDOS i
            if Nidos[cont1][6] == -1:
                self.regenerarSolution(modelo, solutions, cont1)
                cont1 = cont1 - 1
                continue

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

            #os.remove('C:\Puentes\Modificado\PuenteMod.ico')

            #shutil.copyfile('C:\Puentes\Modificado2\PuenteMod.sdb','C:\Puentes\Modificado\PuenteMod.sdb')
            
            '''GUARDO LA INFORMACIÓN OBTENIDA EN "Registro.txt"'''
            Registro.write("ITERACION:" + "," + str(cont1) + ",")
            Registro.write("P1" + "," + str(Nidos[cont1][0]) + ",")
            Registro.write("P2" + "," + str(Nidos[cont1][1]) + ",")
            Registro.write("P3" + "," + str(Nidos[cont1][2]) + ",")
            Registro.write("T1" + "," + str(Nidos[cont1][3]) + ",")
            Registro.write("T2" + "," + str(Nidos[cont1][4]) + ",")
            Registro.write("T3" + "," + str(Nidos[cont1][5]) + ",")
            Registro.write("FIT" + "," + str(Nidos[cont1][6]) + ",")

            tiempototaliteracion = time.time() - star_time #Registro de tiempo por calculo de cada individuo de la población
            print('EL TIEMPO DE POBLACIÓN ' + str(cont1) + ' FUE: ' + str(tiempototaliteracion)) #Mostramos Tiempo del calculo de cada individuo de la población
            Registro.write("Tiempo de Población" + "," + str(tiempototaliteracion) + ",\n") #Guardamos en el .txt del tiempo por calculo de cada individuo de la población
        
            cont1 = cont1 + 1

        #Iniciamos variables a utilizar
        maglevy = [0,0,0]
        mag = [0,0,0]
        orden = [0,0,0]
        

        cont2 = 0
        
        '''LOOP ALGORITMO''' 
        while cont2 < self.iteraciones: # SE REPITE EN FUNCIÓN A LA CANTIDAD DE ITERACIONES.
            star_time = time.time() #Registro de tiempo
            modelo.cargarPuenteModificado()
            NidoJ = randint(0, (N-1))
        
            '''Se crea un Nido con el vuelo de levy'''

            alfa = DATOS_MH["Alpha"] #Obtenemos parametro Alfa
            npend = DATOS_TESADO["NumPendolas"] #Obtenemod Numero de pendolas
            min = modelo.tesadoMinimo #Obtenemos tensión minima

            #Obtenemos orden del mejor nido
            x = int(Nidos[NidoJ][0])
            y = int(Nidos[NidoJ][1])
            z = int(Nidos[NidoJ][2])
            orden = [x,y,z]
            
            #Se crean magnitudes con vuelo levy
            for j in range(3):
                mag[j] = Nidos[NidoJ][j+3]

            #Agregamos el Vuelo de Levy
            for j in range(3):
                maglevy[j] = alfa*(math.pow(mag[j], -1.00 / uniform(1.000, 3.000))) #Generamos el vuelo de Levy
                mag[j] = mag[j] + maglevy[j] # Sumamos el Vuelo de Levy

                if mag[j] > modelo.tesadoMaximo[j]: #Si la nueva mag es mayor al max, utilizamos la minima
                    mag[j] = min

            #Guardamos los datos en solution
            solution = Solution(orden, mag) 

            
            modelo.aplicarTesado([solution])  #Se aplica tensión en la nueva solution con vuelo de Levy
            NidoLevy = solution.calcularFitness(modelo) #GUARDO EL VALOR DE FITNESS DE solution i  EN NIDOS i

            if NidoLevy == -1:
                cont2 = cont2 - 1
                continue
            
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

            #os.remove('C:\Puentes\Modificado\PuenteMod.ico')

            #shutil.copyfile('C:\Puentes\Modificado2\PuenteMod.sdb','C:\Puentes\Modificado\PuenteMod.sdb')

            #Mostramos en pantalla la iteraciónpor ejecutar
            print("***ITERACION***:  " + str(cont2))

            #Comparar NidoLevy con el mejor nido
            if NidoLevy < Nidos[NidoJ][6]: #Si el NidoLevy tiene una solución de mejor calidad, reemplaza el mejor Nido
                #Reemplazamos la mejor solución
                for j in range(3):
                    Nidos[NidoJ][j] = orden[j] 
                    Nidos[NidoJ][j+3] = mag[j]
                Nidos[NidoJ][6] = NidoLevy 
                print("SI REEMPLAZAMOS EL NIDO J") #Mostramos en consola si se ejecuta la mejora

            #Ordenamos la Población de menos a mayor
            Nidos= sorted(Nidos, key=lambda x: x[6], reverse= False)

            #Eliminar la peor Pa de población
            Pa = int(DATOS_MH["Pa"])
            print('SE REEMPLAZARAN LOS PEORES ' + str(Pa) + ' DE LOS NIDOS')
            
            Pb = (self.poblacion - Pa) #Numero de nidos que no se van a borrar que no se van a eliminar
            
            for m in range(Pb, self.poblacion):
                '''GENERAR NIDOS NUEVOS EN solution'''           
                mag = [0,0,0]
                for j in range (3):
                    mag[j] =random.uniform(min, modelo.tesadoMaximo[j])
                #Se crean orden por permutaciones
                z = randint(0, npend-1)
                orden = self.permutaciones[z]
                #Generamos Solution
                solution = Solution(orden, mag)     
                
                modelo.cargarPuenteModificado()
                #Aplicamos tesado en función a Solution
                modelo.aplicarTesado([solution])
                
                #Reemplazamos la Pa Solutions en los Nidos

                for t in range(3):
                    Nidos[m][t] = orden[t]
                    Nidos[m][t+3] = mag[t]
                Nidos[m][6] = solution.calcularFitness(modelo)

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

                #os.remove('C:\Puentes\Modificado\PuenteMod.ico')

                #shutil.copyfile('C:\Puentes\Modificado2\PuenteMod.sdb','C:\Puentes\Modificado\PuenteMod.sdb')

            #Mostramos en consola el mejor Nido
            print("EL MEJOR NIDO DE ESTA ITERACION ES: " + str(Nidos[0][6]))
            print(Nidos[0]) 

            tiempototaliteracion = time.time() - star_time #Registro de tiempo por calculo de cada Iteración
            print('EL TIEMPO DE ESTA ITERACIÓN ' + str(cont2) + ' FUE: ' + str(tiempototaliteracion))
        
            '''GUARDO LA INFORMACIÓN OBTENIDA EN "Registro.txt"'''
            Registro.write("ITERACION:" + "," + str(cont2) + ",")
            Registro.write("P1" + "," + str(Nidos[0][0]) + ",")
            Registro.write("P2" + "," + str(Nidos[0][1]) + ",")
            Registro.write("P3" + "," + str(Nidos[0][2]) + ",")
            Registro.write("T1" + "," + str(Nidos[0][3]) + ",")
            Registro.write("T2" + "," + str(Nidos[0][4]) + ",")
            Registro.write("T3" + "," + str(Nidos[0][5]) + ",")
            Registro.write("FIT" + "," + str(Nidos[0][6]) + ",")
            Registro.write("Tiempo de iteracion" + "," + str(tiempototaliteracion) + ",\n")

            cont2 = cont2 + 1

    '''CREACIÓN DE LA POBLACIÓN'''
    def poblacionInicial(self, modelo):
        self.solutions = []
        npend = DATOS_TESADO["NumPendolas"] #Obtener el numero de pendolas de nuestra instancia
        min = modelo.tesadoMinimo #Obtenemos nuestro valor de tensado minimo
        #Se crean magnitudes Random
        for i in range(self.poblacion):
            mag = []
            for j in range (npend):
                mag.append(random.uniform(min, modelo.tesadoMaximo[j])) #La magnitud esta entre min y max

            #Se crean orden por permutaciones
            z = randint(0, npend-1)
            orden = self.permutaciones[z]
            solution = Solution(orden, mag)     #Solution
            self.solutions.append(solution)     #Solutions

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
