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
    'batteries': [("baterias_chicas", 10, 5000), ("baterias_medianas", 20, 7500), ("baterias_grandes", 50, 10000)],
    'comms': [("radios", 5, 0), ("video_llamadas", 10)],
    }

constraints = []

# Restricción: la autonomía debe ser de 50 minutos
# Hay que ver todos los upgrades seleccionados y dividir la batería por el consumo total por movimiento.
# Este tiene que ser de 50 minutos (movimientos)

def robot_range(variables, values):
    total_cost_per_movement = sum(upgrade[1] for upgrade in values)
    has_small_batteries = "baterias_chicas" in [upgrade[0] for upgrades in values]
    has_medium_batteries = "baterias_medianas" in [upgrade[0] for upgrades in values]
    has_big_batteries = "baterias_grandes" in [upgrade[0] for upgrades in values]

    # Hay formas mucho mejores de resolver esto. 
    # Es una alternativa, pero preguntar directamente 
    # a la variable "batteries" de los upgrades sería mejor
    
    if has_small_batteries:
        return 5000 / total_cost_per_movement >= 50
    elif has_medium_batteries:
        return 7500 / total_cost_per_movement >= 50
    elif has_big_batteries:
        return 10000 / total_cost_per_movement >= 50

constraints.append((problem_variables, robot_range))

# Restricción: si usa baterías grandes necesita usar las orugas

def big_batteries_require_tracks(variables, values):
    has_tracks = "orugas" in [upgrade[0] for upgrades in values]
    has_big_batteries = "baterias_grandes" in [upgrade[0] for upgrades in values]

    if has_big_batteries:
        return has_tracks
    else:
        return True

constraints.append((problem_variables, videocall_require_tracks_or_legs))

# Restricción: si usa caja de suministros superior no puede usar el par extra de patas
# Restricción: si usa sistema radios no puede usar la mejora de motores
# Restricción: si usa sistema de videollamadas necesita el par extra de patas o las orugas

def videocall_require_tracks_or_legs(variables, values):
    has_tracks_or_legs = "orugas" or "patas_extras" in [upgrade[0] for upgrades in values]
    has_videocall = "video_llamadas" in [upgrade[0] for upgrades in values]

    if has_videocall:
        return has_tracks_or_legs
    else:
        return True

constraints.append((problem_variables, videocall_require_tracks_or_legs))



