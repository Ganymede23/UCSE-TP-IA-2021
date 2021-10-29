from itertools import combinations

from simpleai.search import (
    CspProblem,
    backtrack,
    HIGHEST_DEGREE_VARIABLE,
    MOST_CONSTRAINED_VARIABLE,
    LEAST_CONSTRAINING_VALUE,
)

# ID MEJORAS
#                           CONSUMO (mAh)       BATERIA TOTAL (mAh)
# "baterias_chicas"             +10                  +5000
# "baterias_medianas"           +20                  +7500
# "baterias_grandes"            +50                  +10000
# "patas_extras"                +15
# "mejores_motores"             +25
# "orugas"                      +50
# "caja_superior"               +10
# "caja_trasera"                +10
# "radios"                      +5
# "video_llamadas"              +10

problem_variables = ["supplies", "propulsion", "batteries", "comms"]

domains = {
    'supplies': [("caja_superior", 10), ("caja_trasera", 10)],
    'propulsion': [("patas_extras", 15), ("mejores_motores", 25), ("orugas", 50)],
    'batteries': [("baterias_chicas", 10), ("baterias_medianas", 20), ("baterias_grandes", 50)],
    'comms': [("radios", 5), ("video_llamadas", 10)],
    }

constraints = []

# Restricción: la autonomía debe ser de 50 minutos.
# Hay que ver todos los upgrades seleccionados y dividir la batería por el consumo total por movimiento.
# Este tiene que ser de 50 minutos (movimientos)

def robot_range(variables, values):
    total_cost_per_movement = sum(upgrade[1] for upgrade in values)
    has_small_batteries = "baterias_chicas" in [upgrade[0] for upgrade in values]
    has_medium_batteries = "baterias_medianas" in [upgrade[0] for upgrade in values]
    has_big_batteries = "baterias_grandes" in [upgrade[0] for upgrade in values]

    # Hay formas mucho mejores de resolver esto. 
    # Una alternativa es agregar los mAh finales que deja la batería al diccionario y consultar ahí.
    # Esto así es bastante fulero, pero funciona(ría)
    
    if has_small_batteries:
        #print("small:", (5000 / (100+total_cost_per_movement)))
        return 5000 / (100+total_cost_per_movement) >= 50        
    elif has_medium_batteries:
        #print("medium:", (7500 / (100+total_cost_per_movement)))
        return 7500 / (100+total_cost_per_movement) >= 50
    elif has_big_batteries:
        #print("big:", (10000 / (100+total_cost_per_movement)))
        return 10000 / (100+total_cost_per_movement) >= 50
    else:
        return False

constraints.append((problem_variables, robot_range))

# Restricción: si usa baterías grandes necesita usar las orugas

def big_batteries_requires_tracks(variables, values):
    batteries, propulsion = values
    if batteries == "baterias_grandes":
        return propulsion == "orugas"
    else:
        return True

constraints.append((('batteries','propulsion'), big_batteries_requires_tracks))

# Restricción: si usa caja de suministros trasera no puede usar el par extra de patas

def aft_supply_box_uncompatible_with_extra_legs(variables, values):
    supplies, propulsion = values
    if supplies == "caja_trasera" and propulsion == "patas_extras":
        return False
    else:
        return True

constraints.append((('supplies','propulsion'), aft_supply_box_uncompatible_with_extra_legs))

# Restricción: si usa sistema radios no puede usar la mejora de motores

def radio_uncompatible_with_better_engines(variables, values):
    comms, propulsion = values
    if comms == "radios" and propulsion == "mejores_motores":
        return False
    else:
        return True

constraints.append((('comms','propulsion'), radio_uncompatible_with_better_engines))

# Restricción: si usa sistema de videollamadas necesita el par extra de patas o las orugas

def videocall_requires_tracks_or_legs(variables, values):
    comms, propulsion = values
    if comms == "video_llamadas":
        return(propulsion == "orugas" or propulsion == "patas_extras")
    else:
        return True

constraints.append((('comms','propulsion'), videocall_requires_tracks_or_legs))

problem = CspProblem(problem_variables, domains, constraints)
solution = backtrack(problem)

print("Solution:")
print(solution)
