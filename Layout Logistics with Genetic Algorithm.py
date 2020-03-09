import numpy as np
import math
import Ejercicio_2_2 as E2
import Ejercicio_3 as E3
import random as rd


def Temple_Simulado(temperatura, temp_inicial, temp_final, factor_enf, cant_pedidos, costo_anterior,
                    mat, pedidos1, filas, columnas):                                      # MAIN DEL EJERCICIO_3
    all_costos = []
    all_caminos = []
    j = 0

    while temperatura > temp_final:
        j += 1
        print("\n\n--------------- COMIENZA TEMPLE SIMULADO PARA LISTA ALEATORIA N°:", j, "---------------")
        print("Lista de pedidos:", pedidos1)
        pedidos = E3.random_vecinos(pedidos1, cant_pedidos)
        costo_nuevo = E3.dist_total(pedidos, mat, filas, columnas)
        print("---- END TEMPLE SIMULADO PARA LA LISTA ALEATORIA N°:", j, "----")
        print("Distancia total recorrida entre todos los pedidos: ", costo_nuevo)
        all_caminos.append([pedidos])

        diferencia = costo_nuevo - costo_anterior
        if diferencia < 0 or np.e ** (-diferencia / temperatura) > rd.uniform(0, 1):
            costo_anterior = costo_nuevo
        temperatura = temperatura * factor_enf
        all_costos.append(costo_nuevo)
        print("\n")

    min_index = np.argmin(all_costos)
    great_costs = all_costos[min_index]
    great_way = all_caminos[min_index]

    print("---- BIG END TEMPLE SIMULADO ----")

    print("Costo de todos los caminos observados: ", all_costos)
    print("Caminos observados: ", j)
    print("El mejor camino es el número: ", min_index + 1)
    print("Mejor costo: ", great_costs)
    print("Mejor camino: \n", np.array(great_way))
    print("Temperatura inicial: ", temp_inicial)
    print("Temperatura final: ", temp_final)
    print("Factor de enfriamiento: ", factor_enf)

    return great_costs


def crear_indiv_random(filas, columnas):            # Crea matrices random
    c = list(range(1, (filas * columnas)+1))
    vect_rand = rd.sample(c, (filas * columnas))    # Vector sin que se repitan valores
    k = 0
    mat_rand = np.zeros((filas, columnas))
    while k < filas * columnas:
        for i in range(filas):
            for j in range(columnas):
                mat_rand[i][j] = vect_rand[k]       # Lleno una matriz con ese vector sin valores repetidos
                k += 1
    return mat_rand


def dist_total_all_temple(pedidos1, mat, cant_pedidos, temperatura, temp_inicial, temp_final,
                          factor_enf, costo_anterior, filas, columnas):                             # Saca Temple para todas las listas de pedidos para un individuo específico
    fitness = 0                                                                # y suma todas las distancias que dio el Temple en una variable fitness
    j = 0
    for i in range(len(pedidos1)):
        j += 1
        if j < len(pedidos1):
            print("La lista de pedidos n°:", i, "es:", pedidos1[i])
            fitness += Temple_Simulado(temperatura, temp_inicial, temp_final, factor_enf, cant_pedidos,
                                                            costo_anterior, mat, pedidos1[i], filas, columnas)
    return fitness


def crossover(individuos_ordenados, filas, columnas):           # Crossover y mutación
    seed1 = np.arange(1, columnas)
    corte1 = np.random.choice(seed1, 1)                     # Se selecciona el lugar del corte de manera random
    corte1 = int(corte1)
    t = 0

    while t < len(individuos_ordenados):                    # t selecciona un individuo a la vez, salteando cada 2
        for i in range(filas):
            for j in range(corte1, columnas):
                individuos_ordenados[t][i][j], individuos_ordenados[t + 1][i][j] = \
                    individuos_ordenados[t + 1][i][j], individuos_ordenados[t][i][j]    # Intercambio de lados derechos por izq y de izq por derechos de la 1° y 2° matriz (individuo)
        t += 2

    cc = list(range(1, (filas * columnas) + 1))
    print("Lista para averiguar los números que faltan: ", cc)      # Lista con todos los números que debería tener la matriz, para averiguar los números que faltan

    for t in range(len(individuos_ordenados)):
        vect1 = []      # Vector para guardar lados izquierdos
        vect2 = []      # Vector para guardar lados derechos
        vect = []       # Vector para guardar toda la matriz ya cruzada
        vectf = []      # Vector para guardar los números que faltan
        for j in range(filas):
            for i in range(0, corte1):
                vect1.append(individuos_ordenados[t][j][i])     # Guardamos los de la izquierda
            for i in range(corte1, columnas):
                vect2.append(individuos_ordenados[t][j][i])     # Guardamos los de la derecha
            for i in range(columnas):
                vect.append(individuos_ordenados[t][j][i])      # Guardamos todos

        for i in range(len(cc)):
            flag = 0
            for j in range(len(vect)):
                if cc[i] == vect[j]:                # Si en el vector de todos los números falta uno, flag se hace uno y entonces se agreaga ese faltante al vectf
                    flag = 1
            if flag == 0:
                vectf.append(cc[i])                 # Números que faltan en vectf
        print("Números que faltan: ", vectf)
        print("Números de la izquierda: ", vect1)
        print("Números de la derecha: ", vect2)

        k = 0
        while k < len(vectf):                       # Acá se ve si en el vector de la derecha hay números repetidos que ya tiene la parte izquierda
            for i in range(len(vect1)):
                for j in range(len(vect2)):
                    if vect1[i] == vect2[j]:
                        vect1[i] = vectf[k]         # Si hay algún repetido, lo reemplaza por uno faltante
                        k += 1
        print("Vector de la izquierda arreglado: ", vect1)

        k = 0
        l = 0
        for i in range(filas):                      # Se transforman los vectores 1 y 2 de nuevo en una matriz con sus posiciones correspondientes
            for j in range(0, corte1):
                individuos_ordenados[t][i][j] = vect1[k]
                k += 1
            for j in range(corte1, columnas):
                individuos_ordenados[t][i][j] = vect2[l]
                l += 1
        print("\nMatriz arreglada, sin repeticiones: \n", individuos_ordenados[t])
        print("\n\n")

        seed2 = np.arange(1, filas * columnas)                      # MUTACIÓN
        mut_val1 = np.random.choice(seed2, 1)                        # Se eligen dos indices random y se los intercambia entre si
        mut_val2 = np.random.choice(seed2, 1)
        mut_pos1 = E2.paso_a_pos(mut_val1, filas, columnas, individuos_ordenados[t])
        mut_pos2 = E2.paso_a_pos(mut_val2, filas, columnas, individuos_ordenados[t])
        individuos_ordenados[t][mut_pos1[0]][mut_pos1[1]], individuos_ordenados[t][mut_pos2[0]][mut_pos2[1]] = \
            individuos_ordenados[t][mut_pos2[0]][mut_pos2[1]], individuos_ordenados[t][mut_pos1[0]][mut_pos1[1]]

    print("Matrices arreglada, sin repeticiones y con mutación: \n", np.array(individuos_ordenados))
    return individuos_ordenados


if __name__ == "__main__":

    # --VARIABLES PARA ASTAR--
    filas = 12
    columnas = 6
    mat = E2.createMatriz(filas, columnas)              # Creamos la matriz inicial (sólo se usa para observar su diferencia con las demás)
    print("Matriz inicial: \n", mat, "\n\n")

    # --VARIABLES PARA TEMPLE--
    cant_pedidos = 10                                   # Cantidad de pedidos en una lista
    temp_inicial = 20
    temp_final = 0.01
    factor_enf = 0.9
    temperatura = temp_inicial
    costo_anterior = 100

    # --VARIABLES PARA ALG GEN--
    listas_pedidos = []
    individuos = []
    cant_listas_pedidos = 5                             # Cantidad de listas de pedidos de año anterior
    cant_individuos = 4                                 # Cantidad de individuos (matrices individuos) DEBE SER UN NÚMERO PAR

    for i in range(cant_listas_pedidos):                # Creamos listas de pedidos momentáneamente con bahía igual a 1
        listas_pedidos.append(E3.crear_lista_pedidos(cant_pedidos, filas, columnas, bahia_carga=1))
    print("Listas de pedidos (short) del año: \n", np.array(listas_pedidos), "\n\n")

    for i in range(cant_individuos):                    # Creamos los individuos (matrices random)
        individuos.append(crear_indiv_random(filas, columnas))
    print("Individuos: \n", np.array(individuos), "\n\n")

    fitness_porcentaje = []
    for i in range(cant_individuos):                    # Asignamos un fitness normalizado igual a 30 para que sentre al while
        fitness_porcentaje.append(30)
    h = 0
    while (fitness_porcentaje[0] > 22) or (h < 10):     # La h es un contador de iteraciones
        h += 1
        fitness = []

        for i in range(cant_individuos):                                                                                # Aquí utilizamos Temple simulado
            print("\nTEMPLE SIMULADO CON EL INDIV N°:", i + 1)                                                          # La i hace referencia a cada matriz (individuo)
            bahia_carga = E2.paso_a_valor([0, 0], filas, columnas, individuos[i])                                       # Pasamos a valor la posición [0,0] que contiene la nueva bahía
            print("BAHÍA DE CARGA:", bahia_carga)
            fitness.append(dist_total_all_temple(listas_pedidos, individuos[i], cant_pedidos, temperatura, temp_inicial,
                                                 temp_final, factor_enf, costo_anterior, filas, columnas))              # Utilizamos la función dist_total_all_temple para sacar el
            print("\n---- BIG END TEMPLE SIMULADO CON EL INDIV N°", i + 1, "----")                                      # fitness de cada individuo
            print("Distancia total recorrida entre todos los pedidos: ", fitness[i], "en el individuo n°: ", i + 1)

        print("\n\n----- START ALGORITMO GENÉTICO -----")
        print("Funciones fitness de los individuos: ", fitness)
        min_index = []
        dist_all_temples = fitness.copy()

        for i in range(len(dist_all_temples)):                                      # Obtenemos los índices ordenados del mejor al peor fitness
            min_index.append(np.argmin(dist_all_temples))
            dist_all_temples[min_index[i]] = dist_all_temples[min_index[i]] * 100
        print("Indices ordenados: ", min_index)
        fitness.sort()                                                              # Ordenamos el vector fitness de menor a mayor
        print("Funciones fitness de los individuos ordenados: ", fitness)
        fitness_total = 0
        fitness_porcentaje = fitness.copy()

        for i in range(len(fitness)):                                               # Normalizamos el vector fitness
            fitness_total += fitness[i]
        for i in range(len(fitness)):
            fitness_porcentaje[i] = (fitness[i]/fitness_total) * 100
        print("Porcentaje de fitnes total: ", fitness_porcentaje)

        individuos_ordenados = individuos.copy()
        for i in range(len(min_index)):                                             # Ordenamos la matriz de individuos, del mejor indiv al peor
            individuos_ordenados[i] = individuos[min_index[i]]
        print("Individuos ordenados:\n", np.array(individuos_ordenados))

        for i in range(len(individuos_ordenados)):                                  # Se aplica un filtro para los individuos muy malos, se los reemplaza por el mejor indiv
            if fitness_porcentaje[i] > 30:
                individuos_ordenados[i] = individuos_ordenados[0].copy()

        individuos = crossover(individuos_ordenados, filas, columnas)               # Se realiza el crossover y la mutación, (También se actualiza la matriz de (matrices) individuos)

    print("\n\n---- END ALGORITMO GENÉTICO ----")                                       # Imprimimos los datos relevantes
    print("Los mejores individuos son: \n", np.array(individuos_ordenados))
    print("\nEl mejor individuo es: \n", individuos_ordenados[0])
    print("\nEl fitness de este individuo es: ", fitness[0])
    print("El fitness normalizado de este individuo es: ", fitness_porcentaje[0])





