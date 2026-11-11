<script setup lang="ts">
import { ChevronDown } from "@lucide/vue";
import { PAGE_SIZE_OPTIONS, type PageSize } from "~/constants/search";
import { ResultsText } from "~/enums/ResultsText";

const pageCount = defineModel<PageSize>({ required: true });

const selectId = useId();
</script>

<template>
    <div class="flex items-center gap-3">
        <label :for="selectId" class="text-secondary">
            {{ ResultsText.PageSize }}
        </label>
        <div class="relative">
            <select
                :id="selectId"
                v-model.number="pageCount"
                class="h-10 cursor-pointer appearance-none rounded-control border border-primary bg-white pr-10 pl-4 text-primary-dark transition-colors hover:bg-primary-soft"
            >
                <option v-for="option in PAGE_SIZE_OPTIONS" :key="option" :value="option">
                    {{ option }}
                </option>
            </select>
            <ChevronDown
                class="pointer-events-none absolute top-1/2 right-4 size-4 -translate-y-1/2 text-primary-dark"
                aria-hidden="true"
            />
        </div>
    </div>
</template>
