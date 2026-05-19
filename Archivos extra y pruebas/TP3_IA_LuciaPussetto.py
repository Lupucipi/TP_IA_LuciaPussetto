import random

# =====================================================================
# 1. ENTRENAMIENTO DE LA MEMORIA (Red de Hopfield 15x15)
# =====================================================================

# Morfología escalada a 15x15 (225 píxeles totales)
FORMA_ANILLO = [
    ".....#####.....",
    "...##.....##...",
    "..#.........#..",
    ".#...........#.",
    ".#...........#.",
    "#.............#",
    "#.............#",
    "#.............#", # <-- Este espacio central es el punto "A" (Centro de gravedad)
    "#.............#",
    "#.............#",
    ".#...........#.",
    ".#...........#.",
    "..#.........#..",
    "...##.....##...",
    ".....#####....."
]

# Fondo vacío adaptado a 15x15
FONDO_VACIO = [
    "...............",
    "...............",
    "...............",
    "...............",
    "...............",
    "...............",
    "...............",
    "...............",
    "...............",
    "...............",
    "...............",
    "...............",
    "...............",
    "...............",
    "..............."
]

def texto_a_bipolar(patron_texto):
    return [1 if caracter == '#' else -1 for fila in patron_texto for caracter in fila]

def entrenar_hopfield(lista_patrones):
    """
    Aplica la Regla de Hebb para crear la "Memoria" de la red (Matriz Sináptica).
    
    ========================================================================
    REPRESENTACIÓN ESTRUCTURAL DE LA MATRIZ DE PESOS (225x225)
    ========================================================================
    Cada celda W(i,j) guarda la relación entre la Neurona de Origen (Fila i) 
    y la Neurona de Destino (Columna j).
    
           Destino(j):
           N0      N1      N2      N3      ...     N224 
         -----------------------------------------------
    N0  |   0     W0,1    W0,2    W0,3    ...     W0,224 |
    N1  |  W1,0    0      W1,2    W1,3    ...     W1,224 |
    N2  |  W2,0   W2,1     0      W2,3    ...     W2,224 |
    ... |  ...    ...     ...     ...     ...      ...    |
    N224| W224,0 W224,1  W224,2  W224,3   ...       0    |
         -----------------------------------------------
    Origen(i)
    
    * LEYENDA MATEMÁTICA:
      - Diagonal en 0: Una neurona no se conecta a sí misma (i != j).
      - Simetría: La matriz es un espejo (W(i,j) == W(j,i)).
    ========================================================================
    """
    pesos = [[0] * 225 for _ in range(225)]
    for patron in lista_patrones: 
        for i in range(225):       
            for j in range(225):   
                if i != j: 
                    pesos[i][j] += patron[i] * patron[j] 
    return pesos

def limpiar_imagen_hopfield(vector_entrada, matriz_pesos):
    estado = list(vector_entrada) 
    indices = list(range(225))     
    for ciclo in range(10):       
        random.shuffle(indices)   
        hubo_cambios = False      
        for i in indices:         
            suma = sum(matriz_pesos[i][j] * estado[j] for j in range(225))
            nuevo_estado = 1 if suma >= 0 else -1
            if nuevo_estado != estado[i]: 
                estado[i] = nuevo_estado  
                hubo_cambios = True       
        if not hubo_cambios: 
            break 
    return estado

# =====================================================================
# 2. ENTORNO FÍSICO CARTESIANO 2D (Lienzo para 100x100 Lugares)
# =====================================================================

def generar_cinta(lugar_x, lugar_y, aplicar_ruido=False):
    """
    Genera el lienzo cartesiano gigante de la cámara.
    Para soportar centros del 1 al 100 con una pieza de 15x15, 
    necesitamos un lienzo de 114x114 (7 píxeles de margen en cada extremo).
    """
    cinta = [-1] * (114 * 114) 
    inicio_x = lugar_x - 1
    inicio_y = lugar_y - 1
    plantilla = texto_a_bipolar(FORMA_ANILLO) 
    
    for i in range(15):
        for j in range(15):
            cinta[(inicio_y + i) * 114 + (inicio_x + j)] = plantilla[i * 15 + j]
            
    if aplicar_ruido:
        # 5% de polvo ambiental en toda la cuadrícula (Más de 600 píxeles de ruido)
        for idx in random.sample(range(114 * 114), int(114 * 114 * 0.05)):
            cinta[idx] *= -1 
    return cinta

def imprimir_cinta_con_indicadores(cinta_bipolar, lugar_x=None, lugar_y=None):
    for i in range(114):
        fila_texto = ""
        for j in range(114):
            fila_texto += "█ " if cinta_bipolar[i * 114 + j] == 1 else ". "
        if lugar_y is not None and i == (lugar_y + 7): # +7 para alinear el indicador lateral con el centro exacto
            fila_texto += f"  <-- Eje Vertical (Y) [Arriba/Abajo]: {lugar_y}"
        print(fila_texto)
        
    if lugar_x is not None:
        indice_centro = lugar_x + 7 # +7 al índice porque el centro de la pieza está en el medio de sus 15 px
        espacios = " " * (indice_centro * 2) 
        print(f"{espacios}^")
        print(f"{espacios}|__ Eje Horizontal (X) [Izquierda/Derecha]: {lugar_x}\n")

# =====================================================================
# 3. SISTEMA DE CONTROL: ESCANEO CARTESIANO OPTIMIZADO (100x100)
# =====================================================================

if __name__ == "__main__":
    print("======================================================")
    print(" VISIÓN ARTIFICIAL: DETECCIÓN CARTESIANA 100x100 (TP3)")
    print("======================================================\n")
    
    print("[SISTEMA] Entrenando red neuronal de 225 neuronas y 50,625 sinapsis...")
    patron_ideal = texto_a_bipolar(FORMA_ANILLO)
    patron_fondo = texto_a_bipolar(FONDO_VACIO) 
    
    matriz_sinaptica = entrenar_hopfield([patron_ideal, patron_fondo])
    
    lugar_real_x = random.randint(1, 100)
    lugar_real_y = random.randint(1, 100)

    cinta_capturada = generar_cinta(lugar_real_x, lugar_real_y, aplicar_ruido=True)
    
    print("\n>> CÁMARA INDUSTRIAL: PLANO CARTESIANO CON RUIDO <<")
    imprimir_cinta_con_indicadores(cinta_capturada) 
    
    print("\n[PROCESO] Iniciando escaneo Hopfield 2D Optimizado (Hasta 10,000 cuadrantes)...")
    
    coordenada_encontrada = None
    similitud_maxima = 0.0 
    
    # LA VENTANA DESLIZANTE CON OPTIMIZACIÓN COMPUTACIONAL MASIVA:
    for eval_y in range(1, 101):
        
        eval_x = 1 
        while eval_x <= 100:
            
            recorte_15x15 = [] 
            inicio_x = eval_x - 1 
            inicio_y = eval_y - 1 
            
            for i in range(15):
                for j in range(15):
                    recorte_15x15.append(cinta_capturada[(inicio_y + i) * 114 + (inicio_x + j)])
                    
            recorte_limpio = limpiar_imagen_hopfield(recorte_15x15, matriz_sinaptica)
            
            # --- VALIDACIÓN 1: ¿Es el Anillo? ---
            coincidencias_anillo = sum(1 for idx in range(225) if recorte_limpio[idx] == patron_ideal[idx])
            similitud_anillo = coincidencias_anillo / 225.0 
            
            if similitud_anillo >= 0.90:
                coordenada_encontrada = {"X": eval_x, "Y": eval_y}
                similitud_maxima = similitud_anillo
                break # OPTIMIZACIÓN 1: Early Stop. Detenemos la búsqueda en X
                
            # --- VALIDACIÓN 2: ¿Es un Fondo Vacío? ---
            coincidencias_fondo = sum(1 for idx in range(225) if recorte_limpio[idx] == patron_fondo[idx])
            similitud_fondo = coincidencias_fondo / 225.0
            
            if similitud_fondo >= 0.90:
                # OPTIMIZACIÓN 2: Salto Heurístico. 
                # Como nuestra pieza mide 15 píxeles de ancho, si vemos vacío puro
                # podemos saltarnos 10 lugares de forma 100% segura.
                eval_x += 10
            else:
                # Si vemos bordes o ruido que confunde, avanzamos con cautela (1 paso)
                eval_x += 1
                
        if coordenada_encontrada:
            break

    # =====================================================================
    # 4. REPORTE VISUAL Y LÓGICO FINAL
    # =====================================================================
    
    if coordenada_encontrada:
        cinta_limpia = generar_cinta(coordenada_encontrada["X"], coordenada_encontrada["Y"], aplicar_ruido=False)
        print("\n>> IA: IMAGEN RESTAURADA Y COORDENADAS CARTESIANAS IDENTIFICADAS <<")
        
        imprimir_cinta_con_indicadores(cinta_limpia, coordenada_encontrada["X"], coordenada_encontrada["Y"])
        
        print("======================================================")
        print(" REPORTE PARA EL CONTROLADOR DEL ROBOT")
        print("======================================================")
        print(f"[ ✓ ] IDENTIFICACIÓN EXITOSA (Confianza: {similitud_maxima*100:.1f}%).")
        print(f"[ ⌖ ] COORDENADAS DEL CENTRO 'A' (Plano 100x100):")
        print(f"      -> Eje Horizontal (X) : {coordenada_encontrada['X']}")
        print(f"      -> Eje Vertical   (Y) : {coordenada_encontrada['Y']}")
        print(f">> ACCIÓN: Inyectando variables Cartesianas (X={coordenada_encontrada['X']}, Y={coordenada_encontrada['Y']}) al script A*.")
    else:
        print("\n[ X ] ERROR: Pieza no identificada. Nivel de ruido extremo.")