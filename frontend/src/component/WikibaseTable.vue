<script setup lang="ts">
import { useWikiStore } from '@/stores/wikibase-page-store'
import { computed } from 'vue'
import LocaleNumber from './LocaleNumber.vue'

const store = useWikiStore()

const wikibases = computed(() => store.wikibasePage.data?.wikibaseList.data)
</script>

<template>
	<v-table v-if="wikibases" striped="even" :height="800" fixed-header fixed-footer>
		<thead>
			<tr>
				<th>Type</th>
				<th>Title</th>
				<th>URL</th>
				<th>Triples</th>
				<th>Edits</th>
			</tr>
		</thead>
		<tbody>
			<tr v-for="(wikibase, index) in wikibases" :key="index">
				<td>
					{{ wikibase.wikibaseType }}
				</td>
				<td>{{ wikibase.title }}</td>
				<td>{{ wikibase.urls.baseUrl }}</td>
				<td><LocaleNumber :stat="wikibase.quantityObservations.mostRecent?.totalTriples" /></td>
				<td>
					<LocaleNumber
						:stat="
							wikibase.recentChangesObservations.mostRecent?.botChangeCount != undefined ||
							wikibase.recentChangesObservations.mostRecent?.humanChangeCount != undefined
								? (wikibase.recentChangesObservations.mostRecent?.botChangeCount ?? 0) +
									(wikibase.recentChangesObservations.mostRecent?.humanChangeCount ?? 0)
								: undefined
						"
					/>
				</td>
			</tr>
		</tbody>
	</v-table>
</template>

<style lang="css">
.wikibase-card-container {
	display: flex;
	flex-flow: row wrap;
	gap: 6px;
	justify-content: space-evenly;
}
</style>
