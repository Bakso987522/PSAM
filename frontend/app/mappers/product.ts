import { ProductText } from "~/enums/ProductText";
import type {
    ProductCardApiResponse,
    UsageApiResponse,
} from "~/types/api/product";
import type { ProductCard } from "~/types/product/ProductCard";
import type {
    ProductUsage,
    ProductUsageGroup,
} from "~/types/product/ProductUsage";

const toProductUsage = (usage: UsageApiResponse): ProductUsage => {
    return {
        id: usage.id,
        pests: usage.pests ?? [],
        dose: usage.dose,
        timing: usage.timing,
        method: usage.method,
        preHarvestDays: usage.pre_harvest_days,
    };
};

const toUsageGroups = (usages: UsageApiResponse[]): ProductUsageGroup[] => {
    const groups = new Map<string, ProductUsage[]>();

    usages.forEach((usage) => {
        const crops = usage.crops?.length ? usage.crops : [ProductText.OtherCrops];
        crops.forEach((crop) => {
            groups.set(crop, [...(groups.get(crop) ?? []), toProductUsage(usage)]);
        });
    });

    return [...groups.entries()].map(([crop, cropUsages]) => ({
        crop,
        usages: cropUsages,
    }));
};

const toPackaging = (packaging: string | null) => {
    return (packaging ?? "")
        .split("\n")
        .map((line) => line.trim())
        .filter((line) => line !== "");
};

export const toProductCard = (response: ProductCardApiResponse): ProductCard => {
    const { product } = response;

    return {
        idSor: product.id_sor,
        name: product.name,
        producer: product.producer,
        permitNumber: product.permit_number,
        permitValidUntil: product.permit_valid_until,
        saleAllowedUntil: product.sale_allowed_until,
        useAllowedUntil: product.use_allowed_until,
        forAmateurs: product.for_amateurs,
        packaging: toPackaging(product.packaging),
        labelUrl: product.label_url,
        removedAt: product.removed_at,
        productTypes: response.product_types,
        substances: response.active_substances,
        usageGroups: toUsageGroups(response.usages),
    };
};
