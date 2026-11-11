import { ProductUserLabel } from "~/enums/ProductUserLabel";
import type { ProductSubstance } from "~/types/product/ProductSubstance";
import type { SearchResult } from "~/types/search/SearchResult";

const contentFormatter = new Intl.NumberFormat("pl-PL", {
    maximumFractionDigits: 4,
});

export function useProductFormatter() {
    const capitalize = (value: string) => {
        return value.charAt(0).toLocaleUpperCase("pl-PL") + value.slice(1);
    };

    const formatContent = (substance: ProductSubstance) => {
        if (substance.content === null) {
            return "";
        }
        const unit = substance.unit ? ` ${substance.unit}` : "";
        return `${contentFormatter.format(substance.content)}${unit}`;
    };

    const formatSubstance = (substance: ProductSubstance) => {
        const content = formatContent(substance);
        return content ? `${substance.name} (${content})` : substance.name;
    };

    const formatSubstances = (substances: ProductSubstance[]) => {
        return substances.map(formatSubstance).join(", ");
    };

    const formatProductTypes = (productTypes: string[]) => {
        return capitalize(productTypes.join(", "));
    };

    const getUserLabel = (forAmateurs: boolean) => {
        return forAmateurs
            ? ProductUserLabel.Amateur
            : ProductUserLabel.Professional;
    };

    const getProductHint = (
        product: Pick<SearchResult, "substances" | "productTypes">,
    ) => {
        const substances = product.substances
            .map((substance) => substance.name)
            .join(", ");
        return `${substances} - ${product.productTypes.join(", ")}`;
    };

    return {
        capitalize,
        formatContent,
        formatSubstance,
        formatSubstances,
        formatProductTypes,
        getUserLabel,
        getProductHint,
    };
}
