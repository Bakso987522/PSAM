const MOBILE_MEDIA_QUERY = "(max-width: 639px)";

export function useIsMobile() {
    const isMobile = ref(false);
    let mediaQuery: MediaQueryList | undefined;

    const update = () => {
        isMobile.value = mediaQuery?.matches ?? false;
    };

    onMounted(() => {
        mediaQuery = window.matchMedia(MOBILE_MEDIA_QUERY);
        update();
        mediaQuery.addEventListener("change", update);
    });

    onBeforeUnmount(() => {
        mediaQuery?.removeEventListener("change", update);
    });

    return { isMobile };
}
