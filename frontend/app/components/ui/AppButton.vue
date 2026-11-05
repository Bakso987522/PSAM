<script setup lang="ts">
import type { RouteLocationRaw } from "vue-router";

interface AppButtonProps {
    variant?: "primary" | "outline" | "soft";
    type?: "button" | "submit" | "reset";
    to?: RouteLocationRaw;
}

const { variant = "primary", type = "button", to } = defineProps<AppButtonProps>();

const variantClasses = {
    primary: "bg-primary text-white hover:bg-primary-dark",
    outline: "bg-white text-primary hover:bg-primary-soft",
    soft: "bg-primary-soft text-primary-dark hover:bg-primary-tint-2",
};
</script>

<template>
    <NuxtLink
        v-if="to"
        :to="to"
        class="inline-flex h-10 items-center justify-center rounded-control border border-primary px-5 transition-colors"
        :class="variantClasses[variant]"
    >
        <slot />
    </NuxtLink>
    <button
        v-else
        :type="type"
        class="h-10 rounded-control border border-primary px-5 transition-colors disabled:pointer-events-none disabled:opacity-50"
        :class="variantClasses[variant]"
    >
        <slot />
    </button>
</template>
