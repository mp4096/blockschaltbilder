# Boilerplate-Code-Generator
Um den Tippaufwand bei der Erstellung von Blockschaltbildern zu minimieren,
kann man den mitgelieferten Boilerplate-Code-Generator verwenden.
Er stellt lediglich ein Basisgerüst zur Verfügung; so müssen z.B. alle
Beschriftungen sowie Verbindungen mit Knick (`|-`, `-|`) anschließend
manuell hinzugefügt werden.   

## Voraussetzungen
Das Programm setzt Python 3.5+ voraus. Zur Erstellung der `bsb`-Dateien
eignet sich jeder gute Texteditor (Atom, Vim, emacs, Notepad++).

## Einfaches Beispiel
Wir legen eine Textdatei `beispiel.bsb` an. Darin wird das Blockschaltbild
wie folgt spezifiziert:

```
Skizze:
    C1  S1  S2  I1  I2  C2
                P1
                P2

Verbindungen:
    C1 - S1
    S1 - S2
    S2 - I1
    I1 - I2
    I1 - P1
    I2 - C2
    I2 - P2
    P1 - S2
    P2 - S1

Namen:
    C1: eingang
    C2: ausgang
    S1: sum 1
    S2: sum 2
    I1: int 1
    I2: int 2
    P1: p 1
    P2: p 2
```

Nun kann man mit dem Befehl `python generate_boilerplate.py beispiel.bsb`
Datei in eine LaTeX/TikZ-Datei `beispiel.tex` konvertieren.
Mit dem Befehl `python generate_boilerplate.py <Verzeichnis>` werden
alle `bsb`-Dateien im angegebenen Verzeichnis und seinen Unterverzeichnissen
konvertiert. Dabei wird nach jedem Block mit mehreren Ausgängen automatisch
eine Verzweigung platziert:

```tex
\begin{tikzpicture}


% <coordinates>
\coordinate (eingang) at (2.5, 3);
\coordinate (sum 1--coord) at (4.5, 3);
\coordinate (sum 2--coord) at (6.5, 3);
\coordinate (p 2--coord) at (8.5, 0);
\coordinate (p 1--coord) at (8.5, 1.5);
\coordinate (int 1--coord) at (8.5, 3);
\coordinate (ajnt1--coord) at (10.2, 3);
\coordinate (int 2--coord) at (10.5, 3);
\coordinate (ausgang) at (12.5, 3);
\coordinate (ajnt2--coord) at (12.6, 3);
% </coordinates>


% <blocks>
\Summationsstelle{sum 1}{sum 1--coord}{0.4 cm}
\Summationsstelle{sum 2}{sum 2--coord}{0.4 cm}
\PGlied{p 2}{p 2--coord}{1 cm}{}
\PGlied{p 1}{p 1--coord}{1 cm}{}
\IGlied{int 1}{int 1--coord}{1 cm}{}
\Verzweigung{ajnt1}{ajnt1--coord}{2 pt}
\IGlied{int 2}{int 2--coord}{1 cm}{}
\Verzweigung{ajnt2}{ajnt2--coord}{2 pt}
% </blocks>


% <connections>
\draw[thick, -latex] (eingang) -- (sum 1);
\draw[thick, -latex] (sum 1) -- (sum 2);
\draw[thick, -latex] (sum 2) -- (int 1);
\draw[thick, -latex] (p 2) -- (sum 1);
\draw[thick, -latex] (p 1) -- (sum 2);
\draw[thick] (int 1) -- (ajnt1);
\draw[thick, -latex] (ajnt1) -- (p 1);
\draw[thick, -latex] (ajnt1) -- (int 2);
\draw[thick] (int 2) -- (ajnt2);
\draw[thick, -latex] (ajnt2) -- (p 2);
\draw[thick, -latex] (ajnt2) -- (ausgang);
% </connections>


\end{tikzpicture}
```

## Syntax
Jede `bsb`-Datei besteht aus drei Bereichen, die jeweils die Skizze,
Verbindungen und Namen der TikZ-Knoten spezifizieren. Sie werden
wie folgt gekennzeichnet:

* Skizze: `Skizze:` oder `Sketch:`
* Verbindungen: `Verbindungen:` oder `Connections:`
* Namen: `Namen:` oder `Names:`

Der Doppelpunkt nach dem Stichwort ist pflicht! Weiterhin darf es kein
Leerzeichen zwischen dem Stichwort und Doppelpunkt geben.

Der Skizzenabschnitt ist pflicht, da darin die Blöcke definitert werden.
Der Verbindungs- sowie der Namenabschnitt sind optional.

### Abkürzungen für Blöcke
In der Skizze werden die Blöcke definiert, und zwar als `<Abkürzung><Zahl>`.
Hier ist die Liste von Abkürzungen:

| Block                                       | Abkürzung       |
|:--------------------------------------------|:----------------|
| Verzweigung (`\Verzweigung`)                | nicht verfügbar |
| Summationsstelle (`\Summationsstelle`)      | `S`             |
| Allgemeine Übertragungsfunktion (`\UeFunk`) | `U`             |
| M-Glied - Punktsymbol (`\MGlied`)           | `M`             |
| M-Glied - Kreuzsymbol (`\MGliedVar`)        | nicht verfügbar |
| P-Glied (`\PGlied`)                         | `P`             |
| I-Glied (`\IGlied`)                         | `I`             |
| D-Glied (`\DGlied`)                         | `D`             |
| Totzeitglied (`\TZGlied`)                   | `TZ`            |
| PT1-Glied (`\PTEinsGlied`)                  | `PTE`           |
| PT2-Glied (`\PTZweiGlied`)                  | `PTZ`           |
| Kennlinienglied (`\KLGlied`)                | `KL`            |
| Sättigung (`\Saettigung`)                   | `SAT`           |

_Anmerkungen:_

* Verzweigungen werden automatisch nach allen Blöcken mit mehreren
ausgehenden Verbindungen platziert. Ist eine Verzweigung unerwünscht
(z.B. falls ein Block tatsächlich mehrere Ausgänge haben sollte),
soll man die Ausgänge einfach in der `bsb`-Datei auslassen und später
manuell in der `tex`-Datei spezifizieren.
* Für das M-Glied mit Kreuzsymbol soll man einfach das klassische M-Glied
benutzen und anschließend in der `tex`-Datei `\MGlied` durch `\MGliedVar`
ersetzen.

### Skizze
Die Skizze wird so spezifiziert, dass der gewünschte Layout ungefähr
abgebildet wird. Die Abstände zwischen Blöcken werden in der `tex`-Datei
skaliert abgebildet, z.B.:

```
Skizze:
    C1  C2    C3
```

Hier wird der Abstand zwischen `C2` und `C3` doppelt so groß sein,
wie zwischen `C2` und `C1`.


### Verbindungen
Im Verbindungsabschnitt spezifiziert man die gerichteten Verbindungen
zwischen den Blöcken. Zusätzlich kann angegeben werden, ob der Fluss
skalar (`-`, dünne Linie mit Pfeil) oder vektoriell
(`=`, fette Linie mit Pfeil) ist:

```
Skizze:
    C1    C2    C3

Verbindungen:
    C1 - C2
    C2 = C3
```

Wird eine Verzweigung automatisch hinzugefügt, so wird die Verbindung
vom Block zu ihr ohne Pfeil gezeichnet. Leider geht die Information
über die Flussart (skalar oder vektoriell) dabei verloren; das muss
später manuell spezifiziert werden.

### Namen
Das Format `<Abkürzung><Zahl>` ist zwar praktisch für eine knappe und
eindeutige Kennzeichnung der Blöcke, ist aber auch schlecht verständlich.
Deswegen kann man im Namenabschnitt die Abkürzung "erklären". Z.B. wird
die folgende Spezifikation

```
Skizze:
    C1    C2    C3

Namen:
    C1: eingang
    C3: ausgang
```

in eine `tex`-Datei übersetzt, wo Koordinaten `eingang` und `ausgang`
definiert sind. Die Koordinate `C2` wird nicht umbennant.
