# Kaarslicht op het startscherm

## kaarslicht: de startfoto van onderen belicht

`KAARS`, `kaarsStart`, `kaarsLus`, `kaarsWek`, `kaarsPositie`: de foto achter het startscherm en al zijn menu's (`design/menu/held.jpg`) wordt in een WebGL-canvas in `.startart` opnieuw belicht door een flakkerende kaars onder zijn kin. Het reliëf komt uit de helderheid van de foto (klein en vervaagd), dus de lichte kanten en schaduwen schuiven mee met de vlam; geen echte slagschaduw. Het canvas ligt onder de verlopen van `.startart` en legt de foto neer zoals de CSS (cover, dezelfde `background-position`, elke 30 beelden opnieuw gelezen). Draait alleen zolang `#start` open is en het tabblad zichtbaar (`MutationObserver` op de klasse, `visibilitychange`). Zonder WebGL blijft de gewone foto staan
