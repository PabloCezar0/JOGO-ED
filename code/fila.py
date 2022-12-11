class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Queue:
    
    def __init__(self):
        
        self.head = None
        self.tail = None

    def enqueue(self, data):


        if self.head is None:
            self.head = Node(data)
        if self.tail is None:
            self.tail = Node(data)
        else:
            self.tail.next = Node(data)
            self.tail = Node(data)


    def dequeue(self):
        if self.head is None:
            print("Fila vazia!")
            return
        else:
            aux = self.head.data
            self.head = self.head.next
            return aux

    def __str__(self):
        return self.__repr__()

    def __repr__(self) -> str:
        prim = ''
        aux = self.head
        while aux:
            prim += str(aux.data.name) + '-> '
            aux = aux.next
        return prim