import WikibaseTableContainer from '@/view/WikibaseTableContainer.vue'
import { createRouter, createWebHistory } from 'vue-router'

export const router = createRouter({
	history: createWebHistory(),
	routes: [
		{ path: '/', name: 'Wikibase Table', component: WikibaseTableContainer }
		// { path: '/users/:username/posts/:postId', component: UserPost }
	]
})
