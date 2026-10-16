<script setup lang="ts">
import { useSearchStore } from '@/stores/search-store'
import { mdiCheck } from '@mdi/js'
import { computed } from 'vue'

const searchStore = useSearchStore()
const menuValue = computed(() => searchStore.menuValue)
</script>

<template>
	<v-list>
		<v-list-item
			key="instances"
			value="instances"
			v-on:click="() => searchStore.setMenuValue('instances')"
			:append-icon="menuValue == 'instances' ? mdiCheck : undefined"
		>
			<v-list-item-title>Instances</v-list-item-title>
		</v-list-item>
		<v-list-item
			key="items"
			value="items"
			v-on:click="() => searchStore.setMenuValue('items')"
			:append-icon="menuValue == 'items' ? mdiCheck : undefined"
		>
			<v-list-item-title>Items</v-list-item-title>
		</v-list-item>
	</v-list>
</template>

<style lang="scss"></style>
