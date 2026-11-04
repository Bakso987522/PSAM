<script lang="ts" setup>
interface ContainerProps {
    isFixedWidth?: boolean;
}

const { isFixedWidth } = defineProps<ContainerProps>();
</script>

<template>
    <div
        class="rounded-xl bg-white shadow flex flex-col gap-4 px-8 py-4"
        v-bind:class="isFixedWidth ? 'w-108' : ''"
    >
        <slot />
    </div>
</template>
