import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

const STORAGE_KEY = 'theme'

/**
 * Определяет тему по умолчанию, если пользователь ещё не делал выбор.
 */
const getSystemTheme = () => {
  if (typeof window === 'undefined' || !window.matchMedia) return 'light'
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
}

/**
 * Применяет тему к <html>: переключает класс `dark` и нативный
 * `color-scheme` (нужен для корректной отрисовки системных элементов).
 */
const applyTheme = (theme) => {
  if (typeof document === 'undefined') return
  const root = document.documentElement
  root.classList.toggle('dark', theme === 'dark')
  root.style.colorScheme = theme
}

export const useThemeStore = defineStore('theme', () => {
  // Класс `dark` уже проставлен inline-скриптом из index.html,
  // поэтому синхронизируемся с текущим состоянием DOM.
  const theme = ref(
    typeof document !== 'undefined' && document.documentElement.classList.contains('dark')
      ? 'dark'
      : getSystemTheme()
  )

  const isDark = computed(() => theme.value === 'dark')

  const setTheme = (value) => {
    theme.value = value
    applyTheme(value)
    try {
      localStorage.setItem(STORAGE_KEY, value)
    } catch (e) {
      /* localStorage может быть недоступен */
    }
  }

  const toggleTheme = () => {
    setTheme(isDark.value ? 'light' : 'dark')
  }

  /**
   * Инициализация: применяет тему и подписывается на изменение
   * системной темы, пока пользователь не выбрал её вручную.
   */
  const init = () => {
    applyTheme(theme.value)

    if (typeof window !== 'undefined' && window.matchMedia) {
      const media = window.matchMedia('(prefers-color-scheme: dark)')
      const onChange = (event) => {
        let saved = null
        try {
          saved = localStorage.getItem(STORAGE_KEY)
        } catch (e) {
          /* ignore */
        }
        if (!saved) {
          theme.value = event.matches ? 'dark' : 'light'
          applyTheme(theme.value)
        }
      }
      media.addEventListener?.('change', onChange)
    }
  }

  return {
    theme,
    isDark,
    setTheme,
    toggleTheme,
    init
  }
})
