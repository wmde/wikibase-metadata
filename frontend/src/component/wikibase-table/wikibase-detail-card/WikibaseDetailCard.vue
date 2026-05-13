<script setup lang="ts">
import CardLoader from '@/component/wikibase-table/wikibase-detail-card/CardLoader.vue'
import WikibaseAccess from '@/component/wikibase-table/wikibase-detail-card/WikibaseAccess.vue'
import WikibaseDescription from '@/component/wikibase-table/wikibase-detail-card/WikibaseDescription.vue'
import WikibaseDetailStats from '@/component/wikibase-table/wikibase-detail-card/WikibaseDetailStats.vue'
import WikibaseTitle from '@/component/wikibase-table/wikibase-detail-card/WikibaseTitle.vue'
import WikibaseCategoryChip from '@/component/wikibase-table/WikibaseCategoryChip.vue'
import WikibaseTypeChip from '@/component/wikibase-table/WikibaseTypeChip.vue'
import type { SingleWikibaseFragment } from '@/graphql/types'
import { useTheme } from 'vuetify'

defineProps<{ wikibase: SingleWikibaseFragment | undefined; loading: boolean }>()

const theme = useTheme()
</script>

<template>
	<v-card
		variant="outlined"
		class="wikibase-detail-card ma-0 pa-6"
		:style="{ backgroundColor: theme.current.value.colors.background }"
	>
		<CardLoader v-if="loading" />
		<template v-else-if="wikibase">
			<v-container class="ma-0 pa-0 pb-8">
				<WikibaseTitle :wikibase="wikibase" />
				<v-container class="ma-0 pa-0 mb-4 tag-container">
					<WikibaseCategoryChip :category="wikibase.category" class="category" />
					<WikibaseTypeChip :wikibase-type="wikibase.wikibaseType" />
				</v-container>
				<WikibaseDescription :wikibase="wikibase" />
			</v-container>
			<WikibaseDetailStats :wikibase="wikibase" />
			<WikibaseAccess :wikibase="wikibase" />
		</template>
	</v-card>
</template>

<style lang="css">
.wikibase-detail-card {
	max-width: 600px;
	border-color: rgba(255, 255, 255, 0.12);
	border-radius: 0.625rem !important;
}
.tag-container {
	display: flex;
	flex-flow: row wrap;
	gap: 0.75rem;
}
</style>
