<script setup lang="ts">
import LocaleNumber from '@/component/LocaleNumber.vue'

defineProps<{ label: string; stat: number | undefined }>()
</script>

<template>
	<v-container class="stat-container pa-0">
		<v-label class="stat-label">{{ label }}</v-label>
		<div class="stat">
			<LocaleNumber :stat="stat" />
		</div>
	</v-container>
</template>

<style lang="css"></style>
