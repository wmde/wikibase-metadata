<script setup lang="ts">
import { onMounted, ref, computed } from "vue";
import { CdxProgressBar, CdxButton, CdxIcon } from "@wikimedia/codex";
import {
	cdxIconRecentChanges,
	cdxIconDatabase,
	cdxIconArrowUp,
	cdxIconArrowDown,
} from "@wikimedia/codex-icons";
import WikibaseCard from "./WikibaseCard.vue";
import { Wikibase } from "../types";

// Receive endpoint from App
const props = defineProps<{ endpoint: string }>();

const loading = ref(false);
const error = ref<string | null>(null);
const items = ref<Wikibase[]>([]);
type SortKey = "edits" | "triples";
const sortKey = ref<SortKey>("edits");
const sortDir = ref<"asc" | "desc">("desc");

// Single request (large page size)
const PAGE_SIZE = 10000;

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

function buildSingleQuery(pageSize: number) {
	// Always exclude TEST and CLOUD instances
	return `
    query q {
      wikibaseList(pageNumber: 1, pageSize: ${pageSize}, wikibaseFilter: { wikibaseType: { exclude: [TEST, CLOUD] } }) {
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

async function load() {
	loading.value = true;
	error.value = null;
	items.value = [];

	try {
		const res = await fetch(props.endpoint, {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({ query: buildSingleQuery(PAGE_SIZE) }),
			credentials: "omit",
		});
		if (!res.ok) throw new Error(`HTTP ${res.status}`);
		const json = await res.json();
		if (json.errors) {
			throw new Error(json.errors?.[0]?.message || "GraphQL error");
		}
		const data = (json?.data?.wikibaseList?.data ?? []) as any[];
		items.value = data.map((d: any) => Wikibase.from(d));
	} catch (e: any) {
		error.value = e?.message || String(e);
	} finally {
		loading.value = false;
	}
}

onMounted(() => {
	load();
});
</script>

<template>
	<section>
		<div v-if="loading" class="py-6">
			<p class="mb-1 text-xs text-center token-text-subtle">
				Loading known Wikibase instances…
			</p>
			<CdxProgressBar aria-label="Loading known Wikibase instances" />
		</div>
		<div v-else-if="error" class="token-text-destructive">{{ error }}</div>
		<div v-else>
			<div class="mb-3 flex items-center justify-end gap-8">
				<div class="flex items-center gap-2">
					<div class="hidden md:block">Sort by</div>
					<div class="flex items-center">
						<template v-for="def in sortDefs" :key="def.key">
							<CdxButton
								weight="quiet"
								type="button"
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
										:icon="
											sortDir === 'asc' ? cdxIconArrowUp : cdxIconArrowDown
										"
										size="small"
										style="margin-left: var(--spacing-25)"
									/>
								</span>
							</CdxButton>
						</template>
					</div>
				</div>
			</div>
			<div
				class="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4"
			>
				<WikibaseCard v-for="w in sortedItems" :key="w.id" :w="w" />
			</div>
		</div>
	</section>
</template>

<style scoped></style>
