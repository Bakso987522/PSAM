import type { SearchResult } from "~/types/SearchResult";

export interface ProductUsage {
    crops: string[];
    pests: string[];
}

export interface MockProduct extends SearchResult {
    removedAt: string | null;
    usages: ProductUsage[];
}
