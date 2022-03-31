"""
ENTREGA: 1 (solución al tunel con una sola dirección)
GRUPO: 18
NOMBRES: Antonio Francisco Álvarez Gómez, Marcos Rocha Morales, Marina Bueno García
VERSIÓN: 1
En esta versión solo puede haber un coche en el túnel a la vez. Para controlarlo utilizamos
un variable compartida que gestiona el acceso al túnel: 0 si hay un coche en el interior del túnel y 1 si no hay.
"""
import time
import random
from multiprocessing import Lock, Condition, Process, Manager
from multiprocessing import Value

SOUTH = "north"
NORTH = "south"

NCARS = 10

class Monitor():
    def __init__(self, manager):
        self.mutex = Lock()
        self.access = Value('i',1)
        self.free_access = Condition(self.mutex)

    def is_free_access(self):
        return(self.access.value)

    def wants_enter(self):
        self.mutex.acquire()
        self.free_access.wait_for(self.is_free_access)
        self.access.value = 0
        self.mutex.release()

    def leaves_tunnel(self):
        self.mutex.acquire()
        self.access.value = 1
        self.free_access.notify_all()
        self.mutex.release()

def delay(n=3):
    time.sleep(random.random()*n)

def car(cid, direction, monitor):
    print(f"car {cid} direction {direction} created")
    delay(6)
    print(f"car {cid} heading {direction} wants to enter")
    monitor.wants_enter()
    print(f"car {cid} heading {direction} enters the tunnel")
    delay(3)
    print(f"car {cid} heading {direction} leaving the tunnel")
    monitor.leaves_tunnel()
    print(f"car {cid} heading {direction} out of the tunnel")


def main():
    manager = Manager()
    monitor = Monitor(manager)
    cid = 0
    for i in range(NCARS):
        direction = NORTH if i%2==0  else SOUTH
        cid += 1
        p = Process(target=car, args=(cid, direction, monitor))
        p.start()
        time.sleep(random.expovariate(1/0.5)) # a new car enters each 0.5s
    p.join()

if __name__=='__main__':
    main()

