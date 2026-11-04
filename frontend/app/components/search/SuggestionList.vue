<script setup lang="ts">
import {
    ComboboxContent,
    ComboboxEmpty,
    ComboboxItem,
    ComboboxViewport,
} from "reka-ui";
import { useSuggestion } from "~/hooks/useSuggestion";
import type { Suggestion } from "~/types/Suggestion";

interface SuggestionListProps {
    suggestions: Suggestion[];
    isLoading: boolean;
}

const { suggestions, isLoading } = defineProps<SuggestionListProps>();

const { getSuggestionKey } = useSuggestion();
</script>

<template>
    <ComboboxContent
        position="popper"
        :side-offset="4"
        class="z-50 w-(--reka-combobox-trigger-width) overflow-hidden rounded-field border border-line bg-white shadow-card"
    >
        <ComboboxViewport class="max-h-72 p-1">
            <ComboboxEmpty class="px-3 py-2 text-sm text-muted">
                {{ isLoading ? "Szukam…" : "Brak podpowiedzi" }}
            </ComboboxEmpty>
            <ComboboxItem
                v-for="suggestion in suggestions"
                :key="getSuggestionKey(suggestion)"
                :value="suggestion"
                :text-value="suggestion.label"
                class="flex cursor-pointer flex-col rounded-control px-3 py-2 outline-none data-highlighted:bg-primary-soft data-[state=checked]:font-bold"
            >
                <span>{{ suggestion.label }}</span>
                <span v-if="suggestion.hint" class="text-xs font-normal text-muted">
                    {{ suggestion.hint }}
                </span>
            </ComboboxItem>
        </ComboboxViewport>
    </ComboboxContent>
</template>
