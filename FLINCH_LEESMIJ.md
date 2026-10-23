# Schildbandiet: flinch (geraakt) - aanvulling

Alleen de nieuwe geraakt-animatie. Loop en strike had je al.
Zelfde canvas (544x860), grondlijn (781) en anchorX (272) als loop en strike,
dus hij blijft op zijn plek bij het wisselen.

- flinch_metschild/      hit-reactie MET schild (flinch_00..flinch_20), 21 frames
- flinch_zonderschild/   zelfde reactie ZONDER schild (voor na de schildbreuk)

Gedrag bij een treffer:
- Speel de flinch af bij elke treffer (de 3 treffers die het schild stuk maken).
- Hij schuift bij de klap een klein stukje naar ACHTEREN (knockback in code) met de
  bestaande stofwolk-particles aan zijn voeten.
- Speelt REDELIJK SNEL af (zie durations_ms in flinch_metadata.json; holds al kort).
- Hij twist even in naar de camera; het schild blijft vooraan en trackt mee (zit al
  per-frame in de frames).
