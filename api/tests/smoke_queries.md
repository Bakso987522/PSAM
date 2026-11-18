# Ręczne zapytania kontrolne (na uruchomionym API z zaimportowanymi danymi)

Kryteria akceptacji z dokumentacji (6.7.1). Sprawdź `fuzzy` w odpowiedzi i kolejność wyników.

| Zapytanie | Oczekiwane |
|---|---|
| `/search?q=Amistar` | Amistar na początku, `"fuzzy": false`, żadnych "podobnych" środków |
| `/search?q=AMISTAR`, `?q=amistar` | to samo co wyżej |
| `/search?q=Amistr` | Amistar 250 SC w pierwszych 5 wynikach (jeśli żaden środek nie zawiera "amistr") |
| `/search?q=Amitsar`, `?q=Amistarr` | Amistar 250 SC w pierwszych 5, `"fuzzy": true` |
| `/search?q=xyzxyz` | `total: 0`, `"fuzzy": true` |
| `/search?q=Amistar&crops=ziemniak` (brak takiego zastosowania) | `total: 0`, ale `"fuzzy": false` (filtry za ostre, nie literówka) |
| `/suggest/crops?q=pszenzyto` | podpowiada pszenżyto |
| `/suggest/names?q=amistar` | środki Amistar, bez "podobnych" substancji |
| `/search?q=50%25` | traktuje `%` jako zwykły znak |