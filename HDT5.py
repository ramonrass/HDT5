# Universidad del Valle de Guatemala
# Algoritmos y Estructura de Datos
# HDT 5
# 31 de Agosto de 2016
# Ramon Samayoa     15497
# Realizado a partir de ejemplos en clase
 
# Se importan los modulos necesarios
import simpy
import random
 

def proceso(env, tiempro, nom, ram, cantRam, Num_Ins, speed):
 
    # Variables para calcular y guardar la cantidad de tiempo que llevo cada proceso
    global t_tot
    global tiemp
 
    #--------------------------------------ETAPA NEW--------------------------------------
    # El proceso llega al sistema operativo pero debe esperar que se le asigne memoria RAM
    yield env.timeout(tiempro)
    print('%s. Solicita %d de RAM (New)' % ( nom, cantRam))
    # Se guarda el tiempo en el que llego
    tiemp_llegada = env.now
    
    #--------------------------------------ETAPA READY------------------------------------
    # Se solicita la RAM
    yield ram.get(cantRam)
    print('%s. Solicitud aceptada por %d de RAM (Admited)' % ( nom, cantRam))
 
    # En esta variable se almacenara el numero de instrucciones finalizadas
    Ins_Finish = 0
    
    while Ins_Finish < Num_Ins:
        # Conexion con el resocurce CPU
        with cpu.request() as req:
            yield req
            # Instruccion a realizarse
            if (Num_Ins - Ins_Finish) >= speed:
                efec = speed
            else:
                efec = (Num_Ins - Ins_Finish)
 
            print('%s. CPU ejecutara %d instrucciones. (Ready)' % (nom, efec))
            # Tiempo de instrucciones a ejecutar
            yield env.timeout(efec/speed)   
 
            # Numero total de intrucciones terminadas
            Ins_Finish += efec
            print('%s. CPU (%d/%d) completado. (Running)' % ( nom, Ins_Finish, Num_Ins))
 
        # Si la decision es 1 wait, si es 2 procedemos a ready
        desicion = random.randint(1,2)
 
        if desicion == 1 and Ins_Finish < Num_Ins:
            #----------------------------------ETAPA WAITING-------------------------------
            with wait.request() as req2:
                yield req2
                yield env.timeout(1)                
                print('%s. Realizadas operaciones de entrada/salida. (Waiting)' % ( nom))
    
 
    #------------------------------------ETAPA TERMINATED----------------------------------
    # Cantidad de RAM devuelta al SO
    yield ram.put(cantRam)
    print('%s. Retorna %d de RAM. (Terminated)' % (nom, cantRam))
    # Total de tiempo que llevo el proceso
    t_tot += (env.now - tiemp_llegada)
    # Se guarda tiempo en el Array
    tiemp.append(env.now - tiemp_llegada) 
 
 
#-----------------------------------DEFINICION DE VARIABLES---------------------------------

speed = 6.0         # Velocidad del Procesador
Mem_RAM = 100       # Cantidad de Memoria RAM
Num_Pro = 200       # Numero de procesos a Realizar
t_tot = 0.0         # Variable para el tiempo total de un proceso
tiemp=[]            # Array de los Tiempos 
 
 
#------------------------------------AMBIENTES DE SIMULACION---------------------------------

env = simpy.Environment()
# Cola de tipo Resource para el CPU 
cpu = simpy.Resource (env, capacity=1)
# Cola de tipo Container para la RAM
ram = simpy.Container(env, init = Mem_RAM, capacity = Mem_RAM)
# Cola de tipo Resource Wait para operaciones I/O
wait = simpy.Resource (env, capacity=2) 
 
# Semilla del random
n_intervalo = 10 # Numero de intervalos
random.seed(5555)


# Creacion de los procesos a utilizar
for i in range(Num_Pro):
    tiepro = random.expovariate(1.0 / n_intervalo)
    #Se genera un numero de instrucciones aleatorio
    Num_Ins = random.randint(1,10)
    #Se genera una cantidad de memoria RAM aleatoria
    cantRam = random.randint(1,10) 
    env.process(proceso(env, tiepro, 'Proceso %d' % i, ram, cantRam, Num_Ins, speed))
 
# Se corre la simulacion
env.run()

print
# SE CALCULA TIEMPO PROMEDIO
prom = (t_tot/Num_Pro)
# Imprime el resultado
print "El tiempo promedio de los procesos es: ",prom," segundos"
 

print
# SE CALCULA LA DEENVIACION ESTANDAR
suma = 0
for i in tiemp:
    suma += (i - prom)**2
 
desviacion = (suma/(Num_Pro-1))**0.5
# Imprime el resultado
print "La desviacion estandar de los tiempos es: ",desviacion," segundos"
