import { getUrlParamValue, updateUrlParamValue } from '@/util/use-url'
import { describe, expect, it, vi } from 'vitest'

describe('getUrlParamValue', () => {
	it('returns null when param not set', () => {
		const result = getUrlParamValue('NOT_SET')
		expect(result).toEqual(null)
	})

	it('returns data when param not set', () => {
		Object.defineProperty(window, 'location', {
			value: { search: '?value=datum' },
			writable: true
		})
		const result = getUrlParamValue('value')
		expect(result).toEqual('datum')
	})
})

describe('updateUrlParamValue', () => {
	it('set value', () => {
		const mockPushHistory = vi.fn()
		Object.defineProperty(window, 'location', {
			value: 'https://example.test',
			writable: true
		})
		Object.defineProperty(window, 'history', {
			value: { pushState: mockPushHistory },
			writable: true
		})

		expect(mockPushHistory).toHaveBeenCalledTimes(0)

		updateUrlParamValue('value', 'datum')

		expect(mockPushHistory).toHaveBeenCalledTimes(1)
		expect(mockPushHistory).toHaveBeenCalledWith(
			{},
			'',
			new URL('https://example.test/?value=datum')
		)
	})

	it('overwrites value', () => {
		const mockPushHistory = vi.fn()
		Object.defineProperty(window, 'location', {
			value: 'https://example.test/?city=berlin',
			writable: true
		})
		Object.defineProperty(window, 'history', {
			value: { pushState: mockPushHistory },
			writable: true
		})

		expect(mockPushHistory).toHaveBeenCalledTimes(0)

		updateUrlParamValue('city', 'chicago')

		expect(mockPushHistory).toHaveBeenCalledTimes(1)
		expect(mockPushHistory).toHaveBeenCalledWith(
			{},
			'',
			new URL('https://example.test/?city=chicago')
		)
	})

	it('delets value', () => {
		const mockPushHistory = vi.fn()
		Object.defineProperty(window, 'location', {
			value: 'https://example.test/?value=datum',
			writable: true
		})
		Object.defineProperty(window, 'history', {
			value: { pushState: mockPushHistory },
			writable: true
		})

		expect(mockPushHistory).toHaveBeenCalledTimes(0)

		updateUrlParamValue('value', '')

		expect(mockPushHistory).toHaveBeenCalledTimes(1)
		expect(mockPushHistory).toHaveBeenCalledWith({}, '', new URL('https://example.test/'))
	})
})
