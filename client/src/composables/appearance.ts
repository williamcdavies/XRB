import { ref, onMounted } from 'vue'
import { applyTheme, getTheme } from '@/appearance'

export function useAppearance() {
  const isDark = ref<boolean>(true)

  onMounted(() => {
    isDark.value = getTheme() === 'dark'
  })

  function toggleTheme(): void {
    isDark.value = !isDark.value
    applyTheme(isDark.value ? 'dark' : 'light')
  }

  return { isDark, toggleTheme }
}