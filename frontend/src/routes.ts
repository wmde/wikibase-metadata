import TTFVGraphContainer from '@/component/TTFVGraphContainer.vue'
import WikibaseTableContainer from '@/component/WikibaseTableContainer.vue'
import { ref, type Component } from 'vue'

type Route = {
	name: string
	component: Component
}

const routes: Record<string, Route> = {
	'/': { component: WikibaseTableContainer, name: 'Wikibase Table' },
	'/ttfv': { component: TTFVGraphContainer, name: 'Time to First Value' }
}

export const currentPath = ref(window.location.hash.slice(1))
window.addEventListener('hashchange', () => (currentPath.value = window.location.hash.slice(1)))

export default routes
