folderCS = "../Resultados CS/Resumen CS/"
folderDA = "../Resultados DA/Resumen DA/"

instances = ["AB-TCVCS", "CC-TCVCS", "CR-AA10CS", "HW-TCVCS", "PT-TCVCS", "PV-TCVCS", "RC-AA10CS", "RD-AA10CS", "TC-TCVCS", "VC-TCVCS", "WR-TCVCS"]

execute = open("ejecutar.bat", "w")

for instance in instances:
    pathCS = folderCS + instance + ".txt"
    pathDA = folderDA + instance + ".txt"
    path = instance + ".txt"

    fileCS = open(pathCS, "r")
    fileDA = open(pathDA, "r")
    fileResult = open(path, "w")

    contentCS = fileCS.read()
    contentDA = fileDA.read()

    valuesCS = contentCS.split("\n")
    del valuesCS[-1]
    valuesCS.sort()
    contentCS = "\n".join(valuesCS)  
    
    valuesDA = contentDA.split("\n")
    del valuesDA[-1]
    valuesDA.sort()
    valuesDA = contentDA.split("\n")
    contentDA = "\n".join(valuesDA)  

    fullContent = contentCS + "\n\n" + contentDA
    fileResult.write(fullContent.rstrip())
    
    command = "mann-whit.exe " + path + " emptyparam.txt output_" + instance+".txt > resultados_" + instance + ".txt"
    execute.write(command + "\n")

    fileCS.close()
    fileDA.close()
    fileResult.close()
    
execute.close()