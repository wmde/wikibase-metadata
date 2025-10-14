import { CodegenConfig } from '@graphql-codegen/cli'

const config: CodegenConfig = {
  schema: 'https://wikibase-metadata.wmcloud.org/graphql',
  documents: ['../**/queries/*.ts'],
  generates: {
    './src/graphql/': { preset: 'client', presetConfig: { gqlTagName: 'gql' } },
    './src/graphql/types.ts': { plugins: ['typescript', 'typescript-operations'] }
  }
}
export default config
