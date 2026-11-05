import type { RemovedProduct } from "~/types/RemovedProduct";
import type { SearchResult } from "~/types/SearchResult";

export interface SearchResponse {
    total: number;
    items: SearchResult[];
    removed: RemovedProduct[];
    hasProfessionalOnlyResults: boolean;
}
