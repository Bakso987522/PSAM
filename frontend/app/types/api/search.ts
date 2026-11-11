import type { UserRole } from "~/enums/UserRole";

export interface SearchApiRequest {
    q?: string;
    crops?: string[];
    pests?: string[];
    productTypes?: string[];
    role?: UserRole;
}

export interface SearchResultApiResponse {
    id_sor: string;
    name: string;
    producer: string;
    for_amateurs: boolean;
    use_allowed_until: string;
    removed_at: string | null;
    product_types: string[] | null;
    active_substances: string[] | null;
}

export interface SearchFiltersAppliedApiResponse {
    q: string | null;
    crops: string[] | null;
    pests: string[] | null;
    productTypes: string[];
    role: UserRole;
}

export interface SearchApiResponse {
    filters_applied: SearchFiltersAppliedApiResponse;
    count: number;
    results: SearchResultApiResponse[];
}
