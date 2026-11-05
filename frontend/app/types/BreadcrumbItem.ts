import type { RouteLocationRaw } from "vue-router";

export interface BreadcrumbItem {
    label: string;
    to?: RouteLocationRaw;
}
