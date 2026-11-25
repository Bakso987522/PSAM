<script setup lang="ts">
import Logo from "~/components/Logo.vue";
import { DATA_SOURCE_URL } from "~/constants/dataSource";
import { ROUTES } from "~/constants/routes";
import { LayoutText } from "~/enums/LayoutText";

const route = useRoute();
const isHome = computed(() => route.path === ROUTES.home);

const { public: publicConfig } = useRuntimeConfig();
const dataSourceUrl = DATA_SOURCE_URL(String(publicConfig.daneGovDatasetId ?? ""));
</script>

<template>
    <div class="flex min-h-dvh flex-col text-black">
        <header
            class="flex px-4"
            :class="isHome ? 'justify-center pt-10 pb-8' : 'justify-start pt-4 pb-2 sm:px-6'"
        >
            <NuxtLink to="/" :aria-label="LayoutText.HomeLink" class="text-primary">
                <Logo :class="isHome ? 'h-auto w-59' : 'h-auto w-20 sm:w-24'" />
            </NuxtLink>
        </header>
        <main
            class="mx-auto flex w-full flex-1 flex-col items-center px-4 pb-10"
        >
            <slot />
        </main>
        <footer class="flex flex-col gap-1 bg-primary px-4 py-4 text-center text-white">
            <p class="text-sm">
                {{ LayoutText.DataSource }}
                <a
                    :href="dataSourceUrl"
                    target="_blank"
                    rel="noopener"
                    class="inline-flex touch-target items-center underline underline-offset-4 hover:text-primary-soft"
                >
                    {{ LayoutText.DataSourceLink }}</a>.
            </p>
            <p class="font-bold">
                {{ LayoutText.Footer }}
            </p>
        </footer>
    </div>
</template>
