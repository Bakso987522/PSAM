import { PERMIT_EXPIRY_WARNING_DAYS } from "~/constants/search";
import { PermitText } from "~/enums/PermitText";
import type { PermitStatus } from "~/types/product/PermitStatus";

const DAY_IN_MS = 24 * 60 * 60 * 1000;

const dateFormatter = new Intl.DateTimeFormat("pl-PL", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
});

export function usePermitStatus() {
    const formatDate = (value: string) => {
        return dateFormatter.format(new Date(value));
    };

    const getPermitStatus = (
        useAllowedUntil: string,
        today = new Date(),
    ): PermitStatus => {
        const daysLeft =
            (new Date(useAllowedUntil).getTime() - today.getTime()) / DAY_IN_MS;

        if (daysLeft < 0) {
            return "expired";
        }
        if (daysLeft <= PERMIT_EXPIRY_WARNING_DAYS) {
            return "expiring";
        }
        return "active";
    };

    const getPermitLabel = (status: PermitStatus, useAllowedUntil: string) => {
        const labels: Record<PermitStatus, string> = {
            expired: `${PermitText.Expired} ${formatDate(useAllowedUntil)}`,
            expiring: `${PermitText.Expiring} ${formatDate(useAllowedUntil)}`,
            active: PermitText.Active,
        };
        return labels[status];
    };

    return { formatDate, getPermitStatus, getPermitLabel };
}
