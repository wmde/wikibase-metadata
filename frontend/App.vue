<script setup lang="ts">
import WikibaseList from "./components/WikibaseList.vue";
</script>

<template>
	<!-- keeping this as image examples -->
	<!--     <img src="/vite.svg" class="logo" alt="Vite logo" /> -->
	<!--     <img src="./assets/vue.svg" class="logo vue" alt="Vue logo" /> -->
	<div class="p-8">
		<div class="mx-auto max-w-5xl">
      <h1 class="pb-4 text-2xl font-bold">Wikibase Metadata</h1>
			<WikibaseList />
		</div>
	</div>
</template>

<style scoped>
.logo {
	height: 6em;
	padding: 1.5em;
	will-change: filter;
	transition: filter 300ms;
}
.logo:hover {
	filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
	filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
