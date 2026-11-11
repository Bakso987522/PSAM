<script setup lang="ts">
import { ProductText } from "~/enums/ProductText";
import { useProductFormatter } from "~/hooks/useProductFormatter";
import type { ProductUsage, ProductUsageGroup } from "~/types/product/ProductUsage";

interface UsageListProps {
    groups: ProductUsageGroup[];
    labelUrl: string | null;
}

const { groups, labelUrl } = defineProps<UsageListProps>();

const { capitalize } = useProductFormatter();

const joinParts = (parts: (string | null)[]) => {
    return parts.filter((part): part is string => Boolean(part)).join(" · ");
};

const getTitle = (usage: ProductUsage) => {
    return usage.pests.length > 0
        ? capitalize(usage.pests.join(", "))
        : ProductText.UnknownPest;
};

const getDetails = (usage: ProductUsage) => {
    return joinParts([
        usage.dose && `${ProductText.Dose} ${usage.dose}`,
        usage.timing && `${ProductText.Timing} ${usage.timing}`,
    ]);
};

const getMethod = (usage: ProductUsage) => {
    return joinParts([
        usage.method && `${ProductText.Method} ${usage.method}`,
        usage.preHarvestDays !== null
            ? `${ProductText.PreHarvest} ${usage.preHarvestDays} ${ProductText.Days}`
            : null,
    ]);
};
</script>

<template>
    <section class="flex flex-col gap-3">
        <h2 class="text-xl font-bold">{{ ProductText.Usages }}</h2>

        <p v-if="groups.length === 0" class="rounded-field border border-line px-5 py-4 text-muted">
            {{ ProductText.NoUsages }}
        </p>

        <div v-for="group in groups" :key="group.crop" class="flex flex-col gap-2">
            <h3 class="font-bold text-primary">
                {{ ProductText.Crop }} {{ capitalize(group.crop) }}
            </h3>
            <ul class="flex flex-col gap-2">
                <li
                    v-for="usage in group.usages"
                    :key="usage.id"
                    class="flex flex-col gap-0.5 rounded-field border border-line bg-white px-5 py-3"
                >
                    <span class="font-bold">{{ getTitle(usage) }}</span>
                    <span v-if="getDetails(usage)" class="text-sm text-secondary">
                        {{ getDetails(usage) }}
                    </span>
                    <span v-if="getMethod(usage)" class="text-sm text-secondary">
                        {{ getMethod(usage) }}
                    </span>
                    <a
                        v-if="usage.preHarvestDays === null && labelUrl"
                        :href="labelUrl"
                        target="_blank"
                        rel="noopener"
                        class="self-start text-sm text-primary underline underline-offset-4 hover:text-primary-dark"
                    >
                        {{ ProductText.LabelDetails }}
                    </a>
                </li>
            </ul>
        </div>
    </section>
</template>
