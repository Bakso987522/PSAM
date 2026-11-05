import type { LocationQuery, LocationQueryRaw, LocationQueryValue } from "vue-router";
import { ROUTES } from "~/constants/routes";
import { ROLE_OPTIONS } from "~/constants/search";
import { useProductFormatter } from "~/hooks/useProductFormatter";
import { searchMockProducts } from "~/mocks/searchProducts";
import type { ActiveFilter, ListFilterKind } from "~/types/ActiveFilter";
import type { SearchCriteria } from "~/types/SearchCriteria";
import type { UserRole } from "~/types/UserRole";

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

const parseSearchCriteria = (query: LocationQuery): SearchCriteria => {
    const role = toStringList(query.role)[0];

    return {
        q: toStringList(query.q)[0],
        crops: toStringList(query.crops),
        pests: toStringList(query.pests),
        productTypes: toStringList(query.productTypes),
        role: isUserRole(role) ? role : undefined,
    };
};

const toLocationQuery = (criteria: SearchCriteria): LocationQueryRaw => {
    return {
        q: criteria.q,
        crops: criteria.crops,
        pests: criteria.pests,
        productTypes: criteria.productTypes,
        role: criteria.role,
    };
};

export function useSearchResults() {
    const route = useRoute();
    const { capitalize } = useProductFormatter();

    const criteria = computed(() => parseSearchCriteria(route.query));
    const response = computed(() => searchMockProducts(criteria.value));

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
        const nextCriteria = { ...criteria.value };

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
        });
    };

    const setRole = async (role: UserRole) => {
        await replaceCriteria({ ...criteria.value, role });
    };

    return {
        criteria,
        response,
        activeFilters,
        removeFilter,
        clearFilters,
        setRole,
    };
}
