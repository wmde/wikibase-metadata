<script setup lang="ts">
import AppFooter from '@/component/AppFooter.vue'
import AppHeader from '@/component/AppHeader.vue'
import WikibaseTableContainer from '@/component/WikibaseTableContainer.vue'
import routes, { currentPath } from '@/routes'
import { computed } from 'vue'

const currentView = computed(
	() => routes[currentPath.value || '/']?.component || WikibaseTableContainer
)
</script>

<template>
	<v-container class="pa-0 suite-scraper-app">
		<AppHeader />
		<component :is="currentView" />
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
