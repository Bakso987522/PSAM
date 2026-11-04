# AgroLupa

Inteligentna wyszukiwarka środków ochrony roślin (ŚOR).

## Opis projektu

AgroLupa to responsywna aplikacja internetowa do wyszukiwania środków ochrony roślin dopuszczonych do obrotu w Polsce.
Korzysta z publicznego rejestru Ministerstwa Rolnictwa i Rozwoju Wsi, publikowanego raz na kwartał w serwisie
[dane.gov.pl](https://dane.gov.pl/pl/dataset/550). Rejestr ma postać plików XLSX i CSV, które trudno przeglądać na telefonie.

Aplikacja ma umożliwić:
- wyszukiwanie środków po nazwie, uprawie, agrofagu i substancji czynnej, z tolerancją literówek,
- rozróżnienie środków dla użytkowników profesjonalnych i amatorów,
- znajdowanie zamienników o tym samym składzie, np. tańszego środka w większym opakowaniu,
- szybki podgląd dawek, terminów stosowania i okresów karencji.

Dane są pobierane automatycznie przez importer, który sprawdza nowe wersje rejestru i wczytuje je do bazy.

Pełny opis projektu i specyfikacja wymagań: [Docs/Opis_projektu.pdf](Docs/Opis_projektu.pdf).

## Technologie

| Warstwa | Technologie |
|---|---|
| Baza danych | PostgreSQL 17 |
| Importer danych | Python 3.13, httpx, openpyxl, psycopg 3, supercronic (harmonogram) |
| Backend (API) | Python 3.13, FastAPI, Uvicorn, psycopg 3 |
| Frontend | Nuxt 4, Vue 3, Tailwind CSS 4, Reka UI |
| Środowisko | Docker, Docker Compose, Task (opcjonalnie), Nix (opcjonalnie) |

## Wymagania

- [Docker Desktop](https://www.docker.com/products/docker-desktop/), albo Docker Engine z wtyczką Compose v2,
- Git,
- opcjonalnie [Task](https://taskfile.dev) do skrótów poleceń z `Taskfile.yml`,
- opcjonalnie Nix z direnv: `flake.nix` udostępnia powłokę z Pythonem, Node.js, pnpm i Taskiem.

Wszystkie usługi działają w kontenerach, więc Python, Node.js ani PostgreSQL nie muszą być zainstalowane lokalnie.

## Instalacja

```bash
git clone https://github.com/Bakso987522/PSAM.git
cd PSAM
cp .env.example .env        # PowerShell: Copy-Item .env.example .env
```

W pliku `.env` ustaw własne hasło do bazy (`POSTGRES_PASSWORD`). Pozostałe wartości mogą zostać domyślne:

| Zmienna | Znaczenie | Domyślnie |
|---|---|---|
| `FRONTEND_PORT`, `API_PORT`, `DB_PORT` | porty na komputerze | 3000, 8000, 5432 |
| `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` | dane dostępowe bazy | agrolupa, agrolupa, change-me |
| `DANE_GOV_DATASET_ID` | numer zbioru w dane.gov.pl | 550 |
| `IMPORT_CRON` | harmonogram importu w formacie cron | `0 3 * * *` (codziennie o 3:00) |

## Uruchomienie

Uruchomienie bazy, API i frontendu:

```bash
docker compose up -d
```

Pierwsze uruchomienie buduje obrazy i trwa kilka minut. Przy starcie pustej bazy schemat tworzy się
automatycznie z plików w `db/init/`.

Import danych z rejestru (jednorazowo, na żądanie):

```bash
docker compose run --rm importer python -m importer run
```

Importer pomija wersję rejestru, która jest już wczytana. Żeby wczytać ją ponownie, dodaj `--force`.

Po uruchomieniu:
- frontend: http://localhost:3000
- API: http://localhost:8000 (dokumentacja: http://localhost:8000/docs, stan: http://localhost:8000/health)
- baza: `localhost:5432`, z danymi logowania z `.env`

Przydatne polecenia:

| Polecenie | Skrót w Tasku | Działanie |
|---|---|---|
| `docker compose up -d` | `task up` | uruchamia wszystkie usługi |
| `docker compose down` | `task down` | zatrzymuje usługi; dane w bazie zostają |
| `docker compose logs -f api` | `task logs -- api` | pokazuje logi usługi |
| `docker compose up -d --build` | `task rebuild` | przebudowuje obrazy po zmianie zależności |
| `docker compose run --rm importer python -m importer run` | `task import` | wykonuje import danych |
| `docker compose down -v` i `docker compose up -d` | `task db:reset` | usuwa bazę i tworzy ją od nowa z `db/init/` |

## Struktura repozytorium

```
api/        backend (FastAPI)
db/init/    schemat bazy danych, wykonywany przy pierwszym starcie kontenera
frontend/   frontend (Nuxt)
importer/   importer danych z dane.gov.pl
Docs/       dokumentacja projektu (LaTeX)
```

## Autorzy

| Osoba | Odpowiedzialność |
|---|---|
| Jakub Bakaj | baza danych, importer |
| Natalia Duda | backend (API) |
| Damian Nowak | frontend, UX |
