<script setup lang="ts">
import Logo from "~/components/Logo.vue";
import { DATA_SOURCE_URL } from "~/constants/dataSource";
import { LayoutText } from "~/enums/LayoutText";

const { public: publicConfig } = useRuntimeConfig();
const dataSourceUrl = DATA_SOURCE_URL(String(publicConfig.daneGovDatasetId ?? ""));
</script>

<template>
    <div class="flex min-h-dvh flex-col text-black">
        <header class="flex justify-center px-4 pt-10 pb-8">
            <NuxtLink to="/" class="text-4xl font-bold text-primary">
                <Logo />
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
                    class="underline underline-offset-4 hover:text-primary-soft"
                >
                    {{ LayoutText.DataSourceLink }}</a>.
            </p>
            <p class="font-bold">
                {{ LayoutText.Footer }}
            </p>
        </footer>
    </div>
</template>
