Nieuwe sprites voor de schildbandiet, met beschadigde schilden. Zie LEESMIJ_schildfases.md
in de map schildbandiet/ van deze zip.

1. Kopieer de mappen uit schildbandiet/ naar enemies/schildbandiet/ en vervang wat al
   bestaat: strike_metschild, strike_zonderschild, flinch_metschild. Voeg toe:
   strike_fase1, strike_fase2, flinch_fase1, flinch_fase2, flinch_zonderschild.
   Raak loop_metschild en loop_zonderschild niet aan.
2. Vervang enemies/schildbandiet/metadata.json door de nieuwe versie uit de zip.
3. Neem de schildfases op in het spel. Nu wisselt hitSchildman pas na de derde treffer
   van set (s.metSchild). Maak daar een schildstaat van met vier standen:
   0 treffers metschild, 1 treffer fase1, 2 treffers fase2, 3 treffers zonderschild
   (schild weg, daarna in één klap dood, zoals nu).
   - strike en flinch kiezen hun set op die stand.
   - de loop blijft metschild tot de derde treffer, daarna zonderschild.
   - bij een treffer speelt de flinch al in de nieuwe stand, zodat de hap verschijnt op
     het moment van de klap.
   - flinch_zonderschild bestaat nu, dus gebruik die na de derde treffer in plaats van
     flinch_metschild.
4. Neem de nieuwe sets mee in schbLaad, warmBouw, de laadpoort, de offline-download en
   de kleine set (KLEIN_FAM / gen-klein.py).
5. Teken elke set als het hele canvas 544 x 860 met de grondlijn (781) op dezelfde
   scherm-y en anchorX 272, net als de bestaande sets. Niet bijsnijden.
6. Test in het testlevel van de schildbandiet: raak hem drie keer en controleer dat je
   bij elke treffer de volgende schildstaat ziet, in strike en flinch, zonder verspringen.
