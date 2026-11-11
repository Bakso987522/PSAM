<script setup lang="ts">
import FilterField from "~/components/search/FilterField.vue";
import RoleSwitch from "~/components/search/RoleSwitch.vue";
import SearchField from "~/components/search/SearchField.vue";
import AppButton from "~/components/ui/AppButton.vue";
import { API_ENDPOINTS } from "~/constants/api";
import { SearchText } from "~/enums/SearchText";
import { useSearchForm } from "~/hooks/useSearchForm";

const {
    term,
    crops,
    cropsTerm,
    pests,
    pestsTerm,
    productTypes,
    productTypesTerm,
    role,
    canSubmit,
    submitSearch,
} = useSearchForm();
</script>

<template>
    <form role="search" class="flex flex-col gap-5" @submit.prevent="submitSearch">
        <SearchField
            v-model:term="term"
            :label="SearchText.NameLabel"
            :endpoint="API_ENDPOINTS.suggestNames"
        />
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
        <RoleSwitch v-model="role" />
        <AppButton type="submit" :disabled="!canSubmit" class="mt-2 w-full">
            {{ SearchText.Submit }}
        </AppButton>
    </form>
</template>
