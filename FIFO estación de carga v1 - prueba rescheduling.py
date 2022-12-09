#%% solucion inicial
import pandas as pd
from time import time
from statistics import mean
import itertools
import matplotlib.pyplot as plt
import numpy as np

control = time()
#datos de entrada
Instance = pd.read_fwf('inst11.txt', header = None, delim_whitespace = True, skipinitialspace = True )

Hora_entrada = Instance[1]
kw_req = Instance[2]

#datos de cargadores
ratio_carga = [12,15,19] #kw/h
M = 6
ratio_maquina = []
for z in range(0,M):
    if z < 2:
        carga_maq = ratio_carga[0]
        ratio_maquina.append(carga_maq)
    if z < 3 and z > 1:
        carga_maq = ratio_carga[1]
        ratio_maquina.append(carga_maq)
    if z > 2:
        carga_maq = ratio_carga[2]
        ratio_maquina.append(carga_maq)

## datos de estación de carga

precio_carga_por_horas = [4,5,6]
precio_venta = 6.5


#FIFO constructivo
Jobs = list(range(0,len(kw_req)))

Maquinas = list(range(M))
T_acum = [0]*len(Maquinas)
Machines = {Maquinas:T_acum for (Maquinas,T_acum) in zip(Maquinas,T_acum)}

Job_info = {i: {} for i in range(len(kw_req))}
tiempos_inicio = []
t = []

##crear matriz de tiempo de carga
matrix = np.zeros( (len(Jobs),M) )
ma = matrix

for x in Jobs:
    for y in range(0,M):
        matrix[x,y] = kw_req[x]/ratio_maquina[y]
        np.append(ma,matrix[x,y])
    
##asignación de vehículos a cargadores
asignado = []
for job in Jobs:

    first_machine = min(Machines, key = Machines.get)
    start = Machines[first_machine]
    if Hora_entrada[job] < start:
        start = Machines[first_machine] 
        Machines[first_machine] += ma[job,first_machine]
        asignado.append(first_machine)
        t.append(ma[job,first_machine])
        
    else:
        start = Machines[first_machine] + Hora_entrada[job]
        Machines[first_machine] += ma[job,first_machine] + start
        t.append(ma[job,first_machine])
        asignado.append(first_machine)
    Job_info[job] = (first_machine, start)
      
    tiempos_inicio.append(start)

#calculo costos
precio = []

for p in range(0,len(tiempos_inicio)):
    if tiempos_inicio[p] < 5:
        precios = precio_carga_por_horas[0]
        precio.append(precios)
    if tiempos_inicio[p] <= 8 and tiempos_inicio[p] >= 5:
        precios = precio_carga_por_horas[1]
        precio.append(precios)
    if tiempos_inicio[p] >8  :
        precios = precio_carga_por_horas[2]
        precio.append(precios)

costos = precio*kw_req
precios = precio_venta*kw_req

Utilidades = precios - costos

    
lista1 = t
lista2 = tiempos_inicio
lista3 = []

for i in range(len(lista1)):
  lista3.append(lista1[i])

for i in range(len(lista2)):
  lista3[i] = lista3[i] + lista2[i] 

Hora_salida =  lista3

lista4 = t
lista5 = Hora_salida
lista6 = []

for i in range(len(lista4)):
  lista6.append(lista4[i])

for i in range(len(lista5)):
  lista6[i] = lista5[i] - t[i] - Hora_entrada[i]

Hora_espera = lista6
promedio_de_espera = round(mean(Hora_espera),2)

print("secuencia:   ", Jobs)
print("Asignación de maquina:   ", asignado)
print("Hora de entrada:  ", ['%.2f' % elem for elem in list(Hora_entrada)])
print("Carga requerida:  ", ['%.2f' % elem for elem in list(kw_req)])
print("tiempo de inicio: ",['%.2f' % elem for elem in tiempos_inicio])
print("Tiempo de carga:  ",['%.2f' % elem for elem in t])
print("Hora de salida:   ",['%.2f' % elem for elem in Hora_salida])
print("Tiempo de espera: ", ['%.2f' % elem for elem in Hora_espera])
print("Utilidades ($)  : ", ['%.2f' % elem for elem in Utilidades])
print("Promedio de espera: ", promedio_de_espera)
print("Utilidad total ($): ", sum(Utilidades))
times = time() - control
print("El tiempo computacional fue de ", '%.2f' % times, "segundos")

#%% actualizar datos para reprogramacion
TR = 7
mat = [6 for k in Jobs]

ratios = []
for g in range(0,len(asignado)):
    for h in range(0,len(ratio_maquina)):
        if Maquinas[h] == asignado[g]:
            ratios.append(ratio_maquina[h])

enproceso = []
kw_fal = []
for r in range(0,len(Jobs)):
    if tiempos_inicio[r]<TR and Hora_salida[r]>TR:
        enproceso.append(Jobs[r])
        kw_fal.append((t[r]+tiempos_inicio[r]-mat[r])*ratios[r])
    else:
        if tiempos_inicio[r] > TR:
            kw_fal.append(kw_req[r])
        else:
            kw_fal.append(0)

nueva_data = pd.DataFrame(kw_fal,Jobs)

para_programar = []
nueva_hora = []
for y in range(0,len(nueva_data)):
    if kw_fal[y] > 0:
        para_programar.append(kw_fal[y])
        nueva_hora.append(Hora_entrada[y])
    for z in range(0,len(nueva_hora)):
        if nueva_hora[z] < TR:
            nueva_hora[z] = 6

Jobs = list(range(0,len(para_programar)))
print(len(Jobs))            
#%% Tabu
tenure = 5
k = 0
tabu = []
Jobss = Jobs
solution = Jobss
secuencia = 0
Utilidades = 0
promedio_espera = 1000
grupo = []
promedio = []
control = time()
#datos de entrada
for k in range(0,1000):
    
    
    solution = solution.copy()
    # job index in the solution:
    for i in range(0,len(Jobs)-2):
        if Hora_entrada[i] == Hora_entrada[i+1]:
            i_index = solution.index(i)
            j_index = solution.index(i+1)
        #Swap
            solution[i_index], solution[j_index] = solution[j_index], solution[i_index]
        
         
            for t in range(0,len(tabu)):
                if (i_index,j_index) == tabu[t] or (j_index,i_index) == tabu[t]:
                    for i in range(0,len(Jobs)-2):
                        if Hora_entrada[i] == Hora_entrada[i+1]:
                            i_index = solution.index(i)
                            j_index = solution.index(i+1)
                            #Swap
                            solution[i_index], solution[j_index] = solution[j_index], solution[i_index]
                else:
                    solution = solution
    
   
    Hora_entrada = nueva_hora
    kw_req = para_programar
   
    #datos de cargadores
    ratio_carga = [12,15,19] #kw/h
    M = 6
    ratio_maquina = []
    for z in range(0,M):
        if z < 2:
            carga_maq = ratio_carga[0]
            ratio_maquina.append(carga_maq)
        if z < 3 and z > 1:
            carga_maq = ratio_carga[1]
            ratio_maquina.append(carga_maq)
        if z > 2:
            carga_maq = ratio_carga[2]
            ratio_maquina.append(carga_maq)
   
    ## datos de estación de carga
    transformador = 120 #kWh
    precio_carga_por_horas = [4,5,6]
    precio_venta = 6.5               
    #FIFO constructivo
    Jobss = solution

    Maquinas = list(range(M))
    T_acum = [0]*len(Maquinas)
    Machines = {Maquinas:T_acum for (Maquinas,T_acum) in zip(Maquinas,T_acum)}

    Job_infoss = {i: {} for i in range(len(kw_req))}
    tiempos_inicio = []
    t = []

    ##crear matriz de tiempo de carga
    matrix = np.zeros( (len(Jobss),M) )
    ma = matrix

    for x in Jobss:
        for y in range(0,M):
            matrix[x,y] = kw_req[x]/ratio_maquina[y]
            np.append(ma,matrix[x,y])
        
    ##asignación de vehículos a cargadores
    asignado = []
    for job in Jobss:

        first_machine = min(Machines, key = Machines.get)
        start = Machines[first_machine]
        if Hora_entrada[job] < start:
            start = Machines[first_machine] 
            Machines[first_machine] += ma[job,first_machine]
            asignado.append(first_machine)
            t.append(ma[job,first_machine])
            
        else:
            start = Machines[first_machine] + Hora_entrada[job]
            Machines[first_machine] += ma[job,first_machine] + start
            t.append(ma[job,first_machine])
            asignado.append(first_machine)
        Job_infoss[job] = (first_machine, start)
          
        tiempos_inicio.append(start)

    #calculo costos
    precio = []
    costos = []
    for p in range(0,len(tiempos_inicio)):
        if tiempos_inicio[p] < 5:
            precios = precio_carga_por_horas[0]
            precio.append(precios)
        if tiempos_inicio[p] <= 8 and tiempos_inicio[p] >= 5:
            precios = precio_carga_por_horas[1]
            precio.append(precios)
        if tiempos_inicio[p] >8  :
            precios = precio_carga_por_horas[2]
            precio.append(precios)

        costos.append(precio[p]*kw_req[p])
        precios = precio_venta*sum(kw_req)

    nuevaUtilidades = precios - sum(costos)
    
    
           
        
    lista1 = t
    lista2 = tiempos_inicio
    lista3 = []
    
    for i in range(len(lista1)):
      lista3.append(lista1[i])
    
    for i in range(len(lista2)):
      lista3[i] = lista3[i] + lista2[i] 
    
    Hora_salida =  lista3
    
    lista4 = t
    lista5 = Hora_salida
    lista6 = []
    
    for i in range(len(lista4)):
      lista6.append(lista4[i])
    
    for i in range(len(lista5)):
      lista6[i] = lista5[i] - t[i] - Hora_entrada[i]
    
    Hora_espera = lista6
    promedio_de_espera = round(mean(Hora_espera),2)
    
    
    if len(tabu) == tenure:
        tabu.remove(tabu[0])
        cambio = (i_index,j_index)
        tabu.append(cambio)
    else:
        cambio = (i_index,j_index)
        tabu.append(cambio)
    
    if promedio_de_espera < promedio_espera and nuevaUtilidades > Utilidades:
        secuencia = solution
        Jobss = secuencia
        print(secuencia)
        promedio_espera = promedio_de_espera
        Utilidades = nuevaUtilidades
        grupo.append(secuencia)
        promedio.append(promedio_de_espera)
    else:
        secuencia = Jobs
        Jobss = secuencia
        Utilidades = Utilidades
        grupo.append(Jobss)
        promedio.append(promedio_de_espera)
                          
    k = k +1                        
    times = time() - control
    
 #%%   
    print("secuencia optima:   ", secuencia)
    print("Hora de entrada:  ", ['%.2f' % elem for elem in list(Hora_entrada)])
    print("tiempo de inicio: ", ['%.2f' % elem for elem in tiempos_inicio])
    print("Tiempo de carga:  ",['%.2f' % elem for elem in t])
    print("Hora de salida:   ",['%.2f' % elem for elem in Hora_salida])
    print("Tiempo de espera: ", ['%.2f' % elem for elem in Hora_espera])
    print("Promedio de espera: ", promedio_de_espera)
    print("Utilidades: ",nuevaUtilidades)
    print("El tiempo computacional fue de ", '%.2f' % times, "segundos")
    



