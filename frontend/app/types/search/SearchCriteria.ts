import type { PageSize } from "~/constants/search";
import type { UserRole } from "~/enums/UserRole";

export interface SearchCriteria {
    q?: string;
    crops: string[];
    pests: string[];
    productTypes: string[];
    role?: UserRole;
    page: number;
    pageCount: PageSize;
}
