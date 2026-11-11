<script setup lang="ts">
import AppButton from "~/components/ui/AppButton.vue";
import { ROUTES } from "~/constants/routes";
import { ProductText } from "~/enums/ProductText";

interface ProductActionsProps {
    idSor: string;
    name: string;
    labelUrl: string | null;
}

const { idSor, name, labelUrl } = defineProps<ProductActionsProps>();

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
        <a
            v-if="labelUrl"
            :href="labelUrl"
            target="_blank"
            rel="noopener"
            class="inline-flex h-10 flex-1 items-center sm:flex-none justify-center rounded-control border border-primary bg-primary px-5 text-white transition-colors hover:bg-primary-dark"
        >
            {{ ProductText.Label }}
        </a>
        <AppButton
            variant="outline"
            class="flex-1 sm:flex-none"
            :to="ROUTES.alternatives(idSor)"
        >
            {{ ProductText.Alternatives }}
        </AppButton>
        <AppButton
            variant="outline"
            class="flex-1 sm:flex-none"
            aria-live="polite"
            @click="share"
        >
            {{ isCopied ? ProductText.LinkCopied : ProductText.Share }}
        </AppButton>
    </div>
</template>
