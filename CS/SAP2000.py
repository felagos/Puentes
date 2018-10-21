import os
import sys
import comtypes.client
from Constantes import PUENTE_ORIGINAL,PUENTE_MODIFICADO, DATOS_TESADO
import time

class SAP2000():
    mySapObject = None
    SapModel = None

    #datos puente original
    momentos = []   #Lista de [nvigas] listas de momentos
    tensionSup = [] #Lista de [nvigas] listas de tensiones superiores
    tensionInf = [] #Lista de [nvigas] listas de tensiones inferiores

    momentosTransv = []
    tensionSupTransv = []
    tensionInfTransv = []


    #datos puente modificado
    inercia33 = None
    inerciat = None
    fck = None
    fpu = None
    Ependola = None
    area = None
    areaT = None
    largoPendola = None
    fct = None
    fcmax = None
    fxmax2 = None

    Preal = None
    P = None
    npld = None
    tconv = None
    numx = None
    tesadoMinimo = None
    tesadoMaximo = None


    #funcion para cargar modelo
    def abrirSAP(self):
        # set the following flag to True to attach to an existing instance of the program
        # otherwise a new instance of the program will be started
        AttachToInstance = False

        # set the following flag to True to manually specify the path to SAP2000.exe
        # this allows for a connection to a version of SAP2000 other than the latest installation
        # otherwise the latest installed version of SAP2000 will be launched
        SpecifyPath = True

        # if the above flag is set to True, specify the path to SAP2000 below
        ProgramPath = 'C:\Program Files\Computers and Structures\SAP2000 20\SAP2000.exe'
        #ProgramPath = 'C:\Program Files\Computers and Structures\CSiBridge 2017\CSiBridge.exe'

        # full path to the model
        # set it to the desired path of your model
        APIPath = 'D:\Prueba'
        if not os.path.exists(APIPath):
            try:
                os.makedirs(APIPath)
            except OSError:
                pass
        ModelPath = APIPath + os.sep + 'bridge_VB.SDB'

        if AttachToInstance:
            # attach to a running instance of SAP2000
            try:
                # get the active SapObject
                mySapObject = comtypes.client.GetActiveObject("CSI.SAP2000.API.SapObject")
            except (OSError, comtypes.COMError):
                print("No running instance of the program found or failed to attach.")
                sys.exit(-1)
        else:
            # create API helper object
            helper = comtypes.client.CreateObject('SAP2000v19.Helper')
            helper = helper.QueryInterface(comtypes.gen.SAP2000v19.cHelper)

            if SpecifyPath:
                try:
                    # 'create an instance of the SAPObject from the specified path
                    self.mySapObject = helper.CreateObject(ProgramPath)
                except (OSError, comtypes.COMError):
                    print("Cannot start a new instance of the program from " + ProgramPath)
                    sys.exit(-1)
            else:
                try:
                    # create an instance of the SAPObject from the latest installed SAP2000
                    self.mySapObject = helper.CreateObjectProgID("CSI.SAP2000.API.SapObject")
                except (OSError, comtypes.COMError):
                    print("Cannot start a new instance of the program.")
                    sys.exit(-1)

            # start SAP2000 application
            self.mySapObject.ApplicationStart()

    def cerrarSap2000(self):
        # close Sap2000
        self.mySapObject.ApplicationExit(False)
        self.SapModel = None
        self.mySapObject = None

    def cargarPuenteOriginal(self):
        # create SapModel object
        self.SapModel = self.mySapObject.SapModel

        # initialize model
        self.SapModel.InitializeNewModel()

        # open an existing file
        FileName = PUENTE_ORIGINAL
        self.SapModel.File.OpenFile(FileName)
        #Set units to kN, m, C
        self.SapModel.SetPresentUnits(6)

    def cargarPuenteModificado(self):
        # create SapModel object
        self.SapModel = self.mySapObject.SapModel

        # initialize model
        self.SapModel.InitializeNewModel()

        # open an existing file
        FileName = PUENTE_MODIFICADO
        self.SapModel.File.OpenFile(FileName)

        self.SapModel.SetPresentUnits(6)

    # Obtener información necesaria del modelo original
    def getInfoModeloOriginal(self):
        #set load case run flag
        ret = self.SapModel.Analyze.SetRunCaseFlag("COMB SERVICIO", True)
        ret = self.SapModel.Analyze.SetRunCaseFlag("DEAD", True)
        ret = self.SapModel.Analyze.SetRunCaseFlag("CM", True)
        ret = self.SapModel.Analyze.SetRunCaseFlag("q", True)
        ret = self.SapModel.Analyze.SetRunCaseFlag("CAMION", True)

        #run analysis
        ret = self.SapModel.Analyze.RunAnalysis()

        #clear all cases
        ret = self.SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()

        #set comb servicio case
        ret = self.SapModel.Results.Setup.SetCaseSelectedForOutput("COMB SERVICIO")

        vsup = DATOS_TESADO["vsup"]
        vinf = DATOS_TESADO["vinf"]
        FS = DATOS_TESADO["FS"]
        inercias = []

        for x in range(DATOS_TESADO["VigasAAnalizar"]):
            #Se genera string "VIGA1", "VIGA2", etc
            vigaAnalizar = "VIGA"+str(x+1)

            #Obtener las fuerzas en la VIGAx
            ret = self.SapModel.Results.FrameForce(vigaAnalizar,2)
            print("Datos "+vigaAnalizar+ " Modelo Original")
            self.momentos.append(ret[13])
            print(ret[13])

            cant = ret[0]
            momentos = ret[13]  #indice 13, momentos

            #Obtener propiedades de la VIGAx
            ret = self.SapModel.PropFrame.GetSectProps("V" + str(x+1))
            print(ret[5])
            inercia = ret[5]
            inercias.append(inercia)

            tensionSup = []
            tensionInf = []

            for i in range(cant):
                #Calcular Tensiones longitudinales desde los momentos.
                tensionSup.append(FS*momentos[i]*vsup/inercia)
                tensionInf.append(-1*FS*momentos[i]*vinf/inercia)

            self.tensionSup.append(tensionSup)
            self.tensionInf.append(tensionInf)

        self.inercia33 = inercias
        #Analisis vigas transversales
        vsupt = DATOS_TESADO["vsupt"]
        vinft = DATOS_TESADO["vinft"]
        # Escribir momentos de cada viga en excel
        for x in range(DATOS_TESADO["VigasTransv"]):
            # Se genera string "VIGAT1", "VIGAT2", etc
            vigaAnalizar = "VIGAT" + str(x + 1)

            # Obtener las fuerzas en la VIGAx
            ret = self.SapModel.Results.FrameForce(vigaAnalizar, 2)
            cant = ret[0]
            momentos = ret[13]  # indice 13, momentos
            self.momentosTransv.append(momentos)

            # Obtener propiedades de la VIGAx
            ret = self.SapModel.PropFrame.GetSectProps("VTT" + str(x + 1))
            self.areaT = ret[0]
            inerciat = ret[5]
            self.inerciat = inerciat

            tensionSup = []
            tensionInf = []

            for i in range(0, cant):
                # Calcular Tensiones longitudinales desde los momentos.
                tensionSup.append(FS * momentos[i] * vsup / inerciat)
                tensionInf.append((-1 * FS) * momentos[i] * vinf / inerciat)


            self.tensionSupTransv.append(tensionSup)
            self.tensionInfTransv.append(tensionInf)

    # Obtener información necesaria del modelo modificado
    def getInfoModeloModificado(self):
        # set load case run flag
        ret = self.SapModel.Analyze.SetRunCaseFlag("", False, True)
        ret = self.SapModel.SetModelIsLocked(False)
        ret = self.SapModel.Analyze.SetRunCaseFlag("DEAD", True)

        #get Propiedades de pendolas
        for i in range(DATOS_TESADO["NumPendolas"]-1):
            ret = self.SapModel.PropFrame.GetSectProps("PENDOLA"+str(i+1))
            area = ret[0]

        ret = self.SapModel.PropMaterial.GetOConcrete_1("CONC")
        fck = ret[0]  

        #Otras propiedades
        ret = self.SapModel.PropMaterial.GetOSteel_1("SPENDOLA")
        fpu = ret[1]

        #get isotropic mechanical properties
        ret = self.SapModel.PropMaterial.GetMPIsotropic("SPENDOLA")
        Ependola = ret[0]

        #run Model analysis
        ret = self.SapModel.Analyze.RunAnalysis()
        #Clear all cases
        ret = self.SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
        #set Cases
        ret = self.SapModel.Results.Setup.SetCaseSelectedForOutput("DEAD")

        largoPendola = []
        npend = DATOS_TESADO["NumPendolas"]
        for i in range(npend):
            ret = self.SapModel.Results.FrameForce(str(i+1), 2)
            largoPendola.append(ret[2][2])

        #get base reactions
        ret = self.SapModel.Results.BaseReact()
        mintenso = ret[6][0]

        ret = self.SapModel.SetModelIsLocked(False)

        #Definicion de carga por deformacion en las pendolas
        dl = []
        for i in range(npend):
            dl.append(-(0.3*fpu*largoPendola[i])/Ependola)

        self.fpu = fpu
        self.fck = fck
        self.Ependola = Ependola
        self.area = area
        self.largoPendola = largoPendola

        self.fct = 0.3 * 0.7 * 0.85 * pow((fck * 1000 / 1000000),0.67) * 1000
        self.fcmax = 0.6 * fck
        self.fcmax2 = 0.9 * fck

        ret = self.SapModel.Analyze.SetRunCaseFlag("", False, True)
        ret = self.SapModel.SetModelIsLocked(False)

        #assign frame deformation loads
        DOF = [False] * 6
        d = [0.0] * 6

        for i in range(npend):
            DOF[0] = True
            d[0] = dl[i]
            ret = self.SapModel.FrameObj.SetLoadDeformation(str(i+1),"TEMP",DOF,d,1)


        #initialize stage definitions
        MyDuration = [0] * npend
        MyOutput = [False] * npend
        MyOutputName = [""] * npend
        MyOutputName[0] = "Hanger"
        MyComment = [""] * npend
        MyComment[0] = "Tight"

        #Etapas
        MyOperation = [1,4]
        MyObjectType = ["Group"] * 2
        MyMyType = ["", "Load"]
        MyMyName = ["", "TEMP"]
        MyAge = [0]*2
        MySF = [0, 1]

        for i in range(npend):
            #add static nonlinear staged load case
            ret = self.SapModel.LoadCases.StaticNonlinearStaged.SetCase("LCASET"+str(i))
            #set geometric nonlinearity option
            ret = self.SapModel.LoadCases.StaticNonlinearStaged.SetGeometricNonlinearity("LCASET"+str(i), 0)
            #set results saved parameters
            ret = self.SapModel.LoadCases.StaticNonlinearStaged.SetResultsSaved("LCASET"+str(i), 1)
            #set initial condition
            ret = self.SapModel.LoadCases.StaticNonlinearStaged.SetInitialCase("LCASET"+str(i), "LCASE1")

            #definicion de cada etapa
            ret = self.SapModel.LoadCases.StaticNonlinearStaged.SetStageDefinitions_1("LCASET"+str(i), 1, MyDuration, MyOutput, MyOutputName, MyComment)
            MyObjectName = [str(i+1)] * 2
            ret = self.SapModel.LoadCases.StaticNonlinearStaged.SetStageData_1("LCASET"+str(i), 1, 2, MyOperation, MyObjectType, MyObjectName, MyAge, MyMyType, MyMyName, MySF)

        #set load case run flag

        ret = self.SapModel.Analyze.SetRunCaseFlag("DEAD", True)
        ret = self.SapModel.Analyze.SetRunCaseFlag("CM", True)
        ret = self.SapModel.Analyze.SetRunCaseFlag("TENDON", True)
        ret = self.SapModel.Analyze.SetRunCaseFlag("TEMP", True)
        ret = self.SapModel.Analyze.SetRunCaseFlag("LCASE1", True)

        for i in range(npend):
            ret = self.SapModel.Analyze.SetRunCaseFlag("LCASET"+str(i), True)

        ret = self.SapModel.Analyze.RunAnalysis()

        #Condicion de 45% de esfuerzo en pendolas
        P = []
        Preal = [] #N_{ED}
        tconv = []
        numal2 = []
        npld = []
        numx = []
        tesadoMinimo = DATOS_TESADO["numal1"]
        tesadoMaximo = [DATOS_TESADO["numal2"]]*npend
        for i in range(npend):
            ret = self.SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
            ret = self.SapModel.Results.Setup.SetCaseSelectedForOutput("LCASET"+str(i))

            #set output option
            ret = self.SapModel.Results.Setup.SetOptionNLStatic(2)

            ret = self.SapModel.Results.FrameForce(str(i + 1), 2)
            P.append(ret[8][0])
            Preal.append((Ependola*area*abs(dl[i]))/largoPendola[i]) 
            tconv.append(Preal[i]/P[i])
            tesadoMaximo[i] = tesadoMaximo[i]*tconv[i]
            npld.append(0.45*area*fpu)
            numx.append(npld[i]/P[i])

            if tesadoMaximo[i] > numx[i]:
                tesadoMaximo[i] = numx[i]

        print(min(tconv))
        tesadoMinimo = tesadoMinimo * min(tconv)


        self.Preal = Preal
        self.P = P
        self.npld = npld
        self.tconv = tconv
        self.numx = numx
        self.tesadoMaximo = tesadoMaximo
        self.tesadoMinimo = tesadoMinimo

        ret = self.SapModel.SetModelIsLocked(False)

    def aplicarTesado(self,solutions):
        vsup = DATOS_TESADO["vsup"]
        vinf = DATOS_TESADO["vinf"]
        nvigas = DATOS_TESADO["VigasAAnalizar"]
        nvigast = DATOS_TESADO["VigasTransv"]
        npend = DATOS_TESADO["NumPendolas"]

        ret = self.SapModel.Analyze.SetRunCaseFlag("", False, True)

        ret = self.SapModel.Analyze.SetRunCaseFlag("TEMP", True)
        ret = self.SapModel.Analyze.SetRunCaseFlag("DEAD", True)
        ret = self.SapModel.Analyze.SetRunCaseFlag("LCASE1", True)

        #Setear casos de prueba para cada solution
        for x in range(len(solutions)):
            individuo = solutions[x]
            orden = individuo.orden
            magnitud = individuo.magnitud

            #add static nonlinear staged load case
            ret = self.SapModel.LoadCases.StaticNonlinearStaged.SetCase("TCASE"+str(x))
            #set geometric nonlinearity option
            ret = self.SapModel.LoadCases.StaticNonlinearStaged.SetGeometricNonlinearity("TCASE"+str(x), 0)
            #set results saved parameters
            ret = self.SapModel.LoadCases.StaticNonlinearStaged.SetResultsSaved("TCASE"+str(x), 1)
            #set initial condition
            ret = self.SapModel.LoadCases.StaticNonlinearStaged.SetInitialCase("TCASE"+str(x), "LCASE1")

            # initialize stage definitions
            MyDuration = [0] * npend
            MyOutput = [True] * npend
            MyOutputName = [""] * npend
            MyComment = [""] * npend

            for j in range(0, npend):
                MyOutputName[j] = "Hanger" + str(j)
                MyComment[j] = "Tight"
                ret = self.SapModel.LoadCases.StaticNonlinearStaged.SetStageDefinitions_1("TCASE"+str(x), npend, MyDuration, MyOutput, MyOutputName, MyComment)

            # Definición de Etapas
            MyOperation = [1, 4]
            MyObjectType = ["Group"] * 2
            MyMyType = ["", "Load"]
            MyMyName = ["", "TEMP"]
            MyAge = [0] * 2
            for j in range(0, npend):
                MyObjectName = [str(orden[j])] * 2  # GET ORDEN solution
                MySF = [0, magnitud[j]]  # GET MAGNITUD solution
                ret = self.SapModel.LoadCases.StaticNonlinearStaged.SetStageData_1("TCASE"+str(x), j + 1, 2, MyOperation, MyObjectType, MyObjectName, MyAge, MyMyType, MyMyName, MySF)

            # set load case run flag
            ret = self.SapModel.Analyze.RunAnalysis()

        for i in range(len(solutions)):
            solutions[i].momentosViga = [[] for m in range(DATOS_TESADO["VigasAAnalizar"])]

            # clear all cases
            ret = self.SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
            # set case
            ret = self.SapModel.Results.Setup.SetCaseSelectedForOutput("TCASE"+str(i))  # + str(i)
            # set output option
            ret = self.SapModel.Results.Setup.SetOptionNLStatic(2)

            #Se sacan momentos para CADA VIGA
            for v in range(nvigas):
                #set frame forces for line object "1"
                ret = self.SapModel.Results.FrameForce("VIGA"+str(v+1), 2)

                etapas = ret[7]
                momentos = ret[13]
                P = ret[8]

                momentos_etapa = [[] for m in range(npend)] #lista de largo [etapas] que en cada posicion contiene los momentos de la etapa
                axil_por_etapa = [[] for m in range(npend)] #lista de largo [etapas] que en cada posicion contiene el axil de la etapa

                for e in range(ret[0]):
                    etapa_e = int(etapas[e])
                    momento_e = momentos[e]
                    p_e = P[e]

                    momentos_etapa[etapa_e-1].append(momento_e)
                    axil_por_etapa[etapa_e-1].append(p_e)

                #Se agrega la lista de momentos y axiles de la viga V a la solution.
                solutions[i].momentosViga[v] = list(momentos_etapa)  #A la viga [v] del individuo le asignamos los momentos de cada etapa de esa viga
                solutions[i].axilesViga[v] = list(axil_por_etapa)

            #END FOR


            lcd = []
            for j in range(npend):
                #get joint absolute displacement for point object "22"
                ret = self.SapModel.Results.JointDisplAbs("CPILA"+str(j+1), 2)

                etapas = ret[5]
                U3 = ret[8]

                U_etapa = [[] for m in range(npend)]

                for e in range(ret[0]):
                    etapa_e = int(etapas[e])
                    U3_e = U3[e]

                    U_etapa[etapa_e-1].append(U3_e)

                solutions[i].lcd[j] = list(U_etapa)


        areaTotal = DATOS_TESADO["AreaTotal"]
        excentricidad = DATOS_TESADO["ExcentricidadTendon"]
        inerciaTotal = DATOS_TESADO["InerciaTotal"]
        inercia = self.inercia33

        #Cálculo de tensiones para cada solution
        for i in range(len(solutions)):
            solutions[i].tensionSup = None
            solutions[i].tensionInf = None

            Axilt = solutions[i].axilesViga
            Mmt = solutions[i].momentosViga

            Smtsup = [[] for m in range(nvigas)]
            Smtinf = [[] for m in range(nvigas)]
            for v in range(nvigas):
                Smtsup[v] = [[] for m in range(npend)]
                Smtinf[v] = [[] for m in range(npend)]
                for w in range(npend):
                    for x in range(0, len(Axilt[v][w])):
                        Smtsup[v][w].append(-Axilt[v][w][x] / areaTotal + Axilt[v][w][x] * excentricidad * vsup / inerciaTotal + Mmt[v][w][x] * vsup / inercia[v])
                        Smtinf[v][w].append(-Axilt[v][w][x] / areaTotal - Axilt[v][w][x] * excentricidad * vinf / inerciaTotal - Mmt[v][w][x] * vinf / inercia[v])

            solutions[i].tensionSup = list(Smtsup)
            solutions[i].tensionInf = list(Smtinf)
        #END FOR


        #Calculo vigas transversales
        for i in range(len(solutions)):
            ret = self.SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
            ret = self.SapModel.Results.Setup.SetCaseSelectedForOutput("TCASE"+str(i))
            ret = self.SapModel.Results.Setup.SetOptionNLStatic(2)

            Mmtt = []
            Axiltt = []
            for v in range(nvigast):
                ret = self.SapModel.Results.FrameForce("VIGAT"+str(v+1), 2)
                etapasMmtt = [[] for m in range(npend)]
                etapasAxiltt = [[] for m in range(npend)]

                for j in range(ret[0]):
                    etapasMmtt[int(ret[7][j]) - 1].append(ret[13][j])
                    etapasAxiltt[int(ret[7][j]) - 1].append(ret[8][j])
                Mmtt.append(etapasMmtt)
                Axiltt.append(etapasAxiltt)

            Smtsupt = [[] for m in range(nvigast)]
            Smtinft = [[] for m in range(nvigast)]
            for v in range(nvigast):
                Smtsupt[v] = [[] for m in range(npend)]
                Smtinft[v] = [[] for m in range(npend)]
                for w in range(npend):
                    for x in range(0, len(Axiltt[v][w])):
                        Smtsupt[v][w].append(-Axiltt[v][w][x] / self.areaT + Axiltt[v][w][x] * excentricidad * vsup / self.inerciat + Mmtt[v][w][x] * vsup / self.inerciat)
                        Smtinft[v][w].append(-Axiltt[v][w][x] / self.areaT - Axiltt[v][w][x] * excentricidad * vinf / self.inerciat - Mmtt[v][w][x] * vinf / self.inerciat)
            
        #END FOR
