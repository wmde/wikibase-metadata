<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { CdxCard, CdxIcon } from "@wikimedia/codex";
import { cdxIconGlobe, cdxIconAlert } from "@wikimedia/codex-icons";
import type { Wikibase, ObsKind } from "../types";
import WikibaseDetailsDialog from "./WikibaseDetailsDialog.vue";

const props = defineProps<{ w: Wikibase }>();

/* ---------- dialog state ---------- */
const open = ref(false);

/* ---------- favicon ---------- */
const faviconError = ref(false);
const faviconReady = ref(false);
const faviconUrl = computed(() => {
	const base = props.w.urls?.baseUrl;
	if (!base) return "";
	try {
		return new URL("/favicon.ico", base).toString();
	} catch {
		return "";
	}
});
watch(
	faviconUrl,
	(url) => {
		faviconReady.value = false;
		faviconError.value = false;
		if (!url) return;
		const img = new Image();
		img.onload = () => {
			faviconReady.value = true;
		};
		img.onerror = () => {
			faviconError.value = true;
			faviconReady.value = false;
		};
		img.src = url;
	},
	{ immediate: true },
);

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

/* ---------- summary metrics (minimal card) ---------- */
const triples = computed(
	() => props.w.quantityObservations?.mostRecent?.totalTriples,
);
const rcTotal = computed(() => {
	const m = props.w.recentChangesObservations?.mostRecent;
	if (!m) return undefined;
	const h = typeof m.humanChangeCount === "number" ? m.humanChangeCount : 0;
	const b = typeof m.botChangeCount === "number" ? m.botChangeCount : 0;
	const total = h + b;
	return total > 0 ? total : (m.humanChangeCount ?? m.botChangeCount);
});

function obsHeadline(kind: ObsKind): string {
	const d = props.w.getObservationDate(kind);
	const rel = relativeDaysText(d);
	return rel ? `Fetched ${rel}` : "No fetch date";
}
function fmtOrDash(n?: number | null): string {
	return n == null ? "—" : props.w.fmt(n);
}

// All detail fields are shown regardless of data availability.
</script>

<template>
	<CdxCard
		class="flex h-full flex-col clickable-card"
		@click="open = true"
		@keydown.enter.prevent="open = true"
		@keydown.space.prevent="open = true"
		tabindex="0"
		role="button"
	>
		<template #title>
			<div class="flex items-center gap-3 min-w-0">
				<img
					v-if="faviconReady && !faviconError"
					:src="faviconUrl"
					alt=""
					class="h-5 w-5 rounded"
				/>
				<CdxIcon v-else :icon="cdxIconGlobe" size="medium" />
				<span
					:title="props.w.urls?.baseUrl || props.w.baseHost() || ''"
					class="w-0 flex-1 truncate text-lg font-semibold token-text-base"
				>
					{{ props.w.baseHost() || "Unknown" }}
				</span>
			</div>
		</template>

		<template #description>
			<div class="space-y-1">
				<div class="desc-wrapper">
					<div class="desc clamp" :title="props.w.description || ''">
						<template v-if="props.w.description">{{
							props.w.description
						}}</template>
						<template v-else>&nbsp;</template>
					</div>
				</div>
			</div>
		</template>

		<template #supporting-text>
			<!-- Minimal summary: 30-day changes total + triples -->
			<div class="mt-3">
				<dl class="grid grid-cols-2 gap-3">
					<div class="token-rounded token-surface-2 p-3">
						<dt
							class="flex items-center gap-1 text-[11px] uppercase token-text-subtle"
						>
							Edits (30 days)
							<CdxIcon
								v-if="isStale('rc')"
								:icon="cdxIconAlert"
								class="token-text-warning"
								size="small"
								:title="obsHeadline('rc')"
								aria-label="Recent changes data is stale"
							/>
						</dt>
						<dd class="text-xl font-bold token-text-base">
							{{ fmtOrDash(rcTotal) }}
						</dd>
					</div>
					<div class="token-rounded token-surface-2 p-3">
						<dt
							class="flex items-center gap-1 text-[11px] uppercase token-text-subtle"
						>
							Triples
							<CdxIcon
								v-if="isStale('quantity')"
								:icon="cdxIconAlert"
								class="token-text-warning"
								size="small"
								:title="obsHeadline('quantity')"
								aria-label="Totals data is stale"
							/>
						</dt>
						<dd class="text-xl font-bold token-text-base">
							{{ fmtOrDash(triples) }}
						</dd>
					</div>
				</dl>
			</div>

			<WikibaseDetailsDialog v-model:open="open" :w="props.w" />
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
	color: var(--color-base);
}
.desc.clamp {
	display: -webkit-box;
	-webkit-line-clamp: 2;
	-webkit-box-orient: vertical;
	overflow: hidden;
}

.clickable-card {
	cursor: pointer;
}
.clickable-card:focus {
	outline: 2px solid var(--color-progressive);
	outline-offset: 2px;
}
:deep(.cdx-card__text) {
	width: 100%;
}
</style>
