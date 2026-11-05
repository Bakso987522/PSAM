<script setup lang="ts">
import { usePermitStatus } from "~/hooks/usePermitStatus";
import type { PermitStatus } from "~/types/PermitStatus";

interface PermitBadgeProps {
    useAllowedUntil: string;
}

const { useAllowedUntil } = defineProps<PermitBadgeProps>();

const { getPermitStatus, getPermitLabel } = usePermitStatus();

const statusClasses: Record<PermitStatus, string> = {
    expired: "bg-danger-bg text-danger-fg",
    expiring: "bg-warn-bg text-warn-fg",
    active: "bg-neutral-bg text-primary-darker",
};

const status = computed(() => getPermitStatus(useAllowedUntil));
const label = computed(() => getPermitLabel(status.value, useAllowedUntil));
</script>

<template>
    <span
        class="inline-flex min-h-7 items-center rounded-badge px-2.5 py-0.5 text-sm font-bold"
        :class="statusClasses[status]"
    >
        {{ label }}
    </span>
</template>
