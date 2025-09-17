<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from "vue";
import { CdxCard, CdxIcon } from "@wikimedia/codex";
import { cdxIconGlobe, cdxIconAlert } from "@wikimedia/codex-icons";
import type { Wikibase, ObsKind } from "../types";
import WikibaseDetailsDialog from "./WikibaseDetailsDialog.vue";
import { isStaleFor, obsHeadline } from "../utils";
import { fmtOrDash } from "../utils/format";

const props = defineProps<{ w: Wikibase }>();

/* ---------- dialog state ---------- */
const open = ref(false);

/* ---------- favicon ---------- */
// Load the favicon only when the card becomes visible
const cardContainerEl = ref<HTMLElement | null>(null);
let io: IntersectionObserver | null = null;
const shouldLoadFavicon = ref(false);
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
	[faviconUrl, shouldLoadFavicon],
	([url, should]) => {
		faviconReady.value = false;
		faviconError.value = false;
		if (!url || !should) return;
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
	{ immediate: false },
);

onMounted(() => {
	// If IntersectionObserver is not supported, do not load favicon
	if (
		typeof window === "undefined" ||
		typeof IntersectionObserver === "undefined"
	) {
		shouldLoadFavicon.value = false;
		return;
	}
	if (!cardContainerEl.value) return;
	io = new IntersectionObserver(
		(entries) => {
			for (const e of entries) {
				if (e.isIntersecting) {
					shouldLoadFavicon.value = true;
					if (cardContainerEl.value && io) io.unobserve(cardContainerEl.value);
					io?.disconnect();
					io = null;
					break;
				}
			}
		},
		{ root: null, rootMargin: "0px", threshold: 0 },
	);
	io.observe(cardContainerEl.value);
});

onBeforeUnmount(() => {
	io?.disconnect();
	io = null;
});

/* ---------- helpers ---------- */
function isStale(kind: ObsKind): boolean {
	return isStaleFor(props.w, kind);
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

function obsHeadlineLocal(kind: ObsKind): string {
	return obsHeadline(props.w, kind);
}
function fmtOrDashLocal(n?: number | null): string {
	return fmtOrDash(props.w, n);
}
</script>

<template>
	<div ref="cardContainerEl">
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
									:title="obsHeadlineLocal('rc')"
									aria-label="Recent changes data is stale"
								/>
							</dt>
							<dd class="text-xl font-bold token-text-base">
								{{ fmtOrDashLocal(rcTotal) }}
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
									:title="obsHeadlineLocal('quantity')"
									aria-label="Totals data is stale"
								/>
							</dt>
							<dd class="text-xl font-bold token-text-base">
								{{ fmtOrDashLocal(triples) }}
							</dd>
						</div>
					</dl>
				</div>

				<WikibaseDetailsDialog v-model:open="open" :w="props.w" />
			</template>
		</CdxCard>
	</div>
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
