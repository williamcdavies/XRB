const COOKIE_NAME = 'xrb-theme'
const VALID_THEMES = ['dark', 'light'] as const
const DEFAULT_THEME: Theme = 'dark'

type Theme = typeof VALID_THEMES[number]

function getCookieTheme(): Theme {
  const match = document.cookie
    .split('; ')
    .find(row => row.startsWith(COOKIE_NAME + '='))
  const value = match?.split('=')[1]
  return (VALID_THEMES as readonly string[]).includes(value ?? '') 
    ? (value as Theme) 
    : DEFAULT_THEME
}

export function applyTheme(theme: Theme): void {
  document.documentElement.setAttribute('data-theme', theme)
  document.cookie = `${COOKIE_NAME}=${theme}; path=/; max-age=${60 * 60 * 24 * 365}; SameSite=Lax`
}

export function getTheme(): Theme {
  return (document.documentElement.getAttribute('data-theme') as Theme | null) 
    ?? getCookieTheme()
}

// Apply immediately on import
applyTheme(getCookieTheme())