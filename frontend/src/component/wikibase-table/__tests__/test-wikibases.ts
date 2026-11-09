import type { WbFragment } from '@/graphql/types'

const testWikibases: WbFragment[] = [
	{
		id: '1',
		title: 'Test Wikibase',
		category: null,
		description: 'An Example for the Purposes of Testing',
		urls: { baseUrl: 'test-wikibase-001.test' },
		quantityObservations: { mostRecent: null },
		recentChangesObservations: { mostRecent: null },
		wikibaseType: 'CLOUD'
	},
	{
		id: '2',
		title: 'Test Wikibase #2',
		category: 'FICTIONAL_AND_CREATIVE_WORKS',
		description: null,
		urls: { baseUrl: 'test-wikibase-002.test' },
		quantityObservations: { mostRecent: { totalTriples: 14 } },
		recentChangesObservations: { mostRecent: null },
		wikibaseType: 'SUITE'
	},
	{
		id: '3',
		title: 'Test Wikibase #3',
		category: null,
		description: null,
		urls: { baseUrl: 'test-wikibase-003.test' },
		quantityObservations: { mostRecent: { totalTriples: 1 } },
		recentChangesObservations: { mostRecent: { botChangeCount: 100, humanChangeCount: null } },
		wikibaseType: 'OTHER'
	},
	{
		id: '4',
		title: 'Test Wikibase #4',
		category: 'TECHNOLOGY_AND_OPEN_SOURCE',
		description: null,
		urls: { baseUrl: 'test-wikibase-004.test' },
		quantityObservations: { mostRecent: { totalTriples: null } },
		recentChangesObservations: { mostRecent: { botChangeCount: null, humanChangeCount: 31 } },
		wikibaseType: 'SUITE'
	},
	{
		id: '5',
		title: 'Test Wikibase #5',
		category: null,
		description: null,
		urls: { baseUrl: 'test-wikibase-005.test' },
		quantityObservations: { mostRecent: { totalTriples: 300 } },
		recentChangesObservations: { mostRecent: { humanChangeCount: 31, botChangeCount: 69 } },
		wikibaseType: 'UNKNOWN'
	}
]
export default testWikibases
