# Wyszukiwanie z literówkami (WF-02): największa dozwolona odległość edycyjna
# (Levenshtein) między wpisanym tekstem a nazwą z rejestru.
FUZZY_MAX_DISTANCE = 2
# Przy krótkich zapytaniach dwie pomyłki to już większość wyrazu, więc dla
# zapytań krótszych niż ta liczba znaków dopuszczamy tylko jedną.
FUZZY_TWO_TYPOS_MIN_LENGTH = 6
# Dłuższe zapytania są ucinane (levenshtein w PostgreSQL przyjmuje max. 255 znaków).
MAX_QUERY_LENGTH = 100

# Paginacja wyników /search.
DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100