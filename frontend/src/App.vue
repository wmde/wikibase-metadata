<script setup lang="ts">
import AppHeader from '@/component/AppHeader.vue'
import WikibaseTableContainer from '@/component/WikibaseTableContainer.vue'
import routes from '@/routes'
import { computed, ref } from 'vue'

const currentPath = ref(window.location.pathname)
window.addEventListener('hashchange', () => (currentPath.value = window.location.pathname))

const currentView = computed(() => routes[currentPath.value || '/'] || WikibaseTableContainer)
</script>

<template>
	<v-container class="pa-0 suite-scraper-app">
		<AppHeader />
		<component :is="currentView" />
	</v-container>
</template>
