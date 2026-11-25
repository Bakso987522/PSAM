<script setup lang="ts">
import { ChevronDown } from "@lucide/vue";
import {
    AccordionContent,
    AccordionHeader,
    AccordionItem,
    AccordionRoot,
    AccordionTrigger,
} from "reka-ui";
import { ROUTES } from "~/constants/routes";
import { ProductText } from "~/enums/ProductText";
import { useProductFormatter } from "~/hooks/useProductFormatter";
import type { ProductUsage, ProductUsageGroup } from "~/types/product/ProductUsage";

interface UsageListProps {
    idSor: string;
    groups: ProductUsageGroup[];
    labelUrl: string | null;
    labelMatched: boolean;
}

const { idSor, groups, labelUrl, labelMatched } = defineProps<UsageListProps>();

const { capitalize } = useProductFormatter();

const getTitle = (usage: ProductUsage) => {
    return usage.pests.length > 0
        ? capitalize(usage.pests.join(", "))
        : ProductText.UnknownPest;
};

const getItemValue = (group: ProductUsageGroup, usage: ProductUsage) => {
    return `${group.crop}-${usage.id}`;
};

const getFields = (usage: ProductUsage) => {
    return [
        { label: ProductText.Dose, value: usage.dose },
        { label: ProductText.Timing, value: usage.timing },
        { label: ProductText.Method, value: usage.method },
        { label: ProductText.CombinedUse, value: usage.combinedUse },
        {
            label: ProductText.PreHarvest,
            value:
                usage.preHarvestDays !== null
                    ? `${usage.preHarvestDays} ${ProductText.Days}`
                    : null,
        },
    ].filter((field): field is { label: ProductText; value: string } =>
        Boolean(field.value),
    );
};

const labelLink = computed(() => {
    if (!labelUrl) {
        return null;
    }
    return labelMatched
        ? { to: ROUTES.label(idSor), external: false }
        : { to: labelUrl, external: true };
});
</script>

<template>
    <section class="flex min-h-0 flex-col gap-3">
        <h2 class="text-xl font-bold">{{ ProductText.Usages }}</h2>

        <AccordionRoot
            type="multiple"
            class="scrollbar-green flex min-h-0 flex-1 flex-col gap-3 lg:overflow-y-auto lg:pr-2"
        >
            <p v-if="groups.length === 0" class="rounded-field border border-line px-5 py-4 text-muted">
                {{ ProductText.NoUsages }}
            </p>

            <div v-for="group in groups" :key="group.crop" class="flex flex-col gap-2">
                <h3 class="font-bold text-primary">
                    {{ ProductText.Crop }} {{ capitalize(group.crop) }}
                </h3>
                <ul class="flex flex-col gap-2">
                    <AccordionItem
                        v-for="usage in group.usages"
                        :key="usage.id"
                        as="li"
                        :value="getItemValue(group, usage)"
                        class="overflow-hidden rounded-field border border-line bg-white transition-colors has-focus-visible:border-primary data-[state=open]:border-primary"
                    >
                        <AccordionHeader as="div">
                            <AccordionTrigger
                                class="group flex min-h-12 w-full cursor-pointer items-center justify-between gap-3 px-5 py-3 text-left outline-none hover:bg-primary-tint"
                            >
                                <span class="flex flex-wrap items-center gap-2 font-bold">
                                    {{ getTitle(usage) }}
                                    <span
                                        v-if="usage.minorUse"
                                        class="rounded-badge bg-neutral-bg px-2 py-0.5 text-xs text-primary-darker"
                                    >
                                        {{ ProductText.MinorUse }}
                                    </span>
                                </span>
                                <ChevronDown
                                    class="size-5 shrink-0 text-primary transition-transform duration-200 group-data-[state=open]:rotate-180"
                                    aria-hidden="true"
                                />
                            </AccordionTrigger>
                        </AccordionHeader>
                        <AccordionContent
                            class="overflow-hidden data-[state=closed]:animate-accordion-up data-[state=open]:animate-accordion-down"
                        >
                            <dl class="flex flex-col gap-1.5 border-t border-line px-5 py-3 text-sm">
                                <div
                                    v-for="field in getFields(usage)"
                                    :key="field.label"
                                    class="flex flex-col"
                                >
                                    <dt class="font-bold text-secondary">{{ field.label }}</dt>
                                    <dd>{{ field.value }}</dd>
                                </div>
                                <div
                                    v-if="usage.preHarvestDays === null"
                                    class="flex flex-wrap gap-x-2 text-secondary"
                                >
                                    {{ ProductText.PreHarvestOnLabel }}
                                    <NuxtLink
                                        v-if="labelLink"
                                        :to="labelLink.to"
                                        :external="labelLink.external"
                                        :target="labelLink.external ? '_blank' : undefined"
                                        :rel="labelLink.external ? 'noopener' : undefined"
                                        class="inline-flex touch-target items-center text-primary underline underline-offset-4 hover:text-primary-dark"
                                    >
                                        {{ ProductText.LabelDetails }}
                                    </NuxtLink>
                                </div>
                            </dl>
                        </AccordionContent>
                    </AccordionItem>
                </ul>
            </div>
        </AccordionRoot>
    </section>
</template>
