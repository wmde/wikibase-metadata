import { CodegenConfig } from '@graphql-codegen/cli'

const config: CodegenConfig = {
	schema: 'https://wikibase-metadata.wmcloud.org/graphql',
	generates: {
		'./src/graphql/': {
			preset: 'client',
			config: { useTypeImports: true, scalars: { Union: 'number', DateTime: 'Date' } },
			presetConfig: { gqlTagName: 'gql' }
		},
		'./src/graphql/types.ts': {
			config: { useTypeImports: true, scalars: { Union: 'number', DateTime: 'Date' } },
			documents: ['../frontend/src/graphql/queries/*.ts'],
			// plugins: ['typescript', 'typescript-operations'],
			plugins: ['typescript-operations'],
			presetConfig: { gqlTagName: 'gql' }
		}
	}
}
export default config
