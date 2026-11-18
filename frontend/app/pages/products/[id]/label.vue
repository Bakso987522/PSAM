<script setup lang="ts">
import { ArrowLeft, RotateCcw } from "@lucide/vue";
import Container from "~/components/layout/Container.vue";
import EmptyResults from "~/components/results/EmptyResults.vue";
import AppBreadcrumbs from "~/components/ui/AppBreadcrumbs.vue";
import AppButton from "~/components/ui/AppButton.vue";
import { API_ENDPOINTS } from "~/constants/api";
import { ROUTES } from "~/constants/routes";
import { PageTitle } from "~/enums/PageTitle";
import { ProductText } from "~/enums/ProductText";
import { ResultsText } from "~/enums/ResultsText";
import { useLastResultsPath } from "~/hooks/useLastResultsPath";
import { useProductCard } from "~/hooks/useProductCard";
import type { BreadcrumbItem } from "~/types/ui/BreadcrumbItem";

const route = useRoute();
const router = useRouter();
const { lastResultsPath } = useLastResultsPath();

const idSor = computed(() => String(route.params.id));
const { product, status, error } = useProductCard(idSor);

const hasLabel = computed(() => Boolean(product.value?.labelMatched && product.value.labelUrl));

const breadcrumbs = computed<BreadcrumbItem[]>(() => [
    { label: ResultsText.BreadcrumbSearch, to: ROUTES.home },
    ...(lastResultsPath.value
        ? [{ label: ResultsText.BreadcrumbResults, to: lastResultsPath.value }]
        : []),
    { label: ProductText.Breadcrumb, to: ROUTES.product(idSor.value) },
    { label: ProductText.Label },
]);

const goBack = async () => {
    if (window.history.state?.back) {
        router.back();
        return;
    }
    await navigateTo(ROUTES.product(idSor.value));
};

useHead({
    title: () =>
        product.value
            ? `${ProductText.LabelTitle} ${product.value.name} – AgroLupa`
            : PageTitle.Label,
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
                    :aria-label="ProductText.Back"
                    @click="goBack"
                >
                    <ArrowLeft class="size-5 lg:hidden" aria-hidden="true" />
                    <span class="hidden lg:inline">{{ ProductText.Back }}</span>
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
            <h1 class="text-2xl font-bold">
                {{ ProductText.LabelTitle }} {{ product.name }}
            </h1>

            <template v-if="hasLabel">
                <div class="overflow-hidden rounded-field border border-line bg-neutral-100">
                    <iframe
                        :src="API_ENDPOINTS.label(product.idSor, product.name)"
                        :title="`${ProductText.LabelFrame}: ${product.name}`"
                        class="h-[70vh] w-full"
                    />
                </div>

                <div class="flex flex-wrap gap-2 sm:gap-3">
                    <a
                        :href="API_ENDPOINTS.label(product.idSor, product.name, true)"
                        download
                        class="inline-flex h-10 flex-1 items-center justify-center rounded-control border border-primary bg-primary px-5 text-white transition-colors hover:bg-primary-dark sm:flex-none"
                    >
                        {{ ProductText.Download }}
                    </a>
                    <AppButton
                        variant="outline"
                        class="flex-1 sm:flex-none"
                        :to="ROUTES.product(product.idSor)"
                    >
                        {{ ProductText.BackToCard }}
                    </AppButton>
                </div>
            </template>

            <EmptyResults
                v-else
                :title="ProductText.LabelUnavailable"
                :description="ProductText.LabelUnavailableDescription"
            >
                <div class="flex flex-wrap justify-center gap-2">
                    <a
                        v-if="product.labelUrl"
                        :href="product.labelUrl"
                        target="_blank"
                        rel="noopener"
                        class="inline-flex h-10 items-center justify-center rounded-control border border-primary bg-primary px-5 text-white transition-colors hover:bg-primary-dark"
                    >
                        {{ ProductText.LabelExternal }}
                    </a>
                    <AppButton variant="outline" :to="ROUTES.product(product.idSor)">
                        {{ ProductText.BackToCard }}
                    </AppButton>
                </div>
            </EmptyResults>
        </template>
    </Container>
</template>
