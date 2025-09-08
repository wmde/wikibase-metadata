<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { CdxField, CdxTextInput, CdxButton } from "@wikimedia/codex";
import WikibaseList from "./components/WikibaseList.vue";
import AddWikibaseDialog from "./components/AddWikibaseDialog.vue";

// Token handling in App
const token = ref<string | null>(null);
const tokenInput = ref("");
const tokenTouched = ref(false);
const fieldStatus = computed(() =>
	tokenTouched.value && tokenInput.value.trim().length === 0
		? "error"
		: "default",
);
const messages = { error: "Token is required" } as const;

onMounted(() => {
	const saved = localStorage.getItem("authToken");
	if (saved) token.value = saved;
});

function submitToken() {
	tokenTouched.value = true;
	const t = tokenInput.value.trim();
	if (!t) return;
	token.value = t;
	localStorage.setItem("authToken", t);
}

// GraphQL endpoint used by dialog
const endpoint = import.meta.env.DEV
	? "http://localhost:8000/graphql"
	: "/graphql";

// Trigger list refresh after adding
const refreshKey = ref(0);
function handleAdded() {
	refreshKey.value++;
}
</script>

<template>
	<div class="min-h-screen flex flex-col">
		<header class="token-border-b token-surface-2">
			<div
				class="mx-auto max-w-screen-2xl flex items-center justify-between gap-4 px-6 py-4"
			>
				<div class="flex items-center gap-3">
					<img
						src="/wikibase-black.svg"
						class="h-16 w-auto"
						alt="Wikibase logo"
					/>
					<div>
						<h1 class="text-xl md:text-2xl font-semibold">Wikibase Metadata</h1>
						<p class="text-sm token-text-subtle">
							An initiative by Wikimedia Deutschland to map the Wikibase
							ecosystem
						</p>
					</div>
				</div>
				<div class="flex items-center gap-4">
					<div class="flex gap-2">
						<a
							href="https://github.com/wmde/wikibase-metadata"
							target="_blank"
							rel="noopener noreferrer"
							aria-label="GitHub"
							title="find the project on github"
							class="p-2 token-rounded-pill token-text-base token-hover-surface-3 focus-outline-progressive"
						>
							<img src="/github.svg" class="h-6 w-auto" alt="Github logo" />
						</a>
						<a
							href="/graphql"
							target="_blank"
							rel=""
							aria-label="GraphQL"
							title="query the database via graphql api"
							class="p-2 token-rounded-pill token-text-base token-hover-surface-3 focus-outline-progressive"
						>
							<img src="/graphql.svg" class="h-6 w-auto" alt="GraphQL logo" />
						</a>
					</div>
					<AddWikibaseDialog
						:endpoint="endpoint"
						:token="token"
						@added="handleAdded"
					/>
				</div>
			</div>
		</header>
		<main class="px-6 md:px-8 py-6 flex-1">
			<div class="mx-auto max-w-screen-2xl">
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
							<template #description>
								Stored locally and used for API requests.
							</template>
						</CdxField>
						<div class="mt-3 flex justify-center">
							<CdxButton
								action="progressive"
								weight="primary"
								@click="submitToken"
								>Continue</CdxButton
							>
						</div>
					</form>
				</div>
				<div v-else>
					<WikibaseList :key="refreshKey" :token="token" class="mt-2" />
				</div>
			</div>
		</main>
		<footer class="token-border-t token-surface-2">
			<div
				class="mx-auto max-w-screen-2xl px-6 py-6 flex items-center justify-center gap-3"
			>
				<a
					href="https://www.wikimedia.de/"
					target="_blank"
					rel="noopener noreferrer"
					class="flex flex-col items-center gap-3 token-text-base focus-outline-progressive"
					title="Wikimedia Deutschland"
				>
					<img
						src="/wmde.svg"
						alt="Wikimedia Deutschland"
						class="h-24 w-auto"
					/>
				</a>
			</div>
		</footer>
	</div>
</template>

<style scoped></style>
