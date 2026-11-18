import { toPackaging } from "~/mappers/product";
import type { AlternativeApiResponse } from "~/types/api/alternatives";
import type { ProductCardApiResponse } from "~/types/api/product";
import type { Alternative } from "~/types/product/Alternative";

export const toAlternative = (
    alternative: AlternativeApiResponse,
    card?: ProductCardApiResponse,
): Alternative => {
    return {
        idSor: alternative.id_sor,
        name: alternative.name,
        substances: card?.active_substances ?? null,
        rawContent: alternative.content ?? [],
        packaging: toPackaging(alternative.packaging),
        forAmateurs: alternative.for_amateurs,
        useAllowedUntil: alternative.use_allowed_until,
        sameContent: alternative.same_content,
    };
};
