import WikibaseIcon from '@/component/wikibase-table/wikibase-detail-card/WikibaseIcon.vue'
import { vuetify } from '@/main'
import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

describe('WikibaseIcon', async () => {
	it('throws invalid', async () => {
		expect(() =>
			mount(WikibaseIcon, { global: { plugins: [vuetify] }, props: { baseUrl: 'wikibase.test' } })
		).toThrowError('Invalid base URL: wikibase.test')
	})
})
