import type { UserRole } from "~/types/UserRole";

export interface SearchCriteria {
    q?: string;
    crops: string[];
    pests: string[];
    productTypes: string[];
    role?: UserRole;
}
