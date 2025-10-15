<script setup lang="ts">
import LocaleNumber from '@/component/LocaleNumber.vue';
import type { WbFragment } from '@/graphql/types';
import computeTotalEdits from '@/util/computeTotalEdits';

defineProps<{ wikibase: WbFragment }>()

</script>

<template>
	<tr>
		<td>
			{{ wikibase.wikibaseType }}
		</td>
		<td>
			{{ wikibase.title }}
		</td>
		<td>
			{{ wikibase.urls.baseUrl }}
		</td>
		<td>
			<LocaleNumber :stat="wikibase.quantityObservations.mostRecent?.totalTriples" />
		</td>
		<td>
			<LocaleNumber :stat="computeTotalEdits(wikibase.recentChangesObservations)" />
		</td>
	</tr>
</template>

<style lang="css"></style>
