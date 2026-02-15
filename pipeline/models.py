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

    if isinstance(alfa, np.ndarray):
        A = I_2D - dt * (alfa.reshape(-1, 1) * L_2D)
    else:
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

def termostat(u_start, A_inv_on, A_inv_off, T_grzejnika, T_cel, idx_czujnika, kroki):
    u = u_start.copy()
    indeksy_grzejnika = (u_start == T_grzejnika)
    
    for i in range(kroki):
        temp_czujnika = u[idx_czujnika]
        
        if temp_czujnika < T_cel:
            u[indeksy_grzejnika] = T_grzejnika
            u = A_inv_on @ u
        else:
            u = A_inv_off @ u
            
    return u

def symulacja_pokoju(x_grz, y_grz, szer_grz, wys_grz, nx, ny, alfa, dt, h, T_start, T_okna, T_grzejnika, T_cel, idx_czujnika, kroki):
    pokoj = np.ones((ny, nx)) * T_start
    pokoj[0, 15:35] = T_okna
    pokoj[y_grz : y_grz + wys_grz, x_grz : x_grz + szer_grz] = T_grzejnika
    
    u_vector = pokoj.flatten()

    maska_on = (u_vector == T_okna) | (u_vector == T_grzejnika)
    A_inv_on = macierz_A(nx, ny, alfa, dt, h, maska_on)
    maska_off = (u_vector == T_okna)
    A_inv_off = macierz_A(nx, ny, alfa, dt, h, maska_off)

    u_wynik = termostat(u_vector, A_inv_on, A_inv_off, T_grzejnika, T_cel, idx_czujnika, kroki)
    
    return u_wynik.reshape((ny, nx))


def symulacja_trzech_pokoi(nx, ny, alfa_wektor, dt, h, T_start, T_grzejnika, T_cel, idx_czujnikow, maski_grzejnikow, kroki, kto_grzeje=[True, True, True]):
    
    u = np.ones(nx * ny) * T_start
    energia = [0.0, 0.0, 0.0] 
  
    maska_wszystkie_grz = maski_grzejnikow[0] | maski_grzejnikow[1] | maski_grzejnikow[2]
    A_inv_on = macierz_A(nx, ny, alfa_wektor, dt, h, maska_wszystkie_grz)
    A_inv_off = macierz_A(nx, ny, alfa_wektor, dt, h, np.zeros(nx * ny, dtype=bool))

    for i in range(kroki):
        czy_ktokolwiek_grzeje = False
        
        for p in range(3):
            if kto_grzeje[p] and u[idx_czujnikow[p]] < T_cel:
                u[maski_grzejnikow[p]] = T_grzejnika
                energia[p] += np.sum(maski_grzejnikow[p]) * dt
                czy_ktokolwiek_grzeje = True
        
        if czy_ktokolwiek_grzeje:
            u = A_inv_on @ u
        else:
            u = A_inv_off @ u
            
    return u.reshape((ny, nx)), energia