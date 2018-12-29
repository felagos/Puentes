files = ["AB-TCVCS", "CC-TCVCS", "CR-AA10CS", "HW-TCVCS", "PT-TCVCS",
         "PV-TCVCS", "RC-AA10CS", "RD-AA10CS", "TC-TCVCS", "VC-TCVCS", "WR-TCVCS"]

for instancia in files:
    path = "./Resultados DA/"+instancia
    try:
        fileNew = open("./Resultados DA/Resumen DA/"+instancia+".txt", "w")

        for i in range(1, 16):
            fileName = path+str(i)+".txt"
            file = open(fileName, "r")
            lines = file.read().splitlines()
            line = lines[-1]

            try:
                value = ""
                if "FIT:" in line:
                    value = line.split("FIT:")[1].split(",")[0].strip()
                else: 
                    value = line.split("FIT,")[1].split(",")[0].strip()
                fileNew.write(value+"\n")
            except:
                print(line, fileName)

            file.close()

        fileNew.close()
    except Exception as e:
        print(e)
