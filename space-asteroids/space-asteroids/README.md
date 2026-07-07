# Space Asteroids

Prosta gra 2D typu *Asteroids*: statek kosmiczny lata po ekranie i
niszczy nadlatujące asteroidy. Projekt zaliczeniowy z programowania.

## Uruchomienie

```bash
pip install -r requirements.txt
python main.py
```

Sterowanie:
- `Strzałki` / `WASD` - obrót i przyspieszenie statku
- `SPACJA` - strzał
- `ENTER` - start gry / restart po zakończeniu
- `ESC` - powrót do menu z ekranu końcowego

## Testy

Testy jednostkowe kluczowej logiki (kolizje, podział asteroid,
wyjątki) uruchamiane są poleceniem:

```bash
pytest
```

Scenariusze testów manualnych (sprawdzane ręcznie przed każdym commitem)
opisane są w [`docs/manual_tests.md`](docs/manual_tests.md).

## Struktura projektu

```
space-asteroids/
├── main.py                     # punkt wejścia, pętla gry
├── requirements.txt
├── src/
│   ├── settings.py              # wszystkie stałe/parametry w jednym miejscu
│   ├── exceptions.py             # własne wyjątki (InvalidAsteroidSizeError)
│   ├── game.py                   # klasa Game - zarządza przełączaniem stanów
│   ├── entities/                 # obiekty gry (tylko logika + rysowanie siebie)
│   │   ├── ship.py
│   │   ├── asteroid.py
│   │   └── bullet.py
│   ├── states/                   # stany gry: menu / rozgrywka / koniec gry
│   │   ├── base_state.py
│   │   ├── menu_state.py
│   │   ├── gameplay_state.py
│   │   └── game_over_state.py
│   └── utils/
│       ├── collision.py          # czysta logika kolizji, bez zależności od pygame
│       └── asset_loader.py       # buforowane wczytywanie obrazów (raz na rozmiar)
├── assets/
│   └── images/
│       ├── ship.png
│       └── asteroid.png
├── tests/                        # testy jednostkowe (pytest)
│   ├── test_collision.py
│   └── test_asteroid.py
└── docs/
    └── manual_tests.md           # opis testów manualnych
```

## Architektura (dlaczego tak, a nie inaczej)

- **Stany gry (state pattern):** `MenuState`, `GameplayState`,
  `GameOverState` implementują wspólny interfejs `BaseState`
  (`handle_events`, `update`, `draw`). Klasa `Game` trzyma tylko
  aktualny stan i przełącza go na żądanie - stany nie wołają się
  nawzajem bezpośrednio, tylko przez `self.game.xxx()`.
- **Logika oddzielona od rysowania:** np. `src/utils/collision.py`
  operuje tylko na liczbach (nie zna pygame'a), dzięki czemu można ją
  testować bez uruchamiania okna gry. Każda encja (`Ship`, `Asteroid`,
  `Bullet`) ma osobno metodę `update()` (logika) i `draw()`
  (prezentacja).
- **Wyjątki:** `InvalidAsteroidSizeError` (`src/exceptions.py`) jest
  zgłaszany, gdy ktoś spróbuje stworzyć asteroidę z nieistniejącym
  rozmiarem - pokryte testem `test_invalid_size_raises_custom_exception`.
- **Skalowalność:** dodanie nowego typu przeciwnika lub broni nie
  wymaga przebudowy kodu - wystarczy nowa klasa w `entities/`
  korzystająca z tego samego `circles_collide()` i podobnego wzorca
  `update()/draw()`. Dodanie nowego rozmiaru asteroidy to tylko wpis
  w `ASTEROID_SIZES` w `settings.py`.
- **Wydajność:** kształt każdej asteroidy (`_generate_shape`) jest
  losowany raz, w konstruktorze - nie w pętli rysowania.

## Grafika

Statek i asteroida są rysowane na podstawie własnych plików PNG
(`assets/images/ship.png`, `assets/images/asteroid.png`), a nie
prostych kształtów wektorowych. Obrazy są wczytywane i skalowane
tylko raz na dany rozmiar (cache w `src/utils/asset_loader.py`) -
nigdy wewnątrz pętli gry, zgodnie z wymogiem dbania o wydajność.

## Autor

Projekt wykonany samodzielnie (praca indywidualna, bez zespołu).

## Możliwe rozszerzenia (na przyszłość)

- Power-upy (tarcza, potrójny strzał)
- Latający UFO jako dodatkowy przeciwnik
- Zapis najlepszego wyniku (high score) do pliku
