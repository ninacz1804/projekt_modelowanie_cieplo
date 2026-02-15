import numpy as np

nx = 50
ny = 50
szerokosc = 3.0
h = szerokosc / (nx - 1)
T_startowa = 15.0
T_okna = 5.0
T_grzejnika = 40.0
T_cel = 21.0

czujnik_x, czujnik_y = 25, 25
idx_czujnika = czujnik_y * nx + czujnik_x


dt = 20.0
kroki = 10000
mnoznik = 100.0

nx_3 = 90
ny_3 = 30
szerokosc_3 = 9.0
h_3 = szerokosc_3 / (nx_3 - 1)

czujnik_x_sasiad_1 = 15
czujnik_y_sasiad_1 = 15
idx_czujnika_sasiad_1 = czujnik_y_sasiad_1 * nx_3 + czujnik_x_sasiad_1
czujnik_x_sasiad_2 = 75
czujnik_y_sasiad_2 = 15
idx_czujnika_sasiad_2 = czujnik_y_sasiad_2 * nx_3 + czujnik_x_sasiad_2

szerokosc = 10
wysokosc = 4

m_s1 = np.zeros((ny_3, nx_3), dtype=bool)
m_s1[1:5, 10:20] = True
maska_s1 = m_s1.flatten()

m_ja = np.zeros((ny_3, nx_3), dtype=bool)
m_ja[1:5, 40:50] = True
maska_ja = m_ja.flatten()

m_s2 = np.zeros((ny_3, nx_3), dtype=bool)
m_s2[1:5, 70:80] = True
maska_s2 = m_s2.flatten()

lista_masek = [maska_s1, maska_ja, maska_s2]
idx_czujnikow = [idx_czujnika_sasiad_1, idx_czujnika, idx_czujnika_sasiad_2]