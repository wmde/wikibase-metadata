<script setup lang="ts">
import { onMounted, ref, watch, computed } from "vue";
import {
	CdxProgressBar,
	CdxButton,
	CdxIcon,
	CdxToggleSwitch,
} from "@wikimedia/codex";
import {
	cdxIconRecentChanges,
	cdxIconDatabase,
	cdxIconArrowUp,
	cdxIconArrowDown,
} from "@wikimedia/codex-icons";
import WikibaseCard from "./WikibaseCard.vue";
import { Wikibase } from "../types";

// Receive token and endpoint from App
const props = defineProps<{ token: string | null; endpoint: string }>();

const loading = ref(false);
const error = ref<string | null>(null);
const items = ref<Wikibase[]>([]);
const includeCloud = ref(false);
type SortKey = "edits" | "triples";
const sortKey = ref<SortKey>("edits");
const sortDir = ref<"asc" | "desc">("desc");

// Paged loading state
const totalPages = ref<number | null>(null);
const loadedPages = ref<number>(0);
const PAGE_SIZE = 100;

const sortDefs: Array<{ key: SortKey; label: string; icon: any }> = [
	{
		key: "edits",
		label: "Edits last 30 days",
		icon: cdxIconRecentChanges,
	},
	{
		key: "triples",
		label: "Graph triples",
		icon: cdxIconDatabase,
	},
];

function metricFor(w: Wikibase, key: SortKey): number | null {
	if (key === "edits") {
		const m = w.recentChangesObservations?.mostRecent;
		if (!m) return null;
		const human =
			typeof m.humanChangeCount === "number" ? m.humanChangeCount : 0;
		const bot = typeof m.botChangeCount === "number" ? m.botChangeCount : 0;
		const sum = human + bot;
		return sum > 0 ? sum : (m.humanChangeCount ?? m.botChangeCount ?? null);
	}
	// triples
	return w.quantityObservations?.mostRecent?.totalTriples ?? null;
}

const sortedItems = computed(() => {
	// Always sort when a key is selected (default is edits)
	const dir = sortDir.value;
	const arr = [...items.value];
	arr.sort((a, b) => {
		const av = metricFor(a, sortKey.value);
		const bv = metricFor(b, sortKey.value);
		// Place nulls at the end regardless of direction
		const aNull = av == null;
		const bNull = bv == null;
		if (aNull && bNull) return 0;
		if (aNull) return 1;
		if (bNull) return -1;
		const diff = (av as number) - (bv as number);
		return dir === "asc" ? diff : -diff;
	});
	return arr;
});

function onSortClick(k: SortKey) {
	if (sortKey.value === k) {
		sortDir.value = sortDir.value === "asc" ? "desc" : "asc";
	} else {
		sortKey.value = k;
		sortDir.value = "desc";
	}
}

function buildQuery(pageNumber: number, pageSize: number) {
	const exclude = includeCloud.value ? "TEST" : "TEST, CLOUD";
	return `
    query q {
      wikibaseList(pageNumber: ${pageNumber}, pageSize: ${pageSize}, wikibaseFilter: { wikibaseType: { exclude: [${exclude}] } }) {
        meta { totalPages pageNumber pageSize }
        data {
          id
          urls {
            baseUrl
            sparqlEndpointUrl
            sparqlFrontendUrl
            scriptPath
            articlePath
          }
          description
          wikibaseType
          quantityObservations {
            mostRecent {
              observationDate
              totalItems
              totalProperties
              totalLexemes
              totalTriples
            }
          }
          recentChangesObservations {
            mostRecent {
              observationDate
              humanChangeCount
              humanChangeUserCount
              botChangeCount
              botChangeUserCount
            }
          }
          timeToFirstValueObservations {
            mostRecent {
              initiationDate
            }
          }
        }
      }
    }
  `;
}

function buildMetaQuery(pageSize: number) {
	const exclude = includeCloud.value ? "TEST" : "TEST, CLOUD";
	return `
    query qMeta {
      wikibaseList(pageNumber: 1, pageSize: ${pageSize}, wikibaseFilter: { wikibaseType: { exclude: [${exclude}] } }) {
        meta { totalPages pageNumber pageSize }
      }
    }
  `;
}

async function load() {
	if (!props.token) return;
	loading.value = true;
	error.value = null;
	items.value = [];
	totalPages.value = null;
	loadedPages.value = 0;

	try {
		// Cheap initial request to discover total pages only
		const firstRes = await fetch(props.endpoint, {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				authorization: `bearer ${props.token}`,
			},
			body: JSON.stringify({ query: buildMetaQuery(PAGE_SIZE) }),
			credentials: "omit",
		});
		if (!firstRes.ok) throw new Error(`HTTP ${firstRes.status}`);
		const firstJson = await firstRes.json();
		if (firstJson.errors) {
			throw new Error(firstJson.errors?.[0]?.message || "GraphQL error");
		}
		const firstPageMeta = firstJson?.data?.wikibaseList;
		const total = Number(firstPageMeta?.meta?.totalPages ?? 0) || 0;
		totalPages.value = total;
		// No data fetched yet; start progress at 0
		items.value = [];
		loadedPages.value = 0;

		// Fetch all pages in parallel while updating progress
		if (total > 0) {
			const pageNumbers = Array.from({ length: total }, (_, i) => i + 1);
			const promises = pageNumbers.map(async (page) => {
				const res = await fetch(props.endpoint, {
					method: "POST",
					headers: {
						"Content-Type": "application/json",
						authorization: `bearer ${props.token}`,
					},
					body: JSON.stringify({ query: buildQuery(page, PAGE_SIZE) }),
					credentials: "omit",
				});
				if (!res.ok) throw new Error(`HTTP ${res.status}`);
				const json = await res.json();
				if (json.errors) {
					throw new Error(json.errors?.[0]?.message || "GraphQL error");
				}
				const pageData = (json?.data?.wikibaseList?.data ?? []) as any[];
				// Append items for this page
				items.value.push(...pageData.map((d: any) => Wikibase.from(d)));
				// Increment loaded pages count
				loadedPages.value += 1;
			});
			await Promise.all(promises);
		}
	} catch (e: any) {
		error.value = e?.message || String(e);
	} finally {
		loading.value = false;
	}
}

onMounted(() => {
	if (props.token) load();
});
watch(
	() => props.token,
	(t) => {
		if (t) load();
	},
);

watch(includeCloud, () => {
	load();
});
</script>

<template>
	<section>
		<div class="mb-3 flex items-center justify-end gap-8">
			<div class="flex items-center gap-2 ml-4">
				<CdxToggleSwitch
					v-model="includeCloud"
					aria-label="Include Wikibase Cloud instances"
					:disabled="loading"
				>
					wikibase.cloud
				</CdxToggleSwitch>
			</div>
			<div class="flex items-center gap-2">
				<div class="hidden md:block">Sort by</div>
				<div class="flex items-center">
					<template v-for="def in sortDefs" :key="def.key">
						<CdxButton
							weight="quiet"
							type="button"
							:disabled="loading"
							:class="[
								'token-rounded focus-outline-progressive',
								sortKey === def.key ? 'token-surface-3 token-border-all' : '',
							]"
							:aria-pressed="sortKey === def.key"
							:title="
								def.label +
								(sortKey === def.key
									? sortDir === 'asc'
										? ' (ascending)'
										: ' (descending)'
									: '')
							"
							@click="onSortClick(def.key as SortKey)"
						>
							<span class="inline-flex items-center">
								<CdxIcon :icon="def.icon" />
								<CdxIcon
									v-if="sortKey === def.key"
									:icon="sortDir === 'asc' ? cdxIconArrowUp : cdxIconArrowDown"
									size="small"
									style="margin-left: var(--spacing-25)"
								/>
							</span>
						</CdxButton>
					</template>
				</div>
			</div>
		</div>
		<div v-if="loading" class="py-6">
			<p class="mb-1 text-xs text-center token-text-subtle">
				Loading known Wikibase instances — this can take a while...
				<span
					v-if="totalPages != null"
					class="mb-3 text-xs text-center token-text-subtle"
				>
					{{ ((loadedPages / totalPages) * 100).toFixed(0) }}%
				</span>
			</p>
			<CdxProgressBar aria-label="Loading known Wikibase instances" />
		</div>
		<div v-else-if="error" class="token-text-destructive">{{ error }}</div>
		<div v-else>
			<div
				class="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4"
			>
				<WikibaseCard v-for="w in sortedItems" :key="w.id" :w="w" />
			</div>
		</div>
	</section>
</template>

<style scoped></style>
