import vuetify from '@/plugin/vuetify'
import { createPinia } from 'pinia'
import { createApp } from 'vue'
import App from './App.vue'
import { router } from './router'

const app = createApp(App)

app.use(vuetify)

app.use(createPinia())

app.use(router)

app.mount('#app')
