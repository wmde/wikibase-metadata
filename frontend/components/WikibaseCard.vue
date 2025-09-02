<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { CdxCard, CdxIcon } from "@wikimedia/codex";
import { cdxIconGlobe, cdxIconAlert } from "@wikimedia/codex-icons";
import { Wikibase } from "../types";
import type { ObsKind } from "../types";

const props = defineProps<{ w: Wikibase }>();

const showTotals = computed(() => props.w.hasQuantity());
const showRc = computed(() => props.w.hasRecentChanges());
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

function relativeDaysText(dateIso?: string): string {
	if (!dateIso) return "";
	const t = new Date(dateIso).getTime();
	if (Number.isNaN(t)) return "";
	const diffDays = Math.max(
		0,
		Math.floor((Date.now() - t) / (1000 * 60 * 60 * 24)),
	);
	if (diffDays === 0) return "today";
	if (diffDays === 1) return "yesterday";
	return `${diffDays} days ago`;
}

function obsHeadlineSuffix(kind: ObsKind): string {
	const d = props.w.getObservationDate(kind);
	if (!d) return "";
	// const dateStr = props.w.fmtDate(d);
	const rel = relativeDaysText(d);
	return `Fetched ${rel}`;
}

function daysSince(dateIso?: string): number | null {
	if (!dateIso) return null;
	const t = new Date(dateIso).getTime();
	if (Number.isNaN(t)) return null;
	return Math.max(0, Math.floor((Date.now() - t) / (1000 * 60 * 60 * 24)));
}

function isStale(kind: ObsKind): boolean {
	const d = props.w.getObservationDate(kind);
	const days = daysSince(d);
	return days != null && days > 30;
}
</script>

<template>
	<CdxCard class="flex h-full flex-col">
		<template #title>
			<div class="flex items-center gap-3">
				<img
					v-if="faviconReady"
					:src="faviconUrl"
					alt=""
					class="h-5 w-5 rounded"
				/>
				<CdxIcon v-else :icon="cdxIconGlobe" size="medium" />
				<a
					:href="props.w.urls?.baseUrl"
					target="_blank"
					rel="noreferrer noopener"
					class="text-lg font-semibold text-indigo-600 underline hover:text-indigo-500"
				>
					{{ props.w.baseHost() || "Unknown" }}
				</a>
			</div>
		</template>
		<template #description>
			<div class="space-y-1">
				<p
					v-if="
						props.w.timeToFirstValueObservations?.mostRecent?.initiationDate
					"
					class="text-xs text-black"
				>
					Online since
					{{
						props.w.fmtDate(
							props.w.timeToFirstValueObservations?.mostRecent?.initiationDate,
						)
					}}
				</p>
				<p v-if="props.w.description" class="text-sm text-black">
					{{ props.w.description }}
				</p>
			</div>
		</template>
		<template #supporting-text>
			<div class="mt-3 flex flex-col gap-4">
				<div v-if="showTotals" class="border-t border-gray-200 pt-3">
					<p class="text-xs font-semibold uppercase tracking-wide text-black">
						Totals
					</p>
					<div class="mb-2 inline-flex items-center gap-1 text-xs text-black">
						<CdxIcon
							v-if="isStale('quantity')"
							:icon="cdxIconAlert"
							size="small"
						/>
						{{ obsHeadlineSuffix("quantity") }}
					</div>
					<div class="grid grid-cols-2 gap-3">
						<div v-if="props.w.quantityObservations?.mostRecent?.totalItems">
							<div class="text-xs uppercase">Items</div>
							<div class="text-xl font-bold">
								{{
									props.w.fmt(
										props.w.quantityObservations?.mostRecent?.totalItems,
									)
								}}
							</div>
						</div>
						<div
							v-if="props.w.quantityObservations?.mostRecent?.totalProperties"
						>
							<div class="text-xs uppercase">Properties</div>
							<div class="text-xl font-bold">
								{{
									props.w.fmt(
										props.w.quantityObservations?.mostRecent?.totalProperties,
									)
								}}
							</div>
						</div>
						<div v-if="props.w.quantityObservations?.mostRecent?.totalLexemes">
							<div class="text-xs uppercase">Lexemes</div>
							<div class="text-xl font-bold">
								{{
									props.w.fmt(
										props.w.quantityObservations?.mostRecent?.totalLexemes,
									)
								}}
							</div>
						</div>
						<div v-if="props.w.quantityObservations?.mostRecent?.totalTriples">
							<div class="text-xs uppercase">Triples</div>
							<div class="text-xl font-bold">
								{{
									props.w.fmt(
										props.w.quantityObservations?.mostRecent?.totalTriples,
									)
								}}
							</div>
						</div>
					</div>
				</div>

				<div v-if="showRc" class="border-t border-gray-200 pt-3">
					<p class="text-xs font-semibold uppercase tracking-wide text-black">
						Changes in the last 30 days
					</p>
					<p class="mb-2 inline-flex items-center gap-1 text-xs text-black">
						<CdxIcon v-if="isStale('rc')" :icon="cdxIconAlert" size="small" />
						{{ obsHeadlineSuffix("rc") }}
					</p>
					<div class="grid grid-cols-2 gap-3">
						<div
							v-if="
								props.w.recentChangesObservations?.mostRecent?.humanChangeCount
							"
						>
							<div class="text-xs uppercase">Human changes</div>
							<div class="text-xl font-bold">
								{{
									props.w.fmt(
										props.w.recentChangesObservations?.mostRecent
											?.humanChangeCount,
									)
								}}
							</div>
						</div>
						<div
							v-if="
								props.w.recentChangesObservations?.mostRecent
									?.humanChangeUserCount
							"
						>
							<div class="text-xs uppercase">Human users</div>
							<div class="text-xl font-bold">
								{{
									props.w.fmt(
										props.w.recentChangesObservations?.mostRecent
											?.humanChangeUserCount,
									)
								}}
							</div>
						</div>
						<div
							v-if="
								props.w.recentChangesObservations?.mostRecent?.botChangeCount
							"
						>
							<div class="text-xs uppercase">Bot changes</div>
							<div class="text-xl font-bold">
								{{
									props.w.fmt(
										props.w.recentChangesObservations?.mostRecent
											?.botChangeCount,
									)
								}}
							</div>
						</div>
						<div
							v-if="
								props.w.recentChangesObservations?.mostRecent
									?.botChangeUserCount
							"
						>
							<div class="text-xs uppercase">Bot users</div>
							<div class="text-xl font-bold">
								{{
									props.w.fmt(
										props.w.recentChangesObservations?.mostRecent
											?.botChangeUserCount,
									)
								}}
							</div>
						</div>
					</div>
				</div>
			</div>
		</template>
	</CdxCard>
</template>

<style scoped></style>
