import numpy as np
import math
import Ejercicio_2_2 as E2
import random as rd
import matplotlib.pyplot as plt

def AStar(val_inicial, val_final, mat, filas, columnas):            # MAIN DEL EJERCICIO_2_2
    pos_mov = []
    valor_mov = []
    dist_recorrida = []

    pos_inicial = E2.paso_a_pos(val_inicial, filas, columnas, mat)
    pos_final = E2.paso_a_pos(val_final, filas, columnas, mat)

    pos_mov.append(pos_inicial.copy())

    pos, pos_mov = E2.Mov_Heurist(pos_inicial, pos_final)

    for i in range(len(pos_mov)):
        valor_mov.append(E2.paso_a_valor(pos_mov[i], filas, columnas, mat))
        if i > 0:
            if (pos_mov[i][0] != pos_mov[i - 1][0]) and \
                    (pos_mov[i][1] != pos_mov[i - 1][1]):
                dist_recorrida.append(math.sqrt(2))
            else:
                dist_recorrida.append(1)

    dist = E2.H(pos_inicial, pos_final)
    dist_final = 0
    for i in range(len(dist_recorrida)):
        dist_final += dist_recorrida[i]
    pos_val = E2.paso_a_valor(pos, filas, columnas, mat)

    print("Valor inicial:", val_inicial)
    print("Posición inicial:", pos_inicial)
    #print("Movimientos realizados:\n", np.array([pos_mov]))
    #print("Valores de los movimientos realizados:", np.array(valor_mov))
    print("Distancia entre punto inicial y final (pitágoras):", dist)
    print("Distancia que se recorrió:", dist_final)
    #print("Valor final esperado:", val_final)
    #print("Posición final esperada:", pos_final)
    print("Valor final encontrado:", int(pos_val))
    print("Posición final encontrada:", pos)
    print("\n")

    return dist_final


def crear_lista_pedidos(cant, filas, columnas, bahia_carga):                # Creamos lista de pedidos random
    pedidos = []
    for i in range(cant):
        pedidos.append(rd.randint(1, filas * columnas))                     # Random con valores que si se pueden repetir
    pedidos = np.concatenate([[bahia_carga], pedidos, [bahia_carga]])       # Agregamos la bahía de carga al principio y al final
    return pedidos


def random_vecinos(pedidos, cant):                                                  # Esta función intercambia valores de la lista de pedidos contiguos
    seed1 = np.arange(1, cant)
    indice = np.random.choice(seed1, 1)                                             # Selecciona el indice del producto a intercambiar por su vecino derecho (no incluye a la bahía)
    print("Pedido anterior:", np.array(pedidos))
    pedidos[indice], pedidos[indice + 1] = pedidos[indice + 1], pedidos[indice]     # Se produce el intercambio
    print("Pedido vecino nuevo:", np.array(pedidos))
    return pedidos


def dist_total(pos_pedidos, mat,  filas, columnas):                                     # Esta función saca A estrella, cada posición i es la posición inicial y su
    dist = 0                                                                    # vecino de la derecha es la posición final, luego suma todos estos resultados en una variable (dist)
    j = 0
    for i in range(len(pos_pedidos)):
        j += 1
        if j < len(pos_pedidos):
            print("--- ASTAR PARA EL PEDIDO N°:", j - 1, "---")
            dist += AStar(pos_pedidos[i], pos_pedidos[i+1], mat, filas, columnas)
    return dist


if __name__ == "__main__":

    all_costos = []
    all_caminos = []
    all_costos_ynoacep = []
    all_caminos_ynoacep = []

    #filas = input('Ingrese número de filas (preferentemente múltiplo de 4):')
    #print("Número de filas: ", filas)
    #columnas = input('Ingrese número de columnas (debe ser un número par):')
    #print("Número de columnas: ", columnas)
    #cant = input('Ingrese cabtidad de pedidos:')
    #print("Cantidad de pedidos: ", cant)
    #temp_inicial = input('Ingrese Temperatura inicial:')
    #print("Temperatura inicial: ", temp_inicial)
    #temp_final = input('Ingrese Temperatura final:')
    #print("Temperatura final: ", temp_final)
    #factor_enf = input('Ingrese factor de enfriamiento:')
    #print("Factor de enfriamiento: ", factor_enf)

    #filas = int(filas)
    #columnas = int(columnas)
    #temp_inicial = int(temp_inicial)
    #temp_final = int(temp_final)
    #factor_enf = int(factor_enf)

    # --VARIABLES PARA ASTAR--
    filas = 12
    columnas = 6
    mat = E2.createMatriz(filas, columnas)                              # Creamos la matriz
    print("Matriz inicial: \n", mat, "\n\n")

    # --VARIABLES PARA TEMPLE--
    cant = 10                               # Cantidad de pedidos
    temp_inicial = 20
    temp_final = 0.01
    factor_enf = 0.9                        # Factor de enfriamiento
    temperatura = temp_inicial
    costo_anterior = 100
    bahia_carga = E2.paso_a_valor([0, 0], filas, columnas, mat)         # Creamos la bahía de carga que en este caso va a ser 1, porque en la posición [0, 0] de la matriz mat hay un 1
    pedidos = crear_lista_pedidos(cant, filas, columnas, bahia_carga)   # Creamos una lista de pedidos aleatoria

    j = 0
    it = []
    count = 0
    it1 = []
    count1 = 0
    while temperatura > temp_final:
        j += 1

        print("\n\n--------------- COMIENZA TEMPLE SIMULADO PARA LA MODIFICACIÓN N°:", j, " DE LA LISTA---------------")
        pedidos = random_vecinos(pedidos, cant)                                     # Cambiamos de lugar 2 números contiguos dentro de la lista
        costo_nuevo = dist_total(pedidos, mat, filas, columnas)                     # Se saca el costo, es decir la distancia que recorremos al recoger todos los pedidos
        print("---- END TEMPLE SIMULADO PARA LA MODIFICACIÓN N°:", j, " DE LA LISTA ----")     # Partiendo de la bahia de carga y regresando allí al finalizar
        print("Distancia total recorrida entre todos los pedidos: ", costo_nuevo)

        diferencia = costo_nuevo - costo_anterior                                   # Se observa si el costo nuevo es mejor que el anterior (si es mejor, diferencia es negativo)
        if diferencia < 0 or np.e ** (-diferencia/temperatura) > rd.uniform(0, 1):  # Si diferencia es negativo, o si la función e es mayor a un número entre 0 y 1
            costo_anterior = costo_nuevo                                            #   se toma a costo nuevo como costo anterior
            all_caminos.append([pedidos])               # Guardamos la lista modificada (y aceptada) en la lista de todos los caminos (modificaciones aceptadas)
            all_costos.append(costo_nuevo)              # Se agrega el costo del nuevo camino aceptado a la lista de todos los costos
            count += 1
            it.append(count1)
        all_caminos_ynoacep.append([pedidos])  # Guardamos la lista modificada (y aceptada) en la lista de todos los caminos (modificaciones aceptadas)
        all_costos_ynoacep.append(costo_nuevo)  # Se agrega el costo del nuevo camino aceptado a la lista de todos los costos
        count1 += 1
        it1.append(count)
        temperatura = temperatura * factor_enf          # Se enfria (desciende) la temperatura
        print("\n")

    min_index = np.argmin(all_costos)                   # Tomamos el índice del menor costo
    great_costs = all_costos[min_index]                 # Con ese índice tomamos el mejor costo
    great_way = all_caminos[min_index]                  # Con ese índice tomamos la mejor lista modificada (camino)

    print("---- BIG END TEMPLE SIMULADO----")           # Imprimimos los datos relevantes

    print("Caminos observados: ", j)
    print("Costo de todos los caminos aceptados: ", all_costos)
    print("El mejor camino es el número: ", min_index + 1)
    print("Mejor costo: ", great_costs)
    print("Mejor camino: \n", np.array(great_way))
    print("Temperatura inicial: ", temp_inicial)
    print("Temperatura final: ", temp_final)
    print("Factor de enfriamiento: ", factor_enf)

    mov11 = []
    for i in range(len(all_costos_ynoacep)):
        mov11.append(all_costos_ynoacep[i])
    plt.plot(it1, mov11, 'bo-')
    plt.show()

    mov1 = []
    for i in range(len(all_costos)):
        mov1.append(all_costos[i])
    plt.plot(it, mov1, 'ro-')
    plt.show()
