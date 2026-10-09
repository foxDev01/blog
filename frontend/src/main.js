import { createApp } from 'vue'
import { createPinia } from 'pinia'
import Toast, { POSITION } from 'vue-toastification'
import router from './router'
import App from './App.vue'

import './assets/css/main.css'
import './assets/css/dark.css'
import 'vue-toastification/dist/index.css'

import { useThemeStore } from './stores/theme'

const app = createApp(App)
const pinia = createPinia()

// Настройка Toast уведомлений
const toastOptions = {
  position: POSITION.TOP_RIGHT,
  timeout: 5000,
  closeOnClick: true,
  pauseOnFocusLoss: true,
  pauseOnHover: true,
  draggable: true,
  draggablePercent: 0.6,
  showCloseButtonOnHover: false,
  hideProgressBar: false,
  closeButton: 'button',
  icon: true,
  rtl: false,
  maxToasts: 3,
  newestOnTop: true
}

app.use(pinia)

// Инициализируем тему (сохраняется в localStorage)
useThemeStore().init()

app.use(router)
app.use(Toast, toastOptions)

app.mount('#app')