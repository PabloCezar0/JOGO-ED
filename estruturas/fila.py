class Character():
    def __init__(self, nome):
        self.nome = nome

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Queue:
    def __init__(self):
        self.head = None
        self.tail = None

    def enqueue(self, data):
        newNode = Node(data)

        if self.head is None:
            self.head = newNode
        if self.tail is None:
            self.tail = newNode
        else:
            self.tail.next = newNode
            self.tail = newNode
            

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
            prim += str(aux.data.nome) + '-> '
            aux = aux.next
        return prim

if __name__ == "__main__":
    fila = Queue()

    skelet = Character('skeleton')
    zom = Character('zombie')

    fila.enqueue(skelet)
    fila.enqueue(zom)

    print(fila)
    print(fila.head.data.nome)

    fila.dequeue()

    print(fila)
    print(fila.head.data.nome)
