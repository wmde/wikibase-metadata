import computeTotalEdits from '@/util/compute-total-edits'
import { describe, expect, it } from 'vitest'

describe('computeTotalEdits', () => {
	it('computes null observation to undefined', () => {
		expect(computeTotalEdits(null)).toEqual(undefined)
	})
	it('computes undefined observation to undefined', () => {
		expect(computeTotalEdits(undefined)).toEqual(undefined)
	})

	it('computes null values to undefined', () => {
		expect(computeTotalEdits({ botChangeCount: null, humanChangeCount: null })).toEqual(undefined)
	})
	it('computes undefined values to undefined', () => {
		expect(computeTotalEdits({ botChangeCount: undefined, humanChangeCount: undefined })).toEqual(
			undefined
		)
	})

	it('computes null bot values to 0', () => {
		expect(computeTotalEdits({ botChangeCount: null, humanChangeCount: 1 })).toEqual(1)
	})
	it('computes undefined bot values to 0', () => {
		expect(computeTotalEdits({ botChangeCount: undefined, humanChangeCount: 2 })).toEqual(2)
	})

	it('computes null human values to 0', () => {
		expect(computeTotalEdits({ botChangeCount: 3, humanChangeCount: null })).toEqual(3)
	})
	it('computes undefined human values to 0', () => {
		expect(computeTotalEdits({ botChangeCount: 5, humanChangeCount: undefined })).toEqual(5)
	})

	it('computes a sum of bots and humans', () => {
		expect(computeTotalEdits({ botChangeCount: 3, humanChangeCount: 5 })).toEqual(8)
	})
})
