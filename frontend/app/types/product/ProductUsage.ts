export interface ProductUsage {
    id: number;
    pests: string[];
    dose: string | null;
    timing: string | null;
    method: string | null;
    preHarvestDays: number | null;
}

export interface ProductUsageGroup {
    crop: string;
    usages: ProductUsage[];
}
