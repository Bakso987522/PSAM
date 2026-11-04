<script setup lang="ts">
import { ComboboxAnchor, ComboboxInput, ComboboxRoot } from "reka-ui";
import SearchIcon from "~/components/icons/SearchIcon.vue";
import FilterChip from "~/components/search/FilterChip.vue";
import SuggestionList from "~/components/search/SuggestionList.vue";
import { MIN_SUGGESTION_LENGTH } from "~/constants/search";
import { useSuggestion } from "~/hooks/useSuggestion";
import { useSuggestionFetch } from "~/hooks/useSuggestionFetch";
import type { Suggestion } from "~/types/Suggestion";

interface FilterFieldProps {
    label: string;
    endpoint: string;
    placeholder?: string;
    minLength?: number;
}

const {
    label,
    endpoint,
    placeholder = "Szukaj",
    minLength = MIN_SUGGESTION_LENGTH,
} = defineProps<FilterFieldProps>();

const selectedItems = defineModel<Suggestion[]>({ default: () => [] });
const term = defineModel<string>("term", { default: "" });

const inputId = useId();
const { getSuggestionKey, isSameSuggestion } = useSuggestion();
const { suggestions, isLoading, isActive } = useSuggestionFetch(
    endpoint,
    term,
    minLength,
);

const removeItem = (item: Suggestion) => {
    selectedItems.value = selectedItems.value.filter(
        (selectedItem) => !isSameSuggestion(selectedItem, item),
    );
};
</script>

<template>
    <div class="flex flex-col gap-2">
        <label :for="inputId" class="font-bold">{{ label }}</label>
        <ComboboxRoot
            v-model="selectedItems"
            multiple
            :by="isSameSuggestion"
            ignore-filter
            :reset-search-term-on-blur="false"
        >
            <ComboboxAnchor
                class="flex h-10 items-center gap-2 rounded-field border border-field bg-white pr-3 pl-4 focus-within:border-primary focus-within:ring-2 focus-within:ring-primary-soft"
            >
                <ComboboxInput
                    :id="inputId"
                    v-model="term"
                    :placeholder="placeholder"
                    autocomplete="off"
                    class="h-full w-full bg-transparent outline-none placeholder:text-muted"
                />
                <SearchIcon class="size-5 shrink-0 text-primary-darker" />
            </ComboboxAnchor>
            <SuggestionList
                v-if="isActive"
                :suggestions="suggestions"
                :is-loading="isLoading"
            />
        </ComboboxRoot>
        <ul v-if="selectedItems.length > 0" class="flex flex-wrap gap-2">
            <li v-for="item in selectedItems" :key="getSuggestionKey(item)">
                <FilterChip :label="item.label" @remove="removeItem(item)" />
            </li>
        </ul>
    </div>
</template>
