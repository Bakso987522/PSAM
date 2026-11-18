import { toLabelFileName } from "#shared/utils/labelFileName";

export const API_ENDPOINTS = {
    health: "/api/health",
    suggestNames: "/api/suggest/names",
    suggestCrops: "/api/suggest/crops",
    suggestPests: "/api/suggest/pests",
    suggestProductTypes: "/api/suggest/product-types",
    dataVersion: "/api/data-version",
    search: "/api/search",
    product: (idSor: string) => `/api/sor/${encodeURIComponent(idSor)}`,
    alternatives: (idSor: string) =>
        `/api/sor/${encodeURIComponent(idSor)}/alternatives`,
    label: (idSor: string, name: string, download = false) =>
        `/labels/${encodeURIComponent(idSor)}/${encodeURIComponent(toLabelFileName(name))}${download ? "?download=1" : ""}`,
} as const;
