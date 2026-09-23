# Dorpsdecor voor Amir, King of Africa

Acht transparante PNG's voor het bouwen van dorpslevels. Magenta is weggekeyed met
een hue-gebaseerde score inclusief despill, dus geen roze randjes.

## Inhoud

| bestand | wat | spiegelbaar |
|---|---|---|
| village/hut_round_arch.png | ronde leemhut met boogdeur (de bestaande) | ja |
| village/hut_round_door_left.png | ronde leemhut, plankdeur links | ja |
| village/hut_round_back.png | ronde leemhut van achteren | ja |
| village/hut_rect_porch.png | rechthoekige hut met veranda | nee |
| village/hut_rect_back.png | rechthoekige hut van achteren | nee |
| village/cooking_shelter.png | open kookafdak met vuur | ja |
| village/well.png | waterput | ja |
| village/foreground/hut_round_back_closeup.png | grote achterkant als voorgrondlaag | ja |

hut_rect_porch en hut_rect_back hebben harde slagschaduwen van links. Gespiegeld valt
het licht de verkeerde kant op, dus die twee niet flippen.

## Schaal

metadata.json geeft per asset `heightInPlayerHeights`: hoe hoog het object getekend
moet worden, uitgedrukt in de gerenderde hoogte van Amir. Dat werkt ongeacht het
canvasformaat of de zoomstand.

    drawH = amir.renderHoogte * heightInPlayerHeights
    drawW = drawH * png.width / png.height

Ankerpunt is midden onder. Zet het object 3 procent van zijn hoogte onder de grondlijn
(`sinkPct`), dan verdwijnt de rand van de zandplek in de grond.

Gecontroleerd tegen een screenshot van het spel: de ronde hut komt dan precies even
hoog uit als de hut die er nu al staat. Zie preview_testplaatsing.png.

## Nog te maken

De voorgrondhut is een opgeschaalde versie van hut_round_back.png. Bruikbaar, maar
voor een echte close-up is een nieuwe generatie scherper. Grok-prompt daarvoor:

    Using the attached hut as the exact style reference (same line weight, same colour
    palette, same mud and straw texture), draw a DIFFERENT hut in that identical style:
    a large round African village hut seen from BEHIND, close up, filling the entire
    frame from top to bottom, viewed straight on at eye level. Cracked sun-dried mud
    wall in warm tan and ochre filling most of the frame, with visible plaster patches,
    hairline cracks and a coarse surface. NO door on this side. The lower edge of a
    thatched roof of dry straw with a ragged fringed edge crosses the top of the frame.
    Leaning against the wall: a bundle of firewood and a woven basket. Tufts of dry
    savannah grass and a few grey rocks along the bottom. Style: clean 2D cartoon,
    thick black outlines, flat colours with light cross-hatch texture, in the style of
    Blood and Mead. Solid magenta #FF00FF background, nothing else in frame, no shadow
    on the background, no ground plane, no sky. No motion blur, no effects, no text.
