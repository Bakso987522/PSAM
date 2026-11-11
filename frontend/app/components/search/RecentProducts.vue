<script setup lang="ts">
import { ROUTES } from "~/constants/routes";
import { SearchText } from "~/enums/SearchText";
import { useRecentProducts } from "~/hooks/useRecentProducts";

const { recentProducts } = useRecentProducts();
</script>

<template>
    <section v-if="recentProducts.length > 0" class="flex flex-col gap-3">
        <h2 class="text-lg font-bold">{{ SearchText.RecentProducts }}</h2>
        <ul class="flex flex-col gap-2">
            <li v-for="product in recentProducts" :key="product.id">
                <NuxtLink
                    :to="ROUTES.product(product.id)"
                    class="flex flex-col gap-1 rounded-field border border-line bg-white px-5 py-3 transition-colors hover:border-primary"
                >
                    <span class="text-lg">{{ product.name }}</span>
                    <span v-if="product.hint" class="text-sm text-muted">
                        {{ product.hint }}
                    </span>
                </NuxtLink>
            </li>
        </ul>
    </section>
</template>
