import mcfr
import datetime as d
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter)

''' Input: Eingeben der Wert-Häufigkeitspaare als nichtnegatie Ganze Zahlen'''
#xdict = {0: 11, 1: 80, 2: 65, 3: 74, 4: 51, 5: 25, 6: 19, 7: 9, 8:2}
xdict = {0: 14, 1: 80, 2: 77, 3: 77, 4: 42, 5: 25, 6: 16, 7: 3, 8:2}
author_name = 'Autor'
'''Input: Farben der Bars im Plot als (r,g,b) wobei r,g,b je floats zwischen 0 und 1 sind.'''
col1 = (.1,.6,.4,0)

hatch1 = '|'
ecol1 = (0,0,0,1)
col2 = (.6,.2,.3,0)

hatch2 = "/"
ecol2 = (0,0,0,.6)

n = sum(xdict.values())

xvaluelist = [key for key, value in xdict.items() for i in range(value)]

expected_p_1 = mcfr.pois_vnr(xvaluelist)
expected_p_1_vals = [el[0] for el in expected_p_1]

expectedp = [mcfr.poisv(xvaluelist, el) for el in xdict]
expected_p_1_dict = {ind: el for ind, el in enumerate(expected_p_1)}
print("Anzahl an Ereignissen: ",n)
print(f'Die theoretisch erwarteten Werte für p(x) lauten mit Fehler:\n',expected_p_1_dict)


relh = [el/n for el in xdict.values()]

'''Hier beginnt das Plot-Setup'''
today = d.datetime.today().strftime('%d.%m.%Y')
barwidth = 1
fig, ax = plt.subplots(figsize=(20, 21.7))
#fig, ax = plt.subplots()
ax.set_title(f'Vergleich der beobachteten relativen Häufigkeit mit der Poissonwahrscheinlichkeit,\n {author_name}, '+ today,fontsize=30, loc = 'right', y=1.008)

'''Hatch-Linienstärke'''
#matplotlib.rcParams['hatch.linewidth'] = 2  # previous pdf hatch linewidth
#matplotlib.rcParams['hatch.linewidth'] = 2.2  # previous svg hatch linewidth

'''Für übereinander-liegende Bars'''
ax.bar([el for el in xdict.keys()], relh, color=col1, width=barwidth, hatch=hatch1, edgecolor=ecol1,linewidth=2)
ax.bar([el for el in xdict.keys()], expectedp, color=col2, width=barwidth, hatch=hatch2, edgecolor=ecol2,linewidth=2)
ax.set_xlim(xmin=-.5,xmax=8.5)
#txt='Abb. 1: Histogramm zur Detektion von Gamma-Quanten in einer Torzeit von 1s \nbei experimentell bestimmten 2.839 erwarteten Ereignissen'
ax.set_xlabel('Anzahl an detektierten Ereignissen', fontsize=26, labelpad=40)
ax.xaxis.set_major_locator(MultipleLocator(1))
ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
ax.set_ylabel('Detektionswahrscheinlichkeit', fontsize=26, labelpad=40)


ax.yaxis.set_major_locator(MultipleLocator(0.02))
ax.yaxis.set_minor_locator(MultipleLocator(0.01))
ax.yaxis.set_major_formatter(FormatStrFormatter('%.3f'))

ax.tick_params(axis='both', which='major', labelsize=20)
ax.tick_params(which='both', width=2)
ax.tick_params(which='major', length=7)
ax.tick_params(which='minor', length=4)

leg = ax.legend(['Relative Häufigkeit','Poisson-Wahrscheinlichkeit'], loc=(.48,.88), fontsize=30,
          frameon=False, title='Legende', title_fontsize=30)
leg._legend_box.align = "left"

#fig.text(.1195, .03, txt, ha='left', fontsize=20)
fig.savefig('Graphisch/MarvinHist.pdf')
fig.savefig('Graphisch/MarvinHist.png')
print(f'Für \mu ergibt sich: ({mcfr.r_pois_mean_err(xvaluelist)[0]}+-{mcfr.r_pois_mean_err(xvaluelist)[1]})')
mcfr.fig_show(fig, scale=1.3)
