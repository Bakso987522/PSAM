export type ActiveFilterKind =
    | "q"
    | "crops"
    | "pests"
    | "productTypes"
    | "role";

export type ListFilterKind = Exclude<ActiveFilterKind, "q" | "role">;

export interface ActiveFilter {
    key: string;
    kind: ActiveFilterKind;
    value: string;
    label: string;
}
