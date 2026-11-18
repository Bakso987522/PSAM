import {
    ALTERNATIVES_API_LIMIT,
    ALTERNATIVES_PAGE_SIZE,
} from "~/constants/alternatives";
import { DEFAULT_PAGE } from "~/constants/search";
import { UserRole } from "~/enums/UserRole";
import { useUserRole } from "~/hooks/useUserRole";
import { toAlternative } from "~/mappers/alternatives";
import { fetchAlternatives, fetchProductCard } from "~/services/api";
import type { Alternative } from "~/types/product/Alternative";

interface AlternativesResult {
    items: Alternative[];
    hasProfessionalOnlyResults: boolean;
}

const EMPTY_ALTERNATIVES: AlternativesResult = {
    items: [],
    hasProfessionalOnlyResults: false,
};

const loadAlternatives = async (
    idSor: string,
    crop: string | undefined,
    role: UserRole,
): Promise<AlternativesResult> => {
    const { alternatives } = await fetchAlternatives(idSor, { crop, role });

    if (alternatives.length === 0) {
        if (role !== UserRole.Amateur) {
            return EMPTY_ALTERNATIVES;
        }
        const professional = await fetchAlternatives(idSor, {
            crop,
            role: UserRole.Professional,
        });
        return {
            items: [],
            hasProfessionalOnlyResults: professional.alternatives.length > 0,
        };
    }

    const cards = await Promise.allSettled(
        alternatives.map((alternative) => fetchProductCard(alternative.id_sor)),
    );

    return {
        items: alternatives.map((alternative, index) => {
            const card = cards[index];
            return toAlternative(
                alternative,
                card?.status === "fulfilled" ? card.value : undefined,
            );
        }),
        hasProfessionalOnlyResults: false,
    };
};

export function useAlternatives(idSor: MaybeRefOrGetter<string>) {
    const route = useRoute();
    const { role, setRole } = useUserRole();

    const crop = computed(() => {
        const value = [route.query.crop].flat()[0];
        return typeof value === "string" && value.trim() !== ""
            ? value.trim()
            : undefined;
    });

    const page = computed(() => {
        const value = Number([route.query.page].flat()[0]);
        return Number.isInteger(value) && value >= 1 ? value : DEFAULT_PAGE;
    });

    const { data, status, error } = useAsyncData(
        () => `alternatives-${toValue(idSor)}-${crop.value ?? ""}-${role.value}`,
        () => loadAlternatives(toValue(idSor), crop.value, role.value),
        { default: () => EMPTY_ALTERNATIVES },
    );

    const setCrop = async (value: string | undefined) => {
        const next = value?.trim() || undefined;
        if (next === crop.value) {
            return;
        }
        await navigateTo(
            {
                path: route.path,
                query: { ...route.query, crop: next, page: undefined },
            },
            { replace: true },
        );
    };

    const toPageQuery = (value: number) => ({
        ...route.query,
        page: value === DEFAULT_PAGE ? undefined : value,
    });

    const setPage = async (value: number) => {
        await navigateTo({ path: route.path, query: toPageQuery(value) });
        window.scrollTo({ top: 0, behavior: "smooth" });
    };

    const pageItems = computed(() => {
        const start = (page.value - 1) * ALTERNATIVES_PAGE_SIZE;
        return data.value.items.slice(start, start + ALTERNATIVES_PAGE_SIZE);
    });

    const isTruncated = computed(
        () => data.value.items.length >= ALTERNATIVES_API_LIMIT,
    );

    watch(data, ({ items }) => {
        if (status.value !== "success") {
            return;
        }
        const lastPage = Math.max(
            DEFAULT_PAGE,
            Math.ceil(items.length / ALTERNATIVES_PAGE_SIZE),
        );
        if (page.value > lastPage) {
            void navigateTo(
                { path: route.path, query: toPageQuery(lastPage) },
                { replace: true },
            );
        }
    });

    return {
        alternatives: data,
        pageItems,
        isTruncated,
        page,
        setPage,
        status,
        error,
        crop,
        role,
        setCrop,
        setRole,
    };
}
