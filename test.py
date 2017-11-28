from __future__ import division
import random, copy, matplotlib.pyplot as plt
import string, os, math, time
from datetime import datetime
import collections

# openstreat map

# TODO dodac zmienna mierzaca czas kurierowi
# TODO postoje u klientow i na stacjach
# TODO rozwiazac problem(gdy jest ostatnia iteracja for-a nie mozna do funkcji przeslac cities[i +1]):
#            try:
#                new_tour, tank, gasStations_dict = add_gasStation(new_tour, cities[i], cities[i+1], gasStations_dict)
#                print "koordynaty  gas stations - uzupelniony", gasStations_dict
#            except Exception as e:
#                print e
# TODO zrobic inteligentniejszego swap-a - to jest trudniejsze zadanie

# ALGORYTM
# 1. Ustaw tablice  najkrotszych sciezek pomiedzy miastami z przesylka, po drodze uwzglednij trasy przez mista bez przesylki
# 1. Ustaw calkiem losowa kolejnosc odwiedzania mista z przesylkami -> tasae wyznaczana jest na podstawie kolejnosc tablicy cities
# 3. Najkrotsza trase pomiedzy wczesniej wylosowanymi nodami n, a n+1 wez z tablicy najkrotszych sciezek
# 3. licz trase po koleji z wezla n do wezla n+1, gdy bak przekroczy tank treshold, dodaj dystans z obecnego city->najblizszej stacji i z stacji->next hopa, zapisz wspolzedne wybranej stacji do gasStations_dict
# 4. jezeli trasa jest krotsza od ostatnie najlepszej, ustaw ja jako najbardziej optymalna razem z wpisanymi dla tej trasy stacjami
# 5. zrob swapa na dwoch losowych wezlach misat z przesylka
# 6. przejdz do 3, jezeli temperatura powyzej tresholdu

startTime = datetime.now()


def draw_chart(path, added_gasStation, duration=0.5):
    global gas_station
    # added_gasStation = {78:(6,7), 8:(78,93)}
    sorted_ids = sorted(added_gasStation.keys())
    path_copy = path[:]
    for k in sorted_ids[::-1]:
        value = added_gasStation[k]
        value = list(value)
        path.insert(k, value)
    # path.append(path[0])
    ids_tab =[]
    for k in path_copy:
        if k in cities:
            id = cities.index(k)
            ids_tab.append(id)
    print "ids tab ", ids_tab
    print "path ", path
    labels_gasStation = ['GS_{}'.format(i + 1) for i in range(len(gas_station))]
    labels = ['M_{}'.format(i) for i in ids_tab]
    label1 = ['D_{}'.format(i) for i in xrange(len(designated_cities))]

    plt.plot(*zip(*path), marker='x')  # * - skrot do przekazywania wielu zmiennym ktore sa zapakowane w np listach lub krotkach najpierw pierwszy element, pozniej drugi element listy  i tak dalej, tak jak bym przekazywala osobne zmienne, * rozbicie pojemnika
    plt.plot(*zip(*gas_station), marker='o', linestyle=' ')
    plt.plot(*zip(*cities), marker='o', linestyle=' ')
    i = 0
    for cor in path_copy:
        i += 1
        plt.annotate(labels[i - 1], xy=(cor[0], cor[1]), xytext=(2, 2), textcoords='offset points')
    i = 0
    for j in gas_station:
        plt.annotate(labels_gasStation[i], xy=(j[0], j[1]), xytext=(10, 2), textcoords='offset points')
        i += 1
    # i =0
    # for j in designated_cities:
    #     plt.annotate(label1[i], xy=(j[0], j[1]), xytext=(10, 2), textcoords='offset points')
    #     i += 1

    plt.show(block=True)
    time.sleep(duration)
    plt.close()


def swap():
    swap_tab = range(len(designated_cities))
    del swap_tab[0]
    city1_id = random.choice(swap_tab)
    swap_tab.remove(city1_id)
    city2_id = random.choice(swap_tab)
    swap_tab.remove(city2_id)

    temp = designated_cities[city1_id]
    designated_cities[city1_id] = designated_cities[city2_id]
    designated_cities[city2_id] = temp
    # TODO check_swap - funkcja sprawdzajaca czy cities po swapie sa mozliwe


def add_gasStation(new_tour, city1, city2, gasStations_dict, MAIN_PATH):
    global cities
    global gas_station
    cities_working_backup = MAIN_PATH[:]
    # print "find the nearest gas station"
    distances_to_gas_stations = []
    # print "stations paliw -> ", gas_station
    # print "miasto ->", city1
    for cor in gas_station:
        distances_to_gas_stations.append(round(math.sqrt((city1[0] - cor[0]) ** 2 + (city1[1] - cor[1]) ** 2), 2))
    # print "odleglosci ->", distances_to_gas_stations
    closest_station = distances_to_gas_stations.index(min(distances_to_gas_stations))
    cor_closest_station = gas_station[closest_station]
    # print "najblizsza stacja  ->", cor_closest_station
    city1_id = cities_working_backup.index(city1)
    new_tour += min(distances_to_gas_stations)
    # print "new_tour + dystans do stacji ->", new_tour
    cities_working_backup.insert(city1_id + 1, cor_closest_station)
    gasStations_dict[city1_id + 1] = cor_closest_station
    # print "cities z nowa satcja ", cities_working_backup
    distances_to_city2 = (
    round(math.sqrt((city2[0] - cor_closest_station[0]) ** 2 + (city2[1] - cor_closest_station[1]) ** 2), 2))
    new_tour += distances_to_city2
    # print "new_tour + dystans ze stacji", cor_closest_station, "do next hop", city2, " -> ", new_tour
    tank = 200
    return new_tour, tank, gasStations_dict

def define_edges():
    edges = []
    for d  in xrange(len(designated_cities)):
        if d == len(designated_cities)-1:
             temp_path = designated_cities[-1], designated_cities[0]
        else:
            temp_path = designated_cities[d], designated_cities[d+1]
        edges.append(temp_path)
    # print "route\n" ,route
    return edges


def create_coordinates_main_path(edges,MAIN_PATH, PATHS_DICT):
    for h in edges:
        # print "h0 ",h[0], "node startoey", PATHS_DICT[h[0]]
        # print "h1 node docelowy",h[1], "sciazka do tego noda", PATHS_DICT[h[0]][h[1]]
        MAIN_PATH.append(PATHS_DICT[h[0]][h[1]])
    MAIN_PATH.append(designated_cities[0])

    temp_main_path = []
    for element in MAIN_PATH:
        if isinstance(element, list):
            for e in element:
                temp_main_path.append(e)
        else:
             temp_main_path.append(element)

    MAIN_PATH = temp_main_path
    COR_MAIN_PATH = []
    for id in MAIN_PATH:
        COR_MAIN_PATH.append(ref_cities[id])

    return COR_MAIN_PATH, MAIN_PATH

    # print MAIN_PATH
    # print COR_MAIN_PATH


def count_distance(tour, zlamane_iteracje, dis, PATHS_DICT):

    tank = 180
    tank_treshold = 120
    count_sum = True
    new_tour = 0

    cities1 = cities[:]
    gasStations_dict = {}
    MAIN_PATH = []
    route = []


    edges = define_edges()
    COR_MAIN_PATH, MAIN_PATH = create_coordinates_main_path(edges, MAIN_PATH, PATHS_DICT)


    for i in range(len(MAIN_PATH)):

        if i == len(MAIN_PATH) - 1:
            dis.append(round(math.sqrt((COR_MAIN_PATH[i][0] - COR_MAIN_PATH[0][0]) ** 2 + ((COR_MAIN_PATH[i][1] - COR_MAIN_PATH[0][1]) ** 2)), 2))
            # print "trasa od city", i, "do city startowego"
        else:
            dis.append( round(math.sqrt((COR_MAIN_PATH[i][0] - COR_MAIN_PATH[i + 1][0]) ** 2 + ((COR_MAIN_PATH[i][1] - COR_MAIN_PATH[i + 1][1]) ** 2)),2))
            # print "trasa od city", i, "do city ", i+1
        new_tour = new_tour + dis[i]
        tank = tank - dis[i] * 0.30  # zmienijszenie tank
        # print "tank ", tank, "tank tresholdd ", tank_treshold    # print do obserwacji zmiany baku

        # wyrazenie warunkowe obnizajace koszty obliczeniowe w skrypcie
        # jezeli w czasie obliczen kosztu nowej trasy napotkamy na wartosc, ktora JUZ przekracza ostatnia najoptymalniejsza, to przestajemy juz dalej ja liczyc
        if tank < tank_treshold:  # kiedy new_tour przekroczy tank
            # print "KONCZY SIE BENZYNA"
            try:
                new_tour, tank, gasStations_dict = add_gasStation(new_tour, COR_MAIN_PATH[i], COR_MAIN_PATH[i + 1], gasStations_dict, COR_MAIN_PATH)
                # print "koordynaty  gas stations - uzupelniony", gasStations_dict
            except Exception as e:
                print e

        if tour <= new_tour:
            count_sum = False
            zlamane_iteracje += 1
            # print "zlamana petal"
            break

    return count_sum, zlamane_iteracje, new_tour, gasStations_dict, COR_MAIN_PATH


def create_route_table(PATHS, org_cities_tuples, node):
    for key in PATHS:
         PATHS[key] = [org_cities_tuples.index(PATHS[key])]

    print "POCZATKOWO WSZYSTKIE", PATHS
    flag = True
    while flag:
        flag = False
        for i in range(len(PATHS)):
            c = PATHS[i][0]
            # print "POPRZEDNIE MIASTO", c
            if c != node:
                # print "JEDZIEM"
                PATHS[i] = PATHS[c] + PATHS[i]
                if PATHS[c][0] == node:
                    flag = True
    print "KONCOWO", PATHS
    return PATHS



def modified_dijkstra():
    global main_temp_checked_cities
    org_cities_tuples = []
    PATHS_DICT = {}


    for i in original_cities:
        org_cities_tuples.append(tuple(i))

    neighbour_tab = {
        org_cities_tuples[0]: [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        org_cities_tuples[1]: [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        org_cities_tuples[2]: [1, 0, 1, 1, 0, 0, 1, 0, 0, 1],
        org_cities_tuples[3]: [0, 0, 1, 1, 0, 1, 0, 0, 0, 0],
        org_cities_tuples[4]: [0, 0, 0, 0, 1, 1, 0, 0, 1, 0],
        org_cities_tuples[5]: [0, 0, 0, 1, 1, 1, 0, 1, 0, 1],
        org_cities_tuples[6]: [0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
        org_cities_tuples[7]: [0, 0, 0, 0, 0, 1, 0, 1, 1, 0],
        org_cities_tuples[8]: [0, 0, 0, 0, 1, 0, 0, 1, 1, 0],
        org_cities_tuples[9]: [0, 1, 1, 0, 0, 1, 0, 0, 0, 1]
    }
    # print neighbour_tab

    #START FOR-a LICZACEGO DJIKSTRY DLA CALEJ TOPOLOGI
    for node in designated_cities:

        print "################################################################################################################################################\n"
        print "node  root  to: ", node, "ze wspolrzednymi: ", org_cities_tuples[node],"\n\n"
        not_checked_cities = org_cities_tuples[:]
        k = 0
        PATHS = {}
        while len(not_checked_cities):
            # print "-------------------------------------------------------------#####################----------------------------------------------------------"
            temp_checked_cities = main_temp_checked_cities[:]
            temp = []
            dis_vector = {}
            if k == 0:  # przejscie zerowe
                temp_not_checked_cities = []
                temp1_checked_cities = []
                for i in xrange(len(neighbour_tab[org_cities_tuples[0]])):
                    condition_2 = tuple(original_cities[node]) in not_checked_cities
                    condition_1 = neighbour_tab[org_cities_tuples[node]][i]
                    if condition_1 and condition_2:  # sprawdza czy badane misasto jest sasiadem i czy juz dnie niego nie mamy trasy
                        temp = tuple(original_cities[i])
                        value = round(math.sqrt(
                            (temp[1] - org_cities_tuples[node][1]) ** 2 + ((temp[0] - org_cities_tuples[node][0]) ** 2)), 2)
                        dis_vector[i] = value

                        temp1_checked_cities.append(temp)
                        not_checked_cities.remove(temp)
                        PATHS[i] = org_cities_tuples[node]
                main_temp_checked_cities = temp1_checked_cities
                k = 1
                # time.sleep(5)
            # print "SCIEZKA !!!!", PATHS



            temp1_checked_cities = []
            print "\nprzeszukujemy zbior z iteracji: ", temp_checked_cities
            for x in main_temp_checked_cities:
                print "curent node ", x
                for i in xrange(len(neighbour_tab[org_cities_tuples[0]])):
                    check_if = False
                    condition_1 = neighbour_tab[x][i]
                    condition_2 = tuple(original_cities[i]) in not_checked_cities
                    condition_3 = not (tuple(original_cities[i]) == x)
                    # print "cond1", condition_1, "cond2", condition_2, "cond3", condition_3
                    if condition_1 and condition_2 and condition_3:  # sprawdza czy badane misasto jest sasiadem i czy juz dnie niego nie mamy trasy
                        print "nowy sasiad", original_cities[i], "z id ", i, "dla wezla ", x
                        temp = tuple(original_cities[i])
                        check_if = True
                        value = round(math.sqrt((temp[1] - x[1]) ** 2 + ((temp[0] - x[0]) ** 2)), 2)
                        # try:
                        #     print "nowa wartosc ", value, "stara wartosc  ", dis_vector[i]
                        # except Exception as e:
                        #     pass
                        if not (dis_vector.has_key(i)) or value < dis_vector[i]:  # jezeli nie dbylo wpisu dla takiego wezla lub obecna wartosc jest mniejsza od ostatniej wpisanej
                            dis_vector[i] = value
                            # print "\nPATHS  od ", i, "wynosi ", x
                            PATHS[i] = x
                    if temp not in temp1_checked_cities and check_if:
                        temp1_checked_cities.append(temp)
            # print "\ntemp1 czyli sasiedzi dla wezlow z danej iteracji while'a", temp1_checked_cities

            print "odleglosci  do odkrytych sasiadow", dis_vector
            print "odkryci sasiedzi do przekazania do kolejnej iteracji whila ", temp1_checked_cities
            for visited in temp1_checked_cities:
                not_checked_cities.remove(visited)
            print "nieodwiedzone miasta", not_checked_cities

            main_temp_checked_cities = temp1_checked_cities[:]

        PATHS = create_route_table(PATHS, org_cities_tuples, node)

        PATHS_DICT[node] = PATHS
    print  PATHS_DICT
    # time.sleep(30)
    return PATHS_DICT


    # time.sleep(30)


def main():
    # zmienne do stystyk
    temperature = 999999999999
    tour = 600
    zlamane_iteracje = 0
    checkPoint = 0
    cooling_rate = 0.003
    best_cities = []
    PATHS_DICT = modified_dijkstra()
    print "-------------------------------------------------------------#####################----------------------------------------------------------"

    # glowna petla szukajaca optymalnej trasy
    while (temperature > 10):
        checkPoint += 1  # sprawdza iteracje petli
        dis = []
        swap()
        count_sum, zlamane_iteracje, new_tour, stations, COR_MAIN_PATH = count_distance(tour, zlamane_iteracje, dis, PATHS_DICT)
        # if przypisujacy najlepsze rozwiazania do finalnych zmiennych
        if count_sum:
            sum_dis = sum(dis)
            # print sum_dis
            # if math.exp((tour - sum_dis)/temperature ) > (random.randint(0,100)*5) or sum_dis < tour :
            tour = new_tour
            best_cities = COR_MAIN_PATH[:]
            best_stations = dict(stations)  # skopiuj stations
            # print "best cities  to ", cities, "+ stacje  benzymnowe ", best_stations
            # print "\n\n"
        temperature = temperature * (1 - cooling_rate)
        # print "temperatura", temperature, "\n\n"

    # stystyki
    print "przebyty deystans to ", tour
    print "przejsc petli  ", checkPoint
    print "zlamanych iteracji  ", zlamane_iteracje
    print "stosunek zlamanych petli do clakowitych, narazie jedyny czynnik optymalizacyjny:", zlamane_iteracje / checkPoint  # ostatnie wykonanie whila wprowadza count_sum na true
    print "CZAS ", datetime.now() - startTime
    # koncowa trasa
    print "best cities  to ", best_cities, "+ stacje benzynowe", best_stations
    print COR_MAIN_PATH
    draw_chart(best_cities, best_stations, 7)


# GLOBAL VARIABLES
cities_no = 10
cities = [random.sample(range(100), 2) for x in range(cities_no)]
all_distances = []
main_temp_checked_cities = []
# ----------------------------------------------------
# DO TESTOW | zahardkodowane wspolrzedne miast |
# --------------------------------------------------------
cities = [[80, 39], [11, 52], [78, 58], [45, 72]]
# cities = [[16, 50], [62, 91],  [43, 8], [11, 71], [34, 31],[23,89],[76,42],[76,90]] #8


# dest_cities =[[82, 26], [53, 2], [87, 51], [54, 70], [3, 37]]
cities = [[82, 26], [53, 2], [87, 51], [54, 70], [3, 37], [28, 33], [95, 56], [24, 69], [22, 56], [47, 26]]  # 10 miast
ref_cities = cities[:]
# designated_cities = [(82, 26), (95, 56),(3, 37), (22, 56)]
designated_cities = [0, 3 ,5, 1, 6]
# designated_cities = [7]
original_cities = cities[:]
cities_no = len(cities)




# ----------------------------------------------------
# -- GAS STATIONS ---
gas_station = [(1, 1), (85, 34), (83, 54), (38, 23), (94, 32), (47, 67)]
print "oryginalne city ", cities

if __name__ == "__main__":
    main()
