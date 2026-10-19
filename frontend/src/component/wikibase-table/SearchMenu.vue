<script setup lang="ts">
import { useMenuStore } from '@/stores/menu-store'
import { mdiCheck } from '@mdi/js'
import { computed } from 'vue'

const menuStore = useMenuStore()
const menuValue = computed(() => menuStore.value)
</script>

<template>
	<v-list>
		<v-list-item
			key="instances"
			value="instances"
			v-on:click="() => menuStore.setValue('instances')"
			:append-icon="menuValue == 'instances' ? mdiCheck : undefined"
		>
			<v-list-item-title>Instances</v-list-item-title>
		</v-list-item>
		<v-list-item
			key="items"
			value="items"
			v-on:click="() => menuStore.setValue('items')"
			:append-icon="menuValue == 'items' ? mdiCheck : undefined"
		>
			<v-list-item-title>Items</v-list-item-title>
		</v-list-item>
	</v-list>
</template>

<style lang="scss"></style>
