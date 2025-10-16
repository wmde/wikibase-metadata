<script setup lang="ts">
import DateStatBlock from '@/component/wikibase-table/wikibase-detail-card/DateStatBlock.vue'
import NumStatBlock from '@/component/wikibase-table/wikibase-detail-card/NumStatBlock.vue'
import WikibaseIcon from '@/component/wikibase-table/wikibase-detail-card/WikibaseIcon.vue'
import { WikibaseType, type SingleWikibaseFragment } from '@/graphql/types'
import computeTotalEdits from '@/util/computeTotalEdits'

defineProps<{ wikibase: SingleWikibaseFragment | undefined; loading: boolean }>()
</script>

<template>
	<v-card variant="outlined" class="wikibase-detail-card ma-1 pa-1">
		<v-skeleton-loader
			class="wikibase-detail-card-loader"
			v-if="loading"
			color="secondary"
			type="card"
		>
			LOADING
		</v-skeleton-loader>
		<template v-else-if="wikibase">
			<v-container class="card-header ma-0 pa-0">
				<v-container class="ma-0 pa-0">
					<v-container class="url-container ma-0 pa-0">
						<WikibaseIcon :base-url="wikibase.urls.baseUrl" />
						<v-container class="wikibase-url ma-0 pa-0">
							<v-tooltip
								class="base-url-tooltip"
								:text="
									wikibase.wikibaseType == WikibaseType.Cloud
										? `Automatically pulled from Cloud API`
										: `Manually set`
								"
							>
								<template v-slot:activator="{ props }">
									<a v-bind="props" :href="wikibase.urls.baseUrl">
										{{ wikibase.title }}
									</a>
								</template>
							</v-tooltip>
						</v-container>
						<v-container v-if="wikibase.urls.sparqlFrontendUrl" class="wikibase-url ma-0 pa-0">
							<v-tooltip
								class="sparql-url-tooltip"
								:text="
									wikibase.wikibaseType == WikibaseType.Cloud
										? `Automatically pulled from Cloud API`
										: `Manually set`
								"
							>
								<template v-slot:activator="{ props }">
									<a v-bind="props" :href="wikibase.urls.sparqlFrontendUrl">SPARQL</a>
								</template>
							</v-tooltip>
						</v-container>
					</v-container>
					<v-tooltip v-if="wikibase.description" class="desc-tooltip" text="Manually written">
						<template v-slot:activator="{ props }">
							<v-container v-bind="props" class="description ma-0 pa-0">
								{{ wikibase.description }}
							</v-container>
						</template>
					</v-tooltip>
				</v-container>
				<v-container class="wikibase-type ma-0 pa-0">
					<v-tooltip
						class="type-tooltip"
						:text="
							wikibase.wikibaseType == WikibaseType.Cloud
								? `Automatically pulled from Cloud API`
								: wikibase.wikibaseType == undefined
									? `Not set`
									: `Manually set`
						"
					>
						<template v-slot:activator="{ props }">
							<v-chip class="wikibase-type-chip" v-bind="props">{{ wikibase.wikibaseType }}</v-chip>
						</template>
					</v-tooltip>
				</v-container>
			</v-container>
			<v-tooltip
				v-if="wikibase.timeToFirstValueObservations.mostRecent?.initiationDate"
				class="ttfv-tooltip"
				text="Pulled from Action API"
			>
				<template v-slot:activator="{ props }">
					<v-container v-bind="props" class="stat-block-container pa-0">
						<DateStatBlock
							label="First Record"
							:stat="wikibase.timeToFirstValueObservations.mostRecent?.initiationDate"
						/>
						<DateStatBlock
							label="AS OF"
							:stat="wikibase.timeToFirstValueObservations.mostRecent?.observationDate"
						/>
					</v-container>
				</template>
			</v-tooltip>
			<v-tooltip
				v-if="wikibase.quantityObservations.mostRecent"
				class="quantity-tooltip"
				:text="
					wikibase.quantityObservations.mostRecent.totalItems == undefined &&
					wikibase.quantityObservations.mostRecent.totalLexemes == undefined &&
					wikibase.quantityObservations.mostRecent.totalProperties == undefined &&
					wikibase.quantityObservations.mostRecent.totalTriples == undefined
						? `SPARQL Unavailable`
						: `Pulled from SPARQL`
				"
			>
				<template v-slot:activator="{ props }">
					<v-container v-bind="props" class="stat-block-container pa-0">
						<NumStatBlock
							label="ITEMS"
							:stat="wikibase.quantityObservations.mostRecent.totalItems"
						/>
						<NumStatBlock
							label="PROPERTIES"
							:stat="wikibase.quantityObservations.mostRecent.totalProperties"
						/>
						<NumStatBlock
							label="LEXEMES"
							:stat="wikibase.quantityObservations.mostRecent?.totalLexemes"
						/>
						<NumStatBlock
							label="TRIPLES"
							:stat="wikibase.quantityObservations.mostRecent?.totalTriples"
						/>
						<DateStatBlock
							label="AS OF"
							:stat="wikibase.quantityObservations.mostRecent?.observationDate"
						/>
					</v-container>
				</template>
			</v-tooltip>
			<v-tooltip
				v-if="wikibase.recentChangesObservations.mostRecent"
				class="recent-changes-tooltip"
				:text="
					wikibase.recentChangesObservations.mostRecent.botChangeCount == undefined &&
					wikibase.recentChangesObservations.mostRecent.humanChangeCount == undefined
						? `Data Unavailable`
						: `Pulled from Action API`
				"
			>
				<template v-slot:activator="{ props }">
					<v-container v-bind="props" class="stat-block-container pa-0">
						<NumStatBlock
							label="EDITS (30 DAYS)"
							:stat="computeTotalEdits(wikibase.recentChangesObservations)"
						/>
						<DateStatBlock
							label="AS OF"
							:stat="wikibase.recentChangesObservations.mostRecent.observationDate"
						/>
					</v-container>
				</template>
			</v-tooltip>
		</template>
	</v-card>
</template>

<style lang="css">
.wikibase-detail-card {
	display: flex;
	flex-flow: column nowrap;
	justify-content: space-between;
	max-width: 500px;
	background-color: white !important;
}
.card-header {
	display: flex;
	flex-flow: row nowrap;
	gap: 12px;
}
.url-container {
	display: flex;
	flex-flow: row wrap;
	justify-content: flex-start;
	gap: 4px;
	align-items: center;
}
.wikibase-url {
	width: auto;
}
.wikibase-type {
	width: auto;
	align-self: stretch;
	align-content: center;
}
.wikibase-type-chip {
	min-width: 40px;
	font-weight: 500;
}
.stat-block-container {
	display: flex;
	flex-flow: row wrap;
	border: 2px solid grey;
	margin: 6px 0;
}
.stat-block-container .stat-container,
.stat-block-container .v-label {
	width: auto;
	margin: 4px;
}
</style>
