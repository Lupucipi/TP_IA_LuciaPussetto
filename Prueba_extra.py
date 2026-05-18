import random

# =====================================================================
# 1. PATRONES DE ALTA RESOLUCIÓN (10x10 = 100 Neuronas)
# Al tener más píxeles, podemos hacer formas mucho más únicas y curvas.
# =====================================================================

VOCALES_10x10 = {
    "E": [
        ".########.",
        ".##.......",
        ".##.......",
        ".######...",
        ".######...",
        ".##.......",
        ".##.......",
        ".##.......",
        ".########.",
        ".........."
    ],
    "I": [
        ".########.",
        "....##....",
        "....##....",
        "....##....",
        "....##....",
        "....##....",
        "....##....",
        "....##....",
        ".########.",
        ".........."
    ],
    "O": [
        "...####...",
        "..##..##..",
        ".##....##.",
        ".##....##.",
        ".##....##.",
        ".##....##.",
        ".##....##.",
        "..##..##..",
        "...####...",
        ".........."
    ]
}

# =====================================================================
# 2. FUNCIONES AUXILIARES (Ajustadas a 100 iteraciones)
# =====================================================================

def texto_a_bipolar(patron_texto):
    return [1 if caracter == '#' else -1 for fila in patron_texto for caracter in fila]

def bipolar_a_texto(vector_bipolar):
    texto = ""
    for i in range(100):
        texto += "█ " if vector_bipolar[i] == 1 else ". "
        if (i + 1) % 10 == 0: texto += "\n"
    return texto

def aplicar_ruido(vector_original, porcentaje_ruido):
    vector_ruidoso = list(vector_original)
    cantidad = int(100 * porcentaje_ruido)
    indices = random.sample(range(100), cantidad)
    for idx in indices:
        vector_ruidoso[idx] *= -1 
    return vector_ruidoso

# =====================================================================
# 3. NÚCLEO DE HOPFIELD Y CÁLCULO DE ENERGÍA (100 Neuronas)
# =====================================================================

def entrenar_red(lista_patrones):
    pesos = [[0] * 100 for _ in range(100)]
    for patron in lista_patrones:
        for i in range(100):
            for j in range(100):
                if i != j: 
                    pesos[i][j] += patron[i] * patron[j]
    return pesos

def calcular_energia(estado_actual, matriz_pesos):
    energia = 0
    for i in range(100):
        for j in range(100):
            energia += matriz_pesos[i][j] * estado_actual[i] * estado_actual[j]
    return -0.5 * energia

def recuperar_patron(vector_entrada, matriz_pesos, iteraciones_max=10):
    estado = list(vector_entrada)
    indices = list(range(100))
    
    print(f"   -> Energía inicial (Con Ruido): {calcular_energia(estado, matriz_pesos)}")
    
    for ciclo in range(iteraciones_max):
        random.shuffle(indices)
        hubo_cambios = False
        
        for i in indices:
            suma = sum(matriz_pesos[i][j] * estado[j] for j in range(100))
            nuevo_estado = 1 if suma >= 0 else -1
            if nuevo_estado != estado[i]:
                estado[i] = nuevo_estado
                hubo_cambios = True
                
        energia_actual = calcular_energia(estado, matriz_pesos)
        print(f"   -> Energía tras ciclo {ciclo + 1}: {energia_actual}")
        
        if not hubo_cambios:
            print(f"[INFO] Sistema estabilizado (Atractor encontrado).")
            break
            
    return estado

def identificar_letra(vector_recuperado, base_datos_vocales, umbral_tolerancia=0.85):
    mejor_letra = None
    max_similitud = 0.0
    for letra, vector_ideal in base_datos_vocales.items():
        coincidencias = sum(1 for i in range(100) if vector_recuperado[i] == vector_ideal[i])
        similitud = coincidencias / 100.0
        if similitud > max_similitud:
            max_similitud = similitud
            mejor_letra = letra
            
    if max_similitud >= umbral_tolerancia:
        return mejor_letra, max_similitud
    return None, max_similitud

# =====================================================================
# 4. SIMULACIÓN EDUCATIVA
# =====================================================================

if __name__ == "__main__":
    print("======================================================")
    print(" LABORATORIO HOPFIELD: ALTA RESOLUCIÓN (10x10)")
    print("======================================================\n")
    
    base_datos_bipolar = {letra: texto_a_bipolar(dibujo) for letra, dibujo in VOCALES_10x10.items()}
    
    print("[SISTEMA] Entrenando matriz sináptica (10,000 conexiones)...")
    matriz_sinaptica = entrenar_red(base_datos_bipolar.values())
    
    letra_usuario = input("\n>> Ingresa una vocal (A, E, I, O, U): ").upper()
    
    if letra_usuario in base_datos_bipolar:
        vector_ideal = base_datos_bipolar[letra_usuario]
        
        # Con 100 neuronas, podemos darnos el lujo de aplicar un enorme 30% de ruido
        print("\n[PROCESO] Aplicando 30% de ruido físico al sensor...")
        captura_ruidosa = aplicar_ruido(vector_ideal, porcentaje_ruido=0.10)
        
        print("\n>> IMAGEN DEL SENSOR (10x10 CON RUIDO) <<")
        print(bipolar_a_texto(captura_ruidosa))
        
        print("\n[PROCESO] Ejecutando memoria autoasociativa...")
        imagen_recuperada = recuperar_patron(captura_ruidosa, matriz_sinaptica)
        
        print("\n>> IMAGEN RESTAURADA (10x10) <<")
        print(bipolar_a_texto(imagen_recuperada))
        
        resultado, confianza = identificar_letra(imagen_recuperada, base_datos_bipolar)
        
        if resultado:
            print(f"[ ✓ ] LECTURA CONFIRMADA: Letra '{resultado}'")
            print(f"[ i ] SIMILITUD DE PÍXELES: {confianza * 100:.2f}%")
        else:
            print(f"[ X ] FALLO CRÍTICO.")
    else:
        print("Letra no válida.")