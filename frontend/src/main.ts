import vuetify from '@/plugin/vuetify'
import { createPinia } from 'pinia'
import { createApp } from 'vue'
import VueMatomo from 'vue-matomo'
import App from './App.vue'

const app = createApp(App)

createApp(App)
	.use(VueMatomo, {
		host: 'stats.wikimedia.de',
		siteId: 12
	})
	.mount('#app')

app.use(vuetify)

app.use(createPinia())

app.mount('#app')
