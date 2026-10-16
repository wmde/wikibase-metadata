import { getUrlParamValue, updateUrlParamValue } from '@/util/use-url'
import { defineStore } from 'pinia'
import { ref, watch, type Ref } from 'vue'

export type MenuOption = 'instances' | 'items'

export type SearchStoreType = {
	menuValue: MenuOption | Ref<MenuOption>
	setMenuValue: (v: MenuOption) => void
}

const MENU_PARAM_NAME = 'menu'

export const useMenuStore = defineStore('search', (): SearchStoreType => {
	const menuValue = ref<MenuOption>(getUrlParamValue(MENU_PARAM_NAME) ?? 'instances')
	const setMenuValue = (v: MenuOption) => (menuValue.value = v)
	watch(menuValue, () => updateUrlParamValue(MENU_PARAM_NAME, menuValue.value))

	return { menuValue, setMenuValue }
})
