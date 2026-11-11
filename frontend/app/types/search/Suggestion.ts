export type SuggestionKind =
    | "product"
    | "substance"
    | "crop"
    | "pest"
    | "productType";

export interface Suggestion {
    id: number | string;
    kind: SuggestionKind;
    label: string;
    hint?: string;
}
