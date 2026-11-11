<script setup lang="ts">
import { ArrowLeft, RotateCcw } from "@lucide/vue";
import Container from "~/components/layout/Container.vue";
import ActiveFilters from "~/components/results/ActiveFilters.vue";
import EmptyResults from "~/components/results/EmptyResults.vue";
import PageSizeSelect from "~/components/results/PageSizeSelect.vue";
import RemovedProducts from "~/components/results/RemovedProducts.vue";
import ResultCard from "~/components/results/ResultCard.vue";
import ResultsPagination from "~/components/results/ResultsPagination.vue";
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
    criteria,
    response,
    status,
    error,
    activeFilters,
    removeFilter,
    clearFilters,
    setRole,
    setPage,
    setPageCount,
} = useSearchResults();

const page = computed({
    get: () => criteria.value.page,
    set: (value) => void setPage(value),
});

const pageCount = computed({
    get: () => criteria.value.pageCount,
    set: (value) => void setPageCount(value),
});

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
        <div class="flex items-center justify-between gap-4">
            <AppBreadcrumbs :items="breadcrumbs" />
            <div class="flex shrink-0 gap-2">
                <AppButton
                    variant="outline"
                    icon-only="mobile"
                    :aria-label="ResultsText.BackToSearch"
                    @click="goBack"
                >
                    <ArrowLeft class="size-5 lg:hidden" aria-hidden="true" />
                    <span class="hidden lg:inline">{{ ResultsText.BackToSearch }}</span>
                </AppButton>
                <AppButton
                    variant="soft"
                    icon-only="mobile"
                    :to="ROUTES.home"
                    :aria-label="ResultsText.NewSearch"
                >
                    <RotateCcw class="size-5 lg:hidden" aria-hidden="true" />
                    <span class="hidden lg:inline">{{ ResultsText.NewSearch }}</span>
                </AppButton>
            </div>
        </div>

        <h1 class="text-2xl font-bold">{{ ResultsText.Heading }}</h1>

        <ActiveFilters
            :filters="activeFilters"
            @remove="removeFilter"
            @clear="clearFilters"
        />

        <hr class="border-line" />

        <p v-if="status === 'pending'" class="text-muted" role="status">
            {{ ResultsText.Loading }}
        </p>

        <EmptyResults
            v-else-if="error"
            :title="ResultsText.ErrorTitle"
            :description="ResultsText.ErrorDescription"
        />

        <template v-else>
            <RemovedProducts :products="response.removed" />

            <template v-if="response.items.length > 0">
                <div
                    class="flex flex-col-reverse items-start gap-3 sm:flex-row sm:items-center sm:justify-between"
                >
                    <p class="text-secondary">
                        {{ ResultsText.Found }} <strong>{{ response.total }}</strong>
                    </p>
                    <PageSizeSelect v-model="pageCount" />
                </div>

                <ul class="flex flex-col gap-4">
                    <li v-for="result in response.items" :key="result.idSor">
                        <ResultCard :result="result" />
                    </li>
                </ul>

                <ResultsPagination
                    v-model:page="page"
                    :total="response.total"
                    :items-per-page="pageCount"
                />
            </template>

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
