import type { RemovedProduct } from "~/types/search/RemovedProduct";
import type { SearchResult } from "~/types/search/SearchResult";

export interface SearchResponse {
    total: number;
    items: SearchResult[];
    removed: RemovedProduct[];
    hasProfessionalOnlyResults: boolean;
}
