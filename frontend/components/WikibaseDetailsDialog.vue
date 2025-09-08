<script setup lang="ts">
import { computed } from "vue";
import { CdxDialog, CdxIcon } from "@wikimedia/codex";
import { cdxIconAlert } from "@wikimedia/codex-icons";
import type { Wikibase, ObsKind } from "../types";

const props = defineProps<{ w: Wikibase; open: boolean }>();
const emit = defineEmits<{ (e: "update:open", v: boolean): void }>();

/* ---------- helpers (dialog) ---------- */
function daysSince(dateIso?: string): number | null {
  if (!dateIso) return null;
  const t = new Date(dateIso).getTime();
  if (Number.isNaN(t)) return null;
  return Math.max(0, Math.floor((Date.now() - t) / 86400000));
}
function relativeDaysText(dateIso?: string): string {
  const d = daysSince(dateIso);
  if (d == null) return "";
  if (d === 0) return "today";
  if (d === 1) return "yesterday";
  return `${d} days ago`;
}
function isStale(kind: ObsKind): boolean {
  const d = props.w.getObservationDate(kind);
  const ds = daysSince(d);
  return ds != null && ds > 30;
}
const totals = computed(() => {
  const m = props.w.quantityObservations?.mostRecent;
  return [
    { label: "Items", v: m?.totalItems },
    { label: "Properties", v: m?.totalProperties },
    { label: "Lexemes", v: m?.totalLexemes },
    { label: "Triples", v: m?.totalTriples },
  ];
});
const rc = computed(() => {
  const m = props.w.recentChangesObservations?.mostRecent;
  return [
    { label: "Human changes", v: m?.humanChangeCount },
    { label: "Human users", v: m?.humanChangeUserCount },
    { label: "Bot changes", v: m?.botChangeCount },
    { label: "Bot users", v: m?.botChangeUserCount },
  ];
});
function obsHeadline(kind: ObsKind): string {
  const d = props.w.getObservationDate(kind);
  const rel = relativeDaysText(d);
  return rel ? `Fetched ${rel}` : "No fetch date";
}
function fmtOrDash(n?: number | null): string {
  return n == null ? "—" : props.w.fmt(n);
}
function textOrDash(s?: string | null): string {
  return s && String(s).length > 0 ? String(s) : "—";
}
function resolveHref(s?: string | null): string | null {
  if (!s) return null;
  if (typeof s === "string" && s.includes("$1")) return null;
  try {
    const base = props.w.urls?.baseUrl;
    const url = base ? new URL(s as string, base) : new URL(s as string);
    return url.toString();
  } catch {
    return null;
  }
}
</script>

<template>
  <CdxDialog
    :open="props.open"
    @update:open="(v:boolean)=>emit('update:open', v)"
    :title="props.w.baseHost() || 'Details'"
    :use-close-button="true"
    :default-action="{ label: 'Close' }"
    @default="emit('update:open', false)"
  >
    <div class="space-y-5">
      <section>
        {{ props.w.description }}
      </section>
      <section>
        <dl class="grid grid-cols-1 gap-2">
          <div class="token-rounded token-surface-2 px-3">
            <dt class="text-[11px] uppercase token-text-subtle">Base URL</dt>
            <dd class="text-sm token-text-base break-all">
              <template v-if="resolveHref(props.w.urls?.baseUrl)">
                <a
                  :href="resolveHref(props.w.urls?.baseUrl) as string"
                  target="_blank"
                  rel="noreferrer noopener"
                  class="token-link"
                >
                  {{ props.w.urls?.baseUrl }}
                </a>
              </template>
              <template v-else>
                {{ textOrDash(props.w.urls?.baseUrl) }}
              </template>
            </dd>
          </div>
          <div class="token-rounded token-surface-2 p-3">
            <dt class="text-[11px] uppercase token-text-subtle">SPARQL Endpoint</dt>
            <dd class="text-sm token-text-base break-all">
              <template v-if="resolveHref(props.w.urls?.sparqlEndpointUrl)">
                <a
                  :href="resolveHref(props.w.urls?.sparqlEndpointUrl) as string"
                  target="_blank"
                  rel="noreferrer noopener"
                  class="token-link"
                >
                  {{ props.w.urls?.sparqlEndpointUrl }}
                </a>
              </template>
              <template v-else>
                {{ textOrDash(props.w.urls?.sparqlEndpointUrl) }}
              </template>
            </dd>
          </div>
          <div class="token-rounded token-surface-2 p-3">
            <dt class="text-[11px] uppercase token-text-subtle">SPARQL Frontend</dt>
            <dd class="text-sm token-text-base break-all">
              <template v-if="resolveHref(props.w.urls?.sparqlFrontendUrl)">
                <a
                  :href="resolveHref(props.w.urls?.sparqlFrontendUrl) as string"
                  target="_blank"
                  rel="noreferrer noopener"
                  class="token-link"
                >
                  {{ props.w.urls?.sparqlFrontendUrl }}
                </a>
              </template>
              <template v-else>
                {{ textOrDash(props.w.urls?.sparqlFrontendUrl) }}
              </template>
            </dd>
          </div>
          <!-- Script and Article paths side-by-side -->
          <div class="grid grid-cols-2 gap-2">
            <div class="token-rounded token-surface-2 p-3">
              <dt class="text-[11px] uppercase token-text-subtle">Script Path</dt>
              <dd class="text-sm token-text-base break-all">
                {{ textOrDash(props.w.urls?.scriptPath) }}
              </dd>
            </div>
            <div class="token-rounded token-surface-2 p-3">
              <dt class="text-[11px] uppercase token-text-subtle">Article Path</dt>
              <dd class="text-sm token-text-base break-all">
                {{ textOrDash(props.w.urls?.articlePath) }}
              </dd>
            </div>
          </div>
        </dl>
      </section>

      <section>
        <header class="mb-2">
          <p class="text-xs font-semibold uppercase tracking-wide token-text-base">Totals</p>
          <p class="inline-flex items-center gap-1 text-xs token-text-base">
            <CdxIcon v-if="isStale('quantity')" :icon="cdxIconAlert" size="small" />
            {{ obsHeadline("quantity") }}
          </p>
        </header>
        <dl class="grid grid-cols-2 gap-3">
          <template v-for="t in totals" :key="t.label">
            <div class="token-rounded token-surface-2 p-3">
              <dt class="text-[11px] uppercase token-text-subtle">{{ t.label }}</dt>
              <dd class="text-xl font-bold token-text-base">{{ fmtOrDash(t.v) }}</dd>
            </div>
          </template>
        </dl>
      </section>

      <section>
        <header class="mb-2">
          <p class="text-xs font-semibold uppercase tracking-wide token-text-base">Edits in the last 30 days</p>
          <p class="inline-flex items-center gap-1 text-xs token-text-base">
            <CdxIcon v-if="isStale('rc')" :icon="cdxIconAlert" size="small" />
            {{ obsHeadline("rc") }}
          </p>
        </header>
        <dl class="grid grid-cols-2 gap-3">
          <template v-for="t in rc" :key="t.label">
            <div class="token-rounded token-surface-2 p-3">
              <dt class="text-[11px] uppercase token-text-subtle">{{ t.label }}</dt>
              <dd class="text-xl font-bold token-text-base">{{ fmtOrDash(t.v) }}</dd>
            </div>
          </template>
        </dl>
      </section>

      <section>
        <p class="text-xs token-text-base">
          Online since
          {{ textOrDash(props.w.fmtDate(props.w.timeToFirstValueObservations?.mostRecent?.initiationDate)) }}
        </p>
      </section>
    </div>
  </CdxDialog>
</template>

<style scoped></style>

