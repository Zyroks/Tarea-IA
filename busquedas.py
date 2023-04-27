import entrada
import random
import queue

class Nodo:
    # Se inicializan los nodos con sus respectivos parametros
    def __init__(self, v, h):
        self.v = v
        self.h = h
        self.hijos = []
        self.expansion = 0
    # Se añade un hijo a un nodo
    def addHijo(self, hijo, w):
        self.hijos.append((hijo, w))

class Arbol:
    # Se define la clase arbol para realizar las busquedas
    def __init__(self, init, goal, h, e):
        self.lista1 = {}
        self.lista2 = []
        for i in range(len(h)):
            self.lista2.append(h[i][0])
        index = self.lista2.index(init)
        self.lista1[h[index][0]] = Nodo(h[index][0], h[i][1])
        self.init = self.lista1[h[index][0]]
        self.goal = goal
        for i in range(len(h)):
            if h[i][0] not in self.lista1:
                self.lista1[h[i][0]] = Nodo(h[i][0], h[i][1])
        
        for i in range(len(e)):
            self.lista1[e[i][0]].addHijo(self.lista1[e[i][1]], e[i][2])

    def busqueda_profundidad(self):
        s = [(self.init, [], 0)] 
        # Inicializa el conjunto de nodos visitados
        visit = set() 
        # Continúa mientras la pila no está vacía
        while s: 
            # Obtiene el siguiente nodo, ruta y costo de la pila
            nodo, ruta, costo = s.pop() 
            # Comprueba si se alcanzó el objetivo
            if self.goal == nodo.v: 
                # Agrega el nodo actual a la ruta
                ruta.append(nodo) 
                # Genera una cadena de texto con la ruta
                camino = ' -> '.join([i.v for i in ruta]) 
                # Imprime la ruta
                print(camino) 
                # Imprime el costo de la ruta
                print(f"Costo: {costo}") 
                # Itera sobre todos los nodos y imprime las veces que se expandió cada nodo
                for i in self.lista1.values(): 
                    if i.expansion == 1:
                        print(f"El nodo {i.v} se expandio {i.expansion} vez") 
                    else:
                        print(f"El nodo {i.v} se expandio {i.expansion} veces")
                return
            # Incrementa el contador de expansiones del nodo actual
            nodo.expansion += 1 
            # Comprueba si el nodo actual ya ha sido visitado
            if nodo not in visit: 
                # Agrega el nodo actual al conjunto de visitados
                visit.add(nodo) 
                # Crea una copia de la lista de hijos del nodo actual
                hijos = nodo.hijos.copy() 
                # Mezcla la lista de hijos aleatoriamente
                random.shuffle(hijos) 
                # Itera sobre todos los hijos del nodo actual
                for hijo, h in hijos: 
                     # Agrega los hijos a la pila con la nueva ruta y el nuevo costo
                    s.append((hijo, ruta + [nodo], costo + h))
        print("No hay solucion")
        return

    def busqueda_costo_uniforme(self):
        # Inicializar el costo de llegar al nodo inicial
        h = {self.init: 0}
        # Crear una cola de prioridad para ordenar los nodos por costo
        q = queue.PriorityQueue()
        # Insertar el nodo inicial en la cola con costo 0 y una ruta vacía
        q.put((0, self.init, []))
        # Crear un conjunto para almacenar los nodos visitados
        visit = set()
        # Mientras haya nodos en la cola
        while not q.empty():
            # Sacar el nodo con el menor costo de la cola
            aux, nodo, camino = q.get()
            # Si el nodo actual es el objetivo, se encontró la solución
            if self.goal == nodo.v:
                # Agregar el nodo actual a la ruta y mostrarla
                camino.append(nodo)
                camino = ' -> '.join([i.v for i in camino])
                print(camino)
                print(f"Costo: {h[nodo]}")
                # Mostrar el número de veces que cada nodo fue expandido
                for i in self.lista1.values():
                    if i.expansion == 1:
                        print(f"El nodo {i.v} se expandio {i.expansion} vez")
                    else:
                        print(f"El nodo {i.v} se expandio {i.expansion} veces")
                return
            # Marcar el nodo actual como visitado y aumentar su contador de expansiones
            nodo.expansion += 1
            if nodo not in visit:
                visit.add(nodo)
                # Para cada hijo del nodo actual
                for hijo, distancia in nodo.hijos:
                    # Calcular el costo de llegar al hijo desde el nodo actual
                    costo = h[nodo] + distancia
                    # Si el hijo no está en el diccionario de costos o si el costo nuevo es menor
                    if hijo not in h or costo < h[hijo]:
                        # Actualizar el costo del hijo y agregarlo a la cola con su ruta
                        h[hijo] = costo
                        q.put((costo, hijo, camino + [nodo]))  
        print("No hay solucion")
        return
    
    def busqueda_greedy(self):
        # Inicializa la heurística del nodo inicial
        h = {self.init: self.lista1[self.init.v].h}
        # Crea la cola de prioridad y agrega el nodo inicial
        q = queue.PriorityQueue()
        q.put((h[self.init], self.init, []))
        # Crea un conjunto para llevar el registro de los nodos visitados
        visit = set()
        # Itera mientras la cola no esté vacía
        while not q.empty():
            # Obtiene el siguiente nodo de la cola
            _, nodo, ruta = q.get()
            # Si se alcanzó el nodo objetivo, imprime el camino y el costo y termina
            if self.goal == nodo.v:
                ruta.append(nodo)
                camino = ' -> '.join([i.v for i in ruta])
                print(camino)
                print(f"Costo: {h[nodo]}")
                # Imprime información de la cantidad de veces que se expandió cada nodo
                for i in self.lista1.values():
                    if i.expansion == 1:
                        print(f"El nodo {i.v} se expandió {i.expansion} vez")
                    else:
                        print(f"El nodo {i.v} se expandió {i.expansion} veces")
                return
            # Incrementa el contador de expansiones del nodo actual
            nodo.expansion += 1
            # Si el nodo no ha sido visitado antes, agrega sus hijos a la cola de prioridad
            if nodo not in visit:
                visit.add(nodo)
                for hijo, distancia in nodo.hijos:
                    nuevo_h = self.lista1[hijo.v].h
                    if hijo not in h or nuevo_h < h[hijo]:
                        h[hijo] = nuevo_h
                        nueva_ruta_actualizada = ruta + [nodo]
                        q.put((nuevo_h, hijo, nueva_ruta_actualizada))
        print("No hay solución")
        return
    
    def busqueda_a_estrella(self):
        h = {self.init: 0}
        q = queue.PriorityQueue()
        q.put((self.lista1[self.init.v],self.init, []))
        visit = set()
        # Mientras la cola de prioridad no esté vacía
        while q:
            # Obtener el nodo con el menor costo estimado de la cola de prioridad
            aux,nodo, ruta = q.get()
            # Si se llegó al nodo objetivo, imprimir la ruta y el costo total y salir del bucle
            if self.goal == nodo.v:
                ruta.append(nodo)
                camino = ' -> '.join([i.v for i in ruta])
                print(camino)
                print(f"Costo: {h[nodo]}")
                # Imprimir el número de veces que se expandió cada nodo
                for i in self.lista1.values():
                    if i.expansion == 1:
                        print(f"El nodo {i.v} se expandio {i.expansion} vez")
                    else:
                        print(f"El nodo {i.v} se expandio {i.expansion} veces")
                return
            # Incrementar el número de veces que se ha expandido el nodo actual
            nodo.expansion += 1
            # Si el nodo actual no ha sido visitado antes
            if nodo not in visit:
                # Añadirlo al conjunto de nodos visitados
                visit.add(nodo) 
                # Expandir el nodo actual y agregar sus hijos a la cola de prioridad
                for hijo, distancia in nodo.hijos:
                    costo = h[nodo] + distancia
                    if hijo not in h or costo < h[hijo]:
                        h[hijo] = costo
                        # Agregar los hijos a la cola de prioridad con el costo estimado más la heurística y la ruta actual
                        q.put((self.lista1[hijo.v].h + costo, hijo, ruta + [nodo]))
        print("No hay solucion")
        return
    
datos = entrada.entrada()
init = datos[0]
goal = datos[1]
h = datos[2]
e = datos[3]
a = Arbol(init, goal, h, e)
while True:
    print("Ingrese la búsqueda que quiere realizar: \n[1] Busqueda en profundidad\n[2] Busqueda por h uniforme\n[3] Busqueda greedy\n[4] Busqueda A*")
    seleccion = int(input())
    if seleccion == 1:
        print("\nSe realizara una busqueda en profundidad:\n")
        a.busqueda_profundidad()
        print("\n")
        break
    elif seleccion == 2:
        print("\nSe realizara una busqueda por h uniforme:\n")
        a.busqueda_costo_uniforme()
        print("\n")
        break
    elif seleccion == 3:
        print("\nSe realizara una busqueda greedy:\n")
        a.busqueda_greedy()
        print("\n")
        break
    elif seleccion == 4:
        print("\nSe realizara una busqueda A*:\n")
        a.busqueda_a_estrella()
        print("\n")
        break



