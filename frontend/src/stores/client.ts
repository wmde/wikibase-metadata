import { ApolloClient, ApolloLink, HttpLink, InMemoryCache } from '@apollo/client/core'

const cache = new InMemoryCache()
const cloudLink = ApolloLink.from([
	new HttpLink({ uri: 'https://wikibase-metadata.wmcloud.org/graphql' })
])

export const apolloClient = new ApolloClient({ cache, link: cloudLink })
