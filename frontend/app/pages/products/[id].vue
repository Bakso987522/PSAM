<script setup lang="ts">
import { ArrowLeft, RotateCcw } from "@lucide/vue";
import Container from "~/components/layout/Container.vue";
import LegalNotice from "~/components/product/LegalNotice.vue";
import ProductActions from "~/components/product/ProductActions.vue";
import ProductDetails from "~/components/product/ProductDetails.vue";
import UsageList from "~/components/product/UsageList.vue";
import EmptyResults from "~/components/results/EmptyResults.vue";
import AppBreadcrumbs from "~/components/ui/AppBreadcrumbs.vue";
import AppButton from "~/components/ui/AppButton.vue";
import { ROUTES } from "~/constants/routes";
import { PageTitle } from "~/enums/PageTitle";
import { ProductText } from "~/enums/ProductText";
import { ResultsText } from "~/enums/ResultsText";
import { useLastResultsPath } from "~/hooks/useLastResultsPath";
import { usePermitStatus } from "~/hooks/usePermitStatus";
import { useProductCard } from "~/hooks/useProductCard";
import type { BreadcrumbItem } from "~/types/ui/BreadcrumbItem";

const route = useRoute();
const router = useRouter();
const { lastResultsPath } = useLastResultsPath();
const { formatDate } = usePermitStatus();

const idSor = computed(() => String(route.params.id));
const { product, status, error } = useProductCard(idSor);

const breadcrumbs = computed<BreadcrumbItem[]>(() => [
    { label: ResultsText.BreadcrumbSearch, to: ROUTES.home },
    ...(lastResultsPath.value
        ? [{ label: ResultsText.BreadcrumbResults, to: lastResultsPath.value }]
        : []),
    { label: ProductText.Breadcrumb },
]);

const goBack = async () => {
    if (window.history.state?.back) {
        router.back();
        return;
    }
    await navigateTo(lastResultsPath.value ?? ROUTES.home);
};

useHead({
    title: () => (product.value ? `${product.value.name} – AgroLupa` : PageTitle.Product),
});
</script>

<template>
    <Container class="mx-auto w-full max-w-220 gap-6 py-8 sm:px-10">
        <div class="flex items-center justify-between gap-4">
            <AppBreadcrumbs :items="breadcrumbs" />
            <div class="flex shrink-0 gap-2">
                <AppButton
                    variant="outline"
                    icon-only="mobile"
                    :aria-label="ProductText.BackToResults"
                    @click="goBack"
                >
                    <ArrowLeft class="size-5 lg:hidden" aria-hidden="true" />
                    <span class="hidden lg:inline">{{ ProductText.BackToResults }}</span>
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

        <p v-if="status === 'pending'" class="text-muted" role="status">
            {{ ProductText.Loading }}
        </p>

        <EmptyResults
            v-else-if="error || !product"
            :title="ProductText.NotFoundTitle"
            :description="ProductText.NotFoundDescription"
        >
            <AppButton :to="ROUTES.home">{{ ResultsText.NewSearch }}</AppButton>
        </EmptyResults>

        <template v-else>
            <h1 class="text-2xl font-bold">{{ product.name }}</h1>

            <p
                v-if="product.removedAt"
                class="rounded-field bg-danger-bg px-5 py-3 font-bold text-danger-fg"
            >
                {{ ProductText.Removed }}: {{ formatDate(product.removedAt) }}
            </p>

            <ProductDetails :product="product" />
            <ProductActions
                :id-sor="product.idSor"
                :name="product.name"
                :label-url="product.labelUrl"
            />

            <hr class="border-line" />

            <UsageList :groups="product.usageGroups" :label-url="product.labelUrl" />

            <LegalNotice />
        </template>
    </Container>
</template>
