export const ROUTES = {
    home: "/",
    results: "/results",
    product: (id: string) => `/products/${encodeURIComponent(id)}`,
    alternatives: (id: string) =>
        `/products/${encodeURIComponent(id)}/alternatives`,
} as const;
