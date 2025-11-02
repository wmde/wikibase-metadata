import compareByValue from '@/util/compare-by-value'
import { describe, expect, it } from 'vitest'

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
