files = ["AB-TCVCS", "CC-TCVCS", "CR-AA10CS", "HW-TCVCS", "PT-TCVCS", "PV-TCVCS", "RC-AA10CS", "RD-AA10CS", "TC-TCVCS", "VC-TCVCS", "WR-TCVCS"]

for instancia in files:
	path = "./Resultados DA/"+instancia
	try:
		fileNew = open("./Resultados DA/Resumen DA/"+instancia+".txt", "w")

		for i in range(1, 16):
			fileName = path+str(i)+".txt"
			file = open(fileName, "r")

		if len(line) >= 15:
			try:
				fileNew.write(line[15]+"\n")
			except:
				print(line, fileName)
		else:
			line = line[11].split(":")
			try:
				fileNew.write(line[1]+"\n")
			except:
				print(line, fileName)
			file.close()

		fileNew.close()
	except Exception as e:
		print(e)