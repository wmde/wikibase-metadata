<script setup lang="ts">
import WikibaseSearchValid from '@/component/wikibase-table/WikibaseSearchValid.vue'
import { mdiCheck, mdiChevronDown, mdiMagnify } from '@mdi/js'
import { ref, watch } from 'vue'

const { menuValue, setSearchValue } = defineProps<{
	menuValue: 'instances' | 'items'
	setMenuValue: (v: 'instances' | 'items') => void
	setSearchValue: (s: string) => void
}>()

const searchValue = ref('')
watch(searchValue, () => setSearchValue(searchValue.value))

const ALLOWED_CHARACTERS = /^[A-Za-z0-9\-_ .]*$/
const rules: ((value: string) => true | string)[] = [
	(value: string) => ALLOWED_CHARACTERS.test(value) || 'Disallowed Characters'
]

const focused = ref(false)
</script>

<template>
	<v-container class="search-container ma-0 mb-6 pa-0">
		<v-container :class="`ma-0 pa-0  search-text ${focused ? 'search-text-focused' : ''}`">
			<v-menu open-on-hover>
				<template v-slot:activator="{ props }">
					<v-btn
						variant="tonal"
						class="ma-0 dropdown"
						v-bind="props"
						:append-icon="mdiChevronDown"
						:style="{ height: '48px' }"
					>
						{{ menuValue == 'instances' ? 'Instances' : 'Items' }}
					</v-btn>
				</template>
				<v-list>
					<v-list-item
						key="instances"
						value="instances"
						v-on:click="() => setMenuValue('instances')"
						:append-icon="menuValue == 'instances' ? mdiCheck : undefined"
					>
						<v-list-item-title>Instances</v-list-item-title>
					</v-list-item>
					<v-list-item
						key="items"
						value="items"
						v-on:click="() => setMenuValue('items')"
						:append-icon="menuValue == 'items' ? mdiCheck : undefined"
					>
						<v-list-item-title>Items</v-list-item-title>
					</v-list-item>
				</v-list>
			</v-menu>
			<v-text-field
				class="ma-0 ml-3 pa-0"
				variant="plain"
				:prepend-icon="mdiMagnify"
				v-model="searchValue"
				:label="
					menuValue == 'instances'
						? 'Search Wikibase instances...'
						: 'Search for items across all Wikibase instances...'
				"
				:rules="rules"
				:focused="focused"
				@update:focused="(v: boolean) => (focused = v)"
			/>
		</v-container>
		<wikibase-search-valid :menu-value="menuValue" :search-value="searchValue" />
	</v-container>
</template>

<style lang="scss">
.search-text {
	border: 1px solid oklch(87.2% 0.01 285.338);
	border-radius: 4px;
	background: white;
	font-family: Roboto;

	display: flex;
	align-items: center;

	.dropdown {
		text-transform: none;
		font-family: Roboto;
		font-size: 14px;
		color: rgb(54, 40, 245);
		background: rgba(54, 40, 245, 0.06);
		.v-icon {
			color: #717182;
		}
	}

	div.v-input__details {
		display: none;
	}

	div.v-input__prepend {
		padding-top: 14px !important;
	}
	label.v-label {
		top: 14px !important;
		transform: none !important;
	}
	label.v-field-label--floating {
		display: none;
	}

	input {
		margin: 0;
		padding: 0;
		font-size: 16px;
		color: rgb(0, 0, 0);
	}
	label.v-field-label--floating {
		color: #444;
	}
}

.search-text-focused {
	border-color: rgb(54, 40, 245);
}
</style>
