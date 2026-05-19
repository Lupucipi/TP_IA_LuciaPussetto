from collections import deque
import random

# ==========================================
# 1. ESTRUCTURA DEL NODO
# ==========================================

# Solo nos importa la posición y de dónde venimos.
class Posicion:
    def __init__(self, x, anterior=None):
        self.x = x          # Posición horizontal actual
        self.anterior = anterior  # Posición anterior para reconstruir la ruta después

# ==========================================
# 2. ALGORITMO BFS (BÚSQUEDA EN ANCHURA)
# ==========================================
def bfs(inicio_x, meta_x, longitud_cinta):
    # Creamos la posición inicial
    posicion_inicio = Posicion(inicio_x)
    
    #Creamos la cola tipo FIFO e insertamos la posición inicial
    cola = deque([posicion_inicio])
    
    # lista para no volver a visitar posiciones ya exploradas
    posiciones_visitadas = set()
    
    # Agregamos la posición inicial 
    posiciones_visitadas.add(inicio_x)

    #Lista para guardar el orden de exploración (mostrar funcionamiento después)
    orden_exploracion = []

    # Bucle principal: exploramos nivel por nivel mientras haya posiciones en la cola
    while cola:
        # Sacamos la primera posición
        posicion_actual = cola.popleft()
        
        #Registramos la posición apenas la sacamos de la cola
        orden_exploracion.append(posicion_actual.x)

        # Si encontramos el anillo, terminamos
        if posicion_actual.x == meta_x:
            ruta = []
            # Trazamos el camino de vuelta usando la propiedad "anterior"
            while posicion_actual: # Mientras haya un anterior, seguimos subiendo
                ruta.append(posicion_actual.x)
                posicion_actual = posicion_actual.anterior
            # Devolvemos tanto la ruta final como el historial de exploración
            return ruta[::-1], orden_exploracion
            
        #Expansión: Nos movemos 1 paso a la Izquierda (-1) o 1 a la Derecha (+1)
        for mov in [-1, 1]:
            vecino_x = posicion_actual.x + mov
            
            # Evita salirnos de los límites físicos de la cinta
            if vecino_x < 0 or vecino_x >= longitud_cinta:
                continue
                
            # Si NO hemos visitado esta posición, la agregamos
            if vecino_x not in posiciones_visitadas:
                # La marcamos como visitada en el momento que la descubrimos
                posiciones_visitadas.add(vecino_x)
                
                # Creamos la nueva posición indicando que viene de "posicion_actual"
                posicion_vecina = Posicion(vecino_x, posicion_actual)
                
                # Lo agregamos al FINAL de la cola.
                # BFS siempre explorará todos los nodos del nivel actual antes
                # de pasar a los vecinos recién descubiertos.
                cola.append(posicion_vecina)
                
    # Si la cola se vacía y no encontramos la meta
    return [], orden_exploracion

# ==========================================
# 3. PRUEBA DEL PROGRAMA
# ==========================================
longitud_cinta = 10  # La cinta tiene 10 posiciones (0 a 9)
posicion_inicial = random.randint(0, longitud_cinta - 1)  # El ensamble arranca en una posición aleatoria
posicion_anillo = random.randint(0, longitud_cinta - 1)   # El anillo espera en la posición aleatoria

print("Calculando ruta de ensamble horizontal con BFS...")
print(f"Posición inicial: {posicion_inicial}")
print(f"Posición del anillo: {posicion_anillo}")
ruta_optima,exploracion = bfs(posicion_inicial, posicion_anillo, longitud_cinta)

print("Ruta óptima encontrada:")
for paso, posicion in enumerate(ruta_optima):
    print(f"  Paso {paso}: Posición {posicion}")

print("")

print("Ruta recorrida:")
for paso, posicion in enumerate(exploracion):
    print(f"  Paso {paso}: Posición {posicion}")
