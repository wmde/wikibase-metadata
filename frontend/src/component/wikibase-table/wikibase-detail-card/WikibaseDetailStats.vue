<script setup lang="ts">
import LocaleDate from '@/component/LocaleDate.vue'
import LocaleNumber from '@/component/LocaleNumber.vue'
import type { SingleWikibaseFragment } from '@/graphql/types'
import computeTotalEdits from '@/util/compute-total-edits'

defineProps<{ wikibase: SingleWikibaseFragment }>()
</script>

<template>
	<v-table striped="odd" class="wikibase-detail-stats">
		<thead>
			<tr>
				<th colspan="2">STATISTIC</th>
				<th>SOURCE</th>
			</tr>
		</thead>
		<tbody>
			<template v-if="wikibase.timeToFirstValueObservations.mostRecent?.initiationDate">
				<tr>
					<th>FIRST RECORD</th>
					<td>
						<LocaleDate :stat="wikibase.timeToFirstValueObservations.mostRecent.initiationDate" />
					</td>
					<td>Action API</td>
				</tr>
			</template>
			<template v-if="wikibase.quantityObservations.mostRecent">
				<tr>
					<th>ITEMS</th>
					<td>
						<LocaleNumber :stat="wikibase.quantityObservations.mostRecent.totalItems" />
					</td>
					<td rowspan="5">Query Service</td>
				</tr>
				<tr>
					<th>PROPERTIES</th>
					<td>
						<LocaleNumber :stat="wikibase.quantityObservations.mostRecent.totalProperties" />
					</td>
				</tr>
				<tr>
					<th>LEXEMES</th>
					<td>
						<LocaleNumber :stat="wikibase.quantityObservations.mostRecent.totalLexemes" />
					</td>
				</tr>
				<tr>
					<th>TRIPLES</th>
					<td>
						<LocaleNumber :stat="wikibase.quantityObservations.mostRecent.totalTriples" />
					</td>
				</tr>
				<tr>
					<th>AS OF</th>
					<td>
						<LocaleDate :stat="wikibase.quantityObservations.mostRecent.observationDate" />
					</td>
				</tr>
			</template>
			<template v-if="wikibase.recentChangesObservations.mostRecent">
				<tr>
					<th>EDITS (LAST 30 DAYS)</th>
					<td>
						<LocaleNumber :stat="computeTotalEdits(wikibase.recentChangesObservations)" />
					</td>
					<td rowspan="2">Action API</td>
				</tr>
				<tr style="display: none">
					<th>AS OF</th>
					<td>
						<LocaleDate :stat="wikibase.recentChangesObservations.mostRecent.observationDate" />
					</td>
				</tr>
			</template>
		</tbody>
	</v-table>
</template>
