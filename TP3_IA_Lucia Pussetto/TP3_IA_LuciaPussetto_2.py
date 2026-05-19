import random

# =====================================================================
# 1. ENTRENAMIENTO DE LA MEMORIA (Red de Hopfield 5x5)
# =====================================================================

FORMA_ANILLO = [
    ".###.",
    "#...#",
    "#...#", # <-- Este '# ' central es el punto "A" (Centro de gravedad)
    "#...#",
    ".###."
]

FONDO_VACIO = [
    ".....",
    ".....",
    ".....",
    ".....",
    "....."
]

def texto_a_bipolar(patron_texto):
    return [1 if caracter == '#' else -1 for fila in patron_texto for caracter in fila]

def entrenar_hopfield(lista_patrones):
    """
    Aplica la Regla de Hebb para crear la "Memoria" de la red (Matriz Sináptica).
    
    ========================================================================
    REPRESENTACIÓN ESTRUCTURAL DE LA MATRIZ DE PESOS (25x25)
    ========================================================================
    Cada celda W(i,j) guarda la relación entre la Neurona de Origen (Fila i) 
    y la Neurona de Destino (Columna j).
    
           Destino(j):
           N0      N1      N2      N3      ...     N24 
         -----------------------------------------------
    N0  |   0     W0,1    W0,2    W0,3    ...     W0,24  |
    N1  |  W1,0    0      W1,2    W1,3    ...     W1,24  |
    N2  |  W2,0   W2,1     0      W2,3    ...     W2,24  |
    ... |  ...    ...     ...     ...     ...      ...   |
    N24 | W24,0  W24,1   W24,2   W24,3    ...       0    |
         -----------------------------------------------
    Origen(i)
    
    * LEYENDA MATEMÁTICA:
      - Diagonal en 0: Una neurona no se conecta a sí misma (i != j).
      - Simetría: La matriz es un espejo (W(i,j) == W(j,i)).
    ========================================================================
    """
    pesos = [[0] * 25 for _ in range(25)]
    for patron in lista_patrones: 
        for i in range(25):       
            for j in range(25):   
                if i != j: 
                    pesos[i][j] += patron[i] * patron[j] 
    return pesos

def limpiar_imagen_hopfield(vector_entrada, matriz_pesos):
    estado = list(vector_entrada) 
    indices = list(range(25))     
    for ciclo in range(10):       
        random.shuffle(indices)   
        hubo_cambios = False      
        for i in indices:         
            suma = sum(matriz_pesos[i][j] * estado[j] for j in range(25))
            nuevo_estado = 1 if suma >= 0 else -1
            if nuevo_estado != estado[i]: 
                estado[i] = nuevo_estado  
                hubo_cambios = True       
        if not hubo_cambios: 
            break 
    return estado

# =====================================================================
# 2. ENTORNO FÍSICO CARTESIANO 2D (Lienzo para 30x30 Lugares)
# =====================================================================

def generar_cinta(lugar_x, lugar_y, aplicar_ruido=False):
    cinta = [-1] * (34 * 34) 
    inicio_x = lugar_x - 1
    inicio_y = lugar_y - 1
    plantilla = texto_a_bipolar(FORMA_ANILLO) 
    
    for i in range(5):
        for j in range(5):
            cinta[(inicio_y + i) * 34 + (inicio_x + j)] = plantilla[i * 5 + j]
            
    if aplicar_ruido:
        # 10% de polvo ambiental en toda la lente
        for idx in random.sample(range(34 * 34), int(34 * 34 * 0.10)):
            cinta[idx] *= -1 
    return cinta

def imprimir_cinta_con_indicadores(cinta_bipolar, lugar_x=None, lugar_y=None):
    for i in range(34):
        fila_texto = ""
        for j in range(34):
            fila_texto += "█ " if cinta_bipolar[i * 34 + j] == 1 else ". "
        if lugar_y is not None and i == (lugar_y + 1):
            fila_texto += f"  <-- Eje Vertical (Y) [Arriba/Abajo]: {lugar_y}"
        print(fila_texto)
        
    if lugar_x is not None:
        indice_centro = lugar_x + 1 
        espacios = " " * (indice_centro * 2) 
        print(f"{espacios}^")
        print(f"{espacios}|__ Eje Horizontal (X) [Izquierda/Derecha]: {lugar_x}\n")

# =====================================================================
# 3. SISTEMA DE CONTROL: ESCANEO CARTESIANO OPTIMIZADO
# =====================================================================

if __name__ == "__main__":
    print("======================================================")
    print(" VISIÓN ARTIFICIAL: DETECCIÓN CARTESIANA 30x30 (TP3)")
    print("======================================================\n")
    
    print("[SISTEMA] Entrenando red de memoria autoasociativa...")
    patron_ideal = texto_a_bipolar(FORMA_ANILLO)
    patron_fondo = texto_a_bipolar(FONDO_VACIO) 
    
    matriz_sinaptica = entrenar_hopfield([patron_ideal, patron_fondo])
    
    lugar_real_x = random.randint(1, 30)
    lugar_real_y = random.randint(1, 30)

    cinta_capturada = generar_cinta(lugar_real_x, lugar_real_y, aplicar_ruido=True)
    
    print("\n>> CÁMARA INDUSTRIAL: PLANO CARTESIANO CON RUIDO <<")
    imprimir_cinta_con_indicadores(cinta_capturada) 
    
    print("\n[PROCESO] Iniciando escaneo Hopfield 2D Optimizado...")
    
    coordenada_encontrada = None
    similitud_maxima = 0.0 
    
    # LA VENTANA DESLIZANTE CON OPTIMIZACIÓN COMPUTACIONAL:
    for eval_y in range(1, 31):
        
        eval_x = 1 # Usamos un bucle while para poder manipular los saltos en X
        while eval_x <= 30:
            
            recorte_5x5 = [] 
            inicio_x = eval_x - 1 
            inicio_y = eval_y - 1 
            
            for i in range(5):
                for j in range(5):
                    recorte_5x5.append(cinta_capturada[(inicio_y + i) * 34 + (inicio_x + j)])
                    
            recorte_limpio = limpiar_imagen_hopfield(recorte_5x5, matriz_sinaptica)
            
            # --- VALIDACIÓN 1: ¿Es el Anillo? ---
            coincidencias_anillo = sum(1 for idx in range(25) if recorte_limpio[idx] == patron_ideal[idx])
            similitud_anillo = coincidencias_anillo / 25.0 
            
            if similitud_anillo >= 0.90:
                coordenada_encontrada = {"X": eval_x, "Y": eval_y}
                similitud_maxima = similitud_anillo
                break # OPTIMIZACIÓN 1: Early Stop. Detenemos la búsqueda en X
                
            # --- VALIDACIÓN 2: ¿Es un Fondo Vacío? ---
            coincidencias_fondo = sum(1 for idx in range(25) if recorte_limpio[idx] == patron_fondo[idx])
            similitud_fondo = coincidencias_fondo / 25.0
            
            if similitud_fondo >= 0.90:
                # OPTIMIZACIÓN 2: Salto Heurístico. 
                # Si esto es fondo puro, sabemos que el anillo no empieza aquí. 
                # Saltamos 3 espacios de golpe para ahorrar procesamiento.
                eval_x += 3
            else:
                # Si no es anillo ni fondo claro (hay ruido o bordes), avanzamos de a 1 paso.
                eval_x += 1
                
        # OPTIMIZACIÓN 1 (Continuación): Rompemos el ciclo Y si ya lo encontramos
        if coordenada_encontrada:
            break

    # =====================================================================
    # 4. REPORTE VISUAL Y LÓGICO FINAL
    # =====================================================================
    
    if coordenada_encontrada:
        cinta_limpia = generar_cinta(coordenada_encontrada["X"], coordenada_encontrada["Y"], aplicar_ruido=False)
        print("\n>> IA: IMAGEN RESTAURADA Y COORDENADAS CARTESIANAS IDENTIFICADAS <<")
        
        imprimir_cinta_con_indicadores(cinta_limpia, coordenada_encontrada["X"], coordenada_encontrada["Y"])
        
        print("=========================================")
        print(" REPORTE PARA EL CONTROLADOR DEL ROBOT")
        print("=========================================")
        print(f"[ ✓ ] IDENTIFICACIÓN EXITOSA (Confianza: {similitud_maxima*100:.1f}%).")
        print(f"[ ⌖ ] COORDENADAS DEL CENTRO 'A' (Plano 30x30):")
        print(f"      -> Eje Horizontal (X) : {coordenada_encontrada['X']}")
        print(f"      -> Eje Vertical   (Y) : {coordenada_encontrada['Y']}")
    else:
        print("\n[ X ] ERROR: Pieza no identificada. Nivel de ruido extremo.")