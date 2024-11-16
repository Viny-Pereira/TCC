n_no = [1, 2, 3, 4]
no = [[0, 6], [6, 6], [0, 0], [6, 0]]
AREA = []
MOMENTO_INERCIA = []
MODULO_DE_ELASTICIDADE = []
elementosENTOS = []


def calcularSen(elemento):
    cordenada_ponto_1 = elemento[0]
    cordenada_ponto_2 = elemento[1]
    comprimento = calcularComprimento(elemento)
    return (cordenada_ponto_2[1] - cordenada_ponto_1[1]) / (comprimento)


def calcularCos(elemento):
    cordenada_ponto_1 = elemento[0]
    cordenada_ponto_2 = elemento[1]
    comprimento = calcularComprimento(elemento)
    return (cordenada_ponto_2[0] - cordenada_ponto_1[0]) / (comprimento)


def calcularComprimento(elemento):
    cordenada_ponto_1 = elemento[0]
    cordenada_ponto_2 = elemento[1]
    return (
        (cordenada_ponto_2[0] - cordenada_ponto_1[0]) ** 2 + (cordenada_ponto_2[1] - cordenada_ponto_1[1]) ** 2
    ) ** (1 / 2)


def matrizRigidezLocal(elementos, i, L):
    return [
        [(elementos(i, 6) * elementos(i, 4)) / L, 0, 0 - (elementos(i, 6) * elementos(i, 4)) / L, 0, 0],
        [
            0,
            ((12 * elementos(i, 6) * elementos(i, 5)) / L ^ 3) / 10000,
            ((6 * elementos(i, 6) * elementos(i, 5)) / L ^ 2) / 100,
            0,
            -((12 * elementos(i, 6) * elementos(i, 5)) / L ^ 3) / 10000,
            ((6 * elementos(i, 6) * elementos(i, 5)) / L ^ 2) / 100,
        ],
        [
            0,
            ((6 * elementos(i, 6) * elementos(i, 5)) / L ^ 2) / 100,
            (4 * elementos(i, 6) * elementos(i, 5)) / L,
            0,
            -((6 * elementos(i, 6) * elementos(i, 5)) / L ^ 2) / 100,
            (2 * elementos(i, 6) * elementos(i, 5)) / L,
        ],
        [(-elementos(i, 6) * elementos(i, 4)) / L, 0, 0, (elementos(i, 6) * elementos(i, 4)) / L, 0, 0],
        [
            0,
            -((12 * elementos(i, 6) * elementos(i, 5)) / L ^ 3) / 10000,
            -((6 * elementos(i, 6) * elementos(i, 5)) / L ^ 2) / 100,
            0,
            ((12 * elementos(i, 6) * elementos(i, 5)) / L ^ 3) / 10000,
            -((6 * elementos(i, 6) * elementos(i, 5)) / L ^ 2) / 100,
        ],
        [
            0,
            ((6 * elementos(i, 6) * elementos(i, 5)) / L ^ 2) / 100,
            (2 * elementos(i, 6) * elementos(i, 5)) / L,
            0,
            -((6 * elementos(i, 6) * elementos(i, 5)) / L ^ 2) / 100,
            (4 * elementos(i, 6) * elementos(i, 5)) / L,
        ],
    ]
