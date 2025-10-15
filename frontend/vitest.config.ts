import { fileURLToPath } from 'node:url'
import { configDefaults, defineConfig, mergeConfig } from 'vitest/config'
import viteConfig from './vite.config'

export default mergeConfig(
	viteConfig,
	defineConfig({
		test: {
			coverage: {
				provider: 'istanbul',
				thresholds: {
					branches: 95,
					functions: 95,
					lines: 95,
					statements: 95
				}
			},
			environment: 'jsdom',
			exclude: [...configDefaults.exclude, 'e2e/**'],
			root: fileURLToPath(new URL('./', import.meta.url))
		}
	})
)
