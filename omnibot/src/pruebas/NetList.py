#!/usr/bin/env python3
import collections

class Nodo(object):
	def __init__(self,num,n1,n2,value,point,visible):
		self.num=num
		self.n1=n1
		self.n2=n2
		self.value=value
		self.point=point
		self.visible=visible
	
	def __repr__(self):
		return '{}: {}, n1->{}, n2->{}, value->{}, position->{}, visible->{} '.format(self._class_._name_,self.num,self.n1,self.value,self.point,self.visible)
	
	def __cmp__(self, other):
		if hasattr(other, 'getKey'):
			return self.getKey()._cmp_(other.getKey())
	
	def __getKey__(self):
		return self.n1
		
class Netlist():
	def __init__(self):
		self.lista=dict()
		
	def insert(self, item):
		try:
			items=self.lista[str(item.n1)]
			items.append(item)
			self.lista[str(item.n1)]=items
		except KeyError:
			items = list()
			items.append(item)
			self.lista[str(item.n1)] = items
		
	def getKeys(self):
		return self.lista.keys()
	def get(self,key):
		try:
			return self.lista[str(key)]
		except KeyError:
			return None
				
	def display(self):
		for key in self.lista:
			print (self.lista[key])
			
			
			

