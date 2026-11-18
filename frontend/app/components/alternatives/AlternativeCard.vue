<script setup lang="ts">
import PermitBadge from "~/components/results/PermitBadge.vue";
import { ROUTES } from "~/constants/routes";
import { AlternativesText } from "~/enums/AlternativesText";
import { useProductFormatter } from "~/hooks/useProductFormatter";
import type { Alternative } from "~/types/product/Alternative";

interface AlternativeCardProps {
    alternative: Alternative;
}

const { alternative } = defineProps<AlternativeCardProps>();

const { formatContent, formatSubstances, getUserLabel } = useProductFormatter();

const composition = computed(() => {
    if (alternative.substances) {
        return formatSubstances(alternative.substances);
    }
    const contents = alternative.rawContent
        .map((content) => formatContent({ name: "", content, unit: null }))
        .filter((content) => content !== "");
    return [...contents, AlternativesText.ContentOnCard].join(", ");
});

const details = computed(() => {
    return [
        composition.value,
        alternative.packaging.length > 0
            ? `${AlternativesText.Packaging} ${alternative.packaging.join("; ")}`
            : null,
    ]
        .filter(Boolean)
        .join(" · ");
});
</script>

<template>
    <NuxtLink
        :to="ROUTES.product(alternative.idSor)"
        class="flex flex-col gap-3 rounded-field border border-line bg-white px-6 py-3 transition-colors hover:border-primary sm:flex-row sm:items-center sm:justify-between"
    >
        <div class="flex min-w-0 flex-col gap-0.5">
            <span class="text-lg">{{ alternative.name }}</span>
            <span class="text-muted">{{ details }}</span>
            <span class="text-sm text-muted">
                {{ AlternativesText.User }}
                {{ getUserLabel(alternative.forAmateurs) }}
            </span>
        </div>
        <div class="flex shrink-0 flex-wrap gap-2 self-start sm:flex-col sm:items-end sm:self-center">
            <span
                class="inline-flex min-h-7 items-center rounded-badge px-2.5 py-0.5 text-sm font-bold"
                :class="
                    alternative.sameContent
                        ? 'bg-primary-soft text-primary-darker'
                        : 'bg-neutral-bg text-secondary'
                "
            >
                {{
                    alternative.sameContent
                        ? AlternativesText.SameContent
                        : AlternativesText.OtherContent
                }}
            </span>
            <PermitBadge :use-allowed-until="alternative.useAllowedUntil" />
        </div>
    </NuxtLink>
</template>
