import WikibaseTableContainer from '@/component/WikibaseTableContainer.vue'
import { ref, type Component } from 'vue'

type Route = {
	name: string
	component: Component
}

const routes: Record<string, Route> = {
	'/': { component: WikibaseTableContainer, name: 'Wikibase Table' }
}

export const currentPath = ref(window.location.hash.slice(1))
window.addEventListener('hashchange', () => (currentPath.value = window.location.hash.slice(1)))

export default routes
