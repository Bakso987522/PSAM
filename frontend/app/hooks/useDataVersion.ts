import { API_ENDPOINTS } from "~/constants/api";
import type { DataVersion } from "~/types/DataVersion";

const dateFormatter = new Intl.DateTimeFormat("pl-PL", { dateStyle: "long" });

export function useDataVersion() {
    const { data, status } = useFetch<DataVersion>(API_ENDPOINTS.dataVersion, {
        key: "data-version",
        lazy: true,
        immediate: API_ENDPOINTS.dataVersion !== "",
    });

    const publishedAt = computed(() => {
        const value = data.value?.publishedAt;
        return typeof value === "string"
            ? dateFormatter.format(new Date(value))
            : null;
    });

    return { publishedAt, status };
}
