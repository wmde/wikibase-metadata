<script setup lang="ts">
import LocaleNumber from '@/component/LocaleNumber.vue'
import WikibaseDetailCardContainer from '@/component/wikibase-table/wikibase-detail-card/WikibaseDetailCardContainer.vue'
import WikibaseCategoryChip from '@/component/wikibase-table/WikibaseCategoryChip.vue'
import type { WbFragment } from '@/graphql/types'
import computeTotalEdits from '@/util/compute-total-edits'

defineProps<{ wikibase: WbFragment; index: number }>()
</script>

<template>
	<tr>
		<td class="wikibase-table-cell">
			<a :href="wikibase.urls.baseUrl" class="wikibase-title-link">{{ wikibase.title }}</a>
		</td>
		<td class="wikibase-table-cell">
			<LocaleNumber :stat="wikibase.quantityObservations.mostRecent?.totalTriples" />
		</td>
		<td class="wikibase-table-cell">
			<LocaleNumber :stat="computeTotalEdits(wikibase.recentChangesObservations)" />
		</td>
		<td>
			<WikibaseCategoryChip :category="wikibase.category" />
		</td>
		<td class="wikibase-table-cell">
			{{ wikibase.description ?? '–' }}
		</td>
		<td class="wikibase-table-cell">
			<WikibaseDetailCardContainer :wikibase-id="Number.parseInt(wikibase.id)" />
		</td>
	</tr>
</template>

<style lang="css">
.wikibase-table-cell {
	font-family: Roboto;
	font-size: 16px;
}
.wikibase-type-chip {
	min-width: 40px;
}
.wikibase-title-link {
	text-decoration: none;
}
</style>
