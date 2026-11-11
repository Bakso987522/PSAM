<script setup lang="ts">
import Container from "~/components/layout/Container.vue";
import ActiveFilters from "~/components/results/ActiveFilters.vue";
import EmptyResults from "~/components/results/EmptyResults.vue";
import RemovedProducts from "~/components/results/RemovedProducts.vue";
import ResultCard from "~/components/results/ResultCard.vue";
import AppBreadcrumbs from "~/components/ui/AppBreadcrumbs.vue";
import AppButton from "~/components/ui/AppButton.vue";
import { ROUTES } from "~/constants/routes";
import { PageTitle } from "~/enums/PageTitle";
import { ProfessionalOnlyMessage } from "~/enums/ProfessionalOnlyMessage";
import { ResultsText } from "~/enums/ResultsText";
import { UserRole } from "~/enums/UserRole";
import { useSearchResults } from "~/hooks/useSearchResults";
import type { BreadcrumbItem } from "~/types/ui/BreadcrumbItem";

const router = useRouter();
const {
    response,
    status,
    error,
    activeFilters,
    removeFilter,
    clearFilters,
    setRole,
} = useSearchResults();

const breadcrumbs: BreadcrumbItem[] = [
    { label: ResultsText.BreadcrumbSearch, to: ROUTES.home },
    { label: ResultsText.BreadcrumbResults },
];

const goBack = async () => {
    if (window.history.state?.back) {
        router.back();
        return;
    }
    await navigateTo(ROUTES.home);
};

useHead({ title: PageTitle.Results });
</script>

<template>
    <Container class="mx-auto w-full max-w-220 gap-6 py-8 sm:px-10">
        <div class="flex flex-wrap items-center justify-between gap-4">
            <AppBreadcrumbs :items="breadcrumbs" />
            <AppButton variant="soft" :to="ROUTES.home">
                {{ ResultsText.NewSearch }}
            </AppButton>
        </div>

        <div class="flex flex-wrap items-center gap-x-6 gap-y-3">
            <AppButton variant="outline" @click="goBack">
                {{ ResultsText.BackToSearch }}
            </AppButton>
            <h1 class="text-2xl font-bold">{{ ResultsText.Heading }}</h1>
        </div>

        <ActiveFilters :filters="activeFilters" @remove="removeFilter" />

        <p v-if="status === 'pending'" class="text-muted" role="status">
            {{ ResultsText.Loading }}
        </p>

        <EmptyResults
            v-else-if="error"
            :title="ResultsText.ErrorTitle"
            :description="ResultsText.ErrorDescription"
        />

        <template v-else>
            <p class="font-bold">
                {{ ResultsText.Found }} {{ response.total }}
            </p>

            <RemovedProducts :products="response.removed" />

            <ul v-if="response.items.length > 0" class="flex flex-col gap-4">
                <li v-for="result in response.items" :key="result.idSor">
                    <ResultCard :result="result" />
                </li>
            </ul>

            <EmptyResults
                v-else-if="response.hasProfessionalOnlyResults"
                :title="ProfessionalOnlyMessage.Title"
                :description="ProfessionalOnlyMessage.Description"
            >
                <AppButton @click="setRole(UserRole.Professional)">
                    {{ ProfessionalOnlyMessage.Action }}
                </AppButton>
            </EmptyResults>

            <EmptyResults
                v-else
                :title="ResultsText.EmptyTitle"
                :description="ResultsText.EmptyDescription"
            >
                <AppButton @click="clearFilters">
                    {{ ResultsText.ClearFilters }}
                </AppButton>
            </EmptyResults>
        </template>
    </Container>
</template>
