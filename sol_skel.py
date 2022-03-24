"""
Solution to the one-way tunnel
"""
import time
import random
from multiprocessing import Lock, Condition, Process, Manager
from multiprocessing import Value

SOUTH = "north"
NORTH = "south"

NCARS = 4

class Monitor():
    def __init__(self, manager):
        self.mutex = Lock()
        self.d = NORTH
        self.access = manager.list([True])
        self.free_access = Condition(self.mutex)

    def set_current_direction(self, direction):
        self.d = direction

    def is_free_access(self):
        return(self.access[0])

    def wants_enter(self, direction):
        self.mutex.acquire()
        self.set_current_direction(direction)
        self.free_access.wait_for(self.is_free_access)
        self.access[0] = False
        self.mutex.release()

    def leaves_tunnel(self, direction):
        self.mutex.acquire()
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
    for i in range(NCARS):
        direction = NORTH if i%2==0  else SOUTH
        cid += 1
        p = Process(target=car, args=(cid, direction, monitor))
        p.start()
        time.sleep(random.expovariate(1/0.5)) # a new car enters each 0.5s
    p.join()

if __name__=='__main__':
    main()

