<script setup lang="ts">
import type { RouteLocationRaw } from "vue-router";

interface AppButtonProps {
    variant?: "primary" | "outline" | "soft";
    type?: "button" | "submit" | "reset";
    to?: RouteLocationRaw;
    /** true: always square; "mobile": square below `lg`, regular above */
    iconOnly?: boolean | "mobile";
}

const {
    variant = "primary",
    type = "button",
    to,
    iconOnly = false,
} = defineProps<AppButtonProps>();

const variantClasses = {
    primary: "bg-primary text-white hover:bg-primary-dark",
    outline: "bg-white text-primary hover:bg-primary-soft",
    soft: "bg-primary-soft text-primary-dark hover:bg-primary-tint-2",
};

const sizeClasses = computed(() => {
    if (iconOnly === "mobile") {
        return "w-10 lg:w-auto lg:px-5";
    }
    return iconOnly ? "w-10" : "px-5";
});
</script>

<template>
    <NuxtLink
        v-if="to"
        :to="to"
        class="inline-flex h-10 items-center justify-center rounded-control border border-primary transition-colors"
        :class="[variantClasses[variant], sizeClasses]"
    >
        <slot />
    </NuxtLink>
    <button
        v-else
        :type="type"
        class="inline-flex h-10 items-center justify-center rounded-control border border-primary transition-colors disabled:pointer-events-none disabled:opacity-50"
        :class="[variantClasses[variant], sizeClasses]"
    >
        <slot />
    </button>
</template>
