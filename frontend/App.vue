<script setup lang="ts">
import { ref } from "vue";
import WikibaseList from "./components/WikibaseList.vue";
import AddWikibaseDialog from "./components/AddWikibaseDialog.vue";

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
				class="mx-auto max-w-screen-2xl flex flex-wrap md:flex-nowrap items-center justify-center md:justify-between gap-4 px-6 py-4"
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
							An initiative by Wikimedia Deutschland to map the self-hosted
							Wikibase ecosystem.
						</p>
						<p class="text-sm token-text-subtle">
							Find even more Wikibase instances on
							<a
								href="https://www.wikibase.cloud/discovery"
								target="_blank"
								rel="noopener noreferrer"
								aria-label="Wikibase Cloud"
								>Wikibase Cloud</a
							>.
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
							title="Source code on GitHub"
							class="p-2 token-rounded-pill token-text-base token-hover-surface-3 focus-outline-progressive"
						>
							<img src="/github.svg" class="min-w-6 w-6" alt="Github logo" />
						</a>
						<a
							:href="endpoint"
							target="_blank"
							rel=""
							aria-label="GraphQL"
							title="GraphQL API access"
							class="p-2 token-rounded-pill token-text-base token-hover-surface-3 focus-outline-progressive"
						>
							<img src="/graphql.svg" class="min-w-6 w-6" alt="GraphQL logo" />
						</a>
					</div>
					<AddWikibaseDialog :endpoint="endpoint" @added="handleAdded" />
				</div>
			</div>
		</header>
		<main class="px-6 md:px-8 py-6 flex-1">
			<div class="mx-auto max-w-screen-2xl">
				<WikibaseList :key="refreshKey" :endpoint="endpoint" class="mt-2" />
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
