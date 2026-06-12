<script setup lang="ts">
import AppHeader from '@/component/AppHeader.vue'
import WikibaseTableContainer from '@/component/WikibaseTableContainer.vue'
import AppFooter from '@/component/AppFooter.vue'
</script>

<template>
	<v-container class="pa-0 ma-0 suite-scraper-app">
		<AppHeader />
		<WikibaseTableContainer />
		<AppFooter />
	</v-container>
</template>

<style lang="css">
.suite-scraper-app {
	background-color: oklch(98.5% 0.002 247.839);
	max-width: 100%;
	width: 100%;
}
</style>
