// src/utils/wikibaseUrls.test.ts
import { describe, it, expect } from 'vitest'
import getActionApiUrl from '@/util/getActionApiUrl'

describe('getActionApiUrl', () => {
	it('returns null if scriptPath is null', () => {
		expect(getActionApiUrl('https://example.com', null)).toBeNull()
	})

	it('returns null if scriptPath is undefined', () => {
		expect(getActionApiUrl('https://example.com', undefined)).toBeNull()
	})

	it('handles empty scriptPaths', () => {
		expect(getActionApiUrl('https://example.com', '')).toBe('https://example.com/api.php')
		expect(getActionApiUrl('https://example.com', '/')).toBe('https://example.com/api.php')
	})

	it('removes extra trailing and leading slashes in scriptPath', () => {
		const scriptPaths = ['script', '/script', 'script/', '/script/']

		for (const scriptPath of scriptPaths) {
			expect(getActionApiUrl('https://example.com', scriptPath)).toBe(
				`https://example.com/script/api.php`
			)
		}
	})
})
