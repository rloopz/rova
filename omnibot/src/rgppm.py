#!/usr/bin/env python3
from NetList import *
import scipy.sparse as sps
import scipy.sparse.linalg.dsolve as dsl
import numpy as np
from time import time
import warnings
#from bluepy import btle
import socket
import serial
import rospy
from std_msgs.msg import String



#wifi module wx esp8266 
'''
No se cuenta con manejo de excepciones de error. 
'''
nodoInicio = None
nodoFinal= None

def callback(data):
    global nodoInicio, nodoFinal
    nodo = int(data.data)
    if nodoInicio is None:
        nodoInicio = nodo
        rospy.loginfo("nodoInicio: %d", nodoInicio)
    elif nodoFinal is None:
        nodoFinal = nodo
        rospy.loginfo("nodoFinal: %d", nodoFinal)
        CN(nodoInicio,nodoFinal)
    else:
        rospy.loginfo("Ya se recibieron los dos nodos")
    

def CN(nodoInicio, nodoFinal):
    warnings.simplefilter("ignore")
   # cuadrado = int(input("ingrese numero de figuras:"))
    cuadrado = 5
    num, n = 1, 1
  
    '''
    Variables de la comunicacion
    '''
    #addr = '00:13:EF:00:D1:A0'  #rssi: -46dBm
    #port = 1   
    #dev = btle.Peripheral(addr, btle.ADDR_TYPE_PUBLIC)  
    salida = []
   
    '''
    Se muestra el rango aceptable de nodo inicio y final
    '''

    '''
    se pide el numero de figuras version sin  vista grafica
    '''

    tiempo_ini = time()
    nodosLado = cuadrado + 1
    valorFuenteinicio = 100
    valorFuentefinal = 0
    nodosTotales = nodosLado * nodosLado
    orden = nodosTotales + 2
    longitudTotal = []
    ruta = []
    nodosReferencia = []

    nodos = Netlist()
    print("Rango de valores aceptables como nodo incio y final son (1,"+str(nodosTotales)+"):")
    #nodoInicio = int(input("Ingrese nodo inicio:"))
    #nodoFinal = int(input("Ingrese nodo final:"))
    
    nodoFlotante = nodoInicio




    '''
    creacion de tablas para las soluciones
    '''
    a = sps.csc_matrix((orden, orden), dtype=np.int8)
    b = np.zeros(orden)

    '''
    inicio de la lista de resistencias
    '''
    tiempo_iniList = time()
    for j in range(nodosLado):
        for i in range(nodosLado):
            if (i + 1) < nodosLado:
                nodos.insert(num, n, (n + 1), 1, 0, False, 'r')
                num += 1

            if (j + 1) < nodosLado:
                nodos.insert(num, n, (n + nodosLado), 1, 0, False, 'f')
                num += 1

            n += 1
    tiempo_finList = time()



    tiempo_inimatriz = time()
    for item in nodos.getKeys():
        for nodo in nodos.get(item):
            if not nodo.visible and nodo.num != 0:
                a[(nodo.n1-1),(nodo.n1-1)]+=(1/nodo.value)
                a[(nodo.n2 - 1), (nodo.n2 - 1)] += (1 / nodo.value)
                a[(nodo.n1 - 1), (nodo.n2 - 1)] -=(1 / nodo.value)
                a[(nodo.n2 - 1), (nodo.n1 - 1)] -= (1 / nodo.value)

    a[nodoInicio-1, nodosTotales] += 1.0
    a[nodosTotales, nodoInicio-1] += 1.0
    a[nodoFinal-1, nodosTotales + 1] += 1.0
    a[nodosTotales + 1, nodoFinal-1] += 1.0


    b[nodosTotales] += valorFuenteinicio
    b[nodosTotales + 1] += valorFuentefinal
    tiempo_finmatriz = time()


    tiempo_inisolu = time()
    x = dsl.spsolve(a, b,use_umfpack=True)
    tiempo_finsolu = time()

    del a
    del b
    print("SOLUCION MATRIZ \n")
    print(str(x) + "\n")

    tiempo_inruta = time()

    try:
        while nodoFlotante != nodoFinal:  # ciclo hasta que el nodo flotante sea igual al nodo final
            resistenciasDinamicas = []
            nodosDinamicos = []
            corrientesParaMax = []
            vcont = 0  # se busca la posicion de el nodo flotante esto devuelve la ultima posicion conocida de el nodo a buscar
            for item in nodos.get(str(nodoFlotante)):  # se obtiene los elemntos del nodo flotante de la netlist y se iteran
                if not item.visible:  # se comprueba que la resistencia sea permitida
                    resistenciasDinamicas.append([item.num, item.value])
                    nodosDinamicos.append(item.n2)
                    valor = float((x[(nodoFlotante) - 1] - x[nodosDinamicos[vcont] - 1]))
                    valor = str(valor / resistenciasDinamicas[vcont][1])
                    corrientesParaMax.append(float(valor))
                    vcont += 1
            #print(nodosDinamicos)
            #print(corrientesParaMax)
            nodosReferencia.append(nodoFlotante)
            n2 = corrientesParaMax.index(max(corrientesParaMax))
            ruta.append(resistenciasDinamicas[n2][0])
            longitudTotal.append(resistenciasDinamicas[n2][1])
            nodoFlotante = nodosDinamicos[n2]
            #print(nodoFlotante)

    except ValueError:
        print("perdida de ruta, por obstaculo")
    nodosReferencia.append(nodoFinal)
    tiempo_fruta = time()
    tiempo_final = time()
    print("Ruta")
    print(str(ruta) + "\n")
    print("Nodos referencia")
    print(str(nodosReferencia)+"\n")
    print("La longitud total es:" + str(sum(longitudTotal)) + "\n")
    print("El tiempo de lista fue:" + str(tiempo_finList - tiempo_iniList) + "\n")  # En segundos
    print("El tiempo de matriz fue:" + str(tiempo_finmatriz - tiempo_inimatriz) + "\n")  # En segundos
    print("El tiempo de solucion fue:" + str(tiempo_finsolu - tiempo_inisolu) + "\n")  # En segundos
    print("El tiempo de ruta fue:" + str(tiempo_fruta - tiempo_inruta) + "\n")  # En segundos
    print("El tiempo de ejecucion fue:" + str(tiempo_final - tiempo_ini))  # En segundos
    
    
    print("Direcciones:")
    for i in range(len(nodosReferencia)-1):
        n1=nodosReferencia[i]
        n2=nodosReferencia[i+1]
        dir=nodos.getAddress(n1,n2)
        print("De nodo: "+str(n1)+" a nodo:"+str(n2)+" direccion:"+str(dir))
        salida.append(dir)
    send = ','.join(salida)
    print (send)
    #Enviar por bluetooth
    # char = dev.getCharacteristics(uuid=0x0003)[0]
    #char.write(send.encode())
    #dev.disconnect()
    cmd_vel_pub = rospy.Publisher('movee', String, queue_size=1)
    cmd_vel_pub.publish(send)
    rospy.sleep(1.0)
    
    #ENVIO POR WIFI AL MODULO ESP 8266
    esp_ip = "192.168.1.105"  # Dirección IP del ESP8266
    esp_port = 80  # Puerto del servidor web del ESP8266
      
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crea un socket 
    sock.connect((esp_ip, esp_port)) # Establece la conexión con el ESP8266

    # Envía los datos al ESP8266 y cierra la conexión
    #datos= "hey!"
 
    for m in range(len(salida)):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((esp_ip, esp_port))
        sock.sendall(salida[m].encode())
        sock.close()	
    
    

def loadNodosEliminados():
    file=open("eliminados30.txt")
    lista=[int(i) for i in file.readlines()]
    return lista
    
def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("node_number", String, callback)
    rospy.spin()

if __name__ == '__main__':  
        listener()  
        CN()

   
