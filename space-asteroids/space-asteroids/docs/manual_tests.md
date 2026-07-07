# Testy manualne (Manual Tests)

Poniższe scenariusze sprawdzają, że gra działa zgodnie z założeniami.
Wykonywane ręcznie przed każdym commitem do gałęzi `main`.

| # | Scenariusz | Kroki | Oczekiwany wynik | Status |
|---|------------|-------|------------------|--------|
| 1 | Start gry z menu | Uruchom `python main.py`, wciśnij ENTER | Gra przechodzi z menu do rozgrywki | OK |
| 2 | Sterowanie statkiem | Trzymaj strzałki/WASD | Statek skręca i przyspiesza płynnie | OK |
| 3 | Zawijanie ekranu (wrap) | Wylot statku poza krawędź ekranu | Statek pojawia się po przeciwnej stronie | OK |
| 4 | Strzelanie | Wciśnij SPACE kilka razy pod rząd | Pociski lecą z ograniczonym cooldownem | OK |
| 5 | Trafienie dużej asteroidy | Trafić LARGE asteroidę pociskiem | Asteroida znika, pojawiają się 2 MEDIUM | OK |
| 6 | Trafienie małej asteroidy | Trafić SMALL asteroidę | Asteroida znika bez potomków, punkty rosną | OK |
| 7 | Zderzenie statku z asteroidą | Doprowadzić do kolizji statek-asteroida | Statek traci życie i odradza się na środku | OK |
| 8 | Utrata wszystkich żyć | Stracić wszystkie życia (lives = 0) | Gra przechodzi do ekranu GAME OVER z wynikiem | OK |
| 9 | Restart po Game Over | Na ekranie końcowym wciśnij ENTER | Rozpoczyna się nowa gra od zera | OK |
| 10 | Powrót do menu | Na ekranie końcowym wciśnij ESC | Gra wraca do ekranu głównego menu | OK |
| 11 | Kolejny poziom | Zniszczyć wszystkie asteroidy na ekranie | Pojawia się nowe pole asteroid (o jedną więcej), wynik i życia zachowane | OK |
| 12 | Nieprawidłowy rozmiar asteroidy | Wywołać `Asteroid(pos, size="HUGE")` w konsoli | Zgłoszony wyjątek `InvalidAsteroidSizeError` | OK |

Testy automatyczne (jednostkowe) dla logiki kolizji i podziału asteroid
znajdują się w folderze `tests/` i są uruchamiane poleceniem `pytest`.
