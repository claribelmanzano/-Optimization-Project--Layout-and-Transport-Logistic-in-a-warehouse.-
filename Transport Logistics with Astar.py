import numpy as np
import math
import matplotlib.pyplot as plt


def createMatriz(filas, columnas):                   # Se crea la matriz
    x = []
    for i in range(columnas - 1):                    # Creamos un vector (x) de números pares 2, 4, 6 , 8... según el número de columnas
        if i % 2 == 0:
            x.append(i)

    matriz = np.zeros((filas, columnas))
    j = 1
    while j < filas*columnas:                       # j va de 1 a 16 si la matriz es de 4*4
        for k in x:                                 # k va de 2 en 2 según x
            for i in range(filas):                  # i recorre las filas
                matriz[i, k] = j                    # así ordenamos la matriz como se indica en el tp
                matriz[i, k + 1] = j + 1
                j += 2
    return matriz


def paso_a_pos(valor, filas, columnas, mat):        # Pasa de valor 1, 2, 3, 4, ..., m*n a coordenadas [0, 0], [1, 0], ..., [m, n]
    for i in range(filas):                          # Se recorre toda la matriz hasta que se llega al número igual a valor y se entrega la posición de la fila y de la columna
        for j in range(columnas):
                    if mat[i, j] == valor:
                        return [i, j]


def paso_a_valor(pos, filas, columnas, mat):        # Pasa de coordenadas [0, 0], [1, 0], ..., [m, n] a valor 1, 2, 3, 4, ..., m*n
    for i in range(filas):                          # Si i y j coinciden con las coordenadas de esa posición (pos), se devuelve el valor de la matriz en esa coordenada
        for j in range(columnas):
            if (pos[0] == i) & (pos[1] == j):
                return mat[i, j]


def H(pos, pos_final):                              # Se hace pitágoras entre la posición actual y la final
    if (pos_final[0] - pos[0] == 0) and (pos_final[1] - pos[1] == 0):
        return 0                                    # Si la pos actual y la final son iguales se devuelve un cero (daba error al querer sacarle raiz cuadrada al cero)
    else:
        return math.sqrt((pos_final[0] - pos[0]) ** 2 + (pos_final[1] - pos[1]) ** 2)


def G(esq):
    if esq == 0:
        return 1                                    # Se devuelve un 1 si nos movemos hacia arriba - abajo - derecha - izquierda
    if esq == 1:
        return math.sqrt(2)                         # Se devuelve la raiz cuadrada de 2 si nos movemos hacia una esquina


def F(pos, esq, pos_f):                             # F = H + G
    return H(pos, pos_f) + G(esq)


def Mov_Heurist (pos_inicial, pos_final):              # Movimiento según la función heurística

    pos_mov = []
    pos = pos_inicial.copy()
    # print("Estamos en:", pos, "y la posición final es:", pos_final, ".\n")
    pos_mov.append(pos_inicial.copy())              # Agrega la posición inicial al principio del vector de movimientos (que está en coordenadas)

    while not (np.array_equal(pos, pos_final)):
        hijos = []                                  # Reseteo de matriz hijos.
        resultados = []                             # Reseteo de matriz resultados.
        step = 1
        for i in range(len(pos)):

            esq = 0                                 # No nos movemos a una esquina
            pos_sup = pos.copy()                    # Igualamos pos_sup a la posición seleccionada por la heurística anterior
            pos_sup[i] = pos[i] - step              # Movimiento: i=0 => arriba, i=1 => izquierda
            hijos.append(pos_sup.copy())            # Acumulamos esta posición en el vector hijos
            costo_ma = F(pos_sup, esq, pos_final)   # Sacamos el costo de ese hijo (pos_sup)
            resultados.append(costo_ma)             # Se agrega este costo al vector resultados.

            pos_inf = pos.copy()                    # Igualamos pos_inf a la posición seleccionada por la heurística anterior
            pos_inf[i] = pos[i] + step              # Movimiento:  i=0 => abajo, i=1 => derecha
            hijos.append(pos_inf.copy())            # Acumulamos esta posición en el vector hijos
            costo_me = F(pos_inf, esq, pos_final)   # Sacamos el costo de ese hijo (pos_inf)
            resultados.append(costo_me)             # Se agrega este costo al vector resultados.

            if i == 1:                                      # Esto nos asegura que i es igual a 1
                esq = 1
                pos_ArIz = pos_sup.copy()                       # Igualamos pos_ArIz a la pos_sup anterior, lo ya que nos da un movimiento a la izquierda porque (i=1)
                pos_ArIz[0] = pos[0] - step                     # Movimiento: i=1 => arriba izquierda
                hijos.append(pos_ArIz.copy())
                costo_ArIz = F(pos_ArIz, esq, pos_final)        # Sacamos el costo de ese hijo (pos_ArIz)
                resultados.append(costo_ArIz)

                pos_AbIz = pos_sup.copy()                       # Igualamos pos_AbIz a la pos_sup anterior, lo ya que nos da un movimiento a la izquierda porque (i=1)
                pos_AbIz[0] = pos[0] + step                     # Movimiento: i=1 => abajo izquierda
                hijos.append(pos_AbIz.copy())
                costo_AbIz = F(pos_AbIz, esq, pos_final)        # Sacamos el costo de ese hijo (pos_AbIz)
                resultados.append(costo_AbIz)

                pos_ArDe = pos_inf.copy()                       # Igualamos pos_ArDe a la pos_inf anterior, lo ya que nos da un movimiento a la derecha porque (i=1)
                pos_ArDe[0] = pos[0] - step                     # Movimiento: i=0 => arriba derecha
                hijos.append(pos_ArDe.copy())
                costo_ArDe = F(pos_ArDe, esq, pos_final)        # Sacamos el costo de ese hijo (pos_ArDe)
                resultados.append(costo_ArDe)

                pos_AbDe = pos_inf.copy()                       # Igualamos pos_AbDe a la pos_inf anterior, lo ya que nos da un movimiento a la derecha porque (i=1)
                pos_AbDe[0] = pos[0] + step                     # Movimiento: i=0 => abajo derecha
                hijos.append(pos_AbDe.copy())
                costo_AbDe = F(pos_AbDe, esq, pos_final)        # Sacamos el costo de ese hijo (pos_AbDe)
                resultados.append(costo_AbDe)


        min_index = np.argmin(resultados)               # De todos los costos de todos los hijos vistos, seleccionamos el índice del menor costo
        pos = hijos[min_index]                          # pos es entonces el hijo de menor costo (Actualizamos para la siguiente vuelta del while not)
        # print("Estamos en:", pos, "y la posición final es:", pos_final, ".\n")
        pos_mov.append(pos.copy())                      # Agregamos este hijo al vector movimientos realizados

    return pos, pos_mov                             # Devolvemos el último hijo encontrado (posición final) y el vector de movimientos realizados


if __name__ == "__main__":

    valor_mov = []
    dist_recorrida = []

    #filas = input('Ingrese número de filas (preferentemente múltiplo de 4):')
    #print("Número de filas: ", filas)
    #columnas = input('Ingrese número de columnas (debe ser un número par):')
    #print("Número de columnas: ", columnas)
    #filas = int(filas)
    #columnas = int(columnas)

    filas = 12
    columnas = 6

    mat = createMatriz(filas, columnas)
    print("Matriz inicial: \n", mat, "\n\n")

    seed = np.arange(1, filas*columnas)
    val_inicial = np.random.choice(seed, 1)
    val_final = np.random.choice(seed, 1)
    pos_inicial = paso_a_pos(val_inicial, filas, columnas, mat)         # Pasa el valor inicial a coordenadas (posición)
    pos_final = paso_a_pos(val_final, filas, columnas, mat)             # Pasa el valor inicial a coordenadas (posición)

    pos, pos_mov = Mov_Heurist(pos_inicial, pos_final)                  # Realiza el movimiento con la función Heurística

    for i in range(len(pos_mov)):                                       # Pasa las coordenadas del vector de movimientos realizados a valores
        valor_mov.append(paso_a_valor(pos_mov[i], filas, columnas, mat))
        if i > 0:
            if (pos_mov[i][0] != pos_mov[i - 1][0]) and \
            (pos_mov[i][1] != pos_mov[i - 1][1]):                       # Si se movió a una esquina, agrega el valor 1,41 al vector distancia recorrida
                dist_recorrida.append(math.sqrt(2))
            else:
                dist_recorrida.append(1)                                # Si se movió a una posición contínua (no esquina) agrega 1 al vector distancia recorrida

    dist_final = 0
    for i in range(len(dist_recorrida)):                                # Se suman todas las componentes del vector de distancias recorridas para obtener la distancia real recorrida
        dist_final += dist_recorrida[i]

    dist = H(pos_inicial, pos_final)                                    # Calcula la distancia de la posición inicial a la final (se aprovecha la función H que es pitágoras)

    print("----END----")                                                # Imprimimos los datos relevantes
    print("Valor inicial:", val_inicial[0])
    print("Posición inicial:", pos_inicial)
    print("Movimientos realizados:\n", np.array([pos_mov]))
    print("Valores de los movimientos realizados:", np.array(valor_mov))
    print("Distancia entre punto inicial y final (euclidiana):", dist)
    print("Distancia que se recorrió:", dist_final)
    print("Valor final esperado:", val_final[0])
    print("Posición final esperada:", pos_final)
    print("Valor final encontrado:", int(valor_mov[len(pos_mov)-1]))
    print("Posición final encontrada:", pos)

    mov1 = []
    mov2 = []
    for i in range(len(pos_mov)):
        mov1.append(pos_mov[i][0])
        mov2.append(pos_mov[i][1])

    plt.plot(mov2, mov1, 'ro-')
    plt.xlim(0, columnas)
    plt.ylim(0, filas)
    plt.show()