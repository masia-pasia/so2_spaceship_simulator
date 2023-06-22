# Symulator statku kosmicznego
## Opis projektu 
Przedmiotem tego projektu było stworzenie symulotora statku kosmicznego, którego zadaniem jest zebranie 10 puszek piwa, które skończyło sie na studenckiej imprezie. Kierujący statkiem musi unikać asteroid, które to znisczyłyby statek. Pojazd jest wyposażony w działo laserowe, które może zniszczyć asteroidy. Niestety statek ma ograniczoną ilość paliwa, która jest zużywana cały czas, więc aby przetrwać, musi też byc zbierane paliwo. W przypadku kontaktu asteroidy z piwem bądź paliwem oba przedmioty są niszczone. 
## Wątki oraz sekcja krytyczna
W projekcie są dwa wątki (poza głównym), z czego jeden jest odpowiedzialny za zużywanie paliwa, a drugi za tankowanie, gdy statek najedzie na paliwo. Oba wątki pracują na zasadzie pętli while True, natomiast wątek odpowidzialny za zużywanie paliwa jest usypiany na ustalony czas, a wątek odpowiedzialny za dodawanie paliwa czeka na powiadomienie przez wątek główny, że doszło do "kontaktu" pomiędzy statkiem a paliwem. Takie rozwiązanie było konieczne, ponieważ bez zastosowanego powiadamania gra zaczynała się zacinać przy kilku wystrzelonych pociskach, których położenie trzeba było aktualizować. Dostęp do współdzielonego zasobu, w tym przypadku aktualnego stanu paliwa, odbywa się za pomocą semafora, który na czas modyfikacji zaosbu blokuje do niego dostęp. 
