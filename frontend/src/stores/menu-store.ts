import { getUrlParamValue, updateUrlParamValue } from '@/util/use-url'
import { defineStore } from 'pinia'
import { ref, watch, type Ref } from 'vue'

export type MenuOption = 'instances' | 'items'

export type MenuStoreType = {
	value: MenuOption | Ref<MenuOption>
	setValue: (v: MenuOption) => void
}

const PARAM_NAME = 'menu'

export const useMenuStore = defineStore('menu', (): MenuStoreType => {
	const value = ref<MenuOption>(getUrlParamValue(PARAM_NAME) ?? 'instances')
	const setValue = (v: MenuOption) => (value.value = v)
	watch(value, () => updateUrlParamValue(PARAM_NAME, value.value))

	return { value, setValue }
})
