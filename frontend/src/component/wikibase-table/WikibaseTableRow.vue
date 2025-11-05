<script setup lang="ts">
import LocaleNumber from '@/component/LocaleNumber.vue'
import WikibaseDetailCardContainer from '@/component/wikibase-table/wikibase-detail-card/WikibaseDetailCardContainer.vue'
import WikibaseTypeChip from '@/component/wikibase-table/WikibaseTypeChip.vue'
import type { WbFragment } from '@/graphql/types'
import computeTotalEdits from '@/util/compute-total-edits'

defineProps<{ wikibase: WbFragment; index: number }>()
</script>

<template>
	<tr>
		<td>{{ index + 1 }}</td>
		<td>
			<WikibaseTypeChip :wikibase-type="wikibase.wikibaseType" />
		</td>
		<td>
			<a :href="wikibase.urls.baseUrl">{{ wikibase.title }}</a>
		</td>
		<td>
			<LocaleNumber :stat="wikibase.quantityObservations.mostRecent?.totalTriples" />
		</td>
		<td>
			<LocaleNumber :stat="computeTotalEdits(wikibase.recentChangesObservations)" />
		</td>
		<td>{{ wikibase.category ?? '–' }}</td>
		<td>
			<div class="overflow">{{ wikibase.description ?? '–' }}</div>
		</td>
		<td>
			<WikibaseDetailCardContainer :wikibase-id="Number.parseInt(wikibase.id)" />
		</td>
	</tr>
</template>

<style lang="css">
.wikibase-type-chip {
	min-width: 40px;
}
.overflow {
	max-height: 4em;
	overflow-y: scroll;
}
</style>
