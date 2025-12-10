<script setup lang="ts">
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
	</v-container>
</template>
