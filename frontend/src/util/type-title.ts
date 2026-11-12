import type { WikibaseType } from '@/graphql/types'

const typeTitle = (t: WikibaseType | null | undefined): string => {
	switch (t) {
		case 'CLOUD':
			return 'Wikibase Cloud'
		case 'OTHER':
			return 'Other'
		case 'SUITE':
			return 'Self-Hosted'
		case 'TEST':
			return 'Test'
		default:
			return 'Unknown'
	}
}

export default typeTitle
