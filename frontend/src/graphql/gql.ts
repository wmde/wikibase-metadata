/* eslint-disable */
import * as types from './graphql'
import type { TypedDocumentNode as DocumentNode } from '@graphql-typed-document-node/core'

/**
 * Map of all GraphQL operations in the project.
 *
 * This map has several performance disadvantages:
 * 1. It is not tree-shakeable, so it will include all operations in the project.
 * 2. It is not minifiable, so the string of a GraphQL query will be multiple times inside the bundle.
 * 3. It does not support dead code elimination, so it will add unused operations.
 *
 * Therefore it is highly recommended to use the babel or swc plugin for production.
 * Learn more about it here: https://the-guild.dev/graphql/codegen/plugins/presets/preset-client#reducing-bundle-size
 */
type Documents = {
	'\n\tquery SingleWikibase($wikibaseId: Int!) {\n\t\twikibase(wikibaseId: $wikibaseId) {\n\t\t\t...SingleWikibase\n\t\t}\n\t}\n\n\tfragment SingleWikibase on Wikibase {\n\t\tid\n\t\ttitle\n\t\tcategory\n\t\tdescription\n\t\turls {\n\t\t\tbaseUrl\n\t\t\tsparqlFrontendUrl\n\t\t}\n\t\twikibaseType\n\t\tquantityObservations {\n\t\t\tmostRecent {\n\t\t\t\tobservationDate\n\t\t\t\ttotalItems\n\t\t\t\ttotalLexemes\n\t\t\t\ttotalProperties\n\t\t\t\ttotalTriples\n\t\t\t}\n\t\t}\n\t\trecentChangesObservations {\n\t\t\tmostRecent {\n\t\t\t\tobservationDate\n\t\t\t\tbotChangeCount\n\t\t\t\thumanChangeCount\n\t\t\t}\n\t\t}\n\t\ttimeToFirstValueObservations {\n\t\t\tmostRecent {\n\t\t\t\tinitiationDate\n\t\t\t}\n\t\t}\n\t}\n': typeof types.SingleWikibaseDocument
	'\n\tquery PageWikibases(\n\t\t$pageNumber: Int!\n\t\t$pageSize: Int!\n\t\t$wikibaseFilter: WikibaseFilterInput\n\t\t$sortBy: WikibaseSortInput\n\t) {\n\t\twikibaseList(\n\t\t\twikibaseFilter: $wikibaseFilter\n\t\t\tpageNumber: $pageNumber\n\t\t\tpageSize: $pageSize\n\t\t\tsortBy: $sortBy\n\t\t) {\n\t\t\tmeta {\n\t\t\t\ttotalCount\n\t\t\t}\n\t\t\tdata {\n\t\t\t\t...WB\n\t\t\t}\n\t\t}\n\t}\n\n\tfragment WB on Wikibase {\n\t\tid\n\t\ttitle\n\t\tcategory\n\t\tdescription\n\t\turls {\n\t\t\tbaseUrl\n\t\t}\n\t\twikibaseType\n\t\tquantityObservations {\n\t\t\tmostRecent {\n\t\t\t\ttotalTriples\n\t\t\t}\n\t\t}\n\t\trecentChangesObservations {\n\t\t\tmostRecent {\n\t\t\t\tbotChangeCount\n\t\t\t\thumanChangeCount\n\t\t\t}\n\t\t}\n\t}\n': typeof types.PageWikibasesDocument
}
const documents: Documents = {
	'\n\tquery SingleWikibase($wikibaseId: Int!) {\n\t\twikibase(wikibaseId: $wikibaseId) {\n\t\t\t...SingleWikibase\n\t\t}\n\t}\n\n\tfragment SingleWikibase on Wikibase {\n\t\tid\n\t\ttitle\n\t\tcategory\n\t\tdescription\n\t\turls {\n\t\t\tbaseUrl\n\t\t\tsparqlFrontendUrl\n\t\t}\n\t\twikibaseType\n\t\tquantityObservations {\n\t\t\tmostRecent {\n\t\t\t\tobservationDate\n\t\t\t\ttotalItems\n\t\t\t\ttotalLexemes\n\t\t\t\ttotalProperties\n\t\t\t\ttotalTriples\n\t\t\t}\n\t\t}\n\t\trecentChangesObservations {\n\t\t\tmostRecent {\n\t\t\t\tobservationDate\n\t\t\t\tbotChangeCount\n\t\t\t\thumanChangeCount\n\t\t\t}\n\t\t}\n\t\ttimeToFirstValueObservations {\n\t\t\tmostRecent {\n\t\t\t\tinitiationDate\n\t\t\t}\n\t\t}\n\t}\n':
		types.SingleWikibaseDocument,
	'\n\tquery PageWikibases(\n\t\t$pageNumber: Int!\n\t\t$pageSize: Int!\n\t\t$wikibaseFilter: WikibaseFilterInput\n\t\t$sortBy: WikibaseSortInput\n\t) {\n\t\twikibaseList(\n\t\t\twikibaseFilter: $wikibaseFilter\n\t\t\tpageNumber: $pageNumber\n\t\t\tpageSize: $pageSize\n\t\t\tsortBy: $sortBy\n\t\t) {\n\t\t\tmeta {\n\t\t\t\ttotalCount\n\t\t\t}\n\t\t\tdata {\n\t\t\t\t...WB\n\t\t\t}\n\t\t}\n\t}\n\n\tfragment WB on Wikibase {\n\t\tid\n\t\ttitle\n\t\tcategory\n\t\tdescription\n\t\turls {\n\t\t\tbaseUrl\n\t\t}\n\t\twikibaseType\n\t\tquantityObservations {\n\t\t\tmostRecent {\n\t\t\t\ttotalTriples\n\t\t\t}\n\t\t}\n\t\trecentChangesObservations {\n\t\t\tmostRecent {\n\t\t\t\tbotChangeCount\n\t\t\t\thumanChangeCount\n\t\t\t}\n\t\t}\n\t}\n':
		types.PageWikibasesDocument
}

/**
 * The gql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 *
 *
 * @example
 * ```ts
 * const query = gql(`query GetUser($id: ID!) { user(id: $id) { name } }`);
 * ```
 *
 * The query argument is unknown!
 * Please regenerate the types.
 */
export function gql(source: string): unknown

/**
 * The gql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function gql(
	source: '\n\tquery SingleWikibase($wikibaseId: Int!) {\n\t\twikibase(wikibaseId: $wikibaseId) {\n\t\t\t...SingleWikibase\n\t\t}\n\t}\n\n\tfragment SingleWikibase on Wikibase {\n\t\tid\n\t\ttitle\n\t\tcategory\n\t\tdescription\n\t\turls {\n\t\t\tbaseUrl\n\t\t\tsparqlFrontendUrl\n\t\t}\n\t\twikibaseType\n\t\tquantityObservations {\n\t\t\tmostRecent {\n\t\t\t\tobservationDate\n\t\t\t\ttotalItems\n\t\t\t\ttotalLexemes\n\t\t\t\ttotalProperties\n\t\t\t\ttotalTriples\n\t\t\t}\n\t\t}\n\t\trecentChangesObservations {\n\t\t\tmostRecent {\n\t\t\t\tobservationDate\n\t\t\t\tbotChangeCount\n\t\t\t\thumanChangeCount\n\t\t\t}\n\t\t}\n\t\ttimeToFirstValueObservations {\n\t\t\tmostRecent {\n\t\t\t\tinitiationDate\n\t\t\t}\n\t\t}\n\t}\n'
): (typeof documents)['\n\tquery SingleWikibase($wikibaseId: Int!) {\n\t\twikibase(wikibaseId: $wikibaseId) {\n\t\t\t...SingleWikibase\n\t\t}\n\t}\n\n\tfragment SingleWikibase on Wikibase {\n\t\tid\n\t\ttitle\n\t\tcategory\n\t\tdescription\n\t\turls {\n\t\t\tbaseUrl\n\t\t\tsparqlFrontendUrl\n\t\t}\n\t\twikibaseType\n\t\tquantityObservations {\n\t\t\tmostRecent {\n\t\t\t\tobservationDate\n\t\t\t\ttotalItems\n\t\t\t\ttotalLexemes\n\t\t\t\ttotalProperties\n\t\t\t\ttotalTriples\n\t\t\t}\n\t\t}\n\t\trecentChangesObservations {\n\t\t\tmostRecent {\n\t\t\t\tobservationDate\n\t\t\t\tbotChangeCount\n\t\t\t\thumanChangeCount\n\t\t\t}\n\t\t}\n\t\ttimeToFirstValueObservations {\n\t\t\tmostRecent {\n\t\t\t\tinitiationDate\n\t\t\t}\n\t\t}\n\t}\n']
/**
 * The gql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function gql(
	source: '\n\tquery PageWikibases(\n\t\t$pageNumber: Int!\n\t\t$pageSize: Int!\n\t\t$wikibaseFilter: WikibaseFilterInput\n\t\t$sortBy: WikibaseSortInput\n\t) {\n\t\twikibaseList(\n\t\t\twikibaseFilter: $wikibaseFilter\n\t\t\tpageNumber: $pageNumber\n\t\t\tpageSize: $pageSize\n\t\t\tsortBy: $sortBy\n\t\t) {\n\t\t\tmeta {\n\t\t\t\ttotalCount\n\t\t\t}\n\t\t\tdata {\n\t\t\t\t...WB\n\t\t\t}\n\t\t}\n\t}\n\n\tfragment WB on Wikibase {\n\t\tid\n\t\ttitle\n\t\tcategory\n\t\tdescription\n\t\turls {\n\t\t\tbaseUrl\n\t\t}\n\t\twikibaseType\n\t\tquantityObservations {\n\t\t\tmostRecent {\n\t\t\t\ttotalTriples\n\t\t\t}\n\t\t}\n\t\trecentChangesObservations {\n\t\t\tmostRecent {\n\t\t\t\tbotChangeCount\n\t\t\t\thumanChangeCount\n\t\t\t}\n\t\t}\n\t}\n'
): (typeof documents)['\n\tquery PageWikibases(\n\t\t$pageNumber: Int!\n\t\t$pageSize: Int!\n\t\t$wikibaseFilter: WikibaseFilterInput\n\t\t$sortBy: WikibaseSortInput\n\t) {\n\t\twikibaseList(\n\t\t\twikibaseFilter: $wikibaseFilter\n\t\t\tpageNumber: $pageNumber\n\t\t\tpageSize: $pageSize\n\t\t\tsortBy: $sortBy\n\t\t) {\n\t\t\tmeta {\n\t\t\t\ttotalCount\n\t\t\t}\n\t\t\tdata {\n\t\t\t\t...WB\n\t\t\t}\n\t\t}\n\t}\n\n\tfragment WB on Wikibase {\n\t\tid\n\t\ttitle\n\t\tcategory\n\t\tdescription\n\t\turls {\n\t\t\tbaseUrl\n\t\t}\n\t\twikibaseType\n\t\tquantityObservations {\n\t\t\tmostRecent {\n\t\t\t\ttotalTriples\n\t\t\t}\n\t\t}\n\t\trecentChangesObservations {\n\t\t\tmostRecent {\n\t\t\t\tbotChangeCount\n\t\t\t\thumanChangeCount\n\t\t\t}\n\t\t}\n\t}\n']

export function gql(source: string) {
	return (documents as any)[source] ?? {}
}

export type DocumentType<TDocumentNode extends DocumentNode<any, any>> =
	TDocumentNode extends DocumentNode<infer TType, any> ? TType : never
