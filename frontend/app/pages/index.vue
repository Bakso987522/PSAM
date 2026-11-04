<script setup lang="ts">
import Container from "~/components/layout/Container.vue";
import RecentProducts from "~/components/search/RecentProducts.vue";
import SearchForm from "~/components/search/SearchForm.vue";
import { useDataVersion } from "~/hooks/useDataVersion";

const { publishedAt } = useDataVersion();

useHead({ title: "AgroLupa – wyszukiwarka środków ochrony roślin" });
</script>

<template>
    <Container :isFixedWidth="true" class="mx-auto">
        <SearchForm />
        <RecentProducts />
        <p v-if="publishedAt" class="text-center text-sm text-muted">
            Dane z rejestru z dnia {{ publishedAt }}
        </p>
    </Container>
</template>
