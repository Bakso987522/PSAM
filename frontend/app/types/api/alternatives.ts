import type { UserRole } from "~/enums/UserRole";

export interface AlternativesApiRequest {
    crop?: string;
    role?: UserRole;
}

export interface AlternativeApiResponse {
    id_sor: string;
    name: string;
    packaging: string | null;
    for_amateurs: boolean;
    use_allowed_until: string;
    content: (number | null)[];
    same_content: boolean;
}

export interface AlternativesApiResponse {
    alternatives: AlternativeApiResponse[];
}
