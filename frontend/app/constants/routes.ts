export const ROUTES = {
    home: "/",
    results: "/results",
    product: (id: string) => `/products/${encodeURIComponent(id)}`,
} as const;
