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
`\Verzweigung[<1>]{<2>}{<3>}{<4>}`
1. Optionale TikZ-Eigenschaften (z.B. Farbe)
* Name des TikZ-Knotens (`node`)
* Position
* Größe

`\Summationsstelle[<1>]{<2>}{<3>}{<4>}{<5>}{<6>}{<7>}{<8>}`
1. Optionale TikZ-Eigenschaften (z.B. Farbe)
* Name des TikZ-Knotens (`node`)
* Position
* Größe
* Symbol auf 12 Uhr (oben)
* Symbol auf 3 Uhr (rechts)
* Symbol auf 6 Uhr (unten)
* Symbol auf 9 Uhr (links)

`\UeFunk[<1>]{<2>}{<3>}{<4>}{<5>}`
1. Optionale TikZ-Eigenschaften (z.B. Farbe)
* Name des TikZ-Knotens (`node`)
* Position
* Größe
* Inhalt des Knotens

`\PGlied[<1>]{<2>}{<3>}{<4>}{<5>}`, `\IGlied[<1>]{<2>}{<3>}{<4>}{<5>}`, `\DGlied[<1>]{<2>}{<3>}{<4>}{<5>}`
1. Optionale TikZ-Eigenschaften (z.B. Farbe)
* Name des TikZ-Knotens (`node`)
* Position
* Größe
* Verstärkung `K`

`\TZGlied[<1>]{<2>}{<3>}{<4>}{<5>}{<6>}`
1. Optionale TikZ-Eigenschaften (z.B. Farbe)
* Name des TikZ-Knotens (`node`)
* Position
* Größe
* Verstärkung `K`
* Totzeit `T_t`

`\PTEinsGlied[<1>]{<2>}{<3>}{<4>}{<5>}{<6>}`
1. Optionale TikZ-Eigenschaften (z.B. Farbe)
* Name des TikZ-Knotens (`node`)
* Position
* Größe
* Verstärkung `K`
* Zeitkonstante `T`

`\PTZweiGlied[<1>]{<2>}{<3>}{<4>}{<5>}{<6>}`
1. Optionale TikZ-Eigenschaften (z.B. Farbe)
* Name des TikZ-Knotens (`node`)
* Position
* Größe
* Verstärkung `K`
* Zeitkonstante `T` und Dämpfung `d`

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
