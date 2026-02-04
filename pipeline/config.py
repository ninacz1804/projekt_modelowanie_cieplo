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
kroki = 5000
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