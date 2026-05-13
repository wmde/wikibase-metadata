<script setup lang="ts">
import VSelectWorking from '@/component/wikibase-table/VSelectWorking.vue'
import { useWikiStore } from '@/stores/wikibase-page-store'
import {
	mdiChevronDoubleLeft,
	mdiChevronDoubleRight,
	mdiChevronLeft,
	mdiChevronRight
} from '@mdi/js'
import { computed } from 'vue'

const store = useWikiStore()

const pageNumber = computed(() => store.pageNumber)
const pageSize = computed(() => store.pageSize)
const totalCount = computed(() => store.wikibasePage.data?.meta.totalCount)
const totalPages = computed(() => store.wikibasePage.data?.meta.totalPages)
</script>

<template>
	<v-container
		class="pagination-container py-4 px-6"
		v-if="totalPages && totalCount && totalCount > 25"
	>
		<v-container class="ma-0 pa-0 pagination-row-container">
			<v-container class="item-number-container ma-0 pa-0 shrink">
				{{ ((pageNumber - 1) * pageSize + 1).toLocaleString('en') }}&ndash;{{
					Math.min(pageNumber * pageSize, totalCount).toLocaleString('en')
				}}
				of
				{{ totalCount.toLocaleString('en') }}
			</v-container>
			<v-container class="button-container ma-0 pa-0 shrink">
				<v-btn
					:icon="mdiChevronDoubleLeft"
					:disabled="pageNumber == 1"
					variant="plain"
					v-on:click="store.setPageNumber(1)"
					class="ma-0 pa-0"
				/>
				<v-btn
					:icon="mdiChevronLeft"
					:disabled="pageNumber == 1"
					variant="plain"
					v-on:click="store.setPageNumber(pageNumber - 1)"
					class="ma-0 pa-0"
				/>
				<v-btn
					:icon="mdiChevronRight"
					:disabled="pageNumber == totalPages"
					variant="plain"
					v-on:click="store.setPageNumber(pageNumber + 1)"
					class="ma-0 pa-0"
				/>
				<v-btn
					:icon="mdiChevronDoubleRight"
					:disabled="pageNumber == totalPages"
					variant="plain"
					v-on:click="store.setPageNumber(totalPages)"
					class="ma-0 pa-0"
				/>
			</v-container>
		</v-container>
		<v-container class="page-size-container ma-0 pa-0">
			<span class="page-size-label">Items per page:</span>
			<v-container class="ma-0 pa-0 shrink">
				<v-select-working :on-change="store.setPageSize" />
			</v-container>
		</v-container>
	</v-container>
</template>

<style lang="css">
.pagination-container {
	background-color: white;
	/* border-top: 1px solid grey; */
	border-top: 1px solid oklch(87.2% 0.01 285.338);
}
.pagination-row-container {
	display: flex;
	flex-flow: row wrap;
	align-items: center;
	gap: 1rem;
	justify-content: center;
}
.item-number-container {
	font-family: Roboto;
	font-size: 16px;
	color: #000;
}
.button-container {
	display: flex;
	flex-flow: row nowrap;
	gap: 0.25rem;
}
.button-container .v-icon svg,
.button-container .v-btn {
	height: 36px;
	width: 36px;
}
.page-size-container {
	display: flex;
	flex-flow: row nowrap;
	gap: 0.75rem;
	align-items: center;
	justify-content: center;
}
</style>
