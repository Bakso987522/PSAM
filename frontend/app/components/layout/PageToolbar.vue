<script setup lang="ts">
import AppBreadcrumbs from "~/components/ui/AppBreadcrumbs.vue";
import type { BreadcrumbItem } from "~/types/ui/BreadcrumbItem";

interface PageToolbarProps {
    items: BreadcrumbItem[];
}

const { items } = defineProps<PageToolbarProps>();
</script>

<template>
    <div
        class="flex flex-col items-start gap-3 sm:flex-row sm:items-center sm:justify-between sm:gap-4"
    >
        <AppBreadcrumbs :items="items" />
        <div class="flex shrink-0 gap-2">
            <slot />
        </div>
    </div>
</template>
