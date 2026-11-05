<script setup lang="ts">
import Container from "~/components/layout/Container.vue";
import ActiveFilters from "~/components/results/ActiveFilters.vue";
import EmptyResults from "~/components/results/EmptyResults.vue";
import RemovedProducts from "~/components/results/RemovedProducts.vue";
import ResultCard from "~/components/results/ResultCard.vue";
import AppBreadcrumbs from "~/components/ui/AppBreadcrumbs.vue";
import AppButton from "~/components/ui/AppButton.vue";
import { ROUTES } from "~/constants/routes";
import { useSearchResults } from "~/hooks/useSearchResults";
import type { BreadcrumbItem } from "~/types/BreadcrumbItem";

const router = useRouter();
const { response, activeFilters, removeFilter, clearFilters, setRole } =
    useSearchResults();

const breadcrumbs: BreadcrumbItem[] = [
    { label: "Wyszukiwarka", to: ROUTES.home },
    { label: "Wyniki" },
];

const goBack = async () => {
    if (window.history.state?.back) {
        router.back();
        return;
    }
    await navigateTo(ROUTES.home);
};

useHead({ title: "Wyniki wyszukiwania – AgroLupa" });
</script>

<template>
    <Container class="mx-auto w-full max-w-220 gap-6 py-8 sm:px-10">
        <div class="flex flex-wrap items-center justify-between gap-4">
            <AppBreadcrumbs :items="breadcrumbs" />
            <AppButton variant="soft" :to="ROUTES.home">Nowe wyszukiwanie</AppButton>
        </div>

        <div class="flex flex-wrap items-center gap-x-6 gap-y-3">
            <AppButton variant="outline" @click="goBack">Wróć do wyszukiwarki</AppButton>
            <h1 class="text-2xl font-bold">Wyniki wyszukiwania</h1>
        </div>

        <ActiveFilters :filters="activeFilters" @remove="removeFilter" />

        <p class="font-bold">Znaleziono środków: {{ response.total }}</p>

        <RemovedProducts :products="response.removed" />

        <ul v-if="response.items.length > 0" class="flex flex-col gap-4">
            <li v-for="result in response.items" :key="result.idSor">
                <ResultCard :result="result" />
            </li>
        </ul>

        <EmptyResults
            v-else-if="response.hasProfessionalOnlyResults"
            title="Brak środków dla użytkowników nieprofesjonalnych"
            description="Dla wybranych kryteriów dostępne są tylko środki profesjonalne."
        >
            <AppButton @click="setRole('professional')">Pokaż środki profesjonalne</AppButton>
        </EmptyResults>

        <EmptyResults
            v-else
            title="Brak wyników"
            description="Zmień lub usuń część filtrów, aby zobaczyć środki."
        >
            <AppButton @click="clearFilters">Wyczyść filtry</AppButton>
        </EmptyResults>
    </Container>
</template>
