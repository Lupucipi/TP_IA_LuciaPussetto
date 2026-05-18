import random

# =====================================================================
# 1. DEFINICIÓN LÓGICA DE PIEZA (Cuadrícula 15x15)
# =====================================================================

def generar_anillo(centro_x, centro_y):
    """Genera la matriz del anillo (5x5) ubicando su píxel central en X, Y"""
    tablero = [["." for _ in range(15)] for _ in range(15)]
    
    # Plantilla reducida a 5x5. Su centro matemático exacto está en el medio.
    plantilla_circular = [
        ".###.",
        "#...#",
        "#...#", # <-- El centro exacto está aquí
        "#...#",
        ".###."
    ]
    
    # Restamos 2 porque el centro de un arreglo de tamaño 5 es el índice 2
    inicio_x = centro_x - 2
    inicio_y = centro_y - 2
    
    for i in range(5):
        for j in range(5):
            y = inicio_y + i
            x = inicio_x + j
            # Validamos no salirnos del lienzo de 15x15
            if 0 <= y < 15 and 0 <= x < 15:
                if plantilla_circular[i][j] == '#':
                    tablero[y][x] = '#'
    return ["".join(fila) for fila in tablero]

def texto_a_bipolar(patron_texto):
    """Convierte texto a matriz matemática de 225 elementos (+1, -1)"""
    return [1 if caracter == '#' else -1 for fila in patron_texto for caracter in fila]

def bipolar_a_texto(vector_bipolar):
    """Convierte la matemática a un mapa visual auditable de 15x15"""
    texto = ""
    for i in range(225): # Reducido a 225 neuronas
        texto += "█ " if vector_bipolar[i] == 1 else ". "
        if (i + 1) % 15 == 0: # Salto de línea cada 15 caracteres
            texto += "\n"
    return texto

# =====================================================================
# 2. GENERACIÓN DE RUIDO REALISTA A ESCALA REDUCIDA
# =====================================================================

def aplicar_ruido_realista(vector_original, pos_x_reflejo, pos_y_reflejo):
    vector_ruidoso = list(vector_original)
    
    # Polvo ambiental (3% de 225 neuronas son aprox. 6 o 7 píxeles)
    cantidad_polvo = int(225 * 0.03)
    indices_polvo = random.sample(range(225), cantidad_polvo)
    for idx in indices_polvo:
        vector_ruidoso[idx] *= -1
        
    # Reflejo metálico (Reducido a una mancha de 2x2 para ser proporcional a 15x15)
    for i in range(2):
        for j in range(2):
            y = pos_y_reflejo + i
            x = pos_x_reflejo + j
            if 0 <= y < 15 and 0 <= x < 15:
                indice = y * 15 + x
                vector_ruidoso[indice] *= -1 
    return vector_ruidoso

# =====================================================================
# 3. NÚCLEO DE LA RED DE HOPFIELD (225 Neuronas)
# =====================================================================

def entrenar_red(lista_patrones):
    pesos = [[0] * 225 for _ in range(225)]
    for patron in lista_patrones:
        for i in range(225):
            for j in range(225):
                if i != j: 
                    pesos[i][j] += patron[i] * patron[j]
    return pesos

def recuperar_patron(vector_entrada, matriz_pesos, iteraciones_max=10):
    estado = list(vector_entrada)
    indices = list(range(225))
    for ciclo in range(iteraciones_max):
        random.shuffle(indices)
        hubo_cambios = False
        for i in indices:
            suma = sum(matriz_pesos[i][j] * estado[j] for j in range(225))
            nuevo_estado = 1 if suma >= 0 else -1
            if nuevo_estado != estado[i]:
                estado[i] = nuevo_estado
                hubo_cambios = True
        if not hubo_cambios:
            print(f"[INFO] Red estabilizada en el ciclo de filtrado {ciclo + 1}.")
            break
    return estado

def identificar_pieza(vector_recuperado, base_datos_conocida, umbral_tolerancia=0.95):
    mejor_registro = None
    max_similitud = 0.0
    for registro in base_datos_conocida:
        coincidencias = sum(1 for i in range(225) if vector_recuperado[i] == registro["vector"][i])
        similitud = coincidencias / 225.0
        if similitud > max_similitud:
            max_similitud = similitud
            mejor_registro = registro
    if max_similitud >= umbral_tolerancia:
        return mejor_registro, max_similitud
    return None, max_similitud

# =====================================================================
# 4. SIMULACIÓN DE EXTRACCIÓN DE COORDENADAS (15x15)
# =====================================================================

if __name__ == "__main__":
    print("======================================================")
    print(" SISTEMA DE VISIÓN HOPFIELD (ENTORNO REDUCIDO 15x15)")
    print("======================================================\n")
    
    # 1. Generamos coordenadas internas (3 a 11 para que el anillo de 5x5 no corte los bordes)
    centros_aleatorios = [(random.randint(3, 11), random.randint(3, 11)) for _ in range(3)]
    base_de_datos = []
    
    for idx, (cx, cy) in enumerate(centros_aleatorios):
        vector_anillo = texto_a_bipolar(generar_anillo(centro_x=cx, centro_y=cy))
        base_de_datos.append({
            "pieza": "Anillo de Ensamble", 
            "centro_x": cx, 
            "centro_y": cy, 
            "vector": vector_anillo
        })
    
    # Entrenamos la red de 225 neuronas
    vectores_entrenamiento = [registro["vector"] for registro in base_de_datos]
    matriz_sinaptica = entrenar_red(vectores_entrenamiento)
    
    # 2. Elegimos un objetivo y aplicamos interferencia
    centro_objetivo = random.choice(centros_aleatorios)
    vector_objetivo = texto_a_bipolar(generar_anillo(centro_x=centro_objetivo[0], centro_y=centro_objetivo[1]))
    
    # Aplicamos el reflejo rozando el borde superior izquierdo del anillo
    reflejo_x = centro_objetivo[0] - 1
    reflejo_y = centro_objetivo[1] - 1
    captura_con_ruido = aplicar_ruido_realista(vector_objetivo, reflejo_x, reflejo_y)
    
    print(">> MATRIZ ÓPTICA ENTRANTE (15x15 CON RUIDO FÍSICO) <<")
    print(bipolar_a_texto(captura_con_ruido))
    
    # 3. Filtrado neuronal
    print("[PROCESO] Aplicando filtro de memoria autoasociativa...")
    imagen_limpia = recuperar_patron(captura_con_ruido, matriz_sinaptica)
    
    print("\n>> MATRIZ LÓGICA RESTAURADA (15x15 IN SITU) <<")
    print(bipolar_a_texto(imagen_limpia))
    
    # 4. Reporte Final
    print("\n======================================================")
    print(" REPORTE DE EXTRACCIÓN DE COORDENADAS (ESCALA 1-15)")
    print("======================================================")
    
    resultado, certeza = identificar_pieza(imagen_limpia, base_de_datos)
    
    if resultado:
        # Sumamos 1 al índice para el conteo humano (1 al 15)
        coord_x_humana = resultado['centro_x'] + 1
        coord_y_humana = resultado['centro_y'] + 1
        
        print(f"[ ✓ ] ESTADO: PIEZA ENCONTRADA")
        print(f"[ i ] PRECISIÓN: {certeza * 100:.2f}%")
        print(f"[ ⌖ ] COORDENADAS DEL CENTRO (AGARRE):")
        print(f"      -> Eje X (Columnas): {coord_x_humana}")
        print(f"      -> Eje Y (Filas): {coord_y_humana}")
    else:
        print(f"[ X ] ESTADO: NO ENCONTRADO")
        print(">> ACCIÓN: Deteniendo ciclo. Pieza irreconocible.")