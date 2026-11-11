import { API_ENDPOINTS } from "~/constants/api";
import type { DataVersionApiResponse } from "~/types/api/dataVersion";

const dateFormatter = new Intl.DateTimeFormat("pl-PL", { dateStyle: "long" });

export function useDataVersion() {
    const { data, status } = useFetch<DataVersionApiResponse>(
        API_ENDPOINTS.dataVersion,
        {
            key: "data-version",
            lazy: true,
        },
    );

    const publishedAt = computed(() => {
        const value = data.value?.publishedAt;
        return typeof value === "string"
            ? dateFormatter.format(new Date(value))
            : null;
    });

    return { publishedAt, status };
}
