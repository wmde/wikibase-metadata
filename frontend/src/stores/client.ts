import { ApolloClient, ApolloLink, HttpLink, InMemoryCache } from '@apollo/client/core'

const cache = new InMemoryCache()
const cloudLink = ApolloLink.from([new HttpLink({ uri: import.meta.env.VITE_BACKEND_URL })])

export const apolloClient = new ApolloClient({ cache, link: cloudLink })
