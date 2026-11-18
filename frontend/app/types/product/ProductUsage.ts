export interface ProductUsage {
    id: number;
    pests: string[];
    dose: string | null;
    timing: string | null;
    method: string | null;
    preHarvestDays: number | null;
    combinedUse: string | null;
    minorUse: boolean;
}

export interface ProductUsageGroup {
    crop: string;
    usages: ProductUsage[];
}
