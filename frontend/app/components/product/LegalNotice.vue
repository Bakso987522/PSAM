<script setup lang="ts">
import { ProductText } from "~/enums/ProductText";
</script>

<template>
    <p
        class="rounded-field border border-primary bg-primary-tint px-5 py-4 font-bold text-primary-darker"
    >
        {{ ProductText.LegalNotice }}
    </p>
</template>
