import WikibaseTableContainer from '@/component/WikibaseTableContainer.vue'
import type { Component } from 'vue'

type Route = {
	name: string
	component: Component
}

const routes: Record<string, Route> = {
	'/': { component: WikibaseTableContainer, name: 'Wikibase Table' }
}

export default routes
