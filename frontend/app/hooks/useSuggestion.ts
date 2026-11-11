import type { Suggestion } from "~/types/search/Suggestion";

export function useSuggestion() {
    const isSameSuggestion = (first?: Suggestion, second?: Suggestion) => {
        return (
            first !== undefined &&
            second !== undefined &&
            first.kind === second.kind &&
            first.id === second.id
        );
    };

    const getSuggestionKey = (suggestion: Suggestion) => {
        return `${suggestion.kind}-${suggestion.id}`;
    };

    const getSuggestionLabel = (suggestion?: Suggestion) => {
        return suggestion?.label ?? "";
    };

    const getSuggestionLabels = (suggestions: Suggestion[]) => {
        return suggestions.map((suggestion) => suggestion.label);
    };

    return {
        isSameSuggestion,
        getSuggestionKey,
        getSuggestionLabel,
        getSuggestionLabels,
    };
}
