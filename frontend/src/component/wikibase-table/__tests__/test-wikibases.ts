import { WikibaseCategory, WikibaseType, type WbFragment } from '@/graphql/types'

const testWikibases: WbFragment[] = [
	{
		id: '1',
		title: 'Test Wikibase',
		description: 'An Example for the Purposes of Testing',
		urls: { baseUrl: 'test-wikibase-001.test' },
		quantityObservations: {},
		recentChangesObservations: {},
		wikibaseType: WikibaseType.Cloud
	},
	{
		id: '2',
		title: 'Test Wikibase #2',
		category: WikibaseCategory.FictionalAndCreativeWorks,
		urls: { baseUrl: 'test-wikibase-002.test' },
		quantityObservations: { mostRecent: { totalTriples: 14 } },
		recentChangesObservations: {},
		wikibaseType: WikibaseType.Suite
	},
	{
		id: '3',
		title: 'Test Wikibase #3',
		urls: { baseUrl: 'test-wikibase-003.test' },
		quantityObservations: { mostRecent: { totalTriples: 1 } },
		recentChangesObservations: { mostRecent: { botChangeCount: 100 } },
		wikibaseType: WikibaseType.Other
	},
	{
		id: '4',
		title: 'Test Wikibase #4',
		category: WikibaseCategory.TechnologyAndOpenSource,
		urls: { baseUrl: 'test-wikibase-004.test' },
		quantityObservations: { mostRecent: {} },
		recentChangesObservations: { mostRecent: { humanChangeCount: 31 } },
		wikibaseType: WikibaseType.Suite
	},
	{
		id: '5',
		title: 'Test Wikibase #5',
		urls: { baseUrl: 'test-wikibase-005.test' },
		quantityObservations: { mostRecent: { totalTriples: 300 } },
		recentChangesObservations: { mostRecent: { humanChangeCount: 31, botChangeCount: 69 } },
		wikibaseType: WikibaseType.Unknown
	}
]
export default testWikibases
