import { defineStore } from 'pinia'
import { ref, type Ref } from 'vue'

export type MenuOption = 'instances' | 'items'

export type MenuStoreType = {
	value: MenuOption | Ref<MenuOption>
	setValue: (v: MenuOption) => void
}

export const useMenuStore = defineStore('menu', (): MenuStoreType => {
	const value = ref<MenuOption>('instances')
	const setValue = (v: MenuOption) => (value.value = v)

	return { value, setValue }
})
