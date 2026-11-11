<script setup lang="ts">
import { ComboboxAnchor, ComboboxInput, ComboboxRoot } from "reka-ui";
import SearchIcon from "~/components/icons/SearchIcon.vue";
import SuggestionList from "~/components/search/SuggestionList.vue";
import { SearchText } from "~/enums/SearchText";
import { MIN_SEARCH_LENGTH } from "~/constants/search";
import { useSuggestion } from "~/hooks/useSuggestion";
import { useSuggestionFetch } from "~/hooks/useSuggestionFetch";
import type { Suggestion } from "~/types/search/Suggestion";

interface SearchFieldProps {
    label: string;
    endpoint: string;
    placeholder?: string;
    minLength?: number;
}

const {
    label,
    endpoint,
    placeholder = SearchText.DefaultPlaceholder,
    minLength = MIN_SEARCH_LENGTH,
} = defineProps<SearchFieldProps>();

const selection = defineModel<Suggestion>();
const term = defineModel<string>("term", { default: "" });

const inputId = useId();
const { getSuggestionLabel, isSameSuggestion } = useSuggestion();
const { suggestions, isLoading, isActive } = useSuggestionFetch(
    endpoint,
    term,
    minLength,
);

watch(selection, (value) => {
    if (value) {
        term.value = value.label;
    }
});

watch(term, (value) => {
    if (selection.value && value !== selection.value.label) {
        selection.value = undefined;
    }
});
</script>

<template>
    <div class="flex flex-col gap-2">
        <label :for="inputId" class="font-bold">{{ label }}</label>
        <ComboboxRoot
            v-model="selection"
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
                    :display-value="getSuggestionLabel"
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
    </div>
</template>
