import { MOCK_PRODUCTS } from "~/mocks/products";
import type { MockProduct } from "~/types/MockProduct";
import type { RemovedProduct } from "~/types/RemovedProduct";
import type { SearchCriteria } from "~/types/SearchCriteria";
import type { SearchResponse } from "~/types/SearchResponse";
import type { SearchResult } from "~/types/SearchResult";

const normalize = (value: string) => {
    return value
        .toLowerCase()
        .replace(/ł/g, "l")
        .normalize("NFD")
        .replace(/\p{Diacritic}/gu, "")
        .trim();
};

const matchesText = (candidate: string, query: string) => {
    return normalize(candidate).includes(normalize(query));
};

const matchesAny = (candidates: string[], queries: string[]) => {
    return (
        queries.length === 0 ||
        queries.some((query) =>
            candidates.some((candidate) => matchesText(candidate, query)),
        )
    );
};

const matchesName = (product: MockProduct, query?: string) => {
    return (
        !query ||
        matchesText(product.name, query) ||
        product.substances.some((substance) =>
            matchesText(substance.name, query),
        )
    );
};

const matchesUsage = (product: MockProduct, criteria: SearchCriteria) => {
    if (criteria.crops.length === 0 && criteria.pests.length === 0) {
        return true;
    }

    return product.usages.some(
        (usage) =>
            matchesAny(usage.crops, criteria.crops) &&
            matchesAny(usage.pests, criteria.pests),
    );
};

const matchesCriteria = (product: MockProduct, criteria: SearchCriteria) => {
    return (
        matchesName(product, criteria.q) &&
        matchesUsage(product, criteria) &&
        matchesAny(product.productTypes, criteria.productTypes)
    );
};

const matchesRole = (product: MockProduct, criteria: SearchCriteria) => {
    return criteria.role !== "amateur" || product.forAmateurs;
};

const toSearchResult = (product: MockProduct): SearchResult => {
    return {
        idSor: product.idSor,
        name: product.name,
        productTypes: product.productTypes,
        substances: product.substances,
        forAmateurs: product.forAmateurs,
        useAllowedUntil: product.useAllowedUntil,
    };
};

const toRemovedProduct = (product: MockProduct): RemovedProduct => {
    return {
        idSor: product.idSor,
        name: product.name,
        removedAt: product.removedAt ?? "",
    };
};

export const searchMockProducts = (criteria: SearchCriteria): SearchResponse => {
    const matchedProducts = MOCK_PRODUCTS.filter((product) =>
        matchesCriteria(product, criteria),
    );
    const registeredProducts = matchedProducts.filter(
        (product) => product.removedAt === null,
    );
    const items = registeredProducts
        .filter((product) => matchesRole(product, criteria))
        .map(toSearchResult)
        .sort((first, second) => first.name.localeCompare(second.name, "pl"));

    return {
        total: items.length,
        items,
        removed: matchedProducts
            .filter((product) => product.removedAt !== null)
            .map(toRemovedProduct),
        hasProfessionalOnlyResults:
            items.length === 0 && registeredProducts.length > 0,
    };
};
