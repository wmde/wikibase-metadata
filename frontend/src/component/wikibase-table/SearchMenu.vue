<script setup lang="ts">
import { mdiCheck } from '@mdi/js'

defineProps<{
	menuValue: 'instances' | 'items'
	setMenuValue: (v: 'instances' | 'items') => void
}>()
</script>

<template>
	<v-list>
		<v-list-item
			key="instances"
			value="instances"
			v-on:click="() => setMenuValue('instances')"
			:append-icon="menuValue == 'instances' ? mdiCheck : undefined"
		>
			<v-list-item-title>Instances</v-list-item-title>
		</v-list-item>
		<v-list-item
			key="items"
			value="items"
			v-on:click="() => setMenuValue('items')"
			:append-icon="menuValue == 'items' ? mdiCheck : undefined"
		>
			<v-list-item-title>Items</v-list-item-title>
		</v-list-item>
	</v-list>
</template>

<style lang="scss"></style>
