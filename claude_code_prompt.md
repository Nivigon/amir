Update op het lagen-pakket van de schildbandiet (versie lagen-2). Er stonden dubbele
plaatjes in: hetzelfde schildstuk stond per frame opnieuw in de map. Nu staat elk
plaatje er één keer in. Het beeld is exact hetzelfde, alleen de bestandsnamen zijn
anders. Lees schildbandiet/LEESMIJ_lagen.md.

1. Vervang in enemies/schildbandiet/ de map lagen/ helemaal door de nieuwe (submappen
   schild/ en lijf/), en vervang lagen.json. Verwijder eerst de oude map lagen/ met de
   submappen loop/, strike/ en flinch/, zodat er geen oude bestanden achterblijven.
2. Laad elk plaatje één keer op zijn pad (src), ook als het in meerdere frames of staten
   voorkomt: één Image per src, gedeeld. Doe dat ook voor de bewaarde witte kopie (flits)
   en voor de kleine versie.
3. Kleine set: opnieuw halveren via gen-klein.py / KLEIN_FAM met de nieuwe map. dx, dy, w
   en h blijven in grote-set-pixels.
4. Offline-download en cache: oude lagen-bestanden eruit, nieuwe erin, cache-versie
   ophogen.
5. Controleer dat er geen verwijzing meer is naar lagen/loop/, lagen/strike/ of
   lagen/flinch/, en dat het testlevel er precies zo uitziet als met de vorige versie.
   Meet het geheugen van de schildbandiet; het hoort ongeveer 17 MB lager uit te komen.
