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

    const formatSubstance = (substance: ProductSubstance) => {
        if (substance.content === null) {
            return substance.name;
        }
        const unit = substance.unit ? ` ${substance.unit}` : "";
        return `${substance.name} (${contentFormatter.format(substance.content)}${unit})`;
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

    const getProductHint = (product: SearchResult) => {
        const substances = product.substances
            .map((substance) => substance.name)
            .join(", ");
        return `${substances} - ${product.productTypes.join(", ")}`;
    };

    return {
        capitalize,
        formatSubstances,
        formatProductTypes,
        getUserLabel,
        getProductHint,
    };
}
