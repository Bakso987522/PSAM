import { API_ENDPOINTS } from "~/constants/api";
import type {
    AlternativesApiRequest,
    AlternativesApiResponse,
} from "~/types/api/alternatives";
import type { ProductCardApiResponse } from "~/types/api/product";
import type { SearchApiResponse, SearchApiRequest } from "~/types/api/search";

export const fetchSearch = (params: SearchApiRequest) => {
    return $fetch<SearchApiResponse>(API_ENDPOINTS.search, {
        query: { ...params },
    });
};

export const fetchProductCard = (idSor: string) => {
    return $fetch<ProductCardApiResponse>(API_ENDPOINTS.product(idSor));
};

export const fetchAlternatives = (
    idSor: string,
    query: AlternativesApiRequest = {},
) => {
    return $fetch<AlternativesApiResponse>(API_ENDPOINTS.alternatives(idSor), {
        query: { ...query },
    });
};
