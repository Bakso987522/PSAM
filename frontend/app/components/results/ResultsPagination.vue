<script setup lang="ts">
import { ChevronLeft, ChevronRight, ChevronsLeft, ChevronsRight } from "@lucide/vue";
import {
    PaginationEllipsis,
    PaginationFirst,
    PaginationLast,
    PaginationList,
    PaginationListItem,
    PaginationNext,
    PaginationPrev,
    PaginationRoot,
} from "reka-ui";
import { ResultsText } from "~/enums/ResultsText";
import { useIsMobile } from "~/hooks/useIsMobile";

interface ResultsPaginationProps {
    total: number;
    itemsPerPage: number;
}

const { total, itemsPerPage } = defineProps<ResultsPaginationProps>();

const page = defineModel<number>("page", { required: true });

const { isMobile } = useIsMobile();

const buttonClasses =
    "flex size-12 items-center justify-center rounded-control border border-primary bg-white text-primary transition-colors hover:bg-primary-soft disabled:pointer-events-none disabled:opacity-40";
</script>

<template>
    <PaginationRoot
        v-if="total > itemsPerPage"
        v-model:page="page"
        :total="total"
        :items-per-page="itemsPerPage"
        :sibling-count="isMobile ? 0 : 1"
        :show-edges="!isMobile"
        :aria-label="ResultsText.Pagination"
        class="flex justify-center"
    >
        <PaginationList v-slot="{ items }" class="flex flex-wrap items-center justify-center gap-2">
            <PaginationFirst
                v-if="isMobile"
                :class="buttonClasses"
                :aria-label="ResultsText.FirstPage"
            >
                <ChevronsLeft class="size-5" aria-hidden="true" />
            </PaginationFirst>
            <PaginationPrev :class="buttonClasses" :aria-label="ResultsText.PrevPage">
                <ChevronLeft class="size-5" aria-hidden="true" />
            </PaginationPrev>

            <template v-for="(item, index) in items" :key="index">
                <PaginationListItem
                    v-if="item.type === 'page'"
                    :value="item.value"
                    :aria-label="`${ResultsText.Page} ${item.value}`"
                    :class="[
                        buttonClasses,
                        'data-selected:bg-primary data-selected:text-white data-selected:hover:bg-primary-dark',
                    ]"
                >
                    {{ item.value }}
                </PaginationListItem>
                <PaginationEllipsis
                    v-else
                    class="flex size-12 items-center justify-center text-secondary"
                >
                    &#8230;
                </PaginationEllipsis>
            </template>

            <PaginationNext :class="buttonClasses" :aria-label="ResultsText.NextPage">
                <ChevronRight class="size-5" aria-hidden="true" />
            </PaginationNext>
            <PaginationLast
                v-if="isMobile"
                :class="buttonClasses"
                :aria-label="ResultsText.LastPage"
            >
                <ChevronsRight class="size-5" aria-hidden="true" />
            </PaginationLast>
        </PaginationList>
    </PaginationRoot>
</template>
