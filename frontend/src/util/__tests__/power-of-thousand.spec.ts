import powerOfThousand from '@/util/power-of-thousand'
import { describe, expect, it } from 'vitest'

describe('powerOfThousand', () => {
	it('returns under 1k', () => {
		expect(powerOfThousand(100)).toEqual({ power: 0, value: 100 })
	})

	it('returns over 1k', () => {
		expect(powerOfThousand(10000)).toEqual({ power: 1, value: 10 })
	})
})
