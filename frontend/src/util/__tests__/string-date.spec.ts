import stringDate from '@/util/string-date'
import { describe, expect, it } from 'vitest'

describe('stringDate', () => {
	it('returns date from date', () => {
		const returned = stringDate('2025-01-01:00:00:00')

		expect(returned.getFullYear()).toEqual(2025)
		expect(returned.getMonth()).toEqual(0)
		expect(returned.getDate()).toEqual(1)
		expect(returned.getHours()).toEqual(0)
		expect(returned.getMinutes()).toEqual(0)
		expect(returned.getSeconds()).toEqual(0)
	})
})
