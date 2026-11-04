<script setup lang="ts">
import Logo from "~/components/Logo.vue";
</script>

<template>
    <div class="flex min-h-dvh flex-col text-black">
        <header class="flex justify-center px-4 pt-10 pb-8">
            <NuxtLink to="/" class="text-4xl font-bold text-primary">
                <Logo />
            </NuxtLink>
        </header>
        <main
            class="mx-auto w-full max-w-4xl flex flex-1 flex-col items-center px-4 pb-10"
        >
            <slot />
        </main>
        <footer class="bg-primary text-center">
            <p class="py-4 text-white font-bold">
                Created by Damian Nowak, Jakub Bakaj, Natalia Duda
            </p>
        </footer>
    </div>
</template>
