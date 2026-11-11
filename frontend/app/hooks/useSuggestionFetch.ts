import type { Ref } from "vue";
import { SUGGESTION_DEBOUNCE_MS } from "~/constants/search";
import type {
    SuggestApiRequest,
    SuggestionApiResponse,
} from "~/types/api/suggest";
import type { Suggestion } from "~/types/search/Suggestion";

const isSuggestion = (value: unknown): value is Suggestion => {
    return (
        typeof value === "object" &&
        value !== null &&
        typeof (value as Suggestion).label === "string"
    );
};

export function useSuggestionFetch(
    endpoint: string,
    term: Ref<string>,
    minLength: number,
) {
    const suggestions = ref<Suggestion[]>([]);
    const isLoading = ref(false);
    const isActive = computed(
        () => endpoint !== "" && term.value.trim().length >= minLength,
    );

    let debounceTimer: ReturnType<typeof setTimeout> | undefined;
    let abortController: AbortController | undefined;

    const cancelPendingRequest = () => {
        clearTimeout(debounceTimer);
        abortController?.abort();
    };

    const fetchSuggestions = async (query: string) => {
        const controller = new AbortController();
        abortController = controller;

        try {
            const response = await $fetch<SuggestionApiResponse>(endpoint, {
                query: { q: query } satisfies SuggestApiRequest,
                signal: controller.signal,
            });
            suggestions.value = Array.isArray(response)
                ? response.filter(isSuggestion)
                : [];
        } catch {
            if (controller.signal.aborted) {
                return;
            }
            suggestions.value = [];
        }

        isLoading.value = false;
    };

    watch(term, (value) => {
        cancelPendingRequest();

        if (!isActive.value) {
            suggestions.value = [];
            isLoading.value = false;
            return;
        }

        isLoading.value = true;
        debounceTimer = setTimeout(
            () => fetchSuggestions(value.trim()),
            SUGGESTION_DEBOUNCE_MS,
        );
    });

    onScopeDispose(cancelPendingRequest);

    return { suggestions, isLoading, isActive };
}
