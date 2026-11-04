<script setup lang="ts">
const { name, label } = defineProps<{
    name: string;
    label?: string;
}>();

const model = defineModel<string>({ default: "" });
const id = useId();
</script>

<template>
    <div class="flex flex-col gap-1">
        <label v-if="label" :for="id" class="text-sm font-medium">
            {{ label }}
        </label>
        <input
            :id="id"
            v-model="model"
            :name="name"
            type="search"
            autocomplete="off"
            class="rounded-lg border px-3 py-2 focus:outline-none focus:ring-2"
        />
    </div>
</template>
