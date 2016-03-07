![logo](logo.png)
_Einfache Blockschaltbilder in LaTeX/TikZ_

## Installation
Einfach die Datei `src/blockschaltbilder.tex` in das Dokument hinzufügen, z.B.:

```tex
\input{<Pfad zum Verzeichnis mit der Datei>/blockschaltbilder}
```

## Verfügbare Makros
* Verzweigung (`\Verzweigung`)
* Summationsstelle (`\Summationsstelle`)
* Allgemeine Übertragungsfunktion (`\UeFunk`)
* P-Glied (`\PGlied`)
* I-Glied (`\IGlied`)
* D-Glied (`\DGlied`)
* Totzeitglied (`\TZGlied`)
* PT1-Glied (`\PTEinsGlied`)
* PT2-Glied (`\PTZweiGlied`)

## Argumente
* `\Verzweigung[O]{<1>}{<2>}{<3>}`
    0. Optionale TikZ-Eigenschaften (z.B. Farbe)
    1. Name des TikZ-Knotens (`node`)
    2. Position
    3. Größe
* `\Summationsstelle[O]{<1>}{<2>}{<3>}{<4>}{<5>}{<6>}{<7>}`
    0. Optionale TikZ-Eigenschaften (z.B. Farbe)
    1. Name des TikZ-Knotens (`node`)
    2. Position
    3. Größe
    4. Symbol auf 12 Uhr (oben)
    5. Symbol auf 3 Uhr (rechts)
    6. Symbol auf 6 Uhr (unten)
    7. Symbol auf 9 Uhr (links)
* `\UeFunk[O]{<1>}{<2>}{<3>}{<4>}`
    0. Optionale TikZ-Eigenschaften (z.B. Farbe)
    1. Name des TikZ-Knotens (`node`)
    2. Position
    3. Größe
    4. Inhalt des Knotens
* `\PGlied[O]{<1>}{<2>}{<3>}{<4>}`, `\IGlied[O]{<1>}{<2>}{<3>}{<4>}`, `\DGlied[O]{<1>}{<2>}{<3>}{<4>}`
    0. Optionale TikZ-Eigenschaften (z.B. Farbe)
    1. Name des TikZ-Knotens (`node`)
    2. Position
    3. Größe
    4. Verstärkung `K`
* `\TZGlied[O]{<1>}{<2>}{<3>}{<4>}{<5>}`
    0. Optionale TikZ-Eigenschaften (z.B. Farbe)
    1. Name des TikZ-Knotens (`node`)
    2. Position
    3. Größe
    4. Verstärkung `K`
    5. Totzeit `T_t`
* `\PTEinsGlied[O]{<1>}{<2>}{<3>}{<4>}{<5>}`
    0. Optionale TikZ-Eigenschaften (z.B. Farbe)
    1. Name des TikZ-Knotens (`node`)
    2. Position
    3. Größe
    4. Verstärkung `K`
    5. Zeitkonstante `T`
* `\PTZweiGlied[O]{<1>}{<2>}{<3>}{<4>}{<5>}`
    0. Optionale TikZ-Eigenschaften (z.B. Farbe)
    1. Name des TikZ-Knotens (`node`)
    2. Position
    3. Größe
    4. Verstärkung `K`
    5. Zeitkonstante `T` und Dämpfung `d`

## Empfohlene Größen
| Element                         | Größe    | TikZ-Eigenschaften             |
|:--------------------------------|:---------|:-------------------------------|
| Verzweigung (skalar)            | `2 pt`   |                                |
| Verzweigung (vektoriell)        | `4 pt`   |                                |
| Summationsstelle                | `0.4 cm` |                                |
| Vordefinierter Block            | `1 cm`   |                                |
| Allgemeine Übertragungsfunktion | `1 cm`   | _optional:_ `inner sep = 8 pt` |
| Skalarer Signalfluss            |          | `thick, -latex'`               |
| Vektorieller Signalfluss        |          | `ultra thick, -latex'`         |
