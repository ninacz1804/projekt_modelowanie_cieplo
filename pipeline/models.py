import csv
import os
import numpy as np

def wczytanie_materialow():

    folder_skryptu = os.path.dirname(__file__)
    sciezka = os.path.join(folder_skryptu, '..', 'data', 'materials.csv')
    
    materialy = {}
    with open(sciezka, mode='r') as plik:
        czytnik = csv.DictReader(plik)
        for wiersz in czytnik:
            nazwa = wiersz['material']
            materialy[nazwa] = {
                'L': float(wiersz['lambda']),
                'R': float(wiersz['density']),
                'C': float(wiersz['c'])
            }
    return materialy

def D2(n):
    D = np.zeros((n, n))
    for i in range(1, n - 1):
        D[i, i-1], D[i, i], D[i, i+1] = 1, -2, 1
    D[0, 0], D[0, 1] = -1, 1
    D[-1, -1], D[-1, -2] = -1, 1
    return D

def macierz_A(nx, ny, alfa, dt, h, maska_brzegow):
    I_2D = np.eye(nx * ny)
    L_2D = (np.kron(np.eye(ny), D2(nx)) + np.kron(D2(ny), np.eye(nx))) / h**2
    
    A = I_2D - alfa * dt * L_2D
    for i in range(nx * ny):
        if maska_brzegow[i]:
            A[i, :] = 0
            A[i, i] = 1
            
    return np.linalg.inv(A)

def oblicz_alfa(nazwa_materialu, mnoznik):
    dane = wczytanie_materialow()
    m = dane[nazwa_materialu]
    alfa = m['L'] / (m['R'] * m['C'])
    return alfa * mnoznik