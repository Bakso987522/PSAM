<script setup lang="ts">
import { ResultsText } from "~/enums/ResultsText";
import { usePermitStatus } from "~/hooks/usePermitStatus";
import type { RemovedProduct } from "~/types/search/RemovedProduct";

interface RemovedProductsProps {
    products: RemovedProduct[];
}

const { products } = defineProps<RemovedProductsProps>();

const { formatDate } = usePermitStatus();
</script>

<template>
    <section
        v-if="products.length > 0"
        class="flex flex-col gap-1 rounded-field bg-danger-bg px-6 py-3 text-danger-fg"
    >
        <h2 class="font-bold">{{ ResultsText.RemovedHeading }}</h2>
        <ul class="flex flex-col gap-0.5">
            <li v-for="product in products" :key="product.idSor">
                {{ product.name }} – {{ ResultsText.Removed }}
                {{ formatDate(product.removedAt) }}
            </li>
        </ul>
    </section>
</template>
