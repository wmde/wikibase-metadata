<script setup lang="ts">
import LocaleNumber from '@/component/LocaleNumber.vue'
import WikibaseDetailCardContainer from '@/component/wikibase-table/wikibase-detail-card/WikibaseDetailCardContainer.vue'
import WikibaseTypeChip from '@/component/wikibase-table/WikibaseTypeChip.vue'
import type { WbFragment } from '@/graphql/types'
import computeTotalEdits from '@/util/computeTotalEdits'

defineProps<{ wikibase: WbFragment }>()
</script>

<template>
	<tr>
		<td>
			<WikibaseTypeChip :wikibase-type="wikibase.wikibaseType" />
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
		<td>
			<WikibaseDetailCardContainer :wikibase-id="Number.parseInt(wikibase.id)" />
		</td>
	</tr>
</template>

<style lang="css">
.wikibase-type-chip {
	min-width: 40px;
}
</style>
