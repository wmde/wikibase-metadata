import { WikibaseType } from '@/graphql/types'
import { useSingleWikiStore } from '@/stores/wikibase-store'
import { createPinia, setActivePinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { nextTick } from 'vue'

const { mockLoad, mockUseLazyQuery } = vi.hoisted(() => ({
	mockLoad: vi.fn().mockName('load'),
	mockUseLazyQuery: vi.fn().mockName('useLazyQuery')
}))

vi.mock('@vue/apollo-composable', () => ({
	provideApolloClient: vi.fn().mockName('provideApolloClient'),
	useLazyQuery: mockUseLazyQuery.mockReturnValueOnce({
		load: mockLoad,
		result: {
			value: {
				wikibase: {
					id: '1',
					title: 'Test Wikibase',
					description: 'Test Description',
					wikibaseType: WikibaseType.Test,
					urls: { baseUrl: 'wikibase.test', sparqlFrontendUrl: 'query.wikibase.test/frontend' },
					quantityObservations: {
						mostRecent: {
							observationDate: new Date(0),
							totalItems: 1,
							totalLexemes: 2,
							totalProperties: 3,
							totalTriples: 5
						}
					},
					recentChangesObservations: {
						mostRecent: { observationDate: new Date(0), botChangeCount: 8, humanChangeCount: 13 }
					},
					timeToFirstValueObservations: {
						mostRecent: { observationDate: new Date(0), initiationDate: new Date(0) }
					}
				}
			}
		},
		loading: { value: false },
		error: { value: false }
	})
}))

describe('useSingleWikiStore', async () => {
	beforeEach(() => {
		vi.resetAllMocks()
		setActivePinia(createPinia())
	})

	it('reflects query results', async () => {
		const store = useSingleWikiStore()

		expect(store.wikibase).toEqual({
			data: {
				wikibase: {
					description: 'Test Description',
					id: '1',
					quantityObservations: {
						mostRecent: {
							observationDate: new Date(0),
							totalItems: 1,
							totalLexemes: 2,
							totalProperties: 3,
							totalTriples: 5
						}
					},
					recentChangesObservations: {
						mostRecent: {
							botChangeCount: 8,
							humanChangeCount: 13,
							observationDate: new Date(0)
						}
					},
					timeToFirstValueObservations: {
						mostRecent: {
							initiationDate: new Date(0),
							observationDate: new Date(0)
						}
					},
					title: 'Test Wikibase',
					urls: {
						baseUrl: 'wikibase.test',
						sparqlFrontendUrl: 'query.wikibase.test/frontend'
					},
					wikibaseType: 'TEST'
				}
			},
			errorState: false,
			loading: false
		})
	})

	it('calls load on searchWikibase', async () => {
		const store = useSingleWikiStore()

		expect(mockLoad).toHaveBeenCalledTimes(0)

		store.searchWikibase(1)
		await nextTick()

		expect(mockLoad).toHaveBeenCalledTimes(1)
	})
})
