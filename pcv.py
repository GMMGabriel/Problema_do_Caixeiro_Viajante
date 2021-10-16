# IMPORTS ============================================================================================================================

import matplotlib.pyplot as plt
import numpy as np
import random
import math
import itertools as tls
from datetime import datetime
import os


# FUNCTIONS ==========================================================================================================================

def gen_cordinate(n):
    '''
    n: número de cidades.
    ---
    Gera as coordenadas x e y das cidades com um range que vai de 0 até n-1, depois embaralha a lista com o shuffle.
    ---
    Retorna os valores do eixo x e os valores do eixo y em tuplas separadas.
    '''
    x = list(range(n))
    y = list(range(n))
    random.shuffle(x)
    random.shuffle(y)
    return tuple(x), tuple(y)


def distance_between_two_cities(p1, p2):
    '''
    p1: lista ou tupla com o valor x e y do ponto 1.
    p2: lista ou tupla com o valor x e y do ponto 2.
    ---
    Calcula a distancia entre os dois pontos.
    ---
    Retorna seu valor arredondando para no máximo 3 casas.
    '''
    return round(math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2), 3)


def calc_distances_between_cities(x, y):
    '''
    x: tupla com os valores do eixo x.
    y: tupla com os valores do eixo y.
    ---
    Gera uma matriz com os valores referente as distancias entre cada cidade.
    ---
    Retorna essa matriz.
    '''
    return np.array([list(float(distance_between_two_cities((x[i], y[i]), (x[j], y[j]))) for i in range(n)) for j in range(n)])


def gen_possible_paths(n, start_city):
    '''
    n: número de cidades.
    start_city: índice da cidade que inicia e termina o percurso.
    ---
    Gera uma tupla com todas as tuplas de caminhos possíveis, sem contar o índice da cidade que inicia e termina.
    ---
    Retorna a tupla com os resultados.
    '''
    index_cities_to_str = tuple([str(x) for x in range(n) if x != start_city])
    return tuple(tls.permutations(index_cities_to_str))


def calc_total_distances_from_the_paths(start_city, matrix_distances_between_cities, possible_paths):
    '''
    start_city: índice da cidade que inicia e termina o percurso.
    matrix_distances_between_cities: matriz com as distancias entre cada cidade.
    possible_paths: tupla com todas as tuplas de caminhos possíveis.
    ---
    Cria uma lista para armazenar a distancia total percorrida em cada caso dos caminhos possíveis.
    ---
    Retorna essa lista convertendo em tupla.
    '''
    total_distances_from_the_paths = [0]*len(possible_paths)

    for i in range(len(possible_paths)): # percorre a tupla para poder chegar nas tuplas com os caminhos.
        # Já de início, soma a distancia entre a cidade inicial (start_city) e a segunda cidade do percurso, com a distancia
        # entre a penúltima cidade do percurso e a cidade final (start_city).
        total = (matrix_distances_between_cities[start_city][int(possible_paths[i][0])]) + (matrix_distances_between_cities[start_city][int(possible_paths[i][-1])])

        for j in range(len(possible_paths[0])-1): # percorre a tupla que contem os caminhos.
            # Soma ao valor, a distancia entre as cidades do caminho possível.
            total += matrix_distances_between_cities[int(possible_paths[i][j])][int(possible_paths[i][j+1])]

        total_distances_from_the_paths[i] = round(total, 3)

    return tuple(total_distances_from_the_paths)


def start(n, start_city):
    '''
    n: número de cidades.
    start_city: índice da cidade que inicia e termina o percurso.
    ---
    Está função é a função chamada para iniciar o programa.
    Uma das maneiras de dizer é: ela faz o gerenciamento, ou seja, ela que chama as demais funções.
    ---
    Retorna None.
    '''
    x, y = gen_cordinate(n) # gera as coordenadas x e y

    matrix_distances_between_cities = calc_distances_between_cities(x, y) # calcula a distancia entre cada cidade

    possible_paths = gen_possible_paths(n, start_city) # gera todos os caminhos possíveis

    # Calcula a distancia total de cada caminho possível.
    total_distances_from_the_paths = calc_total_distances_from_the_paths(start_city, matrix_distances_between_cities, possible_paths)

    # Pega o índice da menor distancia encontrada.
    value_min_index = total_distances_from_the_paths.index(min(total_distances_from_the_paths))

    # Armazena em uma tupla os índices das cidades na ordem que fazem o menor percurso.
    way_made = (start_city,) + tuple([int(value) for value in possible_paths[value_min_index]]) + (start_city,)
    # Pega o valor da distancia total percorrida.
    total_distance_from_the_way_made = total_distances_from_the_paths[value_min_index]

    # Organiza as coordenadas na ordem do menor percurso.
    _x = [int(x[value]) for value in way_made]
    _y = [int(y[value]) for value in way_made]
    
    # Variáveis auxiliares para colocar os caminhos entre cada cidade.
    x_aux = 0
    y_aux = 0

    # Coloca os caminhos entre cada cidade.
    for i in range(n):
        for j in range(i, n):
            if i != j:
                x_aux = list(str(_x[i])) + list(str(_x[j]))
                x_aux = [int(value) for value in x_aux]
                y_aux = list(str(_y[i])) + list(str(_y[j]))
                y_aux = [int(value) for value in y_aux]
                plt.plot(x_aux, y_aux, 'lightgray')

    # Coloca o último caminho novamente, mas agora com um "label" para aparecer na legenda.
    plt.plot(x_aux, y_aux, 'lightgray', label="Conexões entre cidades")

    # Coloca o Caminho percorrido.
    plt.plot(_x, _y, 'o-', color="green", label="Caminho percorrido")

    # Coloca os índices de cada cidade em cima delas.
    for i in range(len(_x)-1):
        plt.text(_x[i], _y[i] + 0.2, str(way_made[i]), color="k", fontsize=10, fontweight="bold", horizontalalignment="center")

    way_made = str(way_made)
    
    # Coloca a cidade inicial e final de uma cor diferente.
    plt.plot(_x[0], _y[0], "o", color="#591ff9", label="Ponto de partida e chegada")

    # Demais configurações para a janela do gráfico.
    plt.legend(loc=3) # legenda
    plt.axis([-0.5, n-0.5, -3, n+1]) # limita a área de exibição
    plt.xlabel("Eixo X")
    plt.ylabel("Eixo Y")
    plt.title("PCV (Problema do Caixeiro Viajante) com " + str(n) + " cidades")
    plt.text(-0.4, n+0.5, "Caminho percorrido: " + way_made, fontsize=10) # coloca o texto que mostra o caminho percorrido
    plt.text(-0.4, n, "Distancia total do percurso: " + str(round(total_distance_from_the_way_made, 3)), fontsize=10)
    plt.show()


# MAIN ===============================================================================================================================

if __name__ == '__main__':
    os.system('cls')

    now = datetime.now()
    random.seed(now.year + now.month + now.day + now.hour + now.minute + now.second)

    # Pede o número de cidades ao usuário.
    while True:
        n = input("Número de cidades: ")
        try:
            n = int(n)
            if n < 4:
                print("\n\tPor favor, informe um número inteiro maior que 3.\n")
            else:
                break
        except ValueError as e:
            print("\n\tPor favor, informe um número inteiro maior que 3.\n")

    os.system('cls')
    print("Número de cidades:", n)

    # Pede o índice da cidade que ele deseja que seja a cidade inicial e final.
    i_aux = -1
    while True:
        i = input("Índice da cidade para iniciar (responda em branco para ser aleatório): ")
        try:
            i = i_aux = int(i)
            break
        except ValueError as e:
            if i == '':
                i = random.randint(0, n-1)
                break
            else:
                print("\n\tPor favor, informe um número inteiro ou deixe em branco (vazio).\n")

    os.system('cls')

    print("Número de cidades:", n)
    print("Índice da cidade inicial:", (i if i_aux > -1 else "aleatório"))

    start(n, i)
