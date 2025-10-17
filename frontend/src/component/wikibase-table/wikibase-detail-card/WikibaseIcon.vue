<script setup lang="ts">
import { computed, onBeforeMount, ref } from 'vue'

const props = defineProps<{ baseUrl: string }>()
const faviconUrl = computed(() => new URL('/favicon.ico', props.baseUrl).toString())

const image = new Image()
const loaded = ref(false)
const error = ref(false)

image.onload = () => {
	loaded.value = true
	error.value = false
}
image.onerror = () => (error.value = true)

onBeforeMount(() => (image.src = faviconUrl.value))
</script>

<template>
	<v-img v-if="loaded && !error" class="wikibase-icon" :src="image.src" />
</template>

<style lang="css">
.wikibase-icon {
	max-width: 20px;
	max-height: 20px;
}
</style>
