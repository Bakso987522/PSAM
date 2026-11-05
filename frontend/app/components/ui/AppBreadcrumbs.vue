<script setup lang="ts">
import type { BreadcrumbItem } from "~/types/BreadcrumbItem";

interface AppBreadcrumbsProps {
    items: BreadcrumbItem[];
}

const { items } = defineProps<AppBreadcrumbsProps>();
</script>

<template>
    <nav aria-label="Ścieżka nawigacji">
        <ol class="flex flex-wrap items-center gap-2">
            <li
                v-for="(item, index) in items"
                :key="item.label"
                class="flex items-center gap-2"
            >
                <span v-if="index > 0" class="text-sm text-secondary" aria-hidden="true">›</span>
                <NuxtLink
                    v-if="item.to"
                    :to="item.to"
                    class="text-primary underline underline-offset-4 hover:text-primary-dark"
                >
                    {{ item.label }}
                </NuxtLink>
                <span v-else class="font-bold" aria-current="page">{{ item.label }}</span>
            </li>
        </ol>
    </nav>
</template>
