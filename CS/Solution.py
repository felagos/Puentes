from Constantes import DATOS_TESADO

class Solution:
    orden = []
    magnitud = []

    tensionSup = None
    tensionInf = None

    momentosViga = [[] for m in range(DATOS_TESADO["VigasAAnalizar"])]  #Lista de largo [nvigas]. En cada posicion hay una lista de largo [etapas]
                                                                        #que contiene una lista de momentos.
    axilesViga = [[] for m in range(DATOS_TESADO["VigasAAnalizar"])]
    lcd = [[] for m in range(DATOS_TESADO["NumPendolas"])]

    fitness = None

    def __init__(self, orden, mag):
        self.orden = orden
        self.magnitud = mag
        self.fitness = 0

    

    def calcularFitness(self, modelo):
        fct = modelo.fct
        fcmax = modelo.fcmax
        fcmax2 = modelo.fcmax2
        tensSupOriginal = modelo.tensionSup
        tensInfOriginal = modelo.tensionInf
        apoyos = DATOS_TESADO["NumPendolas"]
        etapas = DATOS_TESADO["NumPendolas"]

        #El siguiente ciclo revisa si las tensiones cumplen las restricciones de tesado
        for i in range(DATOS_TESADO["VigasAAnalizar"]):
            for j in range(DATOS_TESADO["NumPendolas"]-1, DATOS_TESADO["NumPendolas"]):
                for k in range(len(tensSupOriginal[i])):
                    var = self.sign(tensInfOriginal[i][k]) + 2 * self.sign(tensSupOriginal[i][k])
                    varm = self.sign(self.tensionInf[i][j][k]) + 2 *self.sign(self.tensionSup[i][j][k])

                    neginf = self.mayor(abs(tensInfOriginal[i][k]), fct)
                    negsup = self.mayor(abs(tensSupOriginal[i][k]), fct)
                    possup = self.mayor(abs(tensSupOriginal[i][k]), fcmax)
                    posinf = self.mayor(abs(tensInfOriginal[i][k]), fcmax)

                    if var == -3:
                        if varm == -3:
                            if not (abs(self.tensionInf[i][j][k]) < neginf and abs(self.tensionSup[i][j][k]) < negsup):
                                return -1

                        if varm == -1:
                            if not (abs(self.tensionInf[i][j][k]) < 0.6 * fcmax and abs(self.tensionSup[i][j][k]) < negsup):
                                return -1

                        if varm == 1:
                            if not (abs(self.tensionInf[i][j][k]) < neginf and abs(self.tensionSup[i][j][k]) < fcmax):
                                return -1

                        if varm == 3:
                            if not (abs(self.tensionInf[i][j][k]) < fcmax and abs(self.tensionSup[i][j][k]) < fcmax):
                                return -1

                    if var == -1:
                        if varm == - 3:
                            if not (abs(self.tensionInf[i][j][k]) < fct and abs(self.tensionSup[i][j][k]) < negsup):
                                return -1

                        if varm == - 1:
                            if not (abs(self.tensionInf[i][j][k]) < posinf and abs(self.tensionSup[i][j][k]) < negsup):
                                return -1

                        if varm == 1:
                            if not (abs(self.tensionInf[i][j][k]) < fct and abs(self.tensionSup[i][j][k]) < fcmax):
                                return -1

                        if varm == 3:
                            if not (abs(self.tensionInf[i][j][k]) < posinf and abs(self.tensionSup[i][j][k]) < fcmax):
                                return -1

                    if var == 1:
                        if varm == - 3:
                            if not (abs(self.tensionInf[i][j][k]) < neginf and abs(self.tensionSup[i][j][k]) < fct):
                                return -1

                        if varm == - 1:
                            if not (abs(self.tensionInf[i][j][k]) < fcmax and abs(self.tensionSup[i][j][k]) < fct):
                                return -1

                        if varm == 1:
                            if not (abs(self.tensionInf[i][j][k]) < neginf and abs(self.tensionSup[i][j][k]) < possup):
                                return -1

                        if varm == 3:
                            if not (abs(self.tensionInf[i][j][k]) < fcmax and abs(self.tensionSup[i][j][k]) < possup):
                                return -1

                    if var == 3:
                        if varm == -3:
                            if not (abs(self.tensionInf[i][j][k]) < fct and abs(self.tensionSup[i][j][k]) < fct):
                                return -1

                        if varm == -1:
                            if not (abs(self.tensionInf[i][j][k]) < posinf and abs(self.tensionSup[i][j][k]) < fct):
                                return -1

                        if varm == 1:
                            if not (abs(self.tensionInf[i][j][k]) < fct and abs(self.tensionSup[i][j][k]) < possup):
                                return -1

                        if varm == 3:
                            if not (abs(self.tensionInf[i][j][k]) < posinf and abs(self.tensionSup[i][j][k]) < possup):
                                return -1


        fit = 0
        z = 0
        for i in range(DATOS_TESADO["VigasAAnalizar"]):
            for j in range(DATOS_TESADO["NumPendolas"]-1, DATOS_TESADO["NumPendolas"]):
                for k in range(len(tensSupOriginal[i])):
                    var = self.sign(tensInfOriginal[i][k]) + 2 * self.sign(tensSupOriginal[i][k])
                    varm = self.sign(self.tensionInf[i][j][k]) + 2 * self.sign(self.tensionSup[i][j][k])

                    if var == -3:
                        if varm == -3:
                            if not (abs(self.tensionInf[i][j][k]) < abs(tensInfOriginal[i][k]) and abs(self.tensionSup[i][j][k]) < abs(tensSupOriginal[i][k])):
                                aa = abs(self.tensionInf[i][j][k]) - abs(tensInfOriginal[i][k])
                                bb = abs(self.tensionSup[i][j][k]) - abs(tensSupOriginal[i][k])

                                if self.sign(aa) == -1:
                                    aa = 0
                                if self.sign(bb) == -1:
                                    bb = 0

                                fit = fit + aa + bb

                        if varm == -1:
                            if abs(self.tensionSup[i][j][k]) < abs(tensSupOriginal[i][k]):
                                aa = abs(self.tensionInf[i][j][k]) + abs(tensInfOriginal[i][k])
                                fit = fit + aa
                            else:
                                aa = abs(self.tensionInf[i][j][k]) + abs(tensInfOriginal[i][k])
                                bb = abs(self.tensionSup[i][j][k]) - abs(tensSupOriginal[i][k])

                                if self.sign(aa) == -1:
                                    aa = 0
                                if self.sign(bb) == -1:
                                    bb = 0

                                fit = fit + aa + bb

                        if varm == 1:
                            if abs(self.tensionInf[i][j][k]) < abs(tensInfOriginal[i][k]):
                                bb = abs(self.tensionSup[i][j][k]) + abs(tensSupOriginal[i][k])
                                fit = fit + bb
                            else:
                                aa = abs(self.tensionInf[i][j][k]) - abs(tensInfOriginal[i][k])
                                bb = abs(self.tensionSup[i][j][k]) + abs(tensSupOriginal[i][k])

                                if self.sign(aa) == -1:
                                    aa = 0
                                if self.sign(bb) == -1:
                                    bb = 0

                                fit = fit + aa + bb

                        if varm == 3:
                            aa = abs(self.tensionInf[i][j][k]) + abs(tensInfOriginal[i][k])
                            bb = abs(self.tensionSup[i][j][k]) + abs(tensSupOriginal[i][k])

                            if self.sign(aa) == -1:
                                aa = 0
                            if self.sign(bb) == -1:
                                bb = 0

                            fit = fit + aa + bb

                    if var == -1:
                        if varm == - 3:
                            if abs(self.tensionSup[i][j][k]) < abs(tensSupOriginal[i][k]):
                                aa = abs(self.tensionInf[i][j][k]) + abs(tensInfOriginal[i][k])
                                fit = fit + aa
                            else:
                                aa = abs(self.tensionInf[i][j][k]) + abs(tensInfOriginal[i][k])
                                bb = abs(self.tensionSup[i][j][k]) - abs(tensSupOriginal[i][k])

                                if self.sign(aa) == -1:
                                    aa = 0

                                if self.sign(bb) == -1:
                                    bb = 0

                                fit = fit + aa + bb

                        if varm == -1:
                            if not (abs(self.tensionInf[i][j][k]) < abs(tensInfOriginal[i][k]) and abs(self.tensionSup[i][j][k]) < abs(tensSupOriginal[i][k])):
                                aa = abs(self.tensionInf[i][j][k]) - abs(tensInfOriginal[i][k])
                                bb = abs(self.tensionSup[i][j][k]) - abs(tensSupOriginal[i][k])

                                if self.sign(aa) == -1:
                                    aa = 0

                                if self.sign(bb) == -1:
                                    bb = 0

                                fit = fit + aa + bb

                        if varm == 1:
                            aa = abs(self.tensionInf[i][j][k]) + abs(tensInfOriginal[i][k])
                            bb = abs(self.tensionSup[i][j][k]) + abs(tensSupOriginal[i][k])

                            if self.sign(aa) == -1:
                                aa = 0

                            if self.sign(bb) == -1:
                                bb = 0

                            fit = fit + aa + bb

                        if varm == 3:
                            if abs(self.tensionInf[i][j][k]) < abs(tensInfOriginal[i][k]):
                                bb = abs(self.tensionSup[i][j][k]) + abs(tensSupOriginal[i][k])
                                fit = fit + bb
                            else:
                                aa = abs(self.tensionInf[i][j][k]) - abs(tensInfOriginal[i][k])
                                bb = abs(self.tensionSup[i][j][k]) + abs(tensSupOriginal[i][k])

                                if self.sign(aa) == -1:
                                    aa = 0

                                if self.sign(bb) == -1:
                                    bb = 0

                                fit = fit + aa + bb

                    if var == 1:
                        if varm == -3:
                            if abs(self.tensionInf[i][j][k]) < abs(tensInfOriginal[i][k]):
                                bb = abs(self.tensionSup[i][j][k]) + abs(tensSupOriginal[i][k])
                                fit = fit + bb
                            else:
                                aa = abs(self.tensionInf[i][j][k]) - abs(tensInfOriginal[i][k])
                                bb = abs(self.tensionSup[i][j][k]) + abs(tensSupOriginal[i][k])

                                if self.sign(aa) == -1:
                                    aa = 0

                                if self.sign(bb) == -1:
                                    bb = 0

                                fit = fit + aa + bb

                        if varm == -1:
                            aa = abs(self.tensionInf[i][j][k]) + abs(tensInfOriginal[i][k])
                            bb = abs(self.tensionSup[i][j][k]) + abs(tensSupOriginal[i][k])

                            if self.sign(aa) == -1:
                                aa = 0

                            if self.sign(bb) == -1:
                                bb = 0

                            fit = fit + aa + bb

                        if varm == 1:
                            if not (abs(self.tensionInf[i][j][k]) < abs(tensInfOriginal[i][k]) and abs(self.tensionSup[i][j][k]) < abs(tensSupOriginal[i][k])):
                                aa = abs(self.tensionInf[i][j][k]) - abs(tensInfOriginal[i][k])
                                bb = abs(self.tensionSup[i][j][k]) - abs(tensSupOriginal[i][k])

                                if self.sign(aa) == -1:
                                    aa = 0

                                if self.sign(bb) == -1:
                                    bb = 0

                                fit = fit + aa + bb

                        if varm == 3:
                            if abs(self.tensionSup[i][j][k]) < abs(tensSupOriginal[i][k]):
                                aa = abs(self.tensionInf[i][j][k]) + abs(tensInfOriginal[i][k])
                                fit = fit + aa
                            else:
                                aa = abs(self.tensionInf[i][j][k]) + abs(tensInfOriginal[i][k])
                                bb = abs(self.tensionSup[i][j][k]) - abs(tensSupOriginal[i][k])

                                if self.sign(aa) == -1:
                                    aa = 0

                                if self.sign(bb) == -1:
                                    bb = 0

                                fit = fit + aa + bb

                    if var == 3:
                        if varm == -3:
                            aa = abs(self.tensionInf[i][j][k]) + abs(tensInfOriginal[i][k])
                            bb = abs(self.tensionSup[i][j][k]) + abs(tensSupOriginal[i][k])

                            if self.sign(aa) == -1:
                                aa = 0

                            if self.sign(bb) == -1:
                                bb = 0

                            fit = fit + aa + bb

                        if varm == -1:
                            if abs(self.tensionInf[i][j][k]) < abs(tensInfOriginal[i][k]):
                                bb = abs(self.tensionSup[i][j][k]) + abs(tensSupOriginal[i][k])
                                fit = fit + bb
                            else:
                                aa = abs(self.tensionInf[i][j][k]) - abs(tensInfOriginal[i][k])
                                bb = abs(self.tensionSup[i][j][k]) + abs(tensSupOriginal[i][k])

                                if self.sign(aa) == -1:
                                    aa = 0

                                if self.sign(bb) == -1:
                                    bb = 0

                                fit = fit + aa + bb

                        if varm == 1:
                            if abs(self.tensionSup[i][j][k]) < abs(tensSupOriginal[i][k]):
                                aa = abs(self.tensionInf[i][j][k]) + abs(tensInfOriginal[i][k])
                                fit = fit + aa
                            else:
                                aa = abs(self.tensionInf[i][j][k]) + abs(tensInfOriginal[i][k])
                                bb = abs(self.tensionSup[i][j][k]) - abs(tensSupOriginal[i][k])

                                if self.sign(aa) == -1:
                                    aa = 0

                                if self.sign(bb) == -1:
                                    bb = 0

                                fit = fit + aa + bb

                        if varm == 3:
                            if not (abs(self.tensionInf[i][j][k]) < abs(tensInfOriginal[i][k]) and abs(self.tensionSup[i][j][k]) < abs(tensSupOriginal[i][k])):
                                aa = abs(self.tensionInf[i][j][k]) - abs(tensInfOriginal[i][k])
                                bb = abs(self.tensionSup[i][j][k]) - abs(tensSupOriginal[i][k])

                                if self.sign(aa) == -1:
                                    aa = 0

                                if self.sign(bb) == -1:
                                    bb = 0

                                fit = fit + aa + bb

        fitnessTesado = fit / (2*DATOS_TESADO["NumPendolas"])
        self.fitness = fitnessTesado
        return fitnessTesado

    def sign(self, x):
        if x > 0:
            return 1
        elif x < 0:
            return -1
        elif x == 0:
            return 0
        else:
            return x

    def mayor(self, a, b):
        if a>=b:
            return a
        else:
            return b
