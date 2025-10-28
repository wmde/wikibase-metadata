<script setup lang="ts">
import LocaleDate from '@/component/LocaleDate.vue'

defineProps<{ label: string; stat: Date | string | null | undefined }>()
</script>

<template>
	<v-container class="stat-container pa-0">
		<v-label class="stat-label">{{ label }}</v-label>
		<div class="stat">
			<LocaleDate :stat="stat" />
		</div>
	</v-container>
</template>

<style lang="css"></style>
