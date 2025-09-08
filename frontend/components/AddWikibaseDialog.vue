<script setup lang="ts">
import { ref, computed, watch } from "vue";
import {
	CdxDialog,
	CdxField,
	CdxTextInput,
	CdxButton,
	CdxTextArea,
} from "@wikimedia/codex";

const props = defineProps<{
	endpoint: string;
	token: string | null;
}>();

const emit = defineEmits<{ (e: "added", id: string): void }>();

const open = ref(false);
const loading = ref(false);
const error = ref<string | null>(null);

// Form fields
const name = ref("");
const baseUrl = ref("");
const description = ref("");
const articlePath = ref("");
const scriptPath = ref("");
const sparqlFrontendUrl = ref("");
const sparqlEndpointUrl = ref("");

// Validation
const touched = ref({ name: false, baseUrl: false });
const nameStatus = computed(() =>
	touched.value.name && !name.value.trim() ? "error" : "default",
);
const baseUrlStatus = computed(() =>
	touched.value.baseUrl && !baseUrl.value.trim() ? "error" : "default",
);
const messages = { error: "This field is required" } as const;
const canSubmit = computed(
	() =>
		!!name.value.trim() &&
		!!baseUrl.value.trim() &&
		!loading.value &&
		!!props.token,
);

function reset() {
	name.value = "";
	baseUrl.value = "";
	description.value = "";
	articlePath.value = "";
	scriptPath.value = "";
	sparqlFrontendUrl.value = "";
	sparqlEndpointUrl.value = "";
	touched.value = { name: false, baseUrl: false };
	error.value = null;
}

watch(open, (o) => {
	if (!o) {
		// Clear the form when closing the dialog
		reset();
	}
});

async function submit() {
	touched.value.name = true;
	touched.value.baseUrl = true;
	if (!canSubmit.value) return;
	loading.value = true;
	error.value = null;
	try {
		const urls: Record<string, string> = { baseUrl: baseUrl.value.trim() };
		if (articlePath.value.trim()) urls.articlePath = articlePath.value.trim();
		if (scriptPath.value.trim()) urls.scriptPath = scriptPath.value.trim();
		if (sparqlFrontendUrl.value.trim())
			urls.sparqlFrontendUrl = sparqlFrontendUrl.value.trim();
		if (sparqlEndpointUrl.value.trim())
			urls.sparqlEndpointUrl = sparqlEndpointUrl.value.trim();

		const mutation = `
      mutation AddWikibase($input: WikibaseInput!) {
        addWikibase(wikibaseInput: $input) { id }
      }
    `;
		const variables = {
			input: {
				wikibaseName: name.value.trim(),
				description: description.value.trim(),
				urls,
			},
		};

		const res = await fetch(props.endpoint, {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				...(props.token ? { authorization: `bearer ${props.token}` } : {}),
			},
			body: JSON.stringify({ query: mutation, variables }),
			credentials: "omit",
		});
		if (!res.ok) throw new Error(`HTTP ${res.status}`);
		const json = await res.json();
		if (json.errors)
			throw new Error(json.errors?.[0]?.message || "GraphQL error");
		const id = json?.data?.addWikibase?.id;
		if (!id) throw new Error("No id returned");
		open.value = false;
		emit("added", id);
	} catch (e: any) {
		error.value = e?.message || String(e);
	} finally {
		loading.value = false;
	}
}
</script>

<template>
	<div class="inline-flex">
		<CdxButton
			action="progressive"
			weight="primary"
			@click="open = true"
			:disabled="!token"
		>
			Add my Wikibase
		</CdxButton>

		<CdxDialog
			v-model:open="open"
			title="Add my Wikibase"
			:use-close-button="true"
			:default-action="{ label: 'Close' }"
			:primary-action="{
				label: 'Add',
				actionType: 'progressive',
				disabled: !canSubmit,
			}"
			@default="open = false"
			@primary="submit"
		>
			<div class="pb-4">
				Publicly available data on the Wikibase will be analyzed periodically.
				To remove your instance, contact
				<a href="mailto:wikibase-suite-support@wikimedia.de"
					>wikibase-suite-support@wikimedia.de</a
				>.
			</div>
			<form class="space-y-4" @submit.prevent="submit">
				<CdxField :status="nameStatus" :messages="messages">
					<CdxTextInput
						v-model="name"
						placeholder="Wikibase name"
						:disabled="loading"
						@blur="touched.name = true"
					/>
					<template #label>Name*</template>
					<template #description> The name of your Wikibase </template>
				</CdxField>

				<CdxField :status="baseUrlStatus" :messages="messages">
					<CdxTextInput
						v-model="baseUrl"
						placeholder="https://wikibase.example"
						:disabled="loading"
						@blur="touched.baseUrl = true"
					/>
					<template #label>Base URL*</template>
					<template #description>
						Root URL of your Wikibase site, the base path of MediaWiki
					</template>
				</CdxField>

				<CdxField>
					<CdxTextArea v-model="description" />
					<template #label>Description</template>
					<template #description
						>Shortly describe the dataset your Wikibase is hosting</template
					>
				</CdxField>
				<CdxField>
					<CdxTextInput
						v-model="articlePath"
						placeholder="e.g. /wiki"
						:disabled="loading"
					/>
					<template #label>Article path</template>
					<template #description> Leave empty if unsure </template>
				</CdxField>
				<CdxField>
					<CdxTextInput
						v-model="scriptPath"
						placeholder="e.g. /w"
						:disabled="loading"
					/>
					<template #label>Script path</template>
					<template #description> Leave empty if unsure </template>
				</CdxField>

				<CdxField>
					<CdxTextInput
						v-model="sparqlFrontendUrl"
						placeholder="https://query.wikibase.example"
						:disabled="loading"
					/>
					<template #label>SPARQL frontend URL</template>
					<template #description> URL of the Query Service UI</template>
				</CdxField>

				<CdxField>
					<CdxTextInput
						v-model="sparqlEndpointUrl"
						placeholder="https://query.wikibase.example/sparql"
						:disabled="loading"
					/>
					<template #label>SPARQL endpoint URL</template>
					<template #description> URL of the Query Service API</template>
				</CdxField>

				<p v-if="error" class="text-sm token-text-destructive">{{ error }}</p>
			</form>
		</CdxDialog>
	</div>
</template>

<style scoped></style>
