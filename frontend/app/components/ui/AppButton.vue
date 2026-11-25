<script setup lang="ts">
import type { RouteLocationRaw } from "vue-router";

interface AppButtonProps {
    variant?: "primary" | "outline" | "soft";
    type?: "button" | "submit" | "reset";
    to?: RouteLocationRaw;
    href?: string;
    download?: boolean;
    external?: boolean;
    iconOnly?: boolean | "mobile";
}

const {
    variant = "primary",
    type = "button",
    to,
    href,
    download = false,
    external = false,
    iconOnly = false,
} = defineProps<AppButtonProps>();

const baseClasses =
    "inline-flex h-12 items-center justify-center rounded-control border border-primary transition-colors";

const variantClasses = {
    primary: "bg-primary text-white hover:bg-primary-dark",
    outline: "bg-white text-primary hover:bg-primary-soft",
    soft: "bg-primary-soft text-primary-dark hover:bg-primary-tint-2",
};

const sizeClasses = computed(() => {
    if (iconOnly === "mobile") {
        return "w-12 lg:w-auto lg:px-5";
    }
    return iconOnly ? "w-12" : "px-5";
});
</script>

<template>
    <a
        v-if="href"
        :href="href"
        :download="download || undefined"
        :target="external ? '_blank' : undefined"
        :rel="external ? 'noopener' : undefined"
        :class="[baseClasses, variantClasses[variant], sizeClasses]"
    >
        <slot />
    </a>
    <NuxtLink
        v-else-if="to"
        :to="to"
        :class="[baseClasses, variantClasses[variant], sizeClasses]"
    >
        <slot />
    </NuxtLink>
    <button
        v-else
        :type="type"
        class="disabled:pointer-events-none disabled:opacity-50"
        :class="[baseClasses, variantClasses[variant], sizeClasses]"
    >
        <slot />
    </button>
</template>
