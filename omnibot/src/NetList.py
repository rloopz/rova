import collections

class Nodo(object):
    def __init__(self,num,n1,n2,value,point,visible,address):
        self.num=num
        self.n1=n1
        self.n2=n2
        self.value=value
        self.point=point
        self.visible=visible
        self.address=address

    def __repr__(self):
        return '{}: {} {} {} {} {} {} {}'.format(self.__class__.__name__,self.num,self.n1,self.n2,self.value,self.point,self.visible,self.address)

    def __cmp__(self, other):
        if hasattr(other, 'getKey'):
            return self.getKey().__cmp__(other.getKey())
    def getKey(self):
        return self.n1

class Netlist():
    def __init__(self):
        self.lista=collections.OrderedDict()

    def insert(self,num,n1,n2,value,point,visible,address):
        for i in range(2):
            try:
                items=self.lista[str(n1)]
                items.append(Nodo(num,n1,n2,value,point,visible,address))
                self.lista[str(n1)]=items
            except KeyError:
                items = list()
                items.append(Nodo(num,n1,n2,value,point,visible,address))
                self.lista[str(n1)] = items
            aux=n2
            n2=n1
            n1=aux
            num=0
            address=self.changeAddres(address)
    def changeAddres(self,dir):
        if dir=='r':
            return 'l'
        return 'b'
    def getKeys(self):
        return self.lista.keys()
    def get(self,key):
        try:
            return self.lista[key]
        except KeyError:
            return None
    def getNodo(self,key,value):
        try:
            for item in self.lista[str(key)]:
                if item.n2==value:
                    return item
        except KeyError:
            return None
    def getAddress(self,nodoOrigen,nodoDestino):
        for item in self.lista[str(nodoOrigen)]:
            if item.n2 == nodoDestino:
                return item.address
    def display(self):
        for key in self.lista:
            print(self.lista[key])

