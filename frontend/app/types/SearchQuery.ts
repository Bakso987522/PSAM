import type { UserRole } from "~/types/UserRole";

export interface SearchQuery {
    q?: string;
    crops?: string[];
    pests?: string[];
    productTypes?: string[];
    role: UserRole;
}
