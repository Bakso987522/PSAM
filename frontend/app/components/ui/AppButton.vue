<script setup lang="ts">
interface AppButtonProps {
    variant?: "primary" | "outline";
    type?: "button" | "submit" | "reset";
}

const { variant = "primary", type = "button" } = defineProps<AppButtonProps>();
</script>

<template>
    <button
        :type="type"
        class="h-10 rounded-control border border-primary px-4 transition-colors disabled:cursor-not-allowed disabled:opacity-50"
        :class="
            variant === 'primary'
                ? 'bg-primary text-white enabled:hover:bg-primary-dark'
                : 'bg-white text-primary enabled:hover:bg-primary-soft'
        "
    >
        <slot />
    </button>
</template>
