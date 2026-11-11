<script setup lang="ts">
import PermitBadge from "~/components/results/PermitBadge.vue";
import { ROUTES } from "~/constants/routes";
import { ResultsText } from "~/enums/ResultsText";
import { useProductFormatter } from "~/hooks/useProductFormatter";
import { useRecentProducts } from "~/hooks/useRecentProducts";
import type { SearchResult } from "~/types/search/SearchResult";

interface ResultCardProps {
    result: SearchResult;
}

const { result } = defineProps<ResultCardProps>();

const { formatSubstances, formatProductTypes, getUserLabel, getProductHint } =
    useProductFormatter();
const { addRecentProduct } = useRecentProducts();

const rememberProduct = () => {
    addRecentProduct({
        id: result.idSor,
        name: result.name,
        hint: getProductHint(result),
    });
};
</script>

<template>
    <NuxtLink
        :to="ROUTES.product(result.idSor)"
        class="flex flex-col gap-3 rounded-field border border-line bg-white px-6 py-3 transition-colors hover:border-primary sm:flex-row sm:items-center sm:justify-between"
        @click="rememberProduct"
    >
        <div class="flex min-w-0 flex-col gap-0.5">
            <span class="text-lg">{{ result.name }}</span>
            <span class="text-muted">
                {{ ResultsText.Substances }}
                {{ formatSubstances(result.substances) }}
            </span>
            <span class="text-sm text-muted">
                {{ formatProductTypes(result.productTypes) }} ·
                {{ ResultsText.User }}
                {{ getUserLabel(result.forAmateurs) }}
            </span>
        </div>
        <PermitBadge :use-allowed-until="result.useAllowedUntil" class="shrink-0 self-start sm:self-center" />
    </NuxtLink>
</template>
