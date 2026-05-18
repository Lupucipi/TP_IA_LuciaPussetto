import random # Única librería nativa importada para generar ruido y elegir neuronas aleatoriamente

# =====================================================================
# 1. DEFINICIÓN DE LOS PATRONES (30x30)
# =====================================================================
# Representamos la cuadrícula con texto. 
# '#' será la pieza (valor +1) y '.' será el fondo (valor -1).

# Patrón 1: El Motor (Una base ancha con un bloque superior)
PATRON_MOTOR = [
    "..............................",
    "..............................",
    "..............................",
    "..............................",
    "......##################......",
    "......##################......",
    "......##################......",
    "......##################......",
    "......##################......",
    "......##################......",
    "......##################......",
    "......##################......",
    "......##################......",
    "......##################......",
    "......##################......",
    "......##################......",
    "......##################......",
    "......##################......",
    "......##################......",
    "......##################......",
    "......##################......",
    "......##################......",
    "......##################......",
    "......##################......",
    "......##################......",
    "..............................",
    "..............................",
    "..............................",
    "..............................",
    ".............................."
]

# Patrón 2: El Anillo (Un recuadro hueco)
PATRON_ANILLO = [
    "..............................",
    "..............................",
    "..............................",
    "..............................",
    "......##################......",
    "......##################......",
    "......##################......",
    "......###............###......",
    "......###............###......",
    "......###............###......",
    "......###............###......",
    "......###............###......",
    "......###............###......",
    "......###............###......",
    "......###............###......",
    "......###............###......",
    "......###............###......",
    "......###............###......",
    "......###............###......",
    "......###............###......",
    "......###............###......",
    "......###............###......",
    "......##################......",
    "......##################......",
    "......##################......",
    "..............................",
    "..............................",
    "..............................",
    "..............................",
    ".............................."
]

# =====================================================================
# 2. FUNCIONES AUXILIARES DE TRANSFORMACIÓN
# =====================================================================

def texto_a_bipolar(patron_texto):
    """Convierte el dibujo de texto a una lista matemática unidimensional de +1 y -1"""
    vector_bipolar = [] # Lista vacía para guardar los 900 valores
    for fila in patron_texto: # Recorremos cada línea del dibujo
        for caracter in fila: # Recorremos cada letra de la línea
            if caracter == '#': # Si es parte de la pieza...
                vector_bipolar.append(1) # Agregamos un +1
            else: # Si es el fondo (punto)...
                vector_bipolar.append(-1) # Agregamos un -1
    return vector_bipolar # Devolvemos la lista de 900 elementos

def bipolar_a_texto(vector_bipolar):
    """Convierte la lista matemática de nuevo a texto 30x30 para imprimirlo en pantalla"""
    texto = "" # Texto vacío inicial
    for i in range(900): # Recorremos las 900 neuronas
        if vector_bipolar[i] == 1: # Si la neurona está activa...
            texto += "█" # Usamos un bloque sólido para que se vea mejor al imprimir
        else: # Si está inactiva...
            texto += " " # Usamos un espacio vacío para el fondo
        
        # Cada 30 caracteres, hacemos un salto de línea para formar la cuadrícula
        if (i + 1) % 30 == 0: 
            texto += "\n"
    return texto

def aplicar_ruido(vector_original, porcentaje_ruido):
    """Toma un patrón perfecto y cambia aleatoriamente algunos píxeles (simula el polvo/sombras)"""
    vector_ruidoso = list(vector_original) # Hacos una copia para no dañar el original
    cantidad_a_cambiar = int(900 * porcentaje_ruido) # Calculamos cuántos píxeles vamos a dañar
    
    # Elegimos posiciones aleatorias sin repetir
    indices_a_cambiar = random.sample(range(900), cantidad_a_cambiar) 
    
    for indice in indices_a_cambiar: # Por cada posición elegida...
        vector_ruidoso[indice] *= -1 # Invertimos su valor (si era 1 pasa a -1, y viceversa)
        
    return vector_ruidoso

# =====================================================================
# 3. FASE DE ENTRENAMIENTO (REGLA DE HEBB)
# =====================================================================

def entrenar_red(lista_patrones):
    """Crea la matriz de pesos de 900x900 grabando los patrones (memoria autoasociativa)"""
    # Creamos una matriz vacía (lista de listas) de 900 filas y 900 columnas, llena de ceros
    pesos = [[0 for _ in range(900)] for _ in range(900)]
    
    for patron in lista_patrones: # Por cada pieza que queramos memorizar (Motor, Anillo)...
        for i in range(900): # Recorremos la neurona de origen
            for j in range(900): # Recorremos la neurona de destino
                if i != j: # REGLA DE ORO: Las neuronas no se conectan a sí mismas
                    # Multiplicamos el estado de ambas neuronas y lo sumamos al peso actual
                    pesos[i][j] += patron[i] * patron[j] 
                    
    return pesos # Devolvemos el "cerebro" entrenado

# =====================================================================
# 4. FASE DE RECUPERACIÓN (ACTUALIZACIÓN ASÍNCRONA)
# =====================================================================

def recuperar_patron(vector_entrada, matriz_pesos, iteraciones_max=5):
    """Toma una imagen dañada y la repara iterando hasta encontrar el atractor"""
    estado_actual = list(vector_entrada) # Copiamos la entrada dañada para empezar a trabajarla
    indices_neuronas = list(range(900)) # Lista del 0 al 899
    
    # Un ciclo de iteración significa que le dimos la oportunidad a TODAS las neuronas de actualizarse
    for ciclo in range(iteraciones_max):
        # Desordenamos la lista para evaluar las neuronas al azar (Actualización Asíncrona)
        random.shuffle(indices_neuronas) 
        hubo_cambios = False # Bandera para saber si la red ya se estabilizó
        
        for i in indices_neuronas: # Tomamos una neurona al azar
            suma = 0 # Inicializamos la energía que le llega en 0
            
            # Calculamos lo que le dicen todas sus vecinas
            for j in range(900): 
                # Multiplicamos el estado de la vecina por el peso del cable que las une
                suma += matriz_pesos[i][j] * estado_actual[j] 
                
            # Función de Activación: Si la suma de las voces es >= 0, se enciende. Si no, se apaga.
            nuevo_estado = 1 if suma >= 0 else -1
            
            # Verificamos si la neurona tuvo que cambiar de opinión
            if nuevo_estado != estado_actual[i]:
                estado_actual[i] = nuevo_estado # Actualizamos su estado
                hubo_cambios = True # Marcamos que la imagen todavía se está modificando
                
        # Si terminamos de revisar las 900 neuronas y NINGUNA cambió, la imagen está perfecta
        if not hubo_cambios:
            print(f"\n[INFO] La red convergió (se estabilizó) en el ciclo {ciclo + 1}.")
            break # Detenemos el proceso para ahorrar tiempo de cómputo
            
    return estado_actual

# =====================================================================
# 5. EJECUCIÓN PRINCIPAL DEL PROGRAMA (SIMULACIÓN)
# =====================================================================

if __name__ == "__main__":
    print("Iniciando Sistema de Visión Artificial (Red de Hopfield)...")
    
    # 1. Transformamos los dibujos a matemáticas
    vector_motor = texto_a_bipolar(PATRON_MOTOR)
    vector_anillo = texto_a_bipolar(PATRON_ANILLO)
    
    # 2. Entrenamos la red (Creamos la matriz de pesos)
    print("\n[PROCESO] Entrenando la red con los patrones perfectos...")
    matriz_sinaptica = entrenar_red([vector_motor, vector_anillo])
    print("[ÉXITO] Matriz de 900x900 creada y memorizada.")
    
    # 3. Simulamos un problema: La cámara capta el Anillo, pero con un 30% de ruido (sombra/polvo)
    print("\n[PROCESO] Aplicando 30% de ruido al patrón del ANILLO para simular la cámara...")
    anillo_con_ruido = aplicar_ruido(vector_anillo, 0.30)
    
    print("\n--- IMAGEN CAPTADA POR LA CÁMARA (CON RUIDO) ---")
    print(bipolar_a_texto(anillo_con_ruido))
    
    # 4. Pasamos la imagen ruidosa por la Red de Hopfield para recuperarla
    print("\n[PROCESO] Pasando la imagen ruidosa por el filtro de la Red de Hopfield...")
    imagen_recuperada = recuperar_patron(anillo_con_ruido, matriz_sinaptica, iteraciones_max=10)
    
    print("\n--- IMAGEN RECUPERADA POR LA INTELIGENCIA ARTIFICIAL ---")
    print(bipolar_a_texto(imagen_recuperada))
    print("\nFin del proceso. Pieza lista para ser ensamblada.")