import { defineStore } from 'pinia'
import { ref, watch, type Ref } from 'vue'

export type MenuOption = 'instances' | 'items'

export type MenuStoreType = {
	value: MenuOption | Ref<MenuOption>
	setValue: (v: MenuOption) => void
}

const getUrlValue = (): MenuOption => {
	const queryString = window.location.search
	const urlParams = new URLSearchParams(queryString)
	return urlParams.get('menu') as MenuOption
}

const updateUrlValue = (v: MenuOption) => {
	const searchURL = new URL(window.location.toString())
	searchURL.searchParams.set('menu', v)
	window.history.pushState({}, '', searchURL)
}

export const useMenuStore = defineStore('menu', (): MenuStoreType => {
	const value = ref<MenuOption>(getUrlValue() ?? 'instances')
	const setValue = (v: MenuOption) => (value.value = v)
	watch(value, () => updateUrlValue(value.value))

	return { value, setValue }
})
