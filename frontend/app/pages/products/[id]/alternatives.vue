<script setup lang="ts">
import { ArrowLeft, RotateCcw } from "@lucide/vue";
import AlternativeCard from "~/components/alternatives/AlternativeCard.vue";
import Container from "~/components/layout/Container.vue";
import PageToolbar from "~/components/layout/PageToolbar.vue";
import EmptyResults from "~/components/results/EmptyResults.vue";
import ResultsPagination from "~/components/results/ResultsPagination.vue";
import SearchField from "~/components/search/SearchField.vue";
import AppButton from "~/components/ui/AppButton.vue";
import { ALTERNATIVES_PAGE_SIZE } from "~/constants/alternatives";
import { API_ENDPOINTS } from "~/constants/api";
import { ROUTES } from "~/constants/routes";
import { MIN_SUGGESTION_LENGTH } from "~/constants/search";
import { AlternativesText } from "~/enums/AlternativesText";
import { PageTitle } from "~/enums/PageTitle";
import { ProductText } from "~/enums/ProductText";
import { ResultsText } from "~/enums/ResultsText";
import { UserRole } from "~/enums/UserRole";
import { useAlternatives } from "~/hooks/useAlternatives";
import { useLastResultsPath } from "~/hooks/useLastResultsPath";
import { useProductCard } from "~/hooks/useProductCard";
import { useProductFormatter } from "~/hooks/useProductFormatter";
import type { Suggestion } from "~/types/search/Suggestion";
import type { BreadcrumbItem } from "~/types/ui/BreadcrumbItem";

const route = useRoute();
const { lastResultsPath } = useLastResultsPath();
const { formatSubstances } = useProductFormatter();

const idSor = computed(() => String(route.params.id));
const { product, status: productStatus, error: productError } = useProductCard(idSor);
const {
    alternatives,
    pageItems,
    isTruncated,
    page,
    setPage,
    status,
    error,
    crop,
    role,
    setCrop,
    setRole,
} = useAlternatives(idSor);

const currentPage = computed({
    get: () => page.value,
    set: (value) => void setPage(value),
});

const cropSelection = ref<Suggestion>();
const cropTerm = ref(crop.value ?? "");

watch(cropSelection, (value) => {
    if (value) {
        void setCrop(value.label);
    }
});

watch(cropTerm, (value) => {
    if (value.trim() === "") {
        void setCrop(undefined);
    }
});

watch(crop, (value) => {
    if ((value ?? "") !== cropTerm.value.trim()) {
        cropTerm.value = value ?? "";
    }
});

const submitCrop = () => {
    void setCrop(cropTerm.value);
};

const clearCrop = () => {
    cropSelection.value = undefined;
    cropTerm.value = "";
};

const breadcrumbs = computed<BreadcrumbItem[]>(() => [
    { label: ResultsText.BreadcrumbSearch, to: ROUTES.home },
    ...(lastResultsPath.value
        ? [{ label: ResultsText.BreadcrumbResults, to: lastResultsPath.value }]
        : []),
    { label: ProductText.Breadcrumb, to: ROUTES.product(idSor.value) },
    { label: AlternativesText.Breadcrumb },
]);

useHead({
    title: () =>
        product.value
            ? `${AlternativesText.Heading}: ${product.value.name} – AgroLupa`
            : PageTitle.Alternatives,
});
</script>

<template>
    <Container class="mx-auto w-full max-w-220 gap-6 py-8 sm:px-10">
        <PageToolbar :items="breadcrumbs">
            <AppButton
                variant="outline"
                icon-only="mobile"
                :to="ROUTES.product(idSor)"
                :aria-label="ProductText.BackToCard"
            >
                <ArrowLeft class="size-5 lg:hidden" aria-hidden="true" />
                <span class="hidden lg:inline">{{ ProductText.BackToCard }}</span>
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
        </PageToolbar>

        <h1 class="text-2xl font-bold">{{ AlternativesText.Heading }}</h1>

        <p v-if="productStatus === 'pending'" class="text-muted" role="status">
            {{ ProductText.Loading }}
        </p>

        <EmptyResults
            v-else-if="productError || !product"
            :title="ProductText.NotFoundTitle"
            :description="ProductText.NotFoundDescription"
        >
            <AppButton :to="ROUTES.home">{{ ResultsText.NewSearch }}</AppButton>
        </EmptyResults>

        <template v-else>
            <section
                class="flex flex-col gap-1 rounded-field border border-line bg-white px-6 py-4 shadow-card"
            >
                <span class="text-sm font-bold text-secondary">
                    {{ AlternativesText.For }}
                </span>
                <NuxtLink
                    :to="ROUTES.product(product.idSor)"
                    class="text-xl font-bold hover:text-primary"
                >
                    {{ product.name }}
                </NuxtLink>
                <span class="text-muted">
                    {{ AlternativesText.Composition }}
                    {{ formatSubstances(product.substances) || ProductText.NoData }}
                </span>
            </section>

            <form @submit.prevent="submitCrop">
                <SearchField
                    v-model="cropSelection"
                    v-model:term="cropTerm"
                    :label="AlternativesText.CropLabel"
                    :placeholder="AlternativesText.CropPlaceholder"
                    :endpoint="API_ENDPOINTS.suggestCrops"
                    :min-length="MIN_SUGGESTION_LENGTH"
                />
            </form>

            <p v-if="status === 'pending'" class="text-muted" role="status">
                {{ AlternativesText.Loading }}
            </p>

            <EmptyResults
                v-else-if="error"
                :title="AlternativesText.ErrorTitle"
                :description="AlternativesText.ErrorDescription"
            />

            <template v-else-if="alternatives.items.length > 0">
                <div class="flex flex-col gap-1">
                    <p class="text-secondary">
                        {{ AlternativesText.Found }}
                        <strong>{{ alternatives.items.length }}</strong>
                    </p>
                    <p v-if="isTruncated" class="text-sm text-secondary">
                        {{ AlternativesText.Truncated }}
                    </p>
                </div>
                <ul class="flex flex-col gap-4">
                    <li v-for="alternative in pageItems" :key="alternative.idSor">
                        <AlternativeCard :alternative="alternative" />
                    </li>
                </ul>
                <ResultsPagination
                    v-if="alternatives.items.length > ALTERNATIVES_PAGE_SIZE"
                    v-model:page="currentPage"
                    :total="alternatives.items.length"
                    :items-per-page="ALTERNATIVES_PAGE_SIZE"
                />
            </template>

            <div
                v-else-if="role === UserRole.Amateur && alternatives.hasProfessionalOnlyResults"
                class="flex flex-col items-start gap-3 rounded-field border border-primary bg-primary-tint px-5 py-4"
            >
                <p class="font-bold text-primary-darker">
                    {{ AlternativesText.AmateurEmpty }}
                </p>
                <AppButton variant="outline" @click="setRole(UserRole.Professional)">
                    {{ AlternativesText.ShowProfessional }}
                </AppButton>
            </div>

            <EmptyResults
                v-else
                :title="AlternativesText.EmptyTitle"
                :description="
                    crop ? AlternativesText.EmptyCropDescription : AlternativesText.EmptyDescription
                "
            >
                <AppButton v-if="crop" @click="clearCrop">
                    {{ AlternativesText.ClearCrop }}
                </AppButton>
            </EmptyResults>
        </template>
    </Container>
</template>
