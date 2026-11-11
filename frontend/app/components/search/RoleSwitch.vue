<script setup lang="ts">
import { RadioGroupItem, RadioGroupRoot } from "reka-ui";
import { ROLE_OPTIONS } from "~/constants/search";
import { SearchText } from "~/enums/SearchText";
import type { UserRole } from "~/enums/UserRole";

const role = defineModel<UserRole>({ required: true });

const labelId = useId();
</script>

<template>
    <div class="flex flex-col gap-2">
        <span :id="labelId" class="font-bold">{{ SearchText.RoleLabel }}</span>
        <RadioGroupRoot
            v-model="role"
            :aria-labelledby="labelId"
            orientation="horizontal"
            class="grid grid-cols-2 gap-4"
        >
            <RadioGroupItem
                v-for="option in ROLE_OPTIONS"
                :key="option.value"
                :value="option.value"
                class="h-10 rounded-control border border-primary bg-white text-primary transition-colors hover:bg-primary-soft data-[state=checked]:bg-primary-soft"
            >
                {{ option.label }}
            </RadioGroupItem>
        </RadioGroupRoot>
    </div>
</template>
