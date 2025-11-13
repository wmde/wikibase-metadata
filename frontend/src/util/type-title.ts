import { WikibaseType } from '@/graphql/types'

const typeTitle = (t: WikibaseType | null | undefined): string => {
	switch (t) {
		case WikibaseType.Cloud:
			return 'Wikibase Cloud'
		case WikibaseType.Other:
			return 'Other'
		case WikibaseType.Suite:
			return 'Self-Hosted'
		case WikibaseType.Test:
			return 'Test'
		default:
			return 'Unknown'
	}
}

export default typeTitle
