import { CodegenConfig } from '@graphql-codegen/cli'

const config: CodegenConfig = {
  schema: 'https://wikibase-metadata.wmcloud.org/graphql',
  //   documents: ["src/**/*.tsx"],
  generates: {
    './src/graphql/': {
      preset: 'client',
      presetConfig: {
        gqlTagName: 'gql',
      },
    },
    './src/graphql/types.ts': {
      plugins: ['typescript', 'typescript-operations'],
    },
  },
  ignoreNoDocuments: true,
}
export default config
