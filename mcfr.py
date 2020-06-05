import math as m
import statistics as st

'''Copyright (c) 2020 Moritz Siebert
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

""" Dieses Package wurde von Moritz Siebert kreiert,
    um die Fehlerrechnung nach den Leitlinien des physikalischen Grundpraktikums 
    der JMU-Wuerzburg zu automatisieren."""




''' Rundet einen Wert auf n stellen rechts des Kommas. 
    Nichtpositive Werte bedeuten Stellen rechts des Kommas.'''
def round_to_n(value, n):
    return int(value * 10 ** n + 0.5) / 10 ** n


'''Das n (also die negative Größenordnung auf die gerundet werden muss) wird anhand des Fehlers bestimmt.'''
def n_from_error(error):
    import math
    from numpy import sign
    if error >=1:
        return int((-sign(math.log(abs(error), 10)) * int(abs(math.log(abs(error), 10)))) + 2)
    else:
        return int((-sign(math.log(abs(error), 10)) * int(abs(math.log(abs(error), 10)))) + 1)


'''Diese Funktion ermittelt die gerundeten Werte und die Größenordnung des Messwertes in einer Liste.'''
def rou_val_n_err(value, error):
    from math import log
    ne = n_from_error(error)
    roundval = round_to_n(value, ne)
    rounderr = round_to_n(error, ne)
    dimen = int(log(abs(value), 10))
    return [round(roundval, ne), round(rounderr, ne), dimen, ne]



''' Hier kann mit der vorigen Funktion aus zwei Listen mit je ungerundeten Werten und Fehlern die zugehöirgen
    gerundeten Werte,sowie die Größenordnung und die Nachkommastelle, auf die gerundet wurde ermittelt werden.'''
def vall_errl(vallist, errlist):
    try:
        joinl = [rou_val_n_err(vallist[i], errlist[i]) for i in range(len(vallist))]
        return joinl
    except:
        if len(vallist) != len(errlist):
            print('Die Listen sind nicht gleich lang!\n')
        else:
            print('Es ist ein anderer Fehler auftgetreten...\n')
        return


''' Berechnet das arithmetische Mittel einer Liste'''
def mean(value_list):
    return sum(value_list) / len(value_list)


''' Nutzt die stdev Funktion des statistics-packages, um die Standardabweichung der Messwerte 	
    einer Liste zu bestimmen.'''
def stand_dev(value_list):
    return st.stdev(value_list)


''' Berechnet den Standardfehler einer Liste als stdev/sqrt(n)'''
def std_err(value_list):
    return st.stdev(value_list)/m.sqrt(len(value_list))


''' Gibt die "Stats" (Arithm. Mittel, Standardabw. und Standardf.) 
    einer gegebenen Liste zurück.'''
def stats_to_list(value_list):
    return mean(value_list), stand_dev(value_list), std_err(value_list)


''' Gibt die gerundeten Werte für arithmetisches Mittel und standardfehler einer Liste
    zurück.'''
def r_mean_err(value_list):
    return rou_val_n_err(mean(value_list), std_err(value_list))[:2]

''' Die gesamte Poisson-Code section geht von einem Input einzelner Messungen aus. 
    Also wird aus 0: 1, 1:3, 2:4,3:3 
    [0,1,1,1,2,2,2,2,3,3,3]
    wobei die Li'''
''' Ermittelt sowohl den Mittelwert, als auch den Fehler einer (jeweils gerundet) 
    als poissonverteilten Menge von Messwerten.'''
def r_pois_mean_err(value_list):
    mu = mean(value_list)
    stddev = m.sqrt(mu)
    n = len(value_list)
    stdf = stddev/m.sqrt(n)
    return rou_val_n_err(mu, stdf)[:2]



''' Errechnet die Wahrscheinlichkeit eines Wertes x basierend auf einer angenommenen
    Poissonverteilung einer Input-Liste'''
def poisv(value_list, x):
    mue = mean(value_list)
    p = (mue**x)/((m.e**mue)*m.factorial(x))
    return p


#Achtung! Diese Funktion ist laut T.Kiesling nicht sinnvoll.
''' Die folgende Funktion gibt den nach Gauss bestimmten Fehler der Poisson-Wahrscheinlichkeit 
    das Ereignis x-mal zu beobachten.'''
def poisv_err(value_list, x):
    mu = mean(value_list)
    err = mu**(-x-1.5) * m.exp(-mu) * (x+mu)
    return err

'''Beides kombiniert in einer Funktion, die eine Liste von Wert-Fehlerpaaren returnt:'''
def pois_vnr(value_list):
    res_list = list()
    for el in range(max(value_list)+1):
        p, sp = rou_val_n_err(poisv(value_list, el), poisv_err(value_list, el))[:2]
        res_list.append((p,sp))
    return res_list

""" Im Folgenden: 
    Die Chi-Quadrat-Abhängigkeit!"""

'''Die Wahrscheinlichkeitsverteilung der zentralen chi-quadrat-abhängigkeit'''
def chiq_vert(n):
    import math as m
    return lambda x: 1/(m.gamma(n/2)*2**(n/2))*x**((n/2) -1)*m.exp(-x/2)

''' Die Wahrscheinlichkeit für Chiq < y bei n-Freiheitsgraden. Wenn greater= True gesetzt wird (standard ist False), so wird die Wahrscheinlcihkeit für x>y ausgegeben. '''
def chiq_wahr(y,n: int,greater=False):
    import scipy.integrate as integrate
    if greater:
        return (1-integrate.quad(chiq_vert(n), 0, y)[0],integrate.quad(chiq_vert(n), 0, y)[1])
    return integrate.quad(chiq_vert(n), 0, y)

''' Hier das Chi-Quadrat zweier Listen: experimentell bestimmte (mess_haeufigkeiten) und theoretisch erwartete (erw_haeufigkeiten).'''
def chiq_of_lists(mess_hauefigkeiten, erw_haeufigkeiten):
    chiq=0
    for ind, erwartung in enumerate(erw_haeufigkeiten):
        chiq += (mess_hauefigkeiten[ind] - erwartung)**2/erwartung
    return chiq

''' Hier soll der Abschnitt zur linearen Regression beginnen.'''
''' Hier wird die Kovarianz zweier Größen berechnet.'''
def covarianz(xy_list):
    import math as m
    x_mean = mean([el[0] for el in xy_list])
    y_mean = mean([el[1] for el in xy_list])
    cov = sum([(el[0] - x_mean)*(el[1] - y_mean) for el in xy_list])/len(xy_list)
    #denominator = m.sqrt(sum([el[0] - x_mean for el in xy_list])*sum([el[1] - y_mean for el in xy_list]))
    return cov

''' Nun die Lineare Regression bei Annahme fehlerfreier Daten
    Der Output ist: (y-Achsenabschnitt, fehler), (Steigung, fehler), korrelationskoeffizient '''
def lin_Reg(xy_list, fehler=False):
    import math as m
    if not fehler:
        n = len(xy_list)
        x_list = [el[0] for el in xy_list]
        y_list = [el[1] for el in xy_list]
        x_sum = sum(x_list)
        y_sum = sum(y_list)
        x_square_sum = sum([el**2 for el in x_list])
        x_sum_square = x_sum**2
        xy_sum = sum([el[0] * el[1] for el in xy_list])
        triangle = n * x_square_sum - x_sum_square
        a = (x_square_sum*y_sum - x_sum*xy_sum)/triangle
        b = (n*xy_sum - x_sum*y_sum)/triangle
        s_square = sum([(el[1] - a - b*el[0])**2 for el in xy_list])/(n-2)
        sa = m.sqrt(abs((s_square*x_square_sum)/triangle))
        sb = m.sqrt(n*s_square/triangle)
        r = n*covarianz(xy_list)/m.sqrt(sum([(el - mean(x_list))**2 for el in x_list])*sum([(el - mean(y_list))**2 for el in y_list]))
    return (a,sa),(b,sb),r





""" Im Folgenden einige Input-/Outputfunktionen:"""


''' Liest aus einer csv-file, die Zeilen ganzer Zahlen, durch Kommata getrennt, enthalten, 
    ein und gibt sie als Liste aus. Eine solche file kann wie folgt aussehen:
    1,2,3
    2,4,8
    9,3,6
    
    ... und so weiter. 
    Dabei muss es sich nicht um tripel handeln. Es funktioneren auch alle anderen n-Tupel.
    '''


def int_from_file(filename: str):
    values = list()
    try:
        with open(filename, 'r') as f:
            strings_of_numbers = ''.join(f.readlines()).split('\n')
            for string in strings_of_numbers:
                values.extend(string.split(','))
        if values[-1] == '':
            values1 = values[:-1]
        values = [int(el) for el in values1]
    except Exception as exc:
        print(exc)
    return values


''' Ermittelt aus einer csv-file, die obigen Anforderungen genügt, 
    den Mittelwert und Fehler bei angenommener Poisson-Verteilung. '''
def pois_stats_f_csv(filename: str):
    try:
        values = int_from_file(filename)
    except:
        values = list()
    return r_pois_mean_err(values)[:2]


'''Zählt das vorkommen aller Ziffern kleinergleich <highest>.'''
def count_dgts(list: list, highest: int):
    count_dict = dict()
    for el in range(highest + 1):
        count_dict[el] = list.count(el)
    return count_dict


''' Führt count_dgts über eine csv-file aus.'''
def count_dgts_csv(filename: str, highest):
    try:
        return count_dgts(int_from_file(filename), highest)
    except Exception as ex:
        print(ex)
        return

''' Mit dieser Funktion kann mittels der obigen Funktionen aus einer Liste von Listenpaaren mit je ungerundeten Werten und
    Fehlern eine csv Datei mit korrekt gerundeten und formatierten Wert-Fehler Strings erstellt werden.
'''
def csv_create(listoflists, filename):
    from math import log
    allines = list()
    listoflists2 = [[el[0], el[1]] for el in listoflists]
    for j, vlnerr in enumerate(listoflists2):
        valerrl = vall_errl(vlnerr[0], vlnerr[1])
        nlist = [el[2] for el in vlnerr]
        lines = []
        for i, el in enumerate(valerrl):
            if el[2] >= 3 or el[2] <= -3 or el[2] == 2 or int(log(abs(el[0]))) == 2:
                # Die Summe aus dimen und ne sollte die nötige Anzahl an Nachkommastellen ergeben, wenn wir in Sci.Not sind.
                formatstr = '{0:.' + str(el[3]+el[2])+'f}'
                # Das r'' markiert einen raw-format string, sodass \ nicht zum escapen führt.
                # \:\pm\: führt escapet in LaTex zu space plusminus space (' +- ').
                lines.append(r'(\:'+formatstr.format(el[0]/10**el[2]) + r'\:\pm\:' + formatstr.format(el[1]/10**el[2]) +r'\:)x10^' + str(el[2]))
            else:
                formatstr = '{0:.' + str(el[3]) + 'f}'
                lines.append(formatstr.format(el[0]) + r'\:\pm\:' + formatstr.format(el[1]))
        allines.append(lines)
    # strwr wird der in die csv-datei zu schreibende string.
    strwr = ''
    # In linesres werden die zu strwr zu formatierenden rows gespeichert.
    linesres=list()

    for j in range(len(allines)):
        for i in range(len(allines[j])):
            try:
                linesres[i] += ',' + allines[j][i]
                # Wenn wir uns am Zeilenende befinden folgt ein Umbruch:
                if i == len(allines[j]):
                   linesres[i] += '\n'
            except:
                linesres.append(allines[j][i])
    for el in linesres:
        strwr += el + '\n'
    with open(filename, 'w', newline='') as csvfile:
        csvfile.write(strwr)
    print('Das CSV-File: ' + filename + ' wurde erstellt.')



''' Hier wird die csv-file filename geöffnet und gelesen. Es wird versucht, eine Liste aus Wert-Fehlerpaaren zu "returnen".
    Wenn Headers=True bedeutet, dass die erste Zeile die Überschriften enthält und somit ignoriert wird.
    Die Funktion geht davon aus, dass Spalten abwechselnd Werte und Fehler enthalten. (Wert1, Fehler1, Wert2, Fehler2,...)'''
def read_csv(filename,Headers=False):
    import csv
    listoflists=list()
    with open(filename,'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        klist = list()
        for line in csv_reader:
            klist.append(line)
        for k, line in enumerate(klist):
            for i in range(int(len(line)/2)):
                if k == 0 and not Headers:
                    listoflists.append([[float(line[2*i])], [float(line[2*i + 1])]])
                elif k == 1 and Headers:
                    listoflists.append([[float(line[2*i])], [float(line[2*i + 1])]])
                elif k >= 1:
                    listoflists[i][0].append(float(line[2 * i]))
                    listoflists[i][1].append(float(line[2*i +1]))
    print('Das CSV-File: ' + filename + ' wurde gelesen.')
    return listoflists

''' Für graphische Ausgaben:
    Um eine schöne graphische Ausgabe zu erhalten, kann pygame verwendet werden.
    Es muss vorher installiert werden:pip install pygame
    Als filename kann der gewünschte Name für die (möglicherweise temporäre) Datei, 
    als die die figure gespeichert wird, spezifiziert werden.
    Wenn keep=True wird die Date nicht gelöscht. Sonst wird sie im letzten Schritt der Methode gelöscht.
    Mit scale kann die Größe des quadratischen Fensters manipuliert werden. 
    Bei scale=1 sind Höhe und Breite 1000 (Pixel).'''
def fig_show(figure, filename= 'plot', scale=1, keep=False):
    import pygame
    import PIL
    import os

    full_filename = filename + '.png'
    figure.savefig(full_filename)
    pygame.init()
    with PIL.Image.open(full_filename) as im:
        width, height = im.size
    width_by_height_ratio = width / height

    X, Y = int(1000 * width_by_height_ratio*scale), int(1000*scale)

    display_surface = pygame.display.set_mode((X, Y))
    pygame.display.set_caption(filename)

    imago = pygame.image.load(full_filename)
    imago = pygame.transform.scale(imago, (X, Y))

    done = False
    while not done:
        display_surface.fill((1, 1, 1))
        display_surface.blit(imago, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        pygame.display.update()

    if not keep:
        os.remove(full_filename)


if __name__ == '__main__':
    import random
    import matplotlib.pyplot as plt
    xsample = [0]+[random.uniform(0,5) for el in range(20)]+[5]
    ysample = list(map(lambda x: 3.212*x+ 2 + random.uniform(-8.5,8.5), xsample))
    ywerte = [el*3.212 + 2 for el in xsample]
    xy_sample = [(xsample[i],ysample[i]) for i in range(len(xsample))]
    cov_xy_1 = covarianz(xy_sample)
    awerte,bewerte,r = lin_Reg(xy_sample)
    a = rou_val_n_err(awerte[0],awerte[1])
    b = rou_val_n_err(bewerte[0], bewerte[1])
    y_reg_werte = [el*b[0] + a[0] for el in xsample]
    y_max_reg_werte = [el*(b[0]+b[1])+a[0]-a[1] for el in xsample]
    y_min_reg_werte = [el * (b[0] - b[1]) + a[0] + a[1] for el in xsample]
    print(f'Die Regression für die Samplewerte ergab: f(x) = {a[0]} + {b[0]} x\n'
          f'Mit einem r von {r} \n'
          f'Dabei nimmt a den Wert {a[0]} +- {a[1]} an.\n'
          f'b = {b[0]} +- {b[1]}\n'
          f'Mit einem r von {r}\n'
          f'Die Kovarianz der Werte beträgt {cov_xy_1}')
    fig, ax = plt.subplots()
    ax.scatter(xsample, ysample, marker='x')
    ax.plot(xsample, ywerte,'--')
    ax.plot(xsample, y_reg_werte)
    ax.plot(xsample, y_max_reg_werte,'-.')
    ax.plot(xsample, y_min_reg_werte,'-.')
    fig_show(fig)
