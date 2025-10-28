import uniqueValues from '@/util/uniqueValues'
import { describe, expect, it } from 'vitest'

describe('uniqueValues', () => {
	it('uniques an empty list', () => {
		expect(uniqueValues([], (i) => i)).toEqual([])
	})

	it('uniques a single-value list', () => {
		expect(uniqueValues(['a'], (i) => i)).toEqual(['a'])
	})

	it('uniques a number list', () => {
		expect(uniqueValues([1, 1, 2, 3], (i) => i)).toEqual([1, 2, 3])
	})

	it('uniques a string list', () => {
		expect(uniqueValues(['a', 'a', 'b', 'a'], (i) => i)).toEqual(['b', 'a'])
	})

	it('uniques an object list by key', () => {
		expect(
			uniqueValues(
				[
					{ a: 1, b: 4 },
					{ a: 2, b: 4 },
					{ a: 1, b: 5 },
					{ a: 3, b: 4 }
				],
				(i) => i.a
			)
		).toEqual([
			{ a: 2, b: 4 },
			{ a: 1, b: 5 },
			{ a: 3, b: 4 }
		])
		expect(
			uniqueValues(
				[
					{ a: 1, b: 4 },
					{ a: 2, b: 4 },
					{ a: 1, b: 5 },
					{ a: 3, b: 4 }
				],
				(i) => i.b
			)
		).toEqual([
			{ a: 1, b: 5 },
			{ a: 3, b: 4 }
		])
	})
})
