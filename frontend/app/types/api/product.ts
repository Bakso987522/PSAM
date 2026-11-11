export interface ProductApiResponse {
    id_sor: string;
    name: string;
    producer: string;
    permit_number: string;
    permit_valid_until: string;
    sale_allowed_until: string;
    use_allowed_until: string;
    for_amateurs: boolean;
    packaging: string | null;
    label_url: string | null;
    label_matched: boolean;
    base_product_name: string | null;
    removed_at: string | null;
}

export interface ProductSubstanceApiResponse {
    name: string;
    content: number | null;
    unit: string | null;
}

export interface UsageApiResponse {
    id: number;
    dose: string | null;
    timing: string | null;
    method: string | null;
    combined_use: string | null;
    minor_use: boolean;
    pre_harvest_days: number | null;
    pre_harvest_source: string | null;
    crops: string[] | null;
    pests: string[] | null;
}

export interface ProductCardApiResponse {
    product: ProductApiResponse;
    product_types: string[];
    active_substances: ProductSubstanceApiResponse[];
    usages: UsageApiResponse[];
}
