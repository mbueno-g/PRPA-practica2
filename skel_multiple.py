"""
ENTREGA: 1 (solución al tunel con una sola dirección)
GRUPO: 18
NOMBRES: Antonio Francisco Álvarez Gómez, Marcos Rocha Morales, Marina Bueno García
VERSIÓN: 2
En esta versión puede haber más de un coche en el túnel siempre y cuando tengan la misma 
dirección, dejando a los coches en dirección contraria esperando a que se les conceda el acceso. 
Con respecto a la versión anterior añadimos dos variables compartidas que cuentan 
el número de coches que hay en cada dirección dentro del túnel. 
"""

import time
import random
from multiprocessing import Lock, Condition, Process, Manager
from multiprocessing import Value

SOUTH = "north"
NORTH = "south"

NCARS = 20

class Monitor():
    def __init__(self, manager):
        self.ncar_n = Value('i', 0)
        self.ncar_s = Value('i', 0)
        self.mutex = Lock()
        self.d = NORTH
        self.access = manager.list([True])
        self.free_access = Condition(self.mutex)

    def set_current_direction(self, direction):
        self.d = direction

    def is_free_access(self):
        if (self.d == NORTH):
            d = self.ncar_n.value > 0
        else:
            d = self.ncar_s.value > 0
        return(self.access[0] or d)

    def wants_enter(self, direction):
        self.mutex.acquire()
        self.set_current_direction(direction)
        self.free_access.wait_for(self.is_free_access)
        if (direction == NORTH):
            self.ncar_n.value += 1
        else:
            self.ncar_s.value += 1
        self.access[0] = False
        self.mutex.release()

    def leaves_tunnel(self, direction):
        self.mutex.acquire()
        if (direction == NORTH):
            self.ncar_n.value -= 1
        else:
            self.ncar_s.value -= 1
        if (self.ncar_n.value == 0 and self.ncar_s.value == 0):
            self.access[0] = True
        self.free_access.notify_all()
        self.mutex.release()

def delay(n=3):
    time.sleep(random.random()*n)

def car(cid, direction, monitor):
    print(f"car {cid} direction {direction} created")
    delay(6)
    print(f"car {cid} heading {direction} wants to enter")
    monitor.wants_enter(direction)
    print(f"car {cid} heading {direction} enters the tunnel")
    delay(3)
    print(f"car {cid} heading {direction} leaving the tunnel")
    monitor.leaves_tunnel(direction)
    print(f"car {cid} heading {direction} out of the tunnel")


def main():
    manager = Manager()
    monitor = Monitor(manager)
    cid = 0
    coche = []
    for i in range(NCARS):
        direction = NORTH if random.randint(0,1)==1 else SOUTH
        cid += 1
        p = Process(target=car, args=(cid, direction, monitor))
        coche += [p]
        p.start()
        time.sleep(random.expovariate(1/0.5)) # a new car enters each 0.5s
    for p in coche:
        p.join()

if __name__=='__main__':
    main()

