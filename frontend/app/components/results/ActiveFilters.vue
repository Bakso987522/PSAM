<script setup lang="ts">
import FilterChip from "~/components/search/FilterChip.vue";
import AppButton from "~/components/ui/AppButton.vue";
import { ResultsText } from "~/enums/ResultsText";
import type { ActiveFilter } from "~/types/search/ActiveFilter";

interface ActiveFiltersProps {
    filters: ActiveFilter[];
}

const { filters } = defineProps<ActiveFiltersProps>();

const emit = defineEmits<{
    remove: [filter: ActiveFilter];
    clear: [];
}>();
</script>

<template>
    <template v-if="filters.length > 0">
        <details class="group rounded-field border border-line sm:hidden">
            <summary
                class="flex cursor-pointer list-none items-center justify-between px-4 py-3 font-bold [&::-webkit-details-marker]:hidden"
            >
                <span>{{ ResultsText.Filters }} ({{ filters.length }})</span>
                <svg
                    viewBox="0 0 12 8"
                    class="size-3 transition-transform group-open:rotate-180"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    aria-hidden="true"
                >
                    <path d="M1 1l5 5 5-5" />
                </svg>
            </summary>
            <div class="flex flex-col gap-4 border-t border-line p-4">
                <ul class="flex flex-wrap gap-2">
                    <li v-for="filter in filters" :key="filter.key">
                        <FilterChip
                            :label="filter.label"
                            @remove="emit('remove', filter)"
                        />
                    </li>
                </ul>
                <AppButton variant="outline" class="w-full" @click="emit('clear')">
                    {{ ResultsText.ClearFilters }}
                </AppButton>
            </div>
        </details>

        <div class="hidden flex-wrap items-center gap-3 sm:flex">
            <span class="font-bold">{{ ResultsText.ActiveFilters }}</span>
            <ul class="contents">
                <li v-for="filter in filters" :key="filter.key">
                    <FilterChip
                        :label="filter.label"
                        @remove="emit('remove', filter)"
                    />
                </li>
            </ul>
            <button
                type="button"
                class="text-primary underline underline-offset-4 hover:text-primary-dark"
                @click="emit('clear')"
            >
                {{ ResultsText.ClearFilters }}
            </button>
        </div>
    </template>
</template>
