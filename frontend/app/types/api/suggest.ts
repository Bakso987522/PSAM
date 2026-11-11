import type { Suggestion } from "~/types/search/Suggestion";

export interface SuggestApiRequest {
    q: string;
}

export type SuggestionApiResponse = Suggestion[];
