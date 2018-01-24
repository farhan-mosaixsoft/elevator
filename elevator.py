import sys, os
import argparse
import cmd
import yaml
import json
import timeit
import httplib
import requests
import argparse

from jproperties import Properties
from os.path import expanduser

ELEVATOR_COUNT = 16

class elevator():
    id = None
    current_floor = None
    goal_floors = None

    def __init__ (self, id):
        self.id = id
        self.current_floor = 1
        self.goal_floors = []
        self.goal_floors.append(1)
  
    def set_current_floor(self, current_floor):
        current_floor = current_floor

    def set_goal_floor(self, goal_floor):
        goal_floors.append(int(goal_floor)) 

    def set_pickup_request(self, pickup_floor):
        if len(self.goal_floors) == 1:
            if self.goal_floors[0] == self.current_floor:
                self.goal_floors[0] = pickup_floor
            else:
                self.goal_floors.append(pickup_floor)
        else:
            self.goal_floors.append(pickup_floor)

    def time_step(self, time):
        if self.goal_floors:
            print self.goal_floors
            if self.current_floor > self.goal_floors[0]:
                self.current_floor -= 1
            elif self.current_floor < self.goal_floors[0]:
                self.current_floor += 1
            else: # both are equal
                if len(self.goal_floors) != 1:
                    del self.goal_floors[0]
            print self.goal_floors

    def __str__(self):
        return 'Elevator Status {} {} {} {}'.format(self.id, self.current_floor, self.goal_floors)

class elevators():
    elevators = []

class elevator(cmd.Cmd):
    """Client for Cloud OS clone service"""

    prompt = "():>"
    requests = []
    selected_elevator = ""
    
    source_cloud = ""
    source_subnets = None
    source_containers = None
    destination_cloud = ""
    client = None
    elevators = []

    for i in range(ELEVATOR_COUNT):
        item = elevator(i)
        elevators.append(item)

    def do_pickup_request(self, line):
        """ Pickup request
        """
  
        split = line.split()
        pickup_request = { "pickup_floor": int(split[0]), "direction": split[1]}
        self.requests.append(pickup_request)
        print self.requests
      
        floor_diff = [0 for i in range(ELEVATOR_COUNT)]
        for i in range(ELEVATOR_COUNT):
            if self.elevators[i].goal_floors:
                floor_diff[i] = abs(self.elevators[i].goal_floors[0] - pickup_request['pickup_floor'])
            else:
                floor_diff[i] = 0
            #print floor_diff[i]

        index = sorted(range(len(floor_diff)), key=lambda k: floor_diff[k])
        floor_diff.sort()
        print 'Sorted floor diff {}'.format(floor_diff)
        print 'Sorted Index is {}'.format(index)
        
        for i in index:
            #print 'My goal is {}'.format(self.elevators[i].goal_floors[0])
            #print 'My current is {}'.format(self.elevators[i].current_floor)
            if self.elevators[i].current_floor > self.elevators[i].goal_floors[0]:
                if pickup_request['direction'] == 'down':
                    print 'Elevator ID to be assigned {}'.format(index[i])
                    self.elevators[i].set_pickup_request(pickup_request['pickup_floor'])
                    break
            elif self.elevators[i].current_floor < self.elevators[i].goal_floors[0]:
                if pickup_request['direction'] == 'up':
                    print 'Elevator ID to be assigned {}'.format(index[i])
                    self.elevators[i].set_pickup_request(pickup_request['pickup_floor'])
                    break
            if self.elevators[i].goal_floors[0] == pickup_request['pickup_floor']:
                print 'Elevator ID to be assigned {}'.format(index[i])
                self.elevators[i].set_pickup_request(pickup_request['pickup_floor'])
                break
            elif self.elevators[i].goal_floors[0] == self.elevators[i].current_floor:
                print 'Elevator ID to be assigned {}'.format(index[i])
                self.elevators[i].set_pickup_request(pickup_request['pickup_floor'])
                break

        for i in range(ELEVATOR_COUNT):
            print self.elevators[i]


    def do_time_step(self, line):
        """ Time step the simulation
        """

        time_step = int(line)
        for t in range(time_step):
            for e in self.elevators:
                e.time_step(t)
    def do_quit(self, line):
        """ quit
        Quit the clone program"""
        return True

    def do_EOF(self, line):
        "Exit"
        return True

    def do_clear(self, line):
        """ clear
        Clear alll entries"""

        self.prompt = "():>"
        self.elevator_queue = None
        self.source_subnets = None
        self.source_containers = None
        self.destination_cloud = ""

        return False

        
def parse_args(args):
    parser = argparse.ArgumentParser('elevator')
    parser.add_argument('--state',
                        help='Querying the state of the elevators (what floor are they on and where they are going)',
                        required=False)
    parser.add_argument('--status',
                        help='receiving an update about the status of an elevator',
                        required=False)
    parser.add_argument('--pickup',
                        help='receiving a pickup request',
                        required=False)
    parser.add_argument('--simulate',
                        help='time-stepping the simulation',
                        required=False)
    args = parser.parse_args(args)
    return args

def main(args):
    #args = parse_args(args)
    elevator().cmdloop()


if __name__ == '__main__':
    main(sys.argv[1:])

