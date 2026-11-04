import {
    DEFAULT_USER_ROLE,
    USER_ROLE_COOKIE,
    USER_ROLE_COOKIE_MAX_AGE,
} from "~/constants/search";
import type { UserRole } from "~/types/UserRole";

export function useUserRole() {
    const role = useCookie<UserRole>(USER_ROLE_COOKIE, {
        default: () => DEFAULT_USER_ROLE,
        maxAge: USER_ROLE_COOKIE_MAX_AGE,
        sameSite: "lax",
    });

    const setRole = (value: UserRole) => {
        role.value = value;
    };

    return { role, setRole };
}
