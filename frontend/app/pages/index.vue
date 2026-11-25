<script setup lang="ts">
import Container from "~/components/layout/Container.vue";
import DataVersion from "~/components/layout/DataVersion.vue";
import RecentProducts from "~/components/search/RecentProducts.vue";
import SearchForm from "~/components/search/SearchForm.vue";
import { PageTitle } from "~/enums/PageTitle";
import { useRecentProducts } from "~/hooks/useRecentProducts";

const { recentProducts } = useRecentProducts();

const hasRecent = computed(() => recentProducts.value.length > 0);

useHead({ title: PageTitle.Home });
</script>

<template>
    <Container
        class="mx-auto w-full sm:px-10"
        :class="hasRecent ? 'max-w-220' : 'max-w-xl'"
    >
        <div
            class="grid gap-6"
            :class="hasRecent ? 'lg:grid-cols-[minmax(0,1fr)_18rem]' : ''"
        >
            <SearchForm />
            <RecentProducts />
        </div>
        <DataVersion class="text-center text-sm" />
    </Container>
</template>
