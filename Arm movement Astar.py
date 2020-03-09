import numpy as np
import math
import matplotlib.pyplot as plt


def H(pos, pos_final):
    return math.sqrt((pos_final[0] - pos[0]) ** 2 + (pos_final[1] - pos[1]) ** 2 +
                     (pos_final[2] - pos[2]) ** 2 + (pos_final[3] - pos[3]) ** 2 +
                     (pos_final[4] - pos[4]) ** 2 + (pos_final[5] - pos[5]) ** 2)


#def G():
def G(pos, pos_inicial):
    return math.sqrt((pos[0] - pos_inicial[0]) ** 2 + (pos[1] - pos_inicial[1]) ** 2 +
                     (pos[2] - pos_inicial[2]) ** 2 + (pos[3] - pos_inicial[3]) ** 2 +
                     (pos[4] - pos_inicial[4]) ** 2 + (pos[5] - pos_inicial[5]) ** 2)
    #return 10


def Costo(pos, pos_i, pos_f):
    peso_H = 0.8
    peso_G = 0.4
    return peso_H * H(pos, pos_f) + peso_G * G(pos, pos_i)

def steps (pos_step):
    flag = 0                                            # Reseteo de control de repetición y de obstáculos.
    j = 0                                               # Para control de obstáculos.
    while flag == 0:                                    # No se usa for porque el obstáculo puede estar en medio
        if j == len(obstaculos):                        # de la matriz obstaculos, con for quedaría el flag
            flag = 2                                    # consecuencia del último obstáculo.
        if flag == 0:                                   # if == 0 para que no se compare con el obstáculo de nuevo + 1.
            if np.array_equal(pos_step, obstaculos[j]): # Compara para que no se salte a un obstáculo.
                flag = 1
        j += 1                                          # Se actualiza j para comparar el siguiente obstáculo.
    if flag == 1:
        obs_saltados.append(pos_step.copy())            # Acumula obstáculos saltados
    if flag == 2:                                       # Si se recorrió toda la matriz obstaculos y no se
        k = 0                                           # encontró igualdad, entonces se agrega a hijos.
        while flag == 2:                                # Se revisa que el valor de este nuevo hijo no se haya
            if k == len(movimientos):                   # visitado antes.
                flag = 3
            if flag == 2:
                if np.array_equal(pos_step, movimientos[k]):
                    flag = 4
            k += 1
        if flag == 3:                                   # Si no se visitó entonces se agrega a hijos ahora si.
            return flag


def Mov_Heurist (pos_inic, pos_final):

    pos_hijos = pos_inic.copy()
    pos = pos_inic.copy()
    it = []
    count = 0
    for i in range(1, 99):
        pos_obst = np.random.choice(seed, 6)
        obstaculos.append(pos_obst.copy())

    while not (np.array_equal(pos, pos_final)):
        count += 1
        hijos = []                                  # Reseteo de matriz hijos.
        resultados = []                             # Reseteo de matriz resultados.
        step = 1
        for i in range(len(pos_hijos)):             # Para los 6 vectores dentro de la matriz pos_hijos.
            pos_sup = pos.copy()
            pos_sup[i] = pos[i] + step              # PARA STEP +1
            flag = steps(pos_sup)
            if flag == 3:
                hijos.append(pos_sup.copy())
                costo_ma = Costo(pos_sup, pos_inic, pos_final)
                resultados.append(costo_ma)          # Se calcula el costo y se agrega este a resultados.
            pos_inf = pos.copy()
            pos_inf[i] = pos[i] - step               # LO MISMO PARA STEP -1
            flag = steps(pos_inf)
            if flag == 3:
                hijos.append(pos_inf.copy())
                costo_me = Costo(pos_inf, pos_inic, pos_final)
                resultados.append(costo_me)           # Se calcula el costo y se agrega este a resultados.

        min_index = np.argmin(resultados)
        pos = hijos[min_index]
        it.append(count)
        print("Estamos en:", pos, "y la posición final es:", pos_final, ".\n")
        movimientos.append(pos.copy())
    return pos, it


if __name__ == "__main__":
    seed = np.arange(360)
    movimientos = []
    obstaculos = []
    obs_saltados = []
    pos_inic = np.random.choice(seed, 6)
    pos_final = np.random.choice(seed, 6)

    pos, it = Mov_Heurist(pos_inic, pos_final)

    print("----END----")
    print("Posición inicial:", pos_inic)
    print("Obstáculos:", np.array([obstaculos]))
    print("Movimientos realizados:", np.array([movimientos]))
    print("Obstáculos Saltados", obs_saltados)
    print("Posición final esperada:  ", pos_final)
    print("Posición final encontrada:", pos)

    mov1 = []
    mov2 = []
    mov3 = []
    mov4 = []
    mov5 = []
    mov6 = []
    for i in range(len(it)):
        mov1.append(movimientos[i][0])
        mov2.append(movimientos[i][1])
        mov3.append(movimientos[i][2])
        mov4.append(movimientos[i][3])
        mov5.append(movimientos[i][4])
        mov6.append(movimientos[i][5])

    plt.plot(it, mov1, 'r--', it, mov2, 'y--', it, mov3, 'g--', it, mov4, 'c--', it, mov5, 'b--', it, mov6, 'm--')
    plt.show()