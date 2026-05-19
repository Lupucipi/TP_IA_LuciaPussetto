import heapq # Para usar la cola de prioridad en A*
import random


# clase para representar cada posición en la cinta
class Posicion:
    def __init__(self, x, anterior=None, g=0, h=0):
        self.x = x          # Posición horizontal actual
        self.anterior = anterior  # Nodo anterior (sirve para trazar la ruta de vuelta al final)
        self.g = g          # Costo real acumulado (cuántos pasos dimos)
        self.h = h          # Heurística (cuántos pasos estimamos que faltan)
        self.f = g + h      # Heurística (cuántos pasos estimamos que faltan)

    # Le enseñamos a la cola de prioridad cómo comparar nodos (gana el de menor costo f)
    def __lt__(self, otro):
        return self.f < otro.f

# ==========================================
# 2. FUNCIÓN HEURÍSTICA
# ==========================================
# En una línea recta, la estimación perfecta es la simple diferencia matemática
def heuristica(posicion_actual, posicion_meta):
    return abs(posicion_actual - posicion_meta)

# ==========================================
# 3. ALGORITMO A* 
# ==========================================
def a_estrella(inicio_x, meta_x, longitud_cinta):
    # Creamos el nodo inicial
    posicion_inicio = Posicion(inicio_x, None, 0, heuristica(inicio_x, meta_x))
    
    # "lista_abierta" es la cola de prioridad con las posiciones por explorar
    lista_abierta = []
    heapq.heappush(lista_abierta, posicion_inicio)
    
    # "posiciones_visitadas" es nuestra memoria para no retroceder infinitamente
    posiciones_visitadas = set() 

    #guardamos el mejor costo encontrado para cada posición
    mejor_g = {inicio_x: 0}

    # Lista para guardar el orden en que el algoritmo revisa las posiciones
    orden_exploracion = []

    # Mientras haya caminos por explorar
    while lista_abierta:
        # Extraemos el nodo más prometedor (el de menor costo 'f')
        posicion_actual = heapq.heappop(lista_abierta)

        # si ya fue procesado con mejor camino, lo ignoramos
        if posicion_actual.x in posiciones_visitadas:
            continue
        
        # Lo guardamos en la memoria para no volver a analizarlo
        posiciones_visitadas.add(posicion_actual.x)
        
        # Registramos la posición que estamos analizando en este momento
        orden_exploracion.append(posicion_actual.x)

        # Si la posición actual es la meta, terminamos
        if posicion_actual.x == meta_x:
            ruta = []
            # Vamos hacia atrás usando la propiedad "anterior" para armar la ruta
            while posicion_actual:
                ruta.append(posicion_actual.x)
                posicion_actual = posicion_actual.anterior
            # Invertimos la lista para devolverla desde el inicio hasta la meta
            return ruta[::-1], orden_exploracion
            
        #Nos movemos 1 paso a la Izquierda (-1) o 1 a la Derecha (+1)
        for mov in [-1, 1]:
            vecino_x = posicion_actual.x + mov
            
            # Evitar salirnos de los bordes de la cinta
            if vecino_x < 0 or vecino_x >= longitud_cinta:
                continue
                
            # cálculo del nuevo costo antes de decidir si lo usamos
            nuevo_g = posicion_actual.g + 1

            # solo seguimos si encontramos un mejor camino
            if vecino_x not in mejor_g or nuevo_g < mejor_g[vecino_x]:
                mejor_g[vecino_x] = nuevo_g

                # Creamos el nuevo nodo vecino y le decimos que viene del nodo_actual
                posicion_vecina = Posicion(
                    vecino_x,
                    posicion_actual,
                    nuevo_g,
                    heuristica(vecino_x, meta_x)
                )
                
                # Agregamos esta nueva posición a la lista para explorarla luego
                heapq.heappush(lista_abierta, posicion_vecina)
            
    # Si la lista se vacía y nunca llegamos a la meta, devolvemos una lista vacía
    return [] , orden_exploracion

# ==========================================
# 4. PRUEBA DEL PROGRAMA
# ==========================================
longitud_cinta = 10  # La cinta tiene 10 posiciones (0 a 9)
posicion_motor = random.randint(0, longitud_cinta - 1)  # El ensamble arranca en una posición aleatoria
posicion_anillo = random.randint(0, longitud_cinta - 1)   # El anillo espera en la posición aleatoria

print("Calculando ruta de ensamble con A*...")
print(f"Posición inicial del motor: {posicion_motor}")
print(f"Posición del anillo: {posicion_anillo}")
ruta_optima, exploracion = a_estrella(posicion_motor, posicion_anillo, longitud_cinta)

print("Ruta óptima encontrada:")
for paso, posicion in enumerate(ruta_optima):
    print(f"  Paso {paso}: Posición {posicion}")

print("")

print("Ruta recorrida:")
for paso, posicion in enumerate(exploracion):
    print(f"  Paso {paso}: Posición {posicion}")