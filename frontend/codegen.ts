import { CodegenConfig } from '@graphql-codegen/cli'

const config: CodegenConfig = {
	schema: 'https://wikibase-metadata.wmcloud.org/graphql',
	documents: ['../frontend/src/graphql/queries/*.ts'],
	generates: {
		'./src/graphql/': {
			preset: 'client',
			config: { useTypeImports: true, scalars: { Union: 'number', DateTime: 'Date' } },
			presetConfig: { gqlTagName: 'gql' }
		},
		'./src/graphql/types.ts': {
			config: { useTypeImports: true, scalars: { Union: 'number', DateTime: 'Date' } },
			plugins: ['typescript', 'typescript-operations']
		}
	}
}
export default config
