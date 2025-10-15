import { vi } from 'vitest'

// Mock the ResizeObserver
export const ResizeObserverMock = vi.fn(() => ({
	observe: vi.fn(),
	unobserve: vi.fn(),
	disconnect: vi.fn()
}))
