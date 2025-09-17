<script setup lang="ts">
import { computed } from "vue";
import { CdxDialog, CdxIcon } from "@wikimedia/codex";
import { cdxIconAlert } from "@wikimedia/codex-icons";
import type { Wikibase, ObsKind } from "../types";
import { isStaleFor, obsHeadline } from "../utils";
import { fmtOrDash, textOrDash } from "../utils";

const props = defineProps<{ w: Wikibase; open: boolean }>();
const emit = defineEmits<{ (e: "update:open", v: boolean): void }>();

/* ---------- helpers (dialog) ---------- */
function isStale(kind: ObsKind): boolean {
	return isStaleFor(props.w, kind);
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
function obsHeadlineLocal(kind: ObsKind): string {
	return obsHeadline(props.w, kind);
}
function fmtOrDashLocal(n?: number | null): string {
	return fmtOrDash(props.w, n);
}
</script>

<template>
	<CdxDialog
		:open="props.open"
		@update:open="(v: boolean) => emit('update:open', v)"
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
							<template v-if="props.w.resolveUrl(props.w.urls?.baseUrl)">
								<a
									:href="props.w.resolveUrl(props.w.urls?.baseUrl) as string"
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
						<dt class="text-[11px] uppercase token-text-subtle">
							SPARQL Endpoint
						</dt>
						<dd class="text-sm token-text-base break-all">
							<template
								v-if="props.w.resolveUrl(props.w.urls?.sparqlEndpointUrl)"
							>
								<a
									:href="
										props.w.resolveUrl(
											props.w.urls?.sparqlEndpointUrl,
										) as string
									"
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
						<dt class="text-[11px] uppercase token-text-subtle">
							SPARQL Frontend
						</dt>
						<dd class="text-sm token-text-base break-all">
							<template
								v-if="props.w.resolveUrl(props.w.urls?.sparqlFrontendUrl)"
							>
								<a
									:href="
										props.w.resolveUrl(
											props.w.urls?.sparqlFrontendUrl,
										) as string
									"
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
							<dt class="text-[11px] uppercase token-text-subtle">
								Script Path
							</dt>
							<dd class="text-sm token-text-base break-all">
								{{ textOrDash(props.w.urls?.scriptPath) }}
							</dd>
						</div>
						<div class="token-rounded token-surface-2 p-3">
							<dt class="text-[11px] uppercase token-text-subtle">
								Article Path
							</dt>
							<dd class="text-sm token-text-base break-all">
								{{ textOrDash(props.w.urls?.articlePath) }}
							</dd>
						</div>
					</div>
				</dl>
			</section>

			<section>
				<header class="mb-2">
					<p
						class="text-xs font-semibold uppercase tracking-wide token-text-base"
					>
						Totals
					</p>
					<p class="inline-flex items-center gap-1 text-xs token-text-base">
						{{ obsHeadlineLocal("quantity") }}
						<CdxIcon
							v-if="isStale('quantity')"
							:icon="cdxIconAlert"
							size="small"
							class="token-text-warning"
						/>
					</p>
				</header>
				<dl class="grid grid-cols-2 gap-3">
					<template v-for="t in totals" :key="t.label">
						<div class="token-rounded token-surface-2 p-3">
							<dt class="text-[11px] uppercase token-text-subtle">
								{{ t.label }}
							</dt>
							<dd class="text-xl font-bold token-text-base">
								{{ fmtOrDashLocal(t.v) }}
							</dd>
						</div>
					</template>
				</dl>
			</section>

			<section>
				<header class="mb-2">
					<p
						class="text-xs font-semibold uppercase tracking-wide token-text-base"
					>
						Edits in the last 30 days
					</p>
					<p class="inline-flex items-center gap-1 text-xs token-text-base">
						{{ obsHeadlineLocal("rc") }}
						<CdxIcon
							v-if="isStale('rc')"
							:icon="cdxIconAlert"
							size="small"
							class="token-text-warning"
						/>
					</p>
				</header>
				<dl class="grid grid-cols-2 gap-3">
					<template v-for="t in rc" :key="t.label">
						<div class="token-rounded token-surface-2 p-3">
							<dt class="text-[11px] uppercase token-text-subtle">
								{{ t.label }}
							</dt>
							<dd class="text-xl font-bold token-text-base">
								{{ fmtOrDashLocal(t.v) }}
							</dd>
						</div>
					</template>
				</dl>
			</section>

			<section>
				<p
					v-if="
						props.w.timeToFirstValueObservations?.mostRecent?.initiationDate
					"
					class="text-xs token-text-base"
				>
					Online since
					{{
						props.w.fmtDate(
							props.w.timeToFirstValueObservations?.mostRecent?.initiationDate,
						)
					}}
				</p>
			</section>
		</div>
	</CdxDialog>
</template>

<style scoped></style>
