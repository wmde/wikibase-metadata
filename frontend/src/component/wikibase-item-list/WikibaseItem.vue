<script setup lang="ts">
import { type WbItemFragment } from '@/graphql/types'
import getActionApiUrl from '@/util/getActionApiUrl'

defineProps<{ wiki: WbItemFragment }>()
</script>

<template>
	<div class="wikibase-item">
		<h4>({{ wiki.id }}) {{ wiki.title }}</h4>
		<p>
			<a :href="getActionApiUrl(wiki.urls.baseUrl, wiki.urls.scriptPath) ?? undefined">
				Action API
			</a>
		</p>
	</div>
</template>

<style lang="css"></style>
