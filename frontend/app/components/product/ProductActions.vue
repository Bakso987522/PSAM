<script setup lang="ts">
import AppButton from "~/components/ui/AppButton.vue";
import { ROUTES } from "~/constants/routes";
import { ProductText } from "~/enums/ProductText";

interface ProductActionsProps {
    idSor: string;
    name: string;
    labelUrl: string | null;
    labelMatched: boolean;
}

const { idSor, name, labelUrl, labelMatched } =
    defineProps<ProductActionsProps>();

const COPIED_RESET_MS = 2000;

const isCopied = ref(false);

const share = async () => {
    const url = window.location.href;

    if (navigator.share) {
        try {
            await navigator.share({ title: name, url });
        } catch {
            return;
        }
        return;
    }

    try {
        await navigator.clipboard.writeText(url);
    } catch {
        return;
    }
    isCopied.value = true;
    setTimeout(() => {
        isCopied.value = false;
    }, COPIED_RESET_MS);
};
</script>

<template>
    <div class="flex flex-wrap gap-2 sm:gap-3">
        <AppButton
            v-if="labelUrl && labelMatched"
            :to="ROUTES.label(idSor)"
        >
            {{ ProductText.Label }}
        </AppButton>
        <AppButton
            v-else-if="labelUrl"
            :href="labelUrl"
            external
        >
            {{ ProductText.LabelExternal }}
        </AppButton>
        <AppButton
            variant="outline"
            :to="ROUTES.alternatives(idSor)"
        >
            {{ ProductText.Alternatives }}
        </AppButton>
        <AppButton
            variant="outline"
            aria-live="polite"
            @click="share"
        >
            {{ isCopied ? ProductText.LinkCopied : ProductText.Share }}
        </AppButton>
    </div>
</template>
