# Stenen bogen (Amir, King of Africa)

Gemetselde bogen met een donkere opening, bedoeld als de poorten waar vijanden in een
arena uit komen (het idee: drie poorten, waarvan een of twee op een richel). Nog nergens
in het spel gebruikt.

De opening is ingevuld zoals de opening van de deur (`design/deur/deur_open.png`): van
boven naar onder donkerbruin dat iets oploopt, links iets lichter dan rechts, een
lichtere vloerstrook onderin en een zachte schaduw onder de boog. De achtergrond is
transparant.

## Wat zit erin

```
boog_steen.png           smalle, vrijstaande boog van gezaagde blokken (hoog)
boog_rots.png            dezelfde soort boog, ingebouwd in een ruwe rotsmassa (hoog)
boog_laag_1..4.png       lage, brede boog met gestapelde muurtjes ernaast; vier bijna
                         gelijke varianten, om af te wisselen
metadata.json            per boog de maat en de opening [x0, y0, x1, y1] in pixels
bron/                    de aangeleverde platen (wit met een magenta opening)
```

## Plaatsing

- De onderkant van de opening is de grondlijn: zet `opening[3]` op de grond.
- Schaal op de hoogte van de opening. In de mockups: hoog (`boog_steen`, `boog_rots`)
  op ongeveer 1,65 keer Amir, laag (`boog_laag_*`) op ongeveer 1,15 keer Amir. De lage
  past op een richel zonder dat hij onder de teller bovenin komt.
- De opening is rond aan de bovenkant; de houten deur uit `design/deur/` is recht en
  past er dus niet in.

## Opnieuw maken

Na een nieuwe of vervangen plaat in `bron/`:

```
python3 tools/boog_vulling.py
python3 tools/gen-offline-manifest.py
```

Ze staan (nog) niet in `klein/`: dat gebeurt pas als ze in het spel komen en hun maat
op een telefoon gemeten is (zie `tools/gen-klein.py`).
