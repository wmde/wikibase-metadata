import WikibaseDetailContainer from '@/view/WikibaseDetailContainer.vue'
import WikibaseTableContainer from '@/view/WikibaseTableContainer.vue'
import { createRouter, createWebHistory } from 'vue-router'

export const router = createRouter({
	history: createWebHistory(),
	routes: [
		{ path: '/', name: 'Wikibase Table', component: WikibaseTableContainer },
		{ path: '/wikibase/:id', name: 'Wikibase', component: WikibaseDetailContainer }
	]
})
