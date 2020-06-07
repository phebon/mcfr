# mcfr
##Verwendung
Dies ist ein python-package, welches einige der wichtigsten Berechnungen und Algorithmen enthält, die für die Veranstaltung 
"Fortgeschrittene Fehlerrechnung und computergestütztes Arbeiten" benötigt werden. Dabei gliedert sich das Modul in verschiedene Bereiche:
###Rundung
Um Werte auf die n-te Nachkommastelle zu runden oder ein (Wert, Fehler)-Paar auf die korrekte Anzahl von signifikanten 
Stellen (2 signifikante des Fehlers) oder ganze Listen von (Werte, Fehler)-Paaren zu runden stehen die Funktionen
1. round_to_n
2. rou_val_n_err
3. vall_errl

zur Verfügung.
###Stats zu Wertelisten
Hier können Mittelwerte, Standardabweichungen oder Standardfehler berechnet werden. 

###Poissonverteilung
Für Listen, die anhand einer Poissonverteilung analysiert werden, stehen Funktionen zur Verfügung,
um den Mittelwertfehler oder Poissonwahrscheinlichkeiten zu berechnen.

###Zentrale Chi-Quadrat-Verteilung
Um Hypothesentests durchzuführen, steht u.a. eine Funktion zur Verfügung, um Chi-Quadrat aus einer Liste von beobachteten 
und theoretischen Werten zu berechnen oder auch, um die Wahrscheinlichkeit eines mindestens so großen Chi-Quadrats zu ermitteln. 

###Korrelation
Covarianz und Korrelationskoeffizient können berechnet werden, um Korrelationen zu beurteilen.

###Lineare Regression
Hier können aus einer Liste von Wertepaaren für eine zugrunde gelegte lineare Abhängigkeit f(x) = a + b x 
die Regressionskoeffizienten und deren Fehler sowie der Korrelationskoeffizient ermittelt werden. 
Momentan nur mit Listen gleichen Fehlers in der abhängigen Variable

###Veranschaulichungen
Hier sollen innovative Visualisierungen entstehen. Die können v.a. benutzt werden, 
wenn fig.show() für matplotlib aus unerdenklichen Gründen nicht funktioniert.

###Examples
Hier sollen einige echte Verwendungszwecke des packages aus FR2 aufgezeigt werden. 
 