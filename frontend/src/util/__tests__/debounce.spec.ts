import { debounce } from '@/util/debounce'
import { describe, expect, it, vi } from 'vitest'

function sleep(milliseconds: number) {
	return new Promise((resolve) => {
		setTimeout(resolve, milliseconds)
	})
}

describe('debounce', async () => {
	it('calls debouncedFunc only once in given period', async () => {
		const testFn = vi.fn().mockName('testFn')
		const [debouncedFunc] = debounce((v: string) => testFn(v), 100)

		debouncedFunc('One')
		await sleep(10)

		debouncedFunc('Two')
		await sleep(10)

		debouncedFunc('Three')

		await sleep(100)

		expect(testFn).toBeCalledTimes(1)
		expect(testFn).toBeCalledWith('Three')
	})
})
