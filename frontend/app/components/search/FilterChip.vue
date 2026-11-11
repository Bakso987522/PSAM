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
    <span
        class="inline-flex h-9.5 items-center gap-3 rounded-control border border-primary bg-primary-soft pr-2 pl-4 text-primary-dark"
    >
        <span>{{ label }}</span>
        <button
            type="button"
            :aria-label="`${LayoutText.RemoveChip} ${label}`"
            class="flex size-6 items-center justify-center rounded-badge transition-colors hover:bg-white"
            @click="emit('remove')"
        >
            <svg
                viewBox="0 0 10 10"
                class="size-2.5"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                aria-hidden="true"
            >
                <path d="M0 0L10 10M10 0L0 10" />
            </svg>
        </button>
    </span>
</template>
