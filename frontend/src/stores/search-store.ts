import { debounce } from '@/util/debounce'
import { getUrlParamValue, updateUrlParamValue } from '@/util/use-url'
import { defineStore } from 'pinia'
import { ref, watch, type Ref } from 'vue'

export type MenuOption = 'instances' | 'items'

export type SearchStoreType = {
	menuValue: MenuOption | Ref<MenuOption>
	setMenuValue: (v: MenuOption) => void

	searchValue: string | Ref<string>
	setSearchValue: (s: string) => void
	debouncedSearchValue: string | Ref<string>
	overrideDebounce: (s: string) => void
}

const MENU_PARAM_NAME = 'menu'
export const SEARCH_PARAM_NAME = 'search'

export const useSearchStore = defineStore('search', (): SearchStoreType => {
	const menuValue = ref<MenuOption>(getUrlParamValue(MENU_PARAM_NAME) ?? 'instances')
	const setMenuValue = (v: MenuOption) => (menuValue.value = v)
	watch(menuValue, () => updateUrlParamValue(MENU_PARAM_NAME, menuValue.value))

	const searchValue = ref<string>('')
	const setSearchValue = (s: string) => (searchValue.value = s)
	watch(menuValue, () => setSearchValue(''))

	const debouncedSearchValue = ref<string>(searchValue.value)
	const overrideDebounce = (s: string) => (debouncedSearchValue.value = s)
	const [setDebouncedSearchValue] = debounce(
		(s: string) => (debouncedSearchValue.value = s),
		menuValue.value == 'instances' ? 300 : 1000
	)
	watch(searchValue, () => setDebouncedSearchValue(searchValue.value))
	watch(debouncedSearchValue, () =>
		updateUrlParamValue(SEARCH_PARAM_NAME, debouncedSearchValue.value)
	)

	return {
		menuValue,
		setMenuValue,
		searchValue,
		setSearchValue,
		debouncedSearchValue,
		overrideDebounce
	}
})
