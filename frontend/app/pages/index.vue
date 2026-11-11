<script setup lang="ts">
import Container from "~/components/layout/Container.vue";
import RecentProducts from "~/components/search/RecentProducts.vue";
import SearchForm from "~/components/search/SearchForm.vue";
import { PageTitle } from "~/enums/PageTitle";
import { SearchText } from "~/enums/SearchText";
import { useDataVersion } from "~/hooks/useDataVersion";

const { publishedAt } = useDataVersion();

useHead({ title: PageTitle.Home });
</script>

<template>
    <Container :isFixedWidth="true" class="mx-auto">
        <SearchForm />
        <RecentProducts />
        <p v-if="publishedAt" class="text-center text-sm text-muted">
            {{ SearchText.DataVersion }} {{ publishedAt }}
        </p>
    </Container>
</template>
