import type { RoleOption } from "~/types/user/RoleOption";
import { UserRole } from "~/enums/UserRole";
import { UserRoleLabel } from "~/enums/UserRoleLabel";

export const MIN_SEARCH_LENGTH = 3;
export const MIN_SUGGESTION_LENGTH = 2;
export const SUGGESTION_DEBOUNCE_MS = 250;

export const RECENT_PRODUCTS_LIMIT = 10;
export const RECENT_PRODUCTS_STORAGE_KEY = "agrolupa:recent-products";

export const USER_ROLE_COOKIE = "agrolupa-role";
export const USER_ROLE_COOKIE_MAX_AGE = 60 * 60 * 24 * 365;
export const DEFAULT_USER_ROLE: UserRole = UserRole.Professional;

export const ROLE_OPTIONS: RoleOption[] = [
    { value: UserRole.Professional, label: UserRoleLabel.Professional },
    { value: UserRole.Amateur, label: UserRoleLabel.Amateur },
];

export const PERMIT_EXPIRY_WARNING_DAYS = 90;
