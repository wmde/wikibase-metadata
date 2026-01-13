<script setup lang="ts">
import type { SingleWikibaseFragment } from '@/graphql/types';
import { useTheme } from 'vuetify';
import WikibaseDetailCardContents from './WikibaseDetailCardContents.vue';

defineProps<{ wikibase: SingleWikibaseFragment | undefined; loading: boolean }>()

const theme = useTheme()
</script>

<template>
	<v-card
		variant="outlined"
		class="wikibase-detail-card ma-1 pa-1"
		:style="{ backgroundColor: theme.current.value.colors.background }"
	>
	<WikibaseDetailCardContents :wikibase="wikibase" :loading="loading" />
	</v-card>
</template>

<style lang="css">
.wikibase-detail-card {
	display: flex;
	flex-flow: column nowrap;
	justify-content: space-between;
	max-width: 500px;
	border-color: rgba(255, 255, 255, 0.12);
}
</style>
