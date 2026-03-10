1. Wejdź na stronę https://sfi.pl/pl
2. Wybierz dzień (Czwartek / Piątek / Sobota)
3. Uruchom konsolę przeglądarki (F12 lub Ctrl+Shift+I)
4. Wklej [util.js](util.js) i naciśnij Enter:
   - skrypt doda do wydarzeń czerwony X, który pozwoli usunąć wydarzenie
   - obsługuje Ctrl+Z (cofnij) i Ctrl+Y (ponów)
5. Usuń wydarzenia, których nie chcesz dodać do kalendarza
6. Wywołaj `calendarHelper.extractEvents("YYYY-MM-DD")` z datą wybranego dnia
7. Przejdź do kolejnego dnia i powtórz kroki 2, 4–6:
   - po zmianie dnia wywołaj `calendarHelper.addDeleteButtons()` aby dodać przyciski usuwania
   - wydarzenia kumulują się między wywołaniami `extractEvents`
8. Po przetworzeniu wszystkich dni wywołaj `calendarHelper.downloadICS()` — pobierze jeden plik .ics ze wszystkimi wydarzeniami

# Daty SFI 21. edycja (2026)
- Czwartek: `calendarHelper.extractEvents("2026-03-12")`
- Piątek: `calendarHelper.extractEvents("2026-03-13")`
- Sobota: `calendarHelper.extractEvents("2026-03-14")`

# Dodatkowe komendy
- `calendarHelper.clearEvents()` — wyczyść zebrane wydarzenia i zacznij od nowa
- `calendarHelper.undoDelete()` / `calendarHelper.redoDelete()` — cofnij/ponów usunięcie
