from itertools import combinations

from simpleai.search import (
    CspProblem,
    backtrack,
    HIGHEST_DEGREE_VARIABLE,
    MOST_CONSTRAINED_VARIABLE,
    LEAST_CONSTRAINING_VALUE,
)

# ID MEJORAS
#
# "baterias_chicas"
# "baterias_medianas"
# "baterias_grandes"
# "patas_extras"
# "mejores_motores"
# "orugas"
# "caja_superior"
# "caja_trasera"
# "radios"
# "video_llamadas"

problem_variables = ["supplies", "propulsion", "batteries", "comms"]

domains = {
    supplies = ["caja_superior", "caja_trasera"],
    propulsion = ["patas_extras", "mejores_motores", "orugas"],
    batteries = ["baterias_chicas", "baterias_medianas", "baterias_grandes"],
    comms = ["radios", "video_llamadas"],
}

constraints = []