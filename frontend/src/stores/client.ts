import { ApolloClient, ApolloLink, HttpLink, InMemoryCache } from '@apollo/client/core'

console.log(process.env.BACKEND_URL)

const cache = new InMemoryCache()
const cloudLink = ApolloLink.from([new HttpLink({ uri: process.env.BACKEND_URL })])

export const apolloClient = new ApolloClient({ cache, link: cloudLink })
