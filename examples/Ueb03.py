import mcfr
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)
import datetime as d

''' Dieses Skript kann benutzt werden, um das Übungsblatt 03 der Fehlerrechnung 2 zu bearbeiten. Hier geht 
    es um die lineare Regression. Dafür werden Werte-Paare in Form einer List eingegeben und die Regressionskoeffizienten 
    sowie der Korrelationskoeffizient berechnet. Desweiteren werden die Ergebnisse auch mittels pyplot veranschaulicht.'''
xy_list = [(1450,1180), (2000, 1640), (2500, 2190), (1800, 1760), (1000, 900), (1500, 1200), (2000,1600), (1500, 1400),
           (1200, 1060), (1800, 1540), (1700, 1460), (1300, 1140), (1850, 1650), (2500, 2400)]
x_list, y_list = [el[0] for el in xy_list], [el[1] for el in xy_list]
''' Die Regressionskoeffizienten werden aus dem Input berechnet und mittels der Rundungsfunktion entsprechend des Fehlers gerundet. '''
awerte, bwerte, r = mcfr.lin_Reg(xy_list)
a,sa = mcfr.rou_val_n_err(awerte[0], awerte[1])[0], mcfr.rou_val_n_err(awerte[0], awerte[1])[1]
b,sb = mcfr.rou_val_n_err(bwerte[0], bwerte[1])[0], mcfr.rou_val_n_err(bwerte[0], bwerte[1])[1]
''' Die Stellenzahl für den Korrelationskoeffizienten ist recht willkürlich gewählt.'''
r = mcfr.round_to_n(r,4)
cov_xy = mcfr.covarianz(xy_list)
''' Hier werden die wichtigsten Daten ausgegeben, die angegeben werden müssen. '''
print(f'Die Gerade mit der Geradengleichung: f(x) = {a}+-{sa} + ({b}+-{sb}) x\n'+
      'Korrelationskoeffizient r = {:.3f}\n'.format(r)+
      f'Die Koeffizienten lauten also:\n'
      f'a = {awerte} = {a}+-{sa}\n'
      f'b = {bwerte} = {b}+-{sb}\n'
      f'Die Kovarianz beträgt: cov_xy = {cov_xy}')
x_basis = list(range(900,2700,20))
y_erw_werte = [a + b*el for el in x_basis]
''' Das sind die Werte für Geraden minimaler und maximaler Steigung.'''
y_max = [a - sa + (b + sb)*el for el in x_basis]
y_min = [a + sa + (b - sb)*el for el in x_basis]

fig, ax = plt.subplots(figsize=(25,20))
ax.scatter(x_list, y_list, marker='x',s=80, label='Angaben zu Ausgaben und Einnahmen')
ax.plot(x_basis, y_erw_werte,'r',linewidth=3,label=f'Beste Regressionsgerade mit r = {r}')
ax.plot(x_basis, y_min,'--b',linewidth=2,label='Regressionsgerade minimaler Steigung')
ax.plot(x_basis, y_max,'-.b',linewidth=2, label='Regressionsgerade maximaler Steigung')
ax.margins(0,.01)

ax.yaxis.set_major_locator(MultipleLocator(100))
ax.yaxis.set_minor_locator(MultipleLocator(50))
ax.xaxis.set_major_locator(MultipleLocator(100))
ax.xaxis.set_minor_locator(MultipleLocator(50))

today = d.datetime.today().strftime('%d.%m.%Y')
ax.set_title('Streudiagramm von monatlichen Ausgaben in Abhängigkeit von Einnahmen,\n Moritz Siebert, '+ today, fontsize=34, loc = 'right', y=1.015)

ax.set_ylabel('Ausgaben (€)', fontsize=30, labelpad=40)
ax.set_xlabel('Einnahmen (€)', fontsize=30, labelpad=40)

ax.tick_params(axis='both', which='major', labelsize=20, length=10, direction='in')
ax.tick_params(axis='both', which='minor', length=5, direction='in')

'''leg = ax.legend(['Angaben zu Ausgaben und Einnahmen', f'Beste Regressionsgerade mit r = {r}','Regressionsgerade minimaler Steigung',
                 'Regressionsgerade maximaler Steigung'], fontsize=24,
                title='Legende',title_fontsize=24,
              frameon=True, loc=(.1, .85))'''
leg = ax.legend(fontsize=24,
                title='Legende',title_fontsize=24,
              frameon=True, loc=(.1, .75))
leg._legend_box.align = "left"
try:
    fig.savefig('Graphisch/Plot.png')
except:
    fig.savefig('Plot.png')
