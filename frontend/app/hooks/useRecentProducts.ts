import {
    RECENT_PRODUCTS_LIMIT,
    RECENT_PRODUCTS_STORAGE_KEY,
} from "~/constants/search";
import type { RecentProduct } from "~/types/product/RecentProduct";

const isRecentProduct = (value: unknown): value is RecentProduct => {
    return (
        typeof value === "object" &&
        value !== null &&
        typeof (value as RecentProduct).id === "string" &&
        typeof (value as RecentProduct).name === "string"
    );
};

const readStorage = (): RecentProduct[] => {
    try {
        const storedValue = localStorage.getItem(RECENT_PRODUCTS_STORAGE_KEY);
        const parsedValue: unknown = storedValue ? JSON.parse(storedValue) : [];

        return Array.isArray(parsedValue)
            ? parsedValue.filter(isRecentProduct).slice(0, RECENT_PRODUCTS_LIMIT)
            : [];
    } catch {
        return [];
    }
};

const writeStorage = (products: RecentProduct[]) => {
    try {
        localStorage.setItem(
            RECENT_PRODUCTS_STORAGE_KEY,
            JSON.stringify(products),
        );
    } catch {
        return;
    }
};

export function useRecentProducts() {
    const recentProducts = useState<RecentProduct[]>(
        "recent-products",
        () => [],
    );
    const isLoaded = useState("recent-products-loaded", () => false);

    const loadRecentProducts = () => {
        if (isLoaded.value || import.meta.server) {
            return;
        }
        recentProducts.value = readStorage();
        isLoaded.value = true;
    };

    const saveRecentProducts = (products: RecentProduct[]) => {
        recentProducts.value = products;
        writeStorage(products);
    };

    const addRecentProduct = (product: RecentProduct) => {
        loadRecentProducts();
        saveRecentProducts(
            [
                product,
                ...recentProducts.value.filter((item) => item.id !== product.id),
            ].slice(0, RECENT_PRODUCTS_LIMIT),
        );
    };

    const removeRecentProduct = (id: string) => {
        loadRecentProducts();
        saveRecentProducts(
            recentProducts.value.filter((item) => item.id !== id),
        );
    };

    const clearRecentProducts = () => {
        saveRecentProducts([]);
    };

    onMounted(loadRecentProducts);

    return {
        recentProducts,
        addRecentProduct,
        removeRecentProduct,
        clearRecentProducts,
    };
}
