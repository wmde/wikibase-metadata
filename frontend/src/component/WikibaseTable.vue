<script setup lang="ts">
import { useWikiStore } from '@/stores/wikibase-page-store'
import { computed } from 'vue'
import LocaleNumber from './LocaleNumber.vue'

const store = useWikiStore()

const error = computed(() => store.wikibasePage.errorState)
const loading = computed(() => store.wikibasePage.loading)
const count = computed(() => store.wikibasePage.data?.wikibaseList.meta.totalCount)
const wikibases = computed(() => store.wikibasePage.data?.wikibaseList.data)
</script>

<template>
	<p v-if="error">Error</p>
	<p v-if="loading">Loading</p>
	<p>Count: <LocaleNumber :stat="count" /></p>
	<v-table v-if="wikibases" striped="even" :height="800" fixed-header fixed-footer>
		<thead>
			<tr>
				<th>Type</th>
				<th>Title</th>
				<th>Triples</th>
				<th>Edits</th>
				<th>URL</th>
				<th>Description</th>
			</tr>
		</thead>
		<tbody>
			<tr v-for="(wikibase, index) in wikibases" :key="index">
				<td>{{ wikibase.wikibaseType }}</td>
				<td>{{ wikibase.title }}</td>
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
				<td>{{ wikibase.urls.baseUrl }}</td>
				<td>{{ wikibase.description }}</td>
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
