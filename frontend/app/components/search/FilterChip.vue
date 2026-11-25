<script setup lang="ts">
import { LayoutText } from "~/enums/LayoutText";

interface FilterChipProps {
    label: string;
}

const { label } = defineProps<FilterChipProps>();

const emit = defineEmits<{
    remove: [];
}>();
</script>

<template>
    <button
        type="button"
        :aria-label="`${LayoutText.RemoveChip} ${label}`"
        class="group inline-flex h-12 cursor-pointer items-center gap-3 rounded-control border border-primary bg-primary-soft pr-3 pl-4 text-primary-dark transition-colors hover:bg-primary-tint-2"
        @click="emit('remove')"
    >
        <span>{{ label }}</span>
        <span
            class="flex size-6 items-center justify-center rounded-badge transition-colors group-hover:bg-white"
            aria-hidden="true"
        >
            <svg
                viewBox="0 0 10 10"
                class="size-2.5"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
            >
                <path d="M0 0L10 10M10 0L0 10" />
            </svg>
        </span>
    </button>
</template>
