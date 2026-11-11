import { toProductCard } from "~/mappers/product";
import { fetchProductCard } from "~/services/api";
import { useProductFormatter } from "~/hooks/useProductFormatter";
import { useRecentProducts } from "~/hooks/useRecentProducts";

export function useProductCard(idSor: MaybeRefOrGetter<string>) {
    const { getProductHint } = useProductFormatter();
    const { addRecentProduct } = useRecentProducts();

    const { data: product, status, error } = useAsyncData(
        () => `product-${toValue(idSor)}`,
        () => fetchProductCard(toValue(idSor)).then(toProductCard),
    );

    onMounted(() => {
        watch(
            product,
            (value) => {
                if (!value) {
                    return;
                }
                addRecentProduct({
                    id: value.idSor,
                    name: value.name,
                    hint: getProductHint(value),
                });
            },
            { immediate: true },
        );
    });

    return { product, status, error };
}
