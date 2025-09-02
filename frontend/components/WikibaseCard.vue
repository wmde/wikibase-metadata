<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { CdxCard, CdxIcon } from "@wikimedia/codex";
import { cdxIconGlobe, cdxIconAlert } from "@wikimedia/codex-icons";
import type { Wikibase, ObsKind } from "../types";

const props = defineProps<{ w: Wikibase }>();

/* ---------- favicon ---------- */
const faviconError = ref(false);
const faviconReady = ref(false);
const faviconUrl = computed(() => {
  const base = props.w.urls?.baseUrl;
  if (!base) return "";
  try { return new URL("/favicon.ico", base).toString(); } catch { return ""; }
});
watch(faviconUrl, (url) => {
  faviconReady.value = false; faviconError.value = false;
  if (!url) return;
  const img = new Image();
  img.onload = () => { faviconReady.value = true; };
  img.onerror = () => { faviconError.value = true; faviconReady.value = false; };
  img.src = url;
}, { immediate: true });

/* ---------- helpers ---------- */
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
const anyStale = computed(() => isStale("quantity") || isStale("rc"));

const showTotals = computed(() => props.w.hasQuantity());
const showRc = computed(() => props.w.hasRecentChanges());

/* ---------- description (clamped, no toggle) ---------- */

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
    { label: "Human users",   v: m?.humanChangeUserCount },
    { label: "Bot changes",   v: m?.botChangeCount },
    { label: "Bot users",     v: m?.botChangeUserCount },
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
</script>

<template>
  <CdxCard class="flex h-full flex-col">
    <template #title>
      <div class="flex items-center gap-3 min-w-0">
        <img v-if="faviconReady && !faviconError" :src="faviconUrl" alt="" class="h-5 w-5 rounded" />
        <CdxIcon v-else :icon="cdxIconGlobe" size="medium" />
        <a
          :href="props.w.urls?.baseUrl"
          target="_blank"
          rel="noreferrer noopener"
          :title="props.w.urls?.baseUrl || props.w.baseHost() || ''"
          class="w-0 flex-1 truncate text-lg font-semibold text-indigo-600 underline hover:text-indigo-500"
        >
          {{ props.w.baseHost() || "Unknown" }}
        </a>
      </div>
    </template>

    <template #description>
      <div class="space-y-1">
        <p v-if="props.w.timeToFirstValueObservations?.mostRecent?.initiationDate" class="text-xs text-black">
          Online since {{ props.w.fmtDate(props.w.timeToFirstValueObservations?.mostRecent?.initiationDate) }}
        </p>
        <div class="desc-wrapper">
          <div class="desc clamp" :title="props.w.description || ''">
            <template v-if="props.w.description">{{ props.w.description }}</template>
            <template v-else>&nbsp;</template>
          </div>
        </div>
      </div>
    </template>

    <template #supporting-text>
      <div class="mt-3 flex flex-col gap-5">
        <!-- Totals -->
        <section v-if="showTotals" class="border-t border-gray-200 pt-3">
          <header class="mb-2">
            <p class="text-xs font-semibold uppercase tracking-wide text-black">Totals</p>
            <p class="inline-flex items-center gap-1 text-xs text-black">
              <CdxIcon v-if="isStale('quantity')" :icon="cdxIconAlert" size="small" />
              {{ obsHeadline('quantity') }}
            </p>
          </header>
          <dl class="grid grid-cols-2 gap-3">
            <template v-for="t in totals" :key="t.label">
              <div class="rounded-lg bg-gray-50 p-3">
                <dt class="text-[11px] uppercase text-gray-700">{{ t.label }}</dt>
                <dd class="text-xl font-bold text-black">{{ fmtOrDash(t.v) }}</dd>
              </div>
            </template>
          </dl>
        </section>

        <!-- Recent changes -->
        <section v-if="showRc" class="border-t border-gray-200 pt-3">
          <header class="mb-2">
            <p class="text-xs font-semibold uppercase tracking-wide text-black">Changes in the last 30 days</p>
            <p class="inline-flex items-center gap-1 text-xs text-black">
              <CdxIcon v-if="isStale('rc')" :icon="cdxIconAlert" size="small" />
              {{ obsHeadline('rc') }}
            </p>
          </header>
          <dl class="grid grid-cols-2 gap-3">
            <template v-for="t in rc" :key="t.label">
              <div class="rounded-lg bg-gray-50 p-3">
                <dt class="text-[11px] uppercase text-gray-700">{{ t.label }}</dt>
                <dd class="text-xl font-bold text-black">{{ fmtOrDash(t.v) }}</dd>
              </div>
            </template>
          </dl>
        </section>

        <!-- Empty state if no data at all -->
        <section v-if="!showTotals && !showRc" class="rounded-md border border-gray-200 bg-white p-3 text-sm text-gray-700">
          No metrics available yet. This wikibase may be newly discovered or missing data.
        </section>
      </div>

      <!-- Staleness banner -->
      <div v-if="anyStale" class="mt-3 rounded-md border border-amber-300 bg-amber-50 px-3 py-2 text-xs text-amber-900" role="status" aria-live="polite">
        <span class="inline-flex items-center gap-1">
          <CdxIcon :icon="cdxIconAlert" size="small" />
          Some metrics may be outdated (last fetch over 30 days ago).
        </span>
      </div>

    </template>
  </CdxCard>
</template>

<style scoped>
.desc-wrapper {
  position: relative;
  min-height: 2.6rem; /* ~2 lines of 1.3rem line-height */
}
.desc {
  font-size: 0.875rem; /* ~text-sm */
  line-height: 1.3rem;
  color: #000;
}
.desc.clamp {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
