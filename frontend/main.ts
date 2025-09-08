import { createApp } from 'vue'
// Load Codex design tokens first so CSS variables are available globally
import '@wikimedia/codex-design-tokens/theme-wikimedia-ui.css'
// Codex components CSS
import '@wikimedia/codex/dist/codex.style.css'
// App styles that use the tokens
import './style.css'
import App from './App.vue'

createApp(App).mount('#app')
