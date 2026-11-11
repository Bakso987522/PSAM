<script setup lang="ts">
import { ROUTES } from "~/constants/routes";
import { SearchText } from "~/enums/SearchText";
import { useRecentProducts } from "~/hooks/useRecentProducts";

const { recentProducts, clearRecentProducts } = useRecentProducts();
</script>

<template>
    <section
        v-if="recentProducts.length > 0"
        class="relative lg:border-l lg:border-line lg:pl-6"
    >
        <div class="flex max-h-96 flex-col gap-3 lg:absolute lg:inset-y-0 lg:right-0 lg:left-6 lg:max-h-none">
            <div class="flex items-center justify-between gap-3">
                <h2 class="text-lg font-bold">{{ SearchText.RecentProducts }}</h2>
                <button
                    type="button"
                    class="text-sm text-primary underline underline-offset-4 hover:text-primary-dark"
                    @click="clearRecentProducts"
                >
                    {{ SearchText.ClearRecentProducts }}
                </button>
            </div>
            <ul class="flex min-h-0 flex-1 flex-col gap-2 overflow-y-auto pr-1">
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
        </div>
    </section>
</template>
