import { useSearchStore } from '@/stores/search-store'
import { createPinia, setActivePinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { nextTick } from 'vue'

const { mockGetUrlParamValue, mockUpdateUrlParamValue } = vi.hoisted(() => ({
	mockGetUrlParamValue: vi.fn().mockName('getUrlParamValue'),
	mockUpdateUrlParamValue: vi.fn().mockName('updateUrlParamValue')
}))

vi.mock('@/util/use-url', () => ({
	getUrlParamValue: mockGetUrlParamValue,
	updateUrlParamValue: mockUpdateUrlParamValue
}))

function sleep(milliseconds: number) {
	return new Promise((resolve) => {
		setTimeout(resolve, milliseconds)
	})
}

describe('useSearchStore', async () => {
	beforeEach(() => {
		setActivePinia(createPinia())
		vi.resetAllMocks()
	})

	describe('menuValue initialization', async () => {
		it('reads items menuValue from url', async () => {
			mockGetUrlParamValue.mockReturnValueOnce('items')

			expect(mockGetUrlParamValue).toHaveBeenCalledTimes(0)

			const store = useSearchStore()

			expect(store.menuValue).toEqual('items')
			expect(mockGetUrlParamValue).toHaveBeenCalledTimes(1)
			expect(mockGetUrlParamValue).toHaveBeenCalledWith('menu')
		})

		it('reads instances menuValue from url', async () => {
			mockGetUrlParamValue.mockReturnValueOnce('instances')

			expect(mockGetUrlParamValue).toHaveBeenCalledTimes(0)

			const store = useSearchStore()

			expect(store.menuValue).toEqual('instances')
			expect(mockGetUrlParamValue).toHaveBeenCalledTimes(1)
			expect(mockGetUrlParamValue).toHaveBeenCalledWith('menu')
		})

		it('sets menuValue to instances on no url value', async () => {
			mockGetUrlParamValue.mockReturnValueOnce(null)

			expect(mockGetUrlParamValue).toHaveBeenCalledTimes(0)

			const store = useSearchStore()

			expect(store.menuValue).toEqual('instances')
			expect(mockGetUrlParamValue).toHaveBeenCalledTimes(1)
			expect(mockGetUrlParamValue).toHaveBeenCalledWith('menu')
		})
	})

	describe('menuValue updates url', async () => {
		it('does not update url on initialization', async () => {
			expect(mockUpdateUrlParamValue).toHaveBeenCalledTimes(0)
			const store = useSearchStore()
			expect(store.menuValue).toEqual('instances')
			expect(mockUpdateUrlParamValue).toHaveBeenCalledTimes(0)
		})

		it('does not update url on change to same value', async () => {
			expect(mockUpdateUrlParamValue).toHaveBeenCalledTimes(0)
			const store = useSearchStore()
			expect(store.menuValue).toEqual('instances')
			expect(mockUpdateUrlParamValue).toHaveBeenCalledTimes(0)

			store.setMenuValue('instances')
			await nextTick()

			expect(mockUpdateUrlParamValue).toHaveBeenCalledTimes(0)
		})

		it('calls update url on change value to items', async () => {
			expect(mockUpdateUrlParamValue).toHaveBeenCalledTimes(0)
			const store = useSearchStore()
			expect(store.menuValue).toEqual('instances')
			expect(mockUpdateUrlParamValue).toHaveBeenCalledTimes(0)

			store.setMenuValue('items')
			await nextTick()

			expect(mockUpdateUrlParamValue).toHaveBeenCalledTimes(1)
			expect(mockUpdateUrlParamValue).toHaveBeenCalledWith('menu', 'items')
		})

		it('calls update url on change value to instances', async () => {
			mockGetUrlParamValue.mockReturnValueOnce('items')
			expect(mockUpdateUrlParamValue).toHaveBeenCalledTimes(0)
			const store = useSearchStore()
			expect(store.menuValue).toEqual('items')
			expect(mockUpdateUrlParamValue).toHaveBeenCalledTimes(0)

			store.setMenuValue('instances')
			await nextTick()

			expect(mockUpdateUrlParamValue).toHaveBeenCalledTimes(1)
			expect(mockUpdateUrlParamValue).toHaveBeenCalledWith('menu', 'instances')
		})
	})

	describe('searchValue', async () => {
		it('does not read searchValue from url', async () => {
			mockGetUrlParamValue.mockReturnValueOnce(null)

			expect(mockGetUrlParamValue).toHaveBeenCalledTimes(0)

			const store = useSearchStore()

			expect(store.searchValue).toEqual('')
			expect(mockGetUrlParamValue).toHaveBeenCalledTimes(1)
			expect(mockGetUrlParamValue).toHaveBeenCalledWith('menu')
			expect(mockGetUrlParamValue).not.toHaveBeenCalledWith('search')
		})

		it('resets searchValue on menuValue update', async () => {
			const store = useSearchStore()

			expect(store.searchValue).toEqual('')
			store.setSearchValue('berlin')
			await nextTick()
			expect(store.searchValue).toEqual('berlin')

			expect(store.menuValue).toEqual('instances')
			store.setMenuValue('items')
			await nextTick()
			expect(store.searchValue).toEqual('')
		})
	})

	describe('debouncedSearchValue', async () => {
		it('does not change immediately on searchValue change', async () => {
			const store = useSearchStore()

			expect(store.searchValue).toEqual('')
			expect(store.debouncedSearchValue).toEqual('')
			store.setSearchValue('berlin')
			await nextTick()
			expect(store.searchValue).toEqual('berlin')
			expect(store.debouncedSearchValue).toEqual('')
		})

		it('changes after 300ms on searchValue change for instances search', async () => {
			const store = useSearchStore()

			expect(store.menuValue).toEqual('instances')

			expect(store.searchValue).toEqual('')
			expect(store.debouncedSearchValue).toEqual('')
			store.setSearchValue('berlin')
			await nextTick()
			expect(store.searchValue).toEqual('berlin')
			expect(store.debouncedSearchValue).toEqual('')

			await sleep(300)

			expect(store.debouncedSearchValue).toEqual('berlin')
		})

		it('changes after 1000ms on searchValue change for items search', async () => {
			mockGetUrlParamValue.mockReturnValueOnce('items')
			const store = useSearchStore()

			expect(store.menuValue).toEqual('items')

			expect(store.searchValue).toEqual('')
			expect(store.debouncedSearchValue).toEqual('')
			store.setSearchValue('berlin')
			await nextTick()
			expect(store.searchValue).toEqual('berlin')
			expect(store.debouncedSearchValue).toEqual('')

			await sleep(1000)

			expect(store.debouncedSearchValue).toEqual('berlin')
		})

		it('calls update url on debounced change', async () => {
			expect(mockUpdateUrlParamValue).toHaveBeenCalledTimes(0)
			const store = useSearchStore()

			expect(store.menuValue).toEqual('instances')

			expect(store.searchValue).toEqual('')
			expect(store.debouncedSearchValue).toEqual('')

			store.setSearchValue('berlin')
			await nextTick()

			expect(mockUpdateUrlParamValue).toHaveBeenCalledTimes(0)
			expect(store.searchValue).toEqual('berlin')
			expect(store.debouncedSearchValue).toEqual('')

			await sleep(300)

			expect(store.debouncedSearchValue).toEqual('berlin')
			expect(mockUpdateUrlParamValue).toHaveBeenCalledTimes(1)
			expect(mockUpdateUrlParamValue).toHaveBeenCalledWith('search', 'berlin')
		})
	})
})
