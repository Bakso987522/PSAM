import type {
    SearchApiResponse,
    SearchResultApiResponse,
} from "~/types/api/search";
import type { RemovedProduct } from "~/types/search/RemovedProduct";
import type { SearchResponse } from "~/types/search/SearchResponse";
import type { SearchResult } from "~/types/search/SearchResult";

export const EMPTY_SEARCH_RESPONSE: SearchResponse = {
    total: 0,
    items: [],
    removed: [],
    hasProfessionalOnlyResults: false,
};

export const toSearchResult = (
    result: SearchResultApiResponse,
): SearchResult => {
    return {
        idSor: result.id_sor,
        name: result.name,
        productTypes: result.product_types ?? [],
        substances: (result.active_substances ?? []).map((name) => ({
            name,
            content: null,
            unit: null,
        })),
        forAmateurs: result.for_amateurs,
        useAllowedUntil: result.use_allowed_until,
    };
};

export const toRemovedProduct = (
    result: SearchResultApiResponse & { removed_at: string },
): RemovedProduct => {
    return {
        idSor: result.id_sor,
        name: result.name,
        removedAt: result.removed_at,
    };
};

const isRemoved = (
    result: SearchResultApiResponse,
): result is SearchResultApiResponse & { removed_at: string } => {
    return result.removed_at !== null;
};

interface Pagination {
    page: number;
    pageCount: number;
}

export const toSearchResponse = (
    response: SearchApiResponse,
    { page, pageCount }: Pagination,
    hasProfessionalOnlyResults = false,
): SearchResponse => {
    const results = response.results
        .filter((result) => !isRemoved(result))
        .map(toSearchResult);

    if (response.total !== undefined) {
        return {
            total: response.total,
            items: results,
            removed: response.results.filter(isRemoved).map(toRemovedProduct),
            hasProfessionalOnlyResults,
        };
    }

    // TODO: usunąć po wdrożeniu paginacji w API — do tego czasu API zwraca
    // wszystkie (maks. 50) wyniki naraz, więc stronicujemy je lokalnie.
    const start = (page - 1) * pageCount;

    return {
        total: results.length,
        items: results.slice(start, start + pageCount),
        removed: response.results.filter(isRemoved).map(toRemovedProduct),
        hasProfessionalOnlyResults,
    };
};
