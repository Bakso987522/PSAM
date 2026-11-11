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
} as const;
