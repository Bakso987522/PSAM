<script setup lang="ts">
import { SearchText } from "~/enums/SearchText";
import { useDataVersion } from "~/hooks/useDataVersion";

const { publishedAt } = useDataVersion();
</script>

<template>
    <p v-if="publishedAt" class="text-muted">
        {{ SearchText.DataVersion }} {{ publishedAt }}
    </p>
</template>
