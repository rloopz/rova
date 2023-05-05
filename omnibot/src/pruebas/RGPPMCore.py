#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from NetList import *

#import pysparse.direct.umfpack as up
#import pysparse.sparse.pysparseMatrix as ps

#import pysparse.umfpack as up
#import pysparse.sparse.pysparseMatrix as ps

import scipy.sparse as sp
import scipy.sparse.linalg as spla


import numpy as np
import serial
from time import time

#ser1 = serial.Serial('/dev/ttyACM0', 9600)

#ser1 = serial.Serial("/dev/ttyACM0") #USB
#ser1.baudrate=9600

def CN():
	num, n = 1, 1
	nodop = list()	
	tiempo_ini = time()
	nodosLado = 5
	valorFuenteinicio = 100
	valorFuentefinal = 0
	nodoInicio = input("ingrese nodo inicial:")
	nodoFinal = input("ingrese nodo final:")
	orden = (nodosLado*nodosLado)+2
	nodosTotales = nodosLado*nodosLado
	nodoFlotante = nodoInicio
	
	longitudTotal = []
	ruta = []
	nodosReferencia = []
	
	vs = True
	nodos = Netlist()
	
	#TABLAS
	#a = ps.spmatrix.ll_mat(orden, orden)	 
	a = sp.lil_matrix((orden,orden))
	
	#a = sp.csc_matrix((orden, orden), dtype=float)	
	#a = sp.csr_matrix((orden, orden))
	#dense = a.toarray() #vector de densidad
	
	#a = [[0 for _ in range(orden)] for _ in range(orden)]
	
	
	# create dense vectors
	#b = np.array([1, 2, 3])
	
	b = np.zeros(orden)
	x = np.zeros(orden)
	
	
	tiempo_iniList = time()
	for j in range(nodosLado):
		for i in range(nodosLado):
			if (i + 1) < nodosLado:
				if not n in nodop:
					if not (n+1) in nodop:
						nodos.insert(Nodo(num, n, (n + 1), 1, [0, 0], False))
					else:
						nodos.insert(Nodo(num, n, (n + 1), 1, [0, 0], True))
				else:
					nodos.insert(Nodo(num, n, (n + 1), 1, [0, 0], True))
					vs = False
				num += 1
			
			if (j + 1) < nodosLado:
				if vs:
					if not (n + nodosLado) in nodop:
						nodos.insert(Nodo(num, n, (n + nodosLado), 1, [0, 0], False))
					else:
						nodos.insert(Nodo(num, n, (n + nodosLado), 1, [0, 0], True))
				else:
					nodos.insert(Nodo(num, n, (n + nodosLado), 1, [0, 0], True))
				num += 1
			vs = True
			n += 1
	tiempo_finList = time()
	
	
	#a[int(nodoInicio)-1,int(nodosTotales)] += 1.0
	#a[int(nodosTotales), int(nodoInicio)-1] += 1.0
	#a[int(nodoFinal) - 1, int(nodosTotales) + 1] += 1.0
	#a[int(nodosTotales) + 1,int(nodoFinal) - 1] += 1.0  este bloque va abajo entre las a[ y las de abajo
	tiempo_inimatriz = time()
	for item in nodos.getKeys():
		for nodo in nodos.get(item):
			if not nodo.visible:
				a[(nodo.n1-1),(nodo.n1-1)]+=(1 / nodo.value)
				a[(nodo.n2 - 1), (nodo.n2 - 1)] -=(1 / nodo.value)
				a[(nodo.n1 - 1), (nodo.n2 - 1)] -=(1 / nodo.value)
				a[(nodo.n2 - 1), (nodo.n1 - 1)] -=(1 / nodo.value)
			
	
	a[int(nodoInicio)-1,nodosTotales] += 1.0
	a[nodosTotales, int(nodoInicio)-1] += 1.0
	a[int(nodoFinal) - 1, nodosTotales + 1] += 1.0
	a[nodosTotales + 1,int(nodoFinal) - 1] += 1.0
	
	
	b[nodosTotales] += valorFuenteinicio
	b[nodosTotales + 1] += valorFuentefinal
	tiempo_finmatriz = time()
	
	
	
	tiempo_inisolu = time()
	#LU = up.factorize(a, strategy="UMFPACK_STRATEGY_AUTO") 
	# Factorize the sparse matrix
	#LU = spla.splu(a, permc_spec="NATURAL")
	#a = a.tocsc()
	#LU = spla.splu(a)
	#LU = spla.spsolve(a,dense)
	#LU = spla.splu(a, permc_spec='MMD_AT_PLUS_A')
	#Q, R = np.linalg.qr(a.todense())
	#y = Q.T @ b
	#x = np.linalg.solve(R, y.reshape(-1, 1))
	#tiempo_finsolu = time()
	#LU.solve(b, x)
	#x = LU.solve(b)
	
	x = spla.spsolve(a, b)

	
	del a
	del b
	
	print ("SOLUCION MATRIZ \n")
	print (str(x) + "\n")
	
	tiempo_inruta = time()
	while nodoFlotante != nodoFinal:
		resistenciasDinamicas = []
		nodosDinamicos = []
		corrientesParaMax = []
		vcont = 0
		for item in nodos.get(nodoFlotante):
			if not item.visible:
				resistenciasDinamicas.append([item.num, item.value])
				nodosDinamicos.append(item.n2)
				valor=float((x[(int(nodoFlotante))-1] - x[nodosDinamicos[vcont] - 1])) #agregue un parentesis de int(nodoFlotante)
				valor=str(valor/ resistenciasDinamicas[vcont][1])
				corrientesParaMax.append(float(valor))
				vcont += 1
				
		nodosReferencia.append(nodoFlotante)
		n2 = corrientesParaMax.index(max(corrientesParaMax))
		ruta.append(resistenciasDinamicas[n2][0])
		longitudTotal.append(resistenciasDinamicas[n2][1])
		nodoFlotante = nodosDinamicos[n2]
	tiempo_fruta = time()
	del x
	del nodosDinamicos
	del resistenciasDinamicas
	nodosReferencia.append(nodoFinal)
	tiempo_final = time()
	
	print ("Ruta")
	print (str(ruta) + "\n")
	print ("Nodos Referencia")
	print (str(nodosReferencia) + "\n")
	print ("La longitud total es: " + str(sum(longitudTotal)) + "\n")
	print ("El tiempo de lista fue: " + str(tiempo_finList - tiempo_iniList) + "\n") #En segundos
	print ("El tiempo de matriz fue: " + str(tiempo_finmatriz - tiempo_inimatriz) + "\n") #En segundos
	print ("El tiempo de solucion fue: " + str(tiempo_finsolu - tiempo_inisolu) + "\n") #En segundos
	print ("El tiempo de ruta fue: " + str(tiempo_fruta - tiempo_inruta) + "\n") #En segundos
	print ("El tiempo de ejecucion fue: " + str(tiempo_final - tiempo_ini) + "\n") #En segundos
	
	
	ino=[]
	it=0
	ts=0
	for snd1 in nodosReferencia:
		if snd1 < nodoFinal:
			ts =it+1
			res = nodosReferencia[ts]-snd1
			if res == 1:
				ino.append('w')	
			elif res > 1:
				ino.append('a')	
			elif res < 1:
				ino.append('d')	
			elif res == -1:
				ino.append('x')	
			it += 1
		
	str1= ''.join(ino)
	ser1=write(str1)
	print (str(ino))
	ser1.close()

def loadNodosEliminados(path):
	file=open(path)
	lista=[int(1) for i in file.readlines()]
	return lista

if __name__ == '__main__':
	CN() 
