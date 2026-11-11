import type { UserRole } from "~/enums/UserRole";

export interface SearchQuery {
    q?: string;
    crops?: string[];
    pests?: string[];
    productTypes?: string[];
    role: UserRole;
}
