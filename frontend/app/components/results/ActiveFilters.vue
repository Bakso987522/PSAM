<script setup lang="ts">
import FilterChip from "~/components/search/FilterChip.vue";
import type { ActiveFilter } from "~/types/ActiveFilter";

interface ActiveFiltersProps {
    filters: ActiveFilter[];
}

const { filters } = defineProps<ActiveFiltersProps>();

const emit = defineEmits<{
    remove: [filter: ActiveFilter];
}>();
</script>

<template>
    <div v-if="filters.length > 0" class="flex flex-wrap items-center gap-3">
        <span class="font-bold">Aktywne filtry:</span>
        <ul class="contents">
            <li v-for="filter in filters" :key="filter.key">
                <FilterChip :label="filter.label" @remove="emit('remove', filter)" />
            </li>
        </ul>
    </div>
</template>
