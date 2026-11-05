import type { ProductSubstance } from "~/types/ProductSubstance";

export interface SearchResult {
    idSor: string;
    name: string;
    productTypes: string[];
    substances: ProductSubstance[];
    forAmateurs: boolean;
    useAllowedUntil: string;
}
