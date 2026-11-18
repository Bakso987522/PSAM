import type { ProductSubstance } from "~/types/product/ProductSubstance";

export interface Alternative {
    idSor: string;
    name: string;
    substances: ProductSubstance[] | null;
    rawContent: (number | null)[];
    packaging: string[];
    forAmateurs: boolean;
    useAllowedUntil: string;
    sameContent: boolean;
}
