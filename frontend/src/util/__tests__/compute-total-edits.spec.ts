import computeTotalEdits from '@/util/compute-total-edits'
import { describe, expect, it } from 'vitest'

describe('computeTotalEdits', () => {
	it('computes null observation to undefined', () => {
		expect(computeTotalEdits({ mostRecent: null })).toEqual(undefined)
	})
	it('computes undefined observation to undefined', () => {
		expect(computeTotalEdits({ mostRecent: undefined })).toEqual(undefined)
	})

	it('computes null values to undefined', () => {
		expect(
			computeTotalEdits({ mostRecent: { botChangeCount: null, humanChangeCount: null } })
		).toEqual(undefined)
	})
	it('computes undefined values to undefined', () => {
		expect(
			computeTotalEdits({ mostRecent: { botChangeCount: undefined, humanChangeCount: undefined } })
		).toEqual(undefined)
	})

	it('computes null bot values to 0', () => {
		expect(
			computeTotalEdits({ mostRecent: { botChangeCount: null, humanChangeCount: 1 } })
		).toEqual(1)
	})
	it('computes undefined bot values to 0', () => {
		expect(
			computeTotalEdits({ mostRecent: { botChangeCount: undefined, humanChangeCount: 2 } })
		).toEqual(2)
	})

	it('computes null human values to 0', () => {
		expect(
			computeTotalEdits({ mostRecent: { botChangeCount: 3, humanChangeCount: null } })
		).toEqual(3)
	})
	it('computes undefined human values to 0', () => {
		expect(
			computeTotalEdits({ mostRecent: { botChangeCount: 5, humanChangeCount: undefined } })
		).toEqual(5)
	})

	it('computes a sum of bots and humans', () => {
		expect(computeTotalEdits({ mostRecent: { botChangeCount: 3, humanChangeCount: 5 } })).toEqual(8)
	})
})
