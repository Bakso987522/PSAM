import { ROUTES } from "~/constants/routes";
import { MIN_SEARCH_LENGTH, MIN_SUGGESTION_LENGTH } from "~/constants/search";
import { useSuggestion } from "~/hooks/useSuggestion";
import { useUserRole } from "~/hooks/useUserRole";
import type { SearchQuery } from "~/types/search/SearchQuery";
import type { Suggestion } from "~/types/search/Suggestion";

export function useSearchForm() {
    const { role } = useUserRole();
    const { getSuggestionLabels } = useSuggestion();

    const term = ref("");
    const crops = ref<Suggestion[]>([]);
    const cropsTerm = ref("");
    const pests = ref<Suggestion[]>([]);
    const pestsTerm = ref("");
    const productTypes = ref<Suggestion[]>([]);
    const productTypesTerm = ref("");

    const normalizeText = (value: string) => {
        return value.trim().replace(/\s+/g, " ");
    };

    const getFilterValues = (items: Suggestion[], filterTerm: string) => {
        const values = getSuggestionLabels(items);
        const pendingText = normalizeText(filterTerm);

        if (
            pendingText.length >= MIN_SUGGESTION_LENGTH &&
            !values.includes(pendingText)
        ) {
            values.push(pendingText);
        }

        return values.length > 0 ? values : undefined;
    };

    const searchText = computed(() => normalizeText(term.value));

    const hasValidTerm = computed(
        () => searchText.value.length >= MIN_SEARCH_LENGTH,
    );

    const filterValues = computed(() => ({
        crops: getFilterValues(crops.value, cropsTerm.value),
        pests: getFilterValues(pests.value, pestsTerm.value),
        productTypes: getFilterValues(
            productTypes.value,
            productTypesTerm.value,
        ),
    }));

    const hasFilters = computed(() =>
        Object.values(filterValues.value).some((values) => values !== undefined),
    );

    const canSubmit = computed(() => hasValidTerm.value || hasFilters.value);

    const buildSearchQuery = (): SearchQuery => {
        return {
            q: hasValidTerm.value ? searchText.value : undefined,
            ...filterValues.value,
            role: role.value,
        };
    };

    const submitSearch = async () => {
        if (!canSubmit.value) {
            return;
        }
        await navigateTo({ path: ROUTES.results, query: { ...buildSearchQuery() } });
    };

    const resetSearchForm = () => {
        term.value = "";
        crops.value = [];
        cropsTerm.value = "";
        pests.value = [];
        pestsTerm.value = "";
        productTypes.value = [];
        productTypesTerm.value = "";
    };

    return {
        term,
        crops,
        cropsTerm,
        pests,
        pestsTerm,
        productTypes,
        productTypesTerm,
        role,
        canSubmit,
        buildSearchQuery,
        submitSearch,
        resetSearchForm,
    };
}
