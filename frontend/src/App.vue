<script setup lang="ts">
import AppHeader from '@/component/AppHeader.vue'
</script>

<template>
	<v-container class="pa-0 suite-scraper-app">
		<AppHeader />
		<router-view />
	</v-container>
</template>
