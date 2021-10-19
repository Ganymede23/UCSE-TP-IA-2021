
from simpleai.search.models import SearchProblem
from simpleai.search import astar, breadth_first, depth_first, greedy, uniform_cost
from simpleai.search.viewers import WebViewer, BaseViewer

TUNELES=[(5,1),(6,1),(6,2)]

ROBOTS = [("s1", "soporte"), ("e1", "escaneador"), ("e2", "escaneador"),("e3", "escaneador")]

class robotsminerosproblem(SearchProblem):

    def is_goal(self, state):
        return state[1] == 0
    
    def cost(self, state, action, state2):
        return super().cost(state, action, state2)

    def actions(self, state):
        return super().actions(state)
    
    def result(self, state, action):
        return super().result(state, action)

def planear_escaneo (tuneles,robots):

    global ROBOTS 
    ROBOTS = list(robots)
    global TUNELES
    TUNELES = list(tuneles)

    for robot in ROBOTS:
        if robot[1] == "escaneador":
            robot= robot + (1000,) 

    INITIAL_STATE = (ROBOTS,TUNELES)

    robotsminerosproblem(INITIAL_STATE)


    pass



