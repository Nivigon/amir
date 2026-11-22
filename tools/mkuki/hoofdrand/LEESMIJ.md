# Hoofdrand van de Mkuki-lijven (22-11)

Repareert de rand van het hoofd: gaten, inkepingen, rafels en paarse zoom weg, en een nette donkere buitenlijn zoals de
goede originelen (springen, bukken). Volgorde: `alles.py` (alle frames, methode `synth` uit `rand.py`), `overrides.py`
(frames waar het hoofd met de hand is aangewezen: `handkop.py`, en de ondersteboven rol `rolcirkels.py` + `rolfix.py`),
dan `vuist.py` (vuistlagen die een stuk van het oude hoofd bevatten). Daarna bakken met `tools/mkuki_spel_bak.py`,
`_los.py`, `_zones.py` op main. De scripts gaan uit van de mappen uit die chat (/home/claude/oud = lijven van voor de fix).

Methode `synth`: vorm = Mkuki zelf, glad (sluiten r3, openen r2), grote inkepingen alleen dicht waar het origineel hoofd
heeft, hooguit 3 px naar het gladde origineel als die samenvallen; nooit een spleet naar arm/hand dichtmaken. Lijn uit
een subpixel-afstandsveld, dikte 1,05% van de hoofdmaat van de set, kleur (16,4,4). Oude donkere/wazige randpixels eerst
opnieuw ingekleurd vanuit de huid. Alleen randen tegen de lucht, niet bij de kralen.

Lessen: de lijn meten (niet alleen de vorm); vuistlagen kunnen een stuk hoofd bevatten; de kleur van doorzichtige pixels
niet meenemen bij inkleuren; per set de hoofdmaat gebruiken (een half herkend hoofd geeft een te dunne lijn).
