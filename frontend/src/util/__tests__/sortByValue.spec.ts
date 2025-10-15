import { describe, expect, it } from 'vitest'
import sortByValue, { compareByValue } from '../sortByValue'

describe('sortByValue', () => {
	it('sorts an empty list', () => {
		expect(sortByValue([], (i) => i)).toEqual([])
	})

	it('sorts a single-value list', () => {
		expect(sortByValue([1], (i) => i)).toEqual([1])
	})

	it('sorts a sorted list', () => {
		expect(
			sortByValue(
				[
					{ a: 1, b: 2 },
					{ a: 2, b: -2 },
					{ a: 4, b: 0 }
				],
				(i) => i.a
			)
		).toEqual([
			{ a: 1, b: 2 },
			{ a: 2, b: -2 },
			{ a: 4, b: 0 }
		])
	})

	it('sorts an unsorted list', () => {
		expect(
			sortByValue(
				[
					{ a: 1, b: 2 },
					{ a: 2, b: -2 },
					{ a: 4, b: 0 }
				],
				(i) => i.b
			)
		).toEqual([
			{ a: 2, b: -2 },
			{ a: 4, b: 0 },
			{ a: 1, b: 2 }
		])
	})
})

describe('compareByValue', () => {
	it('compares nullish-nullish values equal', () => {
		expect(
			compareByValue(
				{ a: undefined, b: undefined, c: 6, d: 6, e: 6, f: 16 },
				{ a: null, b: -12, c: null, d: 16, e: 6, f: 6 },
				(v) => v.a
			)
		).toEqual(0)
	})

	it('compares nullish-nonnullish values inequal', () => {
		expect(
			compareByValue(
				{ a: undefined, b: undefined, c: 6, d: 6, e: 6, f: 16 },
				{ a: null, b: -12, c: null, d: 16, e: 6, f: 6 },
				(v) => v.b
			)
		).toEqual(-1)
	})

	it('compares nonnullish-nullish values inequal', () => {
		expect(
			compareByValue(
				{ a: undefined, b: undefined, c: 6, d: 6, e: 6, f: 16 },
				{ a: null, b: -12, c: null, d: 16, e: 6, f: 6 },
				(v) => v.c
			)
		).toEqual(1)
	})

	it('compares nonnullish-nonnullish values in/equal', () => {
		expect(
			compareByValue(
				{ a: undefined, b: undefined, c: 6, d: 6, e: 6, f: 16 },
				{ a: null, b: -12, c: null, d: 16, e: 6, f: 6 },
				(v) => v.d
			)
		).toEqual(-1)
		expect(
			compareByValue(
				{ a: undefined, b: undefined, c: 6, d: 6, e: 6, f: 16 },
				{ a: null, b: -12, c: null, d: 16, e: 6, f: 6 },
				(v) => v.e
			)
		).toEqual(0)
		expect(
			compareByValue(
				{ a: undefined, b: undefined, c: 6, d: 6, e: 6, f: 16 },
				{ a: null, b: -12, c: null, d: 16, e: 6, f: 6 },
				(v) => v.f
			)
		).toEqual(1)
	})
})
