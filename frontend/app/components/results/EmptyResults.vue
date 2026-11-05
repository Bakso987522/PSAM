<script setup lang="ts">
interface EmptyResultsProps {
    title: string;
    description: string;
}

const { title, description } = defineProps<EmptyResultsProps>();
</script>

<template>
    <div
        class="flex flex-col items-center gap-3 rounded-field border border-line bg-white px-6 py-14 text-center"
    >
        <h2 class="text-lg font-bold">{{ title }}</h2>
        <p class="text-muted">{{ description }}</p>
        <slot />
    </div>
</template>
