#%% solucion inicial
import pandas as pd
from time import time
from statistics import mean
import itertools
import matplotlib.pyplot as plt

control = time()
#datos de entrada
Instance = pd.read_fwf('inst01.txt', header = None, delim_whitespace = True, skipinitialspace = True )

Hora_entrada = [0]*len(Instance[1])
kw_req = Instance[2]

#datos de cargadores
ratio_carga = 10 #kw/h
M = 3

#FIFO constructivo
t = list(map(lambda x: x / ratio_carga, kw_req))
Jobs = list(range(0,len(t)))

Maquinas = list(range(M))
T_acum = [0]*len(Maquinas)
Machines = {Maquinas:T_acum for (Maquinas,T_acum) in zip(Maquinas,T_acum)}

Job_info = {i: {} for i in range(len(t))}
tiempos_inicio = []

for job in Jobs:

    first_machine = min(Machines, key = Machines.get)
    start = Machines[first_machine]
    Machines[first_machine] += t[job]
    
        
    Job_info[job] = (first_machine, start)

       
    tiempos_inicio.append(start)
    
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
print("Hora de entrada:  ", ['%.2f' % elem for elem in list(Hora_entrada)])
print("tiempo de inicio:  ",['%.2f' % elem for elem in tiempos_inicio])
print("Tiempo de carga:  ",['%.2f' % elem for elem in t])
print("Hora de salida:   ",['%.2f' % elem for elem in Hora_salida])
print("Tiempo de espera: ", ['%.2f' % elem for elem in Hora_espera])
print("Promedio de espera: ", promedio_de_espera)
times = time() - control
print("El tiempo computacional fue de ", '%.2f' % times, "segundos")

#%% Tabu papi
tenure = 5 
k = 0
tabu = []
solution = Jobs
secuencia = 0
grupo = []
promedio = []
for k in range(0,1000):
    
    solution = solution.copy()
    # job index in the solution:
    for i in range(0,len(Jobs)-2):
            i_index = solution.index(i)
            j_index = solution.index(i+1)
    #Swap
            solution[i_index], solution[j_index] = solution[j_index], solution[i_index]
    
     
            for t in range(0,len(tabu)):
                if (i_index,j_index) == (j_index,i_index) == tabu[t]:
                    for i in range(0,len(Jobs)-2):
                            i_index = solution.index(i)
                            j_index = solution.index(i+1)
                    #Swap
                            solution[i_index], solution[j_index] = solution[j_index], solution[i_index]
                   
    control = time()
    #datos de entrada
    Instance = pd.read_fwf('inst01.txt', header = None, delim_whitespace = True, skipinitialspace = True )
    
    Hora_entrada = [0]*len(Instance[1])
    kw_req = Instance[2]
    
    #datos de cargadores
    ratio_carga = 10 #kw/h
    M = 3
    
    #FIFO constructivo
    t = list(map(lambda x: x / ratio_carga, kw_req))
    Jobss = solution
    
    Maquinas = list(range(M))
    T_acum = [0]*len(Maquinas)
    Machines = {Maquinas:T_acum for (Maquinas,T_acum) in zip(Maquinas,T_acum)}
    
    Job_infoss = {i: {} for i in range(len(t))}
    tiempos_inicio = []
    
    for job in Jobss:
    
        first_machine = min(Machines, key = Machines.get)
        start = Machines[first_machine]
        Machines[first_machine] += t[job]
        
            
        Job_infoss[job] = (first_machine, start)
    
           
        tiempos_inicio.append(start)
        
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
    promedio_de_espera_new = round(mean(Hora_espera),2)
    
    if len(tabu) == tenure:
        tabu.remove(tabu[0])
        cambio = (i_index,j_index)
        tabu.append(cambio)
    else:
        cambio = (i_index,j_index)
        tabu.append(cambio)
    
    if promedio_de_espera_new < promedio_de_espera:
        secuencia = solution
        Jobss = secuencia
        print(secuencia)
        promedio_de_espera = promedio_de_espera_new
        grupo.append(secuencia)
        promedio.append(promedio_de_espera_new)
    else:
        Jobss = solution
        grupo.append(Jobss)
        promedio.append(promedio_de_espera_new)
                          
    k = k +1                        
    times = time() - control
    
 #%%   
    print("secuencia optima:   ", secuencia)
    print("Hora de entrada:  ", ['%.2f' % elem for elem in list(Hora_entrada)])
    print("tiempo de inicio:  ", ['%.2f' % elem for elem in tiempos_inicio])
    print("Tiempo de carga:  ",['%.2f' % elem for elem in t])
    print("Hora de salida:   ",['%.2f' % elem for elem in Hora_salida])
    print("Tiempo de espera: ", ['%.2f' % elem for elem in Hora_espera])
    print("Promedio de espera: ", promedio_de_espera)
    print("El tiempo computacional fue de ", '%.2f' % times, "segundos")
        
    
    print(tabu)
