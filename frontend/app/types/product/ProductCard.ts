import type { ProductSubstance } from "~/types/product/ProductSubstance";
import type { ProductUsageGroup } from "~/types/product/ProductUsage";

export interface ProductCard {
    idSor: string;
    name: string;
    producer: string;
    permitNumber: string;
    permitValidUntil: string;
    saleAllowedUntil: string;
    useAllowedUntil: string;
    forAmateurs: boolean;
    packaging: string[];
    labelUrl: string | null;
    removedAt: string | null;
    productTypes: string[];
    substances: ProductSubstance[];
    usageGroups: ProductUsageGroup[];
}
