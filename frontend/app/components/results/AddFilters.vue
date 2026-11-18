<script setup lang="ts">
import { ChevronDown, Plus } from "@lucide/vue";
import {
    CollapsibleContent,
    CollapsibleRoot,
    CollapsibleTrigger,
} from "reka-ui";
import FilterField from "~/components/search/FilterField.vue";
import RoleSwitch from "~/components/search/RoleSwitch.vue";
import SearchField from "~/components/search/SearchField.vue";
import AppButton from "~/components/ui/AppButton.vue";
import { API_ENDPOINTS } from "~/constants/api";
import { MIN_SEARCH_LENGTH, MIN_SUGGESTION_LENGTH } from "~/constants/search";
import { ResultsText } from "~/enums/ResultsText";
import { SearchText } from "~/enums/SearchText";
import type { UserRole } from "~/enums/UserRole";
import { useSuggestion } from "~/hooks/useSuggestion";
import type { SearchQuery } from "~/types/search/SearchQuery";
import type { Suggestion } from "~/types/search/Suggestion";

interface AddFiltersProps {
    role: UserRole;
}

const { role } = defineProps<AddFiltersProps>();

const emit = defineEmits<{
    apply: [query: SearchQuery];
}>();

const { getSuggestionLabels } = useSuggestion();

const isOpen = ref(false);
const term = ref("");
const crops = ref<Suggestion[]>([]);
const cropsTerm = ref("");
const pests = ref<Suggestion[]>([]);
const pestsTerm = ref("");
const productTypes = ref<Suggestion[]>([]);
const productTypesTerm = ref("");
const draftRole = ref<UserRole>(role);

watch(
    () => role,
    (value) => {
        draftRole.value = value;
    },
);

const normalizeText = (value: string) => value.trim().replace(/\s+/g, " ");

const getValues = (items: Suggestion[], pending: string) => {
    const values = getSuggestionLabels(items);
    const text = normalizeText(pending);
    if (text.length >= MIN_SUGGESTION_LENGTH && !values.includes(text)) {
        values.push(text);
    }
    return values;
};

const draft = computed<SearchQuery>(() => {
    const q = normalizeText(term.value);
    return {
        q: q.length >= MIN_SEARCH_LENGTH ? q : undefined,
        crops: getValues(crops.value, cropsTerm.value),
        pests: getValues(pests.value, pestsTerm.value),
        productTypes: getValues(productTypes.value, productTypesTerm.value),
        role: draftRole.value,
    };
});

const hasChanges = computed(() => {
    const { q, crops, pests, productTypes } = draft.value;
    return (
        q !== undefined ||
        [crops, pests, productTypes].some((values) => (values?.length ?? 0) > 0) ||
        draftRole.value !== role
    );
});

const reset = () => {
    term.value = "";
    crops.value = [];
    cropsTerm.value = "";
    pests.value = [];
    pestsTerm.value = "";
    productTypes.value = [];
    productTypesTerm.value = "";
};

const apply = () => {
    if (!hasChanges.value) {
        return;
    }
    emit("apply", draft.value);
    reset();
    isOpen.value = false;
};
</script>

<template>
    <CollapsibleRoot
        v-model:open="isOpen"
        class="rounded-field border border-line bg-white data-[state=open]:border-primary"
    >
        <CollapsibleTrigger
            class="group flex w-full cursor-pointer items-center justify-between gap-3 px-4 py-3 font-bold text-primary hover:bg-primary-tint"
        >
            <span class="flex items-center gap-2">
                <Plus class="size-5" aria-hidden="true" />
                {{ ResultsText.AddFilter }}
            </span>
            <ChevronDown
                class="size-5 transition-transform duration-200 group-data-[state=open]:rotate-180"
                aria-hidden="true"
            />
        </CollapsibleTrigger>
        <CollapsibleContent
            class="overflow-hidden data-[state=closed]:animate-collapsible-up data-[state=open]:animate-collapsible-down"
        >
            <form
                class="flex flex-col gap-4 border-t border-line p-4"
                @submit.prevent="apply"
            >
                <p class="text-sm text-secondary">{{ ResultsText.AddFilterHint }}</p>
                <SearchField
                    v-model:term="term"
                    :label="SearchText.NameLabel"
                    :endpoint="API_ENDPOINTS.suggestNames"
                />
                <div class="grid gap-4 md:grid-cols-3">
                    <FilterField
                        v-model="crops"
                        v-model:term="cropsTerm"
                        :label="SearchText.CropLabel"
                        :endpoint="API_ENDPOINTS.suggestCrops"
                    />
                    <FilterField
                        v-model="pests"
                        v-model:term="pestsTerm"
                        :label="SearchText.PestLabel"
                        :placeholder="SearchText.PestPlaceholder"
                        :endpoint="API_ENDPOINTS.suggestPests"
                    />
                    <FilterField
                        v-model="productTypes"
                        v-model:term="productTypesTerm"
                        :label="SearchText.ProductTypeLabel"
                        :placeholder="SearchText.ProductTypePlaceholder"
                        :endpoint="API_ENDPOINTS.suggestProductTypes"
                    />
                </div>
                <RoleSwitch v-model="draftRole" />
                <AppButton type="submit" :disabled="!hasChanges" class="w-full sm:w-auto sm:self-end">
                    {{ ResultsText.ApplyFilters }}
                </AppButton>
            </form>
        </CollapsibleContent>
    </CollapsibleRoot>
</template>
