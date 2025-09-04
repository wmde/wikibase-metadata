<script setup lang="ts">
import { onMounted, ref, computed } from "vue";
import {
	CdxProgressBar,
	CdxField,
	CdxTextInput,
	CdxButton,
} from "@wikimedia/codex";
import WikibaseCard from "./WikibaseCard.vue";
import { Wikibase } from "../types";

// Using shared Wikibase type

const loading = ref(false);
const error = ref<string | null>(null);
const items = ref<Wikibase[]>([]);
const token = ref<string | null>(null);
const tokenInput = ref("");
const tokenTouched = ref(false);
const fieldStatus = computed(() =>
	tokenTouched.value && tokenInput.value.trim().length === 0
		? "error"
		: "default",
);
const messages = { error: "Token is required" } as const;

const endpoint = import.meta.env.DEV
	? "http://localhost:8000/graphql"
	: "/graphql";

const query = `query q {\n  wikibaseList(pageNumber: 1, pageSize: 1000000, wikibaseFilter: { wikibaseType: { exclude: [TEST, CLOUD] } }) {\n    data {\n      id\n      urls {\n        baseUrl\n      }\n      description\n      wikibaseType\n      quantityObservations {\n        mostRecent {\n          observationDate\n          totalItems\n          totalProperties\n          totalLexemes\n          totalTriples\n        }\n      }\n      recentChangesObservations {\n        mostRecent {\n          observationDate\n          humanChangeCount\n          humanChangeUserCount\n          botChangeCount\n          botChangeUserCount\n        }\n      }\n      timeToFirstValueObservations {\n        mostRecent {\n          initiationDate\n        }\n      }\n    }\n  }\n}`;

async function load() {
	if (!token.value) return;
	loading.value = true;
	error.value = null;
	try {
		const res = await fetch(endpoint, {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				authorization: `bearer ${token.value}`,
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
	const saved = localStorage.getItem("authToken");
	if (saved) {
		token.value = saved;
		load();
	}
});

function submitToken() {
	tokenTouched.value = true;
	const t = tokenInput.value.trim();
	if (!t) return;
	token.value = t;
	localStorage.setItem("authToken", t);
	load();
}

// Card-specific helpers moved into WikibaseCard.vue
</script>

<template>
	<section>
		<div v-if="!token" class="py-12 flex justify-center">
			<form class="w-full max-w-md" @submit.prevent="submitToken">
				<CdxField :status="fieldStatus" :messages="messages">
					<CdxTextInput
						v-model="tokenInput"
						type="password"
						placeholder="Enter bearer token"
						@keydown.enter.prevent="submitToken"
					/>
					<template #label>Bearer token</template>
					<template #description
						>Stored locally and used for API requests.</template
					>
				</CdxField>
				<div class="mt-3 flex justify-center">
					<CdxButton action="progressive" weight="primary" @click="submitToken"
						>Continue</CdxButton
					>
				</div>
			</form>
		</div>
		<div v-else-if="loading" class="py-6">
			<p class="mb-3 text-sm text-black">
				Loading known Wikibase instances — this can take a while.
			</p>
			<CdxProgressBar aria-label="Loading known Wikibase instances" />
		</div>
		<div v-else-if="error" class="text-red-600">{{ error }}</div>
		<div v-else>
			<p class="mb-3 text-sm text-black">
				Found
				<span class="font-semibold">{{ items.length }}</span> wikibases
			</p>
			<div
				class="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4"
			>
				<WikibaseCard v-for="w in items" :key="w.id" :w="w" />
			</div>
		</div>
	</section>
</template>

<style scoped></style>
