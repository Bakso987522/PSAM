<script setup lang="ts">
import PermitBadge from "~/components/results/PermitBadge.vue";
import { ProductText } from "~/enums/ProductText";
import { usePermitStatus } from "~/hooks/usePermitStatus";
import { useProductFormatter } from "~/hooks/useProductFormatter";
import type { ProductCard } from "~/types/product/ProductCard";

interface ProductDetailsProps {
    product: ProductCard;
}

const { product } = defineProps<ProductDetailsProps>();

const { formatDate } = usePermitStatus();
const { formatContent, formatProductTypes, getUserLabel } = useProductFormatter();

const productTypes = computed(() => {
    return product.productTypes.length > 0
        ? formatProductTypes(product.productTypes)
        : ProductText.NoData;
});

const fields = computed(() => [
    { label: ProductText.Producer, value: product.producer },
    { label: ProductText.PermitNumber, value: product.permitNumber },
    {
        label: ProductText.PermitValidUntil,
        value: formatDate(product.permitValidUntil),
    },
    {
        label: ProductText.SaleAllowedUntil,
        value: formatDate(product.saleAllowedUntil),
    },
]);
</script>

<template>
    <dl class="grid gap-x-8 gap-y-4 sm:grid-cols-2">
        <div>
            <dt class="text-sm font-bold text-secondary">{{ ProductText.ProductType }}</dt>
            <dd>{{ productTypes }}</dd>
        </div>
        <div>
            <dt class="text-sm font-bold text-secondary">{{ ProductText.UserType }}</dt>
            <dd>{{ getUserLabel(product.forAmateurs) }}</dd>
        </div>
        <div>
            <dt class="text-sm font-bold text-secondary">{{ ProductText.Substances }}</dt>
            <dd v-if="product.substances.length === 0">{{ ProductText.NoData }}</dd>
            <dd v-else>
                <ul>
                    <li v-for="substance in product.substances" :key="substance.name">
                        {{ substance.name }}
                        <template v-if="formatContent(substance)">
                            – {{ formatContent(substance) }}
                        </template>
                    </li>
                </ul>
            </dd>
        </div>
        <div v-for="field in fields" :key="field.label">
            <dt class="text-sm font-bold text-secondary">{{ field.label }}</dt>
            <dd>{{ field.value }}</dd>
        </div>
        <div>
            <dt class="text-sm font-bold text-secondary">{{ ProductText.UseAllowedUntil }}</dt>
            <dd class="flex flex-col items-start gap-1">
                <span>{{ formatDate(product.useAllowedUntil) }}</span>
                <PermitBadge :use-allowed-until="product.useAllowedUntil" />
            </dd>
        </div>
        <div>
            <dt class="text-sm font-bold text-secondary">{{ ProductText.Packaging }}</dt>
            <dd v-if="product.packaging.length === 0">{{ ProductText.NoData }}</dd>
            <dd v-else>
                <ul>
                    <li v-for="line in product.packaging" :key="line">{{ line }}</li>
                </ul>
            </dd>
        </div>
    </dl>
</template>
