set Link=C:\Puentes\&:: Ruta base
set Link2=C:\Puentes\Resultados\&:: Ruta Donde guard /S /Qaremos los resultados
set Instancias=C:\Puentes\Instancias\&:: Ruta donde tenemos las instancias
set Modificado=C:\Puentes\Modificado\&:: Ruta desde donde ejecutaremos la instancia modificada
set Modificado2=C:\Puentes\Modificado2\&:: Copia de la instancia modificada para reemplazar
set Original=C:\Puentes\Original\&:: Ruta desde donde ejecutaremos la instancia original
set ECS=C:\Puentes\CS\&:: Ruta donde esta el codigo de nuestra metaheur�stica

set Reg2=Registro.txt&:: Nombre del archivo que nos entrega nuestra metahehur�stica ejecutada en Python


Rem INICIO DE EJECUCI�N DE INSTANCIA----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
set Inta=PV-TCV&:: Nombre de la instancia a Ejecutar

set "Instance=%Inta%.sdb"&:: Agragamos la extensi�n ".sdb" a la instancia modificada
set "Instance2=Orig-%Inta%.sdb"&:: Agregamos la extensi�n ".Sdb" a la instancia original
set "Mod=PuenteMod.sdb"&:: Inicializamos la variable Mod, la cual contiene la instancia modificada
set "Orig=PuenteOrig.sdb"&:: Inicializamos la varibale Orig, la cual contiene la instancia original

xcopy %Instancias%%Instance% %Modificado%&:: Copiamos la instancia a la carpeta "Modificado"
ren %Modificado%%Instance% %Mod%&:: Cambiamos el nombre de la instancia a "PuenteMod.sdb"
xcopy %Instancias%%Instance% %Modificado2%&:: Copiamos la instancia a la carpeta "Modificado2"
ren %Modificado2%%Instance% %Mod%&:: Cambiamos le nombre de la instancia a "PuenteMod.sdb"
xcopy %Instancias%%Instance2% %Original%&:: Copiamos la instancia original a la carpeta "Original"
ren %Original%%Instance2% %Orig%&:: Cambiamos el nombre de la instancia a "PuenteOrig.sdb"

Rem Ejecutamos la instancia j veces
for %%j in (1,2) do (
	Rem INSTANCIA CS
	cd %ECS%&:: Nos Posicionamos en la ruta donde esta nuestra metaheur�stica
	Python Main.py&:: Ejecutamos la Metaheur�stica
	xcopy "%Ruta%%Reg2%" "%Link2%"&:: Copiamos el resultado de nuestra ejecuci�n a nuestra carpeta de resultados
	cd "%Link2%"&:: Nos posicionamos en la ruta donde estan nuestro resultados
	ren "%Link2%%Reg2%" %Inta%CS%%j.txt&:: Cambiamos el nombre del resultado obtenido por [Nombre de instancia][Nombre de Metaheur�stica]j.txt
	del /f /q *.*"%Link%%EBH%%Reg2%"
	)

rd /S /Q %Modificado%&::Elimino la carpeta "Modificado"
rd /S /Q %Modificado2%&::Elimino la carpeta "Modificado2"
rd /S /Q %Original%&::Elimino la carpeta "Original"
mkdir %Modificado%&::Creo la carpeta "Modificado"
mkdir %Modificado2%&::Creo la carpeta "Modificado2"
mkdir %Original%&::Creo la carpeta "Original"
Rem FIN DE EJECUCI�N DE INSTANCIA ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------


Rem INICIO DE EJECUCI�N DE INSTANCIA----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
set Inta=HW-TCV&:: Nombre de la instancia a Ejecutar

set "Instance=%Inta%.sdb"&:: Agragamos la extensi�n ".sdb" a la instancia modificada
set "Instance2=Orig-%Inta%.sdb"&:: Agregamos la extensi�n ".Sdb" a la instancia original
set "Mod=PuenteMod.sdb"&:: Inicializamos la variable Mod, la cual contiene la instancia modificada
set "Orig=PuenteOrig.sdb"&:: Inicializamos la varibale Orig, la cual contiene la instancia original

xcopy %Instancias%%Instance% %Modificado%&:: Copiamos la instancia a la carpeta "Modificado"
ren %Modificado%%Instance% %Mod%&:: Cambiamos el nombre de la instancia a "PuenteMod.sdb"
xcopy %Instancias%%Instance% %Modificado2%&:: Copiamos la instancia a la carpeta "Modificado2"
ren %Modificado2%%Instance% %Mod%&:: Cambiamos le nombre de la instancia a "PuenteMod.sdb"
xcopy %Instancias%%Instance2% %Original%&:: Copiamos la instancia original a la carpeta "Original"
ren %Original%%Instance2% %Orig%&:: Cambiamos el nombre de la instancia a "PuenteOrig.sdb"

Rem Ejecutamos la instancia j veces
for %%j in (1,2) do (
	Rem INSTANCIA CS
	cd %ECS%&:: Nos Posicionamos en la ruta donde esta nuestra metaheur�stica
	Python Main.py&:: Ejecutamos la Metaheur�stica
	xcopy "%Ruta%%Reg2%" "%Link2%"&:: Copiamos el resultado de nuestra ejecuci�n a nuestra carpeta de resultados
	cd "%Link2%"&:: Nos posicionamos en la ruta donde estan nuestro resultados
	ren "%Link2%%Reg2%" %Inta%CS%%j.txt&:: Cambiamos el nombre del resultado obtenido por [Nombre de instancia][Nombre de Metaheur�stica]j.txt
	del /f /q *.*"%Link%%EBH%%Reg2%"
	)

rd /S /Q %Modificado%&::Elimino la carpeta "Modificado"
rd /S /Q %Modificado2%&::Elimino la carpeta "Modificado2"
rd /S /Q %Original%&::Elimino la carpeta "Original"
mkdir %Modificado%&::Creo la carpeta "Modificado"
mkdir %Modificado2%&::Creo la carpeta "Modificado2"
mkdir %Original%&::Creo la carpeta "Original"
Rem FIN DE EJECUCI�N DE INSTANCIA ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------


Rem INICIO DE EJECUCI�N DE INSTANCIA----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
set Inta=PT-TCV&:: Nombre de la instancia a Ejecutar

set "Instance=%Inta%.sdb"&:: Agragamos la extensi�n ".sdb" a la instancia modificada
set "Instance2=Orig-%Inta%.sdb"&:: Agregamos la extensi�n ".Sdb" a la instancia original
set "Mod=PuenteMod.sdb"&:: Inicializamos la variable Mod, la cual contiene la instancia modificada
set "Orig=PuenteOrig.sdb"&:: Inicializamos la varibale Orig, la cual contiene la instancia original

xcopy %Instancias%%Instance% %Modificado%&:: Copiamos la instancia a la carpeta "Modificado"
ren %Modificado%%Instance% %Mod%&:: Cambiamos el nombre de la instancia a "PuenteMod.sdb"
xcopy %Instancias%%Instance% %Modificado2%&:: Copiamos la instancia a la carpeta "Modificado2"
ren %Modificado2%%Instance% %Mod%&:: Cambiamos le nombre de la instancia a "PuenteMod.sdb"
xcopy %Instancias%%Instance2% %Original%&:: Copiamos la instancia original a la carpeta "Original"
ren %Original%%Instance2% %Orig%&:: Cambiamos el nombre de la instancia a "PuenteOrig.sdb"

Rem Ejecutamos la instancia j veces
for %%j in (1,2) do (
	Rem INSTANCIA CS
	cd %ECS%&:: Nos Posicionamos en la ruta donde esta nuestra metaheur�stica
	Python Main.py&:: Ejecutamos la Metaheur�stica
	xcopy "%Ruta%%Reg2%" "%Link2%"&:: Copiamos el resultado de nuestra ejecuci�n a nuestra carpeta de resultados
	cd "%Link2%"&:: Nos posicionamos en la ruta donde estan nuestro resultados
	ren "%Link2%%Reg2%" %Inta%CS%%j.txt&:: Cambiamos el nombre del resultado obtenido por [Nombre de instancia][Nombre de Metaheur�stica]j.txt
	del /f /q *.*"%Link%%EBH%%Reg2%"
	)

rd /S /Q %Modificado%&::Elimino la carpeta "Modificado"
rd /S /Q %Modificado2%&::Elimino la carpeta "Modificado2"
rd /S /Q %Original%&::Elimino la carpeta "Original"
mkdir %Modificado%&::Creo la carpeta "Modificado"
mkdir %Modificado2%&::Creo la carpeta "Modificado2"
mkdir %Original%&::Creo la carpeta "Original"
Rem FIN DE EJECUCI�N DE INSTANCIA ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------


Rem INICIO DE EJECUCI�N DE INSTANCIA----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
set Inta=AB-TCV&:: Nombre de la instancia a Ejecutar

set "Instance=%Inta%.sdb"&:: Agragamos la extensi�n ".sdb" a la instancia modificada
set "Instance2=Orig-%Inta%.sdb"&:: Agregamos la extensi�n ".Sdb" a la instancia original
set "Mod=PuenteMod.sdb"&:: Inicializamos la variable Mod, la cual contiene la instancia modificada
set "Orig=PuenteOrig.sdb"&:: Inicializamos la varibale Orig, la cual contiene la instancia original

xcopy %Instancias%%Instance% %Modificado%&:: Copiamos la instancia a la carpeta "Modificado"
ren %Modificado%%Instance% %Mod%&:: Cambiamos el nombre de la instancia a "PuenteMod.sdb"
xcopy %Instancias%%Instance% %Modificado2%&:: Copiamos la instancia a la carpeta "Modificado2"
ren %Modificado2%%Instance% %Mod%&:: Cambiamos le nombre de la instancia a "PuenteMod.sdb"
xcopy %Instancias%%Instance2% %Original%&:: Copiamos la instancia original a la carpeta "Original"
ren %Original%%Instance2% %Orig%&:: Cambiamos el nombre de la instancia a "PuenteOrig.sdb"

Rem Ejecutamos la instancia j veces
for %%j in (1,2) do (
	Rem INSTANCIA CS
	cd %ECS%&:: Nos Posicionamos en la ruta donde esta nuestra metaheur�stica
	Python Main.py&:: Ejecutamos la Metaheur�stica
	xcopy "%Ruta%%Reg2%" "%Link2%"&:: Copiamos el resultado de nuestra ejecuci�n a nuestra carpeta de resultados
	cd "%Link2%"&:: Nos posicionamos en la ruta donde estan nuestro resultados
	ren "%Link2%%Reg2%" %Inta%CS%%j.txt&:: Cambiamos el nombre del resultado obtenido por [Nombre de instancia][Nombre de Metaheur�stica]j.txt
	del /f /q *.*"%Link%%EBH%%Reg2%"
	)

rd /S /Q %Modificado%&::Elimino la carpeta "Modificado"
rd /S /Q %Modificado2%&::Elimino la carpeta "Modificado2"
rd /S /Q %Original%&::Elimino la carpeta "Original"
mkdir %Modificado%&::Creo la carpeta "Modificado"
mkdir %Modificado2%&::Creo la carpeta "Modificado2"
mkdir %Original%&::Creo la carpeta "Original"
Rem FIN DE EJECUCI�N DE INSTANCIA ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------


Rem INICIO DE EJECUCI�N DE INSTANCIA----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
set Inta=WR-TCV&:: Nombre de la instancia a Ejecutar

set "Instance=%Inta%.sdb"&:: Agragamos la extensi�n ".sdb" a la instancia modificada
set "Instance2=Orig-%Inta%.sdb"&:: Agregamos la extensi�n ".Sdb" a la instancia original
set "Mod=PuenteMod.sdb"&:: Inicializamos la variable Mod, la cual contiene la instancia modificada
set "Orig=PuenteOrig.sdb"&:: Inicializamos la varibale Orig, la cual contiene la instancia original

xcopy %Instancias%%Instance% %Modificado%&:: Copiamos la instancia a la carpeta "Modificado"
ren %Modificado%%Instance% %Mod%&:: Cambiamos el nombre de la instancia a "PuenteMod.sdb"
xcopy %Instancias%%Instance% %Modificado2%&:: Copiamos la instancia a la carpeta "Modificado2"
ren %Modificado2%%Instance% %Mod%&:: Cambiamos le nombre de la instancia a "PuenteMod.sdb"
xcopy %Instancias%%Instance2% %Original%&:: Copiamos la instancia original a la carpeta "Original"
ren %Original%%Instance2% %Orig%&:: Cambiamos el nombre de la instancia a "PuenteOrig.sdb"

Rem Ejecutamos la instancia j veces
for %%j in (1,2) do (
	Rem INSTANCIA CS
	cd %ECS%&:: Nos Posicionamos en la ruta donde esta nuestra metaheur�stica
	Python Main.py&:: Ejecutamos la Metaheur�stica
	xcopy "%Ruta%%Reg2%" "%Link2%"&:: Copiamos el resultado de nuestra ejecuci�n a nuestra carpeta de resultados
	cd "%Link2%"&:: Nos posicionamos en la ruta donde estan nuestro resultados
	ren "%Link2%%Reg2%" %Inta%CS%%j.txt&:: Cambiamos el nombre del resultado obtenido por [Nombre de instancia][Nombre de Metaheur�stica]j.txt
	del /f /q *.*"%Link%%EBH%%Reg2%"
	)

rd /S /Q %Modificado%&::Elimino la carpeta "Modificado"
rd /S /Q %Modificado2%&::Elimino la carpeta "Modificado2"
rd /S /Q %Original%&::Elimino la carpeta "Original"
mkdir %Modificado%&::Creo la carpeta "Modificado"
mkdir %Modificado2%&::Creo la carpeta "Modificado2"
mkdir %Original%&::Creo la carpeta "Original"
Rem FIN DE EJECUCI�N DE INSTANCIA ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------


Rem INICIO DE EJECUCI�N DE INSTANCIA----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
set Inta=VC-TCV&:: Nombre de la instancia a Ejecutar

set "Instance=%Inta%.sdb"&:: Agragamos la extensi�n ".sdb" a la instancia modificada
set "Instance2=Orig-%Inta%.sdb"&:: Agregamos la extensi�n ".Sdb" a la instancia original
set "Mod=PuenteMod.sdb"&:: Inicializamos la variable Mod, la cual contiene la instancia modificada
set "Orig=PuenteOrig.sdb"&:: Inicializamos la varibale Orig, la cual contiene la instancia original

xcopy %Instancias%%Instance% %Modificado%&:: Copiamos la instancia a la carpeta "Modificado"
ren %Modificado%%Instance% %Mod%&:: Cambiamos el nombre de la instancia a "PuenteMod.sdb"
xcopy %Instancias%%Instance% %Modificado2%&:: Copiamos la instancia a la carpeta "Modificado2"
ren %Modificado2%%Instance% %Mod%&:: Cambiamos le nombre de la instancia a "PuenteMod.sdb"
xcopy %Instancias%%Instance2% %Original%&:: Copiamos la instancia original a la carpeta "Original"
ren %Original%%Instance2% %Orig%&:: Cambiamos el nombre de la instancia a "PuenteOrig.sdb"

Rem Ejecutamos la instancia j veces
for %%j in (1,2) do (
	Rem INSTANCIA CS
	cd %ECS%&:: Nos Posicionamos en la ruta donde esta nuestra metaheur�stica
	Python Main.py&:: Ejecutamos la Metaheur�stica
	xcopy "%Ruta%%Reg2%" "%Link2%"&:: Copiamos el resultado de nuestra ejecuci�n a nuestra carpeta de resultados
	cd "%Link2%"&:: Nos posicionamos en la ruta donde estan nuestro resultados
	ren "%Link2%%Reg2%" %Inta%CS%%j.txt&:: Cambiamos el nombre del resultado obtenido por [Nombre de instancia][Nombre de Metaheur�stica]j.txt
	del /f /q *.*"%Link%%EBH%%Reg2%"
	)

rd /S /Q %Modificado%&::Elimino la carpeta "Modificado"
rd /S /Q %Modificado2%&::Elimino la carpeta "Modificado2"
rd /S /Q %Original%&::Elimino la carpeta "Original"
mkdir %Modificado%&::Creo la carpeta "Modificado"
mkdir %Modificado2%&::Creo la carpeta "Modificado2"
mkdir %Original%&::Creo la carpeta "Original"
Rem FIN DE EJECUCI�N DE INSTANCIA ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------


Rem INICIO DE EJECUCI�N DE INSTANCIA----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
set Inta=CC-TCV&:: Nombre de la instancia a Ejecutar

set "Instance=%Inta%.sdb"&:: Agragamos la extensi�n ".sdb" a la instancia modificada
set "Instance2=Orig-%Inta%.sdb"&:: Agregamos la extensi�n ".Sdb" a la instancia original
set "Mod=PuenteMod.sdb"&:: Inicializamos la variable Mod, la cual contiene la instancia modificada
set "Orig=PuenteOrig.sdb"&:: Inicializamos la varibale Orig, la cual contiene la instancia original

xcopy %Instancias%%Instance% %Modificado%&:: Copiamos la instancia a la carpeta "Modificado"
ren %Modificado%%Instance% %Mod%&:: Cambiamos el nombre de la instancia a "PuenteMod.sdb"
xcopy %Instancias%%Instance% %Modificado2%&:: Copiamos la instancia a la carpeta "Modificado2"
ren %Modificado2%%Instance% %Mod%&:: Cambiamos le nombre de la instancia a "PuenteMod.sdb"
xcopy %Instancias%%Instance2% %Original%&:: Copiamos la instancia original a la carpeta "Original"
ren %Original%%Instance2% %Orig%&:: Cambiamos el nombre de la instancia a "PuenteOrig.sdb"

Rem Ejecutamos la instancia j veces
for %%j in (1,2) do (
	Rem INSTANCIA CS
	cd %ECS%&:: Nos Posicionamos en la ruta donde esta nuestra metaheur�stica
	Python Main.py&:: Ejecutamos la Metaheur�stica
	xcopy "%Ruta%%Reg2%" "%Link2%"&:: Copiamos el resultado de nuestra ejecuci�n a nuestra carpeta de resultados
	cd "%Link2%"&:: Nos posicionamos en la ruta donde estan nuestro resultados
	ren "%Link2%%Reg2%" %Inta%CS%%j.txt&:: Cambiamos el nombre del resultado obtenido por [Nombre de instancia][Nombre de Metaheur�stica]j.txt
	del /f /q *.*"%Link%%EBH%%Reg2%"
	)

rd /S /Q %Modificado%&::Elimino la carpeta "Modificado"
rd /S /Q %Modificado2%&::Elimino la carpeta "Modificado2"
rd /S /Q %Original%&::Elimino la carpeta "Original"
mkdir %Modificado%&::Creo la carpeta "Modificado"
mkdir %Modificado2%&::Creo la carpeta "Modificado2"
mkdir %Original%&::Creo la carpeta "Original"
Rem FIN DE EJECUCI�N DE INSTANCIA ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------


Rem INICIO DE EJECUCI�N DE INSTANCIA----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
set Inta=TC-TCV&:: Nombre de la instancia a Ejecutar

set "Instance=%Inta%.sdb"&:: Agragamos la extensi�n ".sdb" a la instancia modificada
set "Instance2=Orig-%Inta%.sdb"&:: Agregamos la extensi�n ".Sdb" a la instancia original
set "Mod=PuenteMod.sdb"&:: Inicializamos la variable Mod, la cual contiene la instancia modificada
set "Orig=PuenteOrig.sdb"&:: Inicializamos la varibale Orig, la cual contiene la instancia original

xcopy %Instancias%%Instance% %Modificado%&:: Copiamos la instancia a la carpeta "Modificado"
ren %Modificado%%Instance% %Mod%&:: Cambiamos el nombre de la instancia a "PuenteMod.sdb"
xcopy %Instancias%%Instance% %Modificado2%&:: Copiamos la instancia a la carpeta "Modificado2"
ren %Modificado2%%Instance% %Mod%&:: Cambiamos le nombre de la instancia a "PuenteMod.sdb"
xcopy %Instancias%%Instance2% %Original%&:: Copiamos la instancia original a la carpeta "Original"
ren %Original%%Instance2% %Orig%&:: Cambiamos el nombre de la instancia a "PuenteOrig.sdb"

Rem Ejecutamos la instancia j veces
for %%j in (1,2) do (
	Rem INSTANCIA CS
	cd %ECS%&:: Nos Posicionamos en la ruta donde esta nuestra metaheur�stica
	Python Main.py&:: Ejecutamos la Metaheur�stica
	xcopy "%Ruta%%Reg2%" "%Link2%"&:: Copiamos el resultado de nuestra ejecuci�n a nuestra carpeta de resultados
	cd "%Link2%"&:: Nos posicionamos en la ruta donde estan nuestro resultados
	ren "%Link2%%Reg2%" %Inta%CS%%j.txt&:: Cambiamos el nombre del resultado obtenido por [Nombre de instancia][Nombre de Metaheur�stica]j.txt
	del /f /q *.*"%Link%%EBH%%Reg2%"
	)

rd /S /Q %Modificado%&::Elimino la carpeta "Modificado"
rd /S /Q %Modificado2%&::Elimino la carpeta "Modificado2"
rd /S /Q %Original%&::Elimino la carpeta "Original"
mkdir %Modificado%&::Creo la carpeta "Modificado"
mkdir %Modificado2%&::Creo la carpeta "Modificado2"
mkdir %Original%&::Creo la carpeta "Original"
Rem FIN DE EJECUCI�N DE INSTANCIA ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------


Rem INICIO DE EJECUCI�N DE INSTANCIA----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
set Inta=RD-AA10&:: Nombre de la instancia a Ejecutar

set "Instance=%Inta%.sdb"&:: Agragamos la extensi�n ".sdb" a la instancia modificada
set "Instance2=Orig-%Inta%.sdb"&:: Agregamos la extensi�n ".Sdb" a la instancia original
set "Mod=PuenteMod.sdb"&:: Inicializamos la variable Mod, la cual contiene la instancia modificada
set "Orig=PuenteOrig.sdb"&:: Inicializamos la varibale Orig, la cual contiene la instancia original

xcopy %Instancias%%Instance% %Modificado%&:: Copiamos la instancia a la carpeta "Modificado"
ren %Modificado%%Instance% %Mod%&:: Cambiamos el nombre de la instancia a "PuenteMod.sdb"
xcopy %Instancias%%Instance% %Modificado2%&:: Copiamos la instancia a la carpeta "Modificado2"
ren %Modificado2%%Instance% %Mod%&:: Cambiamos le nombre de la instancia a "PuenteMod.sdb"
xcopy %Instancias%%Instance2% %Original%&:: Copiamos la instancia original a la carpeta "Original"
ren %Original%%Instance2% %Orig%&:: Cambiamos el nombre de la instancia a "PuenteOrig.sdb"

Rem Ejecutamos la instancia j veces
for %%j in (1,2) do (
	Rem INSTANCIA CS
	cd %ECS%&:: Nos Posicionamos en la ruta donde esta nuestra metaheur�stica
	Python Main.py&:: Ejecutamos la Metaheur�stica
	xcopy "%Ruta%%Reg2%" "%Link2%"&:: Copiamos el resultado de nuestra ejecuci�n a nuestra carpeta de resultados
	cd "%Link2%"&:: Nos posicionamos en la ruta donde estan nuestro resultados
	ren "%Link2%%Reg2%" %Inta%CS%%j.txt&:: Cambiamos el nombre del resultado obtenido por [Nombre de instancia][Nombre de Metaheur�stica]j.txt
	del /f /q *.*"%Link%%EBH%%Reg2%"
	)

rd /S /Q %Modificado%&::Elimino la carpeta "Modificado"
rd /S /Q %Modificado2%&::Elimino la carpeta "Modificado2"
rd /S /Q %Original%&::Elimino la carpeta "Original"
mkdir %Modificado%&::Creo la carpeta "Modificado"
mkdir %Modificado2%&::Creo la carpeta "Modificado2"
mkdir %Original%&::Creo la carpeta "Original"
Rem FIN DE EJECUCI�N DE INSTANCIA ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------


Rem INICIO DE EJECUCI�N DE INSTANCIA----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
set Inta=RC-AA10&:: Nombre de la instancia a Ejecutar

set "Instance=%Inta%.sdb"&:: Agragamos la extensi�n ".sdb" a la instancia modificada
set "Instance2=Orig-%Inta%.sdb"&:: Agregamos la extensi�n ".Sdb" a la instancia original
set "Mod=PuenteMod.sdb"&:: Inicializamos la variable Mod, la cual contiene la instancia modificada
set "Orig=PuenteOrig.sdb"&:: Inicializamos la varibale Orig, la cual contiene la instancia original

xcopy %Instancias%%Instance% %Modificado%&:: Copiamos la instancia a la carpeta "Modificado"
ren %Modificado%%Instance% %Mod%&:: Cambiamos el nombre de la instancia a "PuenteMod.sdb"
xcopy %Instancias%%Instance% %Modificado2%&:: Copiamos la instancia a la carpeta "Modificado2"
ren %Modificado2%%Instance% %Mod%&:: Cambiamos le nombre de la instancia a "PuenteMod.sdb"
xcopy %Instancias%%Instance2% %Original%&:: Copiamos la instancia original a la carpeta "Original"
ren %Original%%Instance2% %Orig%&:: Cambiamos el nombre de la instancia a "PuenteOrig.sdb"

Rem Ejecutamos la instancia j veces
for %%j in (1,2) do (
	Rem INSTANCIA CS
	cd %ECS%&:: Nos Posicionamos en la ruta donde esta nuestra metaheur�stica
	Python Main.py&:: Ejecutamos la Metaheur�stica
	xcopy "%Ruta%%Reg2%" "%Link2%"&:: Copiamos el resultado de nuestra ejecuci�n a nuestra carpeta de resultados
	cd "%Link2%"&:: Nos posicionamos en la ruta donde estan nuestro resultados
	ren "%Link2%%Reg2%" %Inta%CS%%j.txt&:: Cambiamos el nombre del resultado obtenido por [Nombre de instancia][Nombre de Metaheur�stica]j.txt
	del /f /q *.*"%Link%%EBH%%Reg2%"
	)

rd /S /Q %Modificado%&::Elimino la carpeta "Modificado"
rd /S /Q %Modificado2%&::Elimino la carpeta "Modificado2"
rd /S /Q %Original%&::Elimino la carpeta "Original"
mkdir %Modificado%&::Creo la carpeta "Modificado"
mkdir %Modificado2%&::Creo la carpeta "Modificado2"
mkdir %Original%&::Creo la carpeta "Original"
Rem FIN DE EJECUCI�N DE INSTANCIA ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------


Rem INICIO DE EJECUCI�N DE INSTANCIA----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
set Inta=CR-AA10&:: Nombre de la instancia a Ejecutar

set "Instance=%Inta%.sdb"&:: Agragamos la extensi�n ".sdb" a la instancia modificada
set "Instance2=Orig-%Inta%.sdb"&:: Agregamos la extensi�n ".Sdb" a la instancia original
set "Mod=PuenteMod.sdb"&:: Inicializamos la variable Mod, la cual contiene la instancia modificada
set "Orig=PuenteOrig.sdb"&:: Inicializamos la varibale Orig, la cual contiene la instancia original

xcopy %Instancias%%Instance% %Modificado%&:: Copiamos la instancia a la carpeta "Modificado"
ren %Modificado%%Instance% %Mod%&:: Cambiamos el nombre de la instancia a "PuenteMod.sdb"
xcopy %Instancias%%Instance% %Modificado2%&:: Copiamos la instancia a la carpeta "Modificado2"
ren %Modificado2%%Instance% %Mod%&:: Cambiamos le nombre de la instancia a "PuenteMod.sdb"
xcopy %Instancias%%Instance2% %Original%&:: Copiamos la instancia original a la carpeta "Original"
ren %Original%%Instance2% %Orig%&:: Cambiamos el nombre de la instancia a "PuenteOrig.sdb"

Rem Ejecutamos la instancia j veces
for %%j in (1,2) do (
	Rem INSTANCIA CS
	cd %ECS%&:: Nos Posicionamos en la ruta donde esta nuestra metaheur�stica
	Python Main.py&:: Ejecutamos la Metaheur�stica
	xcopy "%Ruta%%Reg2%" "%Link2%"&:: Copiamos el resultado de nuestra ejecuci�n a nuestra carpeta de resultados
	cd "%Link2%"&:: Nos posicionamos en la ruta donde estan nuestro resultados
	ren "%Link2%%Reg2%" %Inta%CS%%j.txt&:: Cambiamos el nombre del resultado obtenido por [Nombre de instancia][Nombre de Metaheur�stica]j.txt
	del /f /q *.*"%Link%%EBH%%Reg2%"
	)

rd /S /Q %Modificado%&::Elimino la carpeta "Modificado"
rd /S /Q %Modificado2%&::Elimino la carpeta "Modificado2"
rd /S /Q %Original%&::Elimino la carpeta "Original"
mkdir %Modificado%&::Creo la carpeta "Modificado"
mkdir %Modificado2%&::Creo la carpeta "Modificado2"
mkdir %Original%&::Creo la carpeta "Original"
Rem FIN DE EJECUCI�N DE INSTANCIA ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------



