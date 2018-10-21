from SAP2000 import SAP2000
from DA import Meta
from Constantes import DATOS_TESADO,DATOS_MH
from Solution import Solution
import time

#nueva instancia de SAP
modelo = SAP2000()


#abrir SAP
print("Abriendo SAP2000...")
modelo.abrirSAP()
print("Listo!\n")


#cargar Puente original
print("Cargando puente original...")
modelo.cargarPuenteOriginal()
print("Listo!\n")


#obtener datos puente original
print("Obteniendo info del puente original...")
modeloOriginal = modelo.getInfoModeloOriginal()
print("Listo!\n")


#cargar Puente Modificado
print("Cargando puente modificado...")
modelo.cargarPuenteModificado()
print("Listo!\n")


#obtener datos puente modificado
print("Obteniendo info del puente modificado...")
modelo.getInfoModeloModificado()
print("Listo!\n")

print("DATOS DEL MODELO: \n")
print("TesadoMinimo:                    "+str(modelo.tesadoMinimo))
print("TesadoMaximo(numx):              "+str(modelo.numx))
print("Tension inicial aplicada(Preal): "+str(modelo.Preal))
print("Tension efectiva sin tasa(P):    "+str(modelo.P))
print("Tension admisible pendola(npld): "+str(modelo.npld))
print("Tasa conversion(tconv):          "+str(modelo.tconv))
print("fc(fck):                         "+str(modelo.fck))
print("fpu:                             "+str(modelo.fpu))
print("E pendola:                       "+str(modelo.Ependola))
print("Area pendola(areasp):            "+str(modelo.area))
print("Largo péndola(lpendola):         "+str(modelo.largoPendola))
print("fct:                             "+str(modelo.fct))
print("fcmax:                           "+str(modelo.fcmax))
print("fcmax2:                          "+str(modelo.fcmax2))


print("\nSe procede a aplicar tesado")
MT = Meta(DATOS_MH["Poblacion"], DATOS_MH["Iteraciones"])
valor = MT.Metaheuristic(modelo)


'''
#Tesado de prueba
orden = [1, 2, 3]
mag = [2.340070389, 1.236889534, 1.579377348]
solution = Solution(orden,mag)
st = [solution]
modelo.aplicarTesado(st)
print("FIT: "+str(solution.calcularFitness(modelo)))
#Deberia dar como resultado de Fitness: 534218.4325913534
'''


print("Listo!")

print("\nCerrando SAP2000...")
modelo.cerrarSap2000()
print("Terminado.")