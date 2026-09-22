import DataFetcher from '@/util/fetch-data'
import { beforeEach, describe, expect, it, vi } from 'vitest'

const mockFetch = vi.fn()
global.fetch = mockFetch
const mockJson = vi.fn()

describe('DataFetcher', async () => {
	beforeEach(() => vi.clearAllMocks())

	it('initializes with a provided url', async () => {
		const fetcher = new DataFetcher('https://www.asdf.test/api.php')
		expect(fetcher.actionApiUrl).toEqual('https://www.asdf.test/api.php')
		expect(fetcher.data.value).toEqual(undefined)
		expect(fetcher.loading.value).toEqual(false)
		expect(fetcher.status.value).toEqual(undefined)
	})

	it('initializes with null provided url', async () => {
		const fetcher = new DataFetcher(null)
		expect(fetcher.actionApiUrl).toEqual(null)
		expect(fetcher.data.value).toEqual(undefined)
		expect(fetcher.loading.value).toEqual(false)
		expect(fetcher.status.value).toEqual(undefined)
	})

	it('calls fetch on search', async () => {
		const fetcher = new DataFetcher('https://www.asdf.test/api.php')
		mockJson.mockResolvedValueOnce({ searchInfo: 'asdf', search: [], success: 0 })
		mockFetch.mockResolvedValueOnce({
			ok: true,
			status: 200,
			statusText: 'ok',
			json: mockJson
		})

		expect(mockFetch).toHaveBeenCalledTimes(0)
		expect(mockJson).toHaveBeenCalledTimes(0)

		await fetcher.getData('asdf')

		expect(mockFetch).toHaveBeenCalledTimes(1)
		expect(mockJson).toHaveBeenCalledTimes(1)

		expect(fetcher.status.value).toEqual({ code: 200, text: 'ok' })
		expect(fetcher.data.value).toEqual({ search: [], searchInfo: 'asdf', success: 0 })
	})

	it('does not load data on error', async () => {
		const fetcher = new DataFetcher('https://www.asdf.test/api.php')
		mockFetch.mockResolvedValueOnce({
			ok: false,
			status: 403,
			statusText: 'Forbidden',
			json: mockJson
		})

		expect(mockFetch).toHaveBeenCalledTimes(0)
		expect(mockJson).toHaveBeenCalledTimes(0)

		await fetcher.getData('asdf')

		expect(mockFetch).toHaveBeenCalledTimes(1)
		expect(mockJson).toHaveBeenCalledTimes(0)

		expect(fetcher.status.value).toEqual({ code: 403, text: 'Forbidden' })
		expect(fetcher.data.value).toEqual(undefined)
	})

	it('does not call fetch on empty search', async () => {
		const fetcher = new DataFetcher('https://www.asdf.test/api.php')

		expect(mockFetch).toHaveBeenCalledTimes(0)
		expect(mockJson).toHaveBeenCalledTimes(0)

		await fetcher.getData('')

		expect(mockFetch).toHaveBeenCalledTimes(0)
		expect(mockJson).toHaveBeenCalledTimes(0)
	})

	it('does not call fetch on empty api url', async () => {
		const fetcher = new DataFetcher(null)

		expect(mockFetch).toHaveBeenCalledTimes(0)
		expect(mockJson).toHaveBeenCalledTimes(0)

		await fetcher.getData('data')

		expect(mockFetch).toHaveBeenCalledTimes(0)
		expect(mockJson).toHaveBeenCalledTimes(0)
	})

	it('returns error on an error', async () => {
		const fetcher = new DataFetcher('https://www.asdf.test/api.php')

		mockFetch.mockThrowOnce(new Error('Failed Fetch'))

		expect(mockFetch).toHaveBeenCalledTimes(0)
		expect(mockJson).toHaveBeenCalledTimes(0)

		await fetcher.getData('data')

		expect(mockFetch).toHaveBeenCalledTimes(1)
		expect(mockJson).toHaveBeenCalledTimes(0)

		expect(fetcher.status.value).toEqual({ code: 500, text: 'Error: Failed Fetch' })
		expect(fetcher.data.value).toEqual(undefined)
	})
})
