=======================================================================================================================================================


Verwendete Module:
pygame 1.9.6
keras 2.4.3
numpy 1.19.3
tensorflow 2.4.0
PIL 7.1.1

Programmiersprache:
Python 3.7 x64 (wahrscheinlich funktioniert aber auch alles in 3.9)

IDE:
Entwickelt in PyCharm Community Edition 2020.1.1 x64


=======================================================================================================================================================


Meine Implementation eines Neuronalen Netzes mit dem Backpropagation Algorithmus ist wie folgt zu bedienen:
1.	Lokalisieren Sie die „python.exe“ Datei und Kopieren sie ihren Pfad (sollte also auf „\python.exe“ enden)
2.	Öffnen Sie ein neues Terminal Fenster in dem Ordner in dem sich die „neuralNetworkFromConsole.py“ Datei befindet.
3.	Kopieren Sie den Pfad der „python.exe“ Datei in das Terminal (wenn ihr Pfad Leerzeichen enthält muss er in doppelten Anführungszeichen geschrieben sein)
4.	Nach einem Leerzeichen folgt dann der Name der Datei, die sie ausführen möchten nämlich “neuralNetworkFromConsole.py“
5.	Nach einem weiteren Leerzeichen „--h“ eingeben um Hilfe über die Parameter zu erhalten.
6.	Wenn Sie sich die Parameterverwendung durchgelesen haben können Sie anstatt des „-h“ die jeweiligen Parameter schreiben und durch Ausführen des Befehls das Programm starten.

Hier ein Beispiel: 
C:\ ... \Programm>"C:\ ... \python.exe" neuralNetworkFromConsole.py -e 2 -h [2] -o 1 -i 10000

Ich empfehle sehr das Programm, wie beschrieben, in der Console auszuführen,
da sonst manche Features nicht funktionieren!

(Noch was: In der Network Console können sie "help" eingeben, um sich Hilfe anzeigen zu lassen)

(Noch noch was: Sie können (meistens) Prozesse in der Console mit Strg+C abbrechen)

(Noch noch noch was: Wenn sie gefragt werden, ob sie ein vorgefertigtes model laden möchten, gehen sie auf
		     Ja und laden sie den ORDNER "model_80%" (nicht die inhalte in dem ordner))

Wenn ihnen die Live-Visualisierung, die Sie unbedingt ausprobieren sollten, des NN zu langsam ist, können sie in "NeuralNetwork.py" in c.a. Zeile 144
die step_size variieren, wobei eine größere step_size zu besserer performance führt (aber auch zu schlechtere grafik).
Sie können einstellen, ob die Live-Visualisierung mit oder ohne Gradienten passieren soll, indem sie in c.a. Zeile 146
die Variable fade auf entweder True oder False setzen. (Einen Einfluss auf die Performance wird diese Variable nicht haben).


=======================================================================================================================================================


Das datasetgenerator.py skript ist ein ausführbares Tool um sog. ".dataset" Dateien zu erstellen. 
Diese können theoretisch auch in LayerApplyingTool.py geladen werden, aber das ist
optional und erfordet leichte modifikationen am Code. Daher muss, wenn man normale
Bilder in LayerApplyingTool.py laden will, der Datentyp zuerst von "Dataset Files"
nach "all files" geändert werden.
Das Skript LayerApplyingTool.py habe ich irgendwann im Dezember geschrieben
und dabei einige Bugs eingebaut. Es ist alles andere als Stabil, aber wenn 
man es richtig bedient funktioniert es noch.


=======================================================================================================================================================


Das presentResults.py skript enthält den Editor, der für die Präsentation der 
Ergebnisse im letzten Teil der Facharbeit genutzt wird. Dieses Skript ist
von sich aus nicht ausführbar und wird nur von "Convolutional Neural Network.py" importiert.


=======================================================================================================================================================


Die Skripte "showimage.py" und "visualize_w_nn.py" sind beides Skripte, die nur
von anderen Skripten importiert werden. "showimage.py" zeigt Bilder in einem
pygame Fenster an und "visualize_w_nn.py" visualisiert die Outputs eines NNs
bei zwei Inputs von 0-1 im Bereich von 0-1 auf der x und y Achse und im Bereich
von 0 (rot) und 1 (grün) bei der Farbe. 


=======================================================================================================================================================

Alle Skripte sind von mir geschrieben und 
Alle Kommentare und Textausgaben in den Programmen sind auf Englisch,
da ich vorhabe alles noch auf GitHub hochzuladen und ich mir das einfach
so angeeignet habe.