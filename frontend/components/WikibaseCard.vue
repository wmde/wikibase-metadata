<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { CdxCard, CdxIcon, CdxDialog } from "@wikimedia/codex";
import { cdxIconGlobe, cdxIconAlert } from "@wikimedia/codex-icons";
import type { Wikibase, ObsKind } from "../types";

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

/* ---------- detail data for dialog ---------- */
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
	// Avoid linking templated article paths like "/wiki/$1"
	if (typeof s === "string" && s.includes("$1")) return null;
	try {
		const base = props.w.urls?.baseUrl;
		const url = base ? new URL(s as string, base) : new URL(s as string);
		return url.toString();
	} catch {
		return null;
	}
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
					class="w-0 flex-1 truncate text-lg font-semibold text-black"
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
					<div class="rounded-lg bg-gray-50 p-3">
						<dt
							class="flex items-center gap-1 text-[11px] uppercase text-gray-700"
						>
							Edits (30 days)
							<CdxIcon
								v-if="isStale('rc')"
								:icon="cdxIconAlert"
								size="small"
								:title="obsHeadline('rc')"
								aria-label="Recent changes data is stale"
							/>
						</dt>
						<dd class="text-xl font-bold text-black">
							{{ fmtOrDash(rcTotal) }}
						</dd>
					</div>
					<div class="rounded-lg bg-gray-50 p-3">
						<dt
							class="flex items-center gap-1 text-[11px] uppercase text-gray-700"
						>
							Triples
							<CdxIcon
								v-if="isStale('quantity')"
								:icon="cdxIconAlert"
								size="small"
								:title="obsHeadline('quantity')"
								aria-label="Totals data is stale"
							/>
						</dt>
						<dd class="text-xl font-bold text-black">
							{{ fmtOrDash(triples) }}
						</dd>
					</div>
				</dl>
			</div>

			<!-- Detail dialog with all numbers -->
			<CdxDialog
				v-model:open="open"
				:title="props.w.baseHost() || 'Details'"
				:use-close-button="true"
				:default-action="{ label: 'Close' }"
				@default="open = false"
			>
				<div class="space-y-5">
					<section>
						{{ props.w.description }}
					</section>
					<section>
						<dl class="grid grid-cols-1 gap-2">
							<div class="rounded-lg bg-gray-50 px-3">
								<dt class="text-[11px] uppercase text-gray-700">Base URL</dt>
								<dd class="text-sm text-black break-all">
									<template v-if="resolveHref(props.w.urls?.baseUrl)">
										<a
											:href="resolveHref(props.w.urls?.baseUrl) as string"
											target="_blank"
											rel="noreferrer noopener"
											class="text-indigo-600 underline hover:text-indigo-500"
										>
											{{ props.w.urls?.baseUrl }}
										</a>
									</template>
									<template v-else>
										{{ textOrDash(props.w.urls?.baseUrl) }}
									</template>
								</dd>
							</div>
							<div class="rounded-lg bg-gray-50 p-3">
								<dt class="text-[11px] uppercase text-gray-700">SPARQL Endpoint</dt>
								<dd class="text-sm text-black break-all">
									<template v-if="resolveHref(props.w.urls?.sparqlEndpointUrl)">
										<a
											:href="resolveHref(props.w.urls?.sparqlEndpointUrl) as string"
											target="_blank"
											rel="noreferrer noopener"
											class="text-indigo-600 underline hover:text-indigo-500"
										>
											{{ props.w.urls?.sparqlEndpointUrl }}
										</a>
									</template>
									<template v-else>
										{{ textOrDash(props.w.urls?.sparqlEndpointUrl) }}
									</template>
								</dd>
							</div>
							<div class="rounded-lg bg-gray-50 p-3">
								<dt class="text-[11px] uppercase text-gray-700">SPARQL Frontend</dt>
								<dd class="text-sm text-black break-all">
									<template v-if="resolveHref(props.w.urls?.sparqlFrontendUrl)">
										<a
											:href="resolveHref(props.w.urls?.sparqlFrontendUrl) as string"
											target="_blank"
											rel="noreferrer noopener"
											class="text-indigo-600 underline hover:text-indigo-500"
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
                                <div class="rounded-lg bg-gray-50 p-3">
                                    <dt class="text-[11px] uppercase text-gray-700">Script Path</dt>
                                    <dd class="text-sm text-black break-all">
                                        {{ textOrDash(props.w.urls?.scriptPath) }}
                                    </dd>
                                </div>
                                <div class="rounded-lg bg-gray-50 p-3">
                                    <dt class="text-[11px] uppercase text-gray-700">Article Path</dt>
                                    <dd class="text-sm text-black break-all">
                                        {{ textOrDash(props.w.urls?.articlePath) }}
                                    </dd>
                                </div>
                            </div>
						</dl>
					</section>
					<section>
						<header class="mb-2">
							<p
								class="text-xs font-semibold uppercase tracking-wide text-black"
							>
								Totals
							</p>
							<p class="inline-flex items-center gap-1 text-xs text-black">
								<CdxIcon
									v-if="isStale('quantity')"
									:icon="cdxIconAlert"
									size="small"
								/>
								{{ obsHeadline("quantity") }}
							</p>
						</header>
						<dl class="grid grid-cols-2 gap-3">
							<template v-for="t in totals" :key="t.label">
								<div class="rounded-lg bg-gray-50 p-3">
									<dt class="text-[11px] uppercase text-gray-700">
										{{ t.label }}
									</dt>
									<dd class="text-xl font-bold text-black">
										{{ fmtOrDash(t.v) }}
									</dd>
								</div>
							</template>
						</dl>
					</section>

					<section>
						<header class="mb-2">
							<p
								class="text-xs font-semibold uppercase tracking-wide text-black"
							>
								Edits in the last 30 days
							</p>
							<p class="inline-flex items-center gap-1 text-xs text-black">
								<CdxIcon
									v-if="isStale('rc')"
									:icon="cdxIconAlert"
									size="small"
								/>
								{{ obsHeadline("rc") }}
							</p>
						</header>
						<dl class="grid grid-cols-2 gap-3">
							<template v-for="t in rc" :key="t.label">
								<div class="rounded-lg bg-gray-50 p-3">
									<dt class="text-[11px] uppercase text-gray-700">
										{{ t.label }}
									</dt>
									<dd class="text-xl font-bold text-black">
										{{ fmtOrDash(t.v) }}
									</dd>
								</div>
							</template>
						</dl>
					</section>

					<section>
						<p class="text-xs text-black">
							Online since
							{{ textOrDash(
								props.w.fmtDate(
									props.w.timeToFirstValueObservations?.mostRecent?.initiationDate,
								),
							) }}
						</p>
					</section>
				</div>
			</CdxDialog>
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

.clickable-card {
	cursor: pointer;
}
.clickable-card:focus {
	outline: 2px solid #4f46e5; /* indigo-600 */
	outline-offset: 2px;
}
:deep(.cdx-card__text) {
  width: 100%;
}
</style>
