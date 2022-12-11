class Node:
    def __init__(self, dado):
        self.dado = dado
        self.prox = None

class Fila:
    def __init__(self):
        self.head = None
        self.tail = None

    def enqueue(self, dado):
        no = Node(dado)

        if self.head is None:
            self.head = no
        if self.tail is None:
            self.tail = no
        else:
            self.tail.prox = no
            self.tail = no
            

    def dequeue(self):
        if self.head is None:
            print("Fila vazia!")
            return
        else:
            aux = self.head.dado
            self.head = self.head.prox
            return aux
    
    def __str__(self):
        return self.__repr__()

    def __repr__(self) -> str:
        prim = ''
        aux = self.head
        while aux:
            prim += str(aux.dado) + '-> '
            aux = aux.prox
        return prim