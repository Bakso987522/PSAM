import type { LocationQuery, LocationQueryRaw, LocationQueryValue } from "vue-router";
import { ROUTES } from "~/constants/routes";
import {
    DEFAULT_PAGE,
    DEFAULT_PAGE_SIZE,
    PAGE_SIZE_OPTIONS,
    ROLE_OPTIONS,
    type PageSize,
} from "~/constants/search";
import { useProductFormatter } from "~/hooks/useProductFormatter";
import { EMPTY_SEARCH_RESPONSE, toSearchResponse } from "~/mappers/search";
import { fetchSearch } from "~/services/api";
import type { SearchApiRequest } from "~/types/api/search";
import type { ActiveFilter, ListFilterKind } from "~/types/search/ActiveFilter";
import type { SearchCriteria } from "~/types/search/SearchCriteria";
import { UserRole } from "~/enums/UserRole";

const LIST_FILTER_KINDS: ListFilterKind[] = ["crops", "pests", "productTypes"];

const toStringList = (
    value: LocationQueryValue | LocationQueryValue[] | undefined,
) => {
    return [value]
        .flat()
        .filter((item): item is string => typeof item === "string")
        .map((item) => item.trim())
        .filter((item) => item !== "");
};

const isUserRole = (value: unknown): value is UserRole => {
    return ROLE_OPTIONS.some((option) => option.value === value);
};

const isPageSize = (value: number): value is PageSize => {
    return PAGE_SIZE_OPTIONS.some((option) => option === value);
};

const parsePage = (value: string | undefined) => {
    const page = Number(value);
    return Number.isInteger(page) && page >= 1 ? page : DEFAULT_PAGE;
};

const parsePageCount = (value: string | undefined): PageSize => {
    const pageCount = Number(value);
    return isPageSize(pageCount) ? pageCount : DEFAULT_PAGE_SIZE;
};

const parseSearchCriteria = (query: LocationQuery): SearchCriteria => {
    const role = toStringList(query.role)[0];

    return {
        q: toStringList(query.q)[0],
        crops: toStringList(query.crops),
        pests: toStringList(query.pests),
        productTypes: toStringList(query.productTypes),
        role: isUserRole(role) ? role : undefined,
        page: parsePage(toStringList(query.page)[0]),
        pageCount: parsePageCount(toStringList(query.pageCount)[0]),
    };
};

const toSearchApiRequest = (criteria: SearchCriteria): SearchApiRequest => {
    return {
        q: criteria.q,
        crops: criteria.crops,
        pests: criteria.pests,
        productTypes: criteria.productTypes,
        role: criteria.role,
        page: criteria.page,
        pageCount: criteria.pageCount,
    };
};

const searchProducts = async (criteria: SearchCriteria) => {
    const params = toSearchApiRequest(criteria);
    const response = await fetchSearch(params);

    const hasResults = (result: typeof response) => {
        return (result.total ?? result.count) > 0;
    };

    if (criteria.role !== UserRole.Amateur || hasResults(response)) {
        return toSearchResponse(response, criteria);
    }

    const professional = await fetchSearch({ ...params, role: UserRole.Professional });
    return toSearchResponse(response, criteria, hasResults(professional));
};

const toLocationQuery = (criteria: SearchCriteria): LocationQueryRaw => {
    return {
        q: criteria.q,
        crops: criteria.crops,
        pests: criteria.pests,
        productTypes: criteria.productTypes,
        role: criteria.role,
        page: criteria.page === DEFAULT_PAGE ? undefined : criteria.page,
        pageCount:
            criteria.pageCount === DEFAULT_PAGE_SIZE ? undefined : criteria.pageCount,
    };
};

export function useSearchResults() {
    const route = useRoute();
    const { capitalize } = useProductFormatter();

    const criteria = computed(() => parseSearchCriteria(route.query));
    const {
        data: response,
        status,
        error,
    } = useAsyncData("search-results", () => searchProducts(criteria.value), {
        watch: [criteria],
        default: () => EMPTY_SEARCH_RESPONSE,
    });

    const activeFilters = computed<ActiveFilter[]>(() => {
        const { q, role } = criteria.value;
        const filters: ActiveFilter[] = [];

        if (q) {
            filters.push({ key: `q-${q}`, kind: "q", value: q, label: q });
        }

        LIST_FILTER_KINDS.forEach((kind) => {
            criteria.value[kind].forEach((value) => {
                filters.push({
                    key: `${kind}-${value}`,
                    kind,
                    value,
                    label: capitalize(value),
                });
            });
        });

        const roleOption = ROLE_OPTIONS.find((option) => option.value === role);
        if (roleOption) {
            filters.push({
                key: `role-${roleOption.value}`,
                kind: "role",
                value: roleOption.value,
                label: roleOption.label,
            });
        }

        return filters;
    });

    const replaceCriteria = async (nextCriteria: SearchCriteria) => {
        await navigateTo(
            { path: ROUTES.results, query: toLocationQuery(nextCriteria) },
            { replace: true },
        );
    };

    const removeFilter = async (filter: ActiveFilter) => {
        const nextCriteria = { ...criteria.value, page: DEFAULT_PAGE };

        if (filter.kind === "q") {
            nextCriteria.q = undefined;
        } else if (filter.kind === "role") {
            nextCriteria.role = undefined;
        } else {
            nextCriteria[filter.kind] = nextCriteria[filter.kind].filter(
                (value) => value !== filter.value,
            );
        }

        await replaceCriteria(nextCriteria);
    };

    const clearFilters = async () => {
        await replaceCriteria({
            q: criteria.value.q,
            crops: [],
            pests: [],
            productTypes: [],
            role: criteria.value.role,
            page: DEFAULT_PAGE,
            pageCount: criteria.value.pageCount,
        });
    };

    const setRole = async (role: UserRole) => {
        await replaceCriteria({ ...criteria.value, role, page: DEFAULT_PAGE });
    };

    const setPage = async (page: number) => {
        await navigateTo({
            path: ROUTES.results,
            query: toLocationQuery({ ...criteria.value, page }),
        });
        window.scrollTo({ top: 0, behavior: "smooth" });
    };

    const setPageCount = async (pageCount: PageSize) => {
        await replaceCriteria({ ...criteria.value, pageCount, page: DEFAULT_PAGE });
    };

    // Strona spoza zakresu (np. ręcznie wpisany ?page=99) — wróć na ostatnią.
    watch(response, ({ total }) => {
        if (status.value !== "success") {
            return;
        }
        const lastPage = Math.max(1, Math.ceil(total / criteria.value.pageCount));
        if (criteria.value.page > lastPage) {
            void replaceCriteria({ ...criteria.value, page: lastPage });
        }
    });

    return {
        criteria,
        response,
        status,
        error,
        activeFilters,
        removeFilter,
        clearFilters,
        setRole,
        setPage,
        setPageCount,
    };
}
