<script setup lang="ts">
import { onMounted, ref, watch } from "vue";
import { CdxProgressBar } from "@wikimedia/codex";
import WikibaseCard from "./WikibaseCard.vue";
import { Wikibase } from "../types";

// Receive token from App
const props = defineProps<{ token: string | null }>();

const loading = ref(false);
const error = ref<string | null>(null);
const items = ref<Wikibase[]>([]);

const endpoint = import.meta.env.DEV
	? "http://localhost:8000/graphql"
	: "/graphql";

const query = `
  query q {
    wikibaseList(pageNumber: 1, pageSize: 1000000, wikibaseFilter: { wikibaseType: { exclude: [TEST, CLOUD] } }) {
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

async function load() {
	if (!props.token) return;
	loading.value = true;
	error.value = null;
	try {
		const res = await fetch(endpoint, {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				authorization: `bearer ${props.token}`,
			},
			body: JSON.stringify({ query }),
			credentials: "omit",
		});
		if (!res.ok) throw new Error(`HTTP ${res.status}`);
		const json = await res.json();
		if (json.errors) {
			throw new Error(json.errors?.[0]?.message || "GraphQL error");
		}
		const data = (json?.data?.wikibaseList?.data ?? []) as any[];
		items.value = data.map((d) => Wikibase.from(d));
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

</script>

<template>
	<section>
		<div v-if="loading" class="py-6">
			<p class="mb-3 text-sm text-center token-text-base">
				Loading known Wikibase instances — this can take a while.
			</p>
			<CdxProgressBar aria-label="Loading known Wikibase instances" />
		</div>
		<div v-else-if="error" class="token-text-destructive">{{ error }}</div>
		<div v-else>
			<div
				class="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4"
			>
				<WikibaseCard v-for="w in items" :key="w.id" :w="w" />
			</div>
		</div>
	</section>
</template>

<style scoped></style>
