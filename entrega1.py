
from simpleai.search.models import SearchProblem
from simpleai.search import astar, breadth_first, depth_first, greedy, uniform_cost
from simpleai.search.viewers import WebViewer, BaseViewer

TUNELES=[(5,1),(6,1),(6,2)]

ROBOTS = [("s1", "soporte"), ("e1", "escaneador"), ("e2", "escaneador"),("e3", "escaneador")]

ACCIONES_MOVER = [('Arriba', (-1, 0)),
                  ('Abajo', (1, 0)),
                  ('Izquierda', (0, -1)),
                  ('Derecha', (0, 1))]

def posicion_valida(fila, columna):
    # No es valido estar afuera del depósito
    if fila < 0 or fila > 12 or columna < 0 or columna > 11:
        return False
    # Las demás posiciones son validas
    return True

class robotsminerosproblem(SearchProblem):

    def is_goal(self, state):
        return state[1] == 0
    
    def cost(self, state, action, state2):
        id_robot, accion, destino = action
        #si la accion es cargar, el robot demora 5min
        if accion == "cargar":
            return 5
        #si la accion es mover, el robot demora 1min
        return 1
     

    def actions(self, state):
        tuneles, robots = state
        #las acciones estarán conformadas por tupla de robot, acción que se va a realizar y destino
        #las acciones disponibles son Mover y Cargar
        #el destino puede venir definido por una posicion (fila, columna) o por un id de robot escaneador 
        #("s1", "mover", (5, 1))
        #("s1", "cargar", "e2")

        #comienzo recorriendo los robots disponibles
        for robot in robots:
            #me guardo el id, la posicion y la bateria actual del robot
            id_robot, tipo_robot, posicion, bateria = robot
            #lo que hago es sacar la fila y columna en la que se encuentra el robot
            fila_robot, columna_robot = posicion
            #Si el robot es escaneador
            if tipo_robot == "escaneador":
                #si la bateria actual es mayor que 100mAh, el robot se puede mover
                if bateria >= 100:               
                    acciones = []
                    # recorro las acciones_mover (arriba, abajo, derecha, izquierda), calculo la nueva posición y la agrego en acciones
                    for x, (fila, columna) in ACCIONES_MOVER:
                        nueva_fila = fila_robot + fila
                        nueva_columna = columna_robot + columna
                        posicion_destino = (nueva_fila, nueva_columna)
                        #FALTARIA VERIFICAR SI LA NUEVA POSICIÓN CREADA ES VÁLIDA
                        if posicion_valida(nueva_fila, nueva_columna) and (posicion_destino in tuneles):
                            acciones.append(id_robot, "mover", posicion_destino)
            if tipo_robot == "soporte":
                #recorro la lista de robots
                for robot_a_abastecer in robots:
                    id_robot_a_abastecer, tipo_robot_a_abastecer = robot_a_abastecer
                    #lo que hago es preguntar si la posicion del robot a abastecer es la misma que el robot de soporte
                    # tambien pregunto si la bateria del robot a abastecer es menor a 1000
                    if (robot_a_abastecer[2] == posicion) and (robot_a_abastecer [3] < 1000):
                        #si cumple estas caracteristicas debo generar una acción de cargar
                        #en acciones cargo el id del robot de soporte, la accion y el id del robot escaneador que se abasteció
                        acciones.append(id_robot, "cargar", id_robot_a_abastecer)

        return acciones
    
    def result(self, state, action):
        return super().result(state, action)

def planear_escaneo (tuneles,robots):

    global ROBOTS 
    ROBOTS = list(robots)
    global TUNELES
    TUNELES = list(tuneles)

    for robot in ROBOTS:
        if robot[1] == "escaneador":
            robot[2] = (5,0)
            robot [3] = 1000

    INITIAL_STATE = (ROBOTS,TUNELES)

    robotsminerosproblem(INITIAL_STATE)


    pass



