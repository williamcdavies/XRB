<script setup lang="ts">
import { ref, computed } from 'vue'
import { useApi } from '@/composables/api'
import { useUser } from '@/composables/account'

const { user } = useUser()
const emit = defineEmits<{
  (e: 'close'): void
  (e: 'saved'): void
}>()

const VALID_LANGUAGES = [
  'Afrikaans', 'Albanian', 'Amharic', 'Arabic', 'Armenian', 'Azerbaijani',
  'Basque', 'Belarusian', 'Bengali', 'Bosnian', 'Bulgarian', 'Catalan',
  'Cebuano', 'Chinese (Simplified)', 'Chinese (Traditional)', 'Corsican',
  'Croatian', 'Czech', 'Danish', 'Dutch', 'English', 'Esperanto', 'Estonian',
  'Finnish', 'French', 'Frisian', 'Galician', 'Georgian', 'German', 'Greek',
  'Gujarati', 'Haitian Creole', 'Hausa', 'Hawaiian', 'Hebrew', 'Hindi',
  'Hmong', 'Hungarian', 'Icelandic', 'Igbo', 'Indonesian', 'Irish', 'Italian',
  'Japanese', 'Javanese', 'Kannada', 'Kazakh', 'Khmer', 'Kinyarwanda',
  'Korean', 'Kurdish', 'Kyrgyz', 'Lao', 'Latin', 'Latvian', 'Lithuanian',
  'Luxembourgish', 'Macedonian', 'Malagasy', 'Malay', 'Malayalam', 'Maltese',
  'Maori', 'Marathi', 'Mongolian', 'Myanmar', 'Nepali', 'Norwegian', 'Nyanja',
  'Odia', 'Pashto', 'Persian', 'Polish', 'Portuguese', 'Punjabi', 'Romanian',
  'Russian', 'Samoan', 'Scots Gaelic', 'Serbian', 'Sesotho', 'Shona',
  'Sindhi', 'Sinhala', 'Slovak', 'Slovenian', 'Somali', 'Spanish', 'Sundanese',
  'Swahili', 'Swedish', 'Tagalog', 'Tajik', 'Tamil', 'Tatar', 'Telugu',
  'Thai', 'Turkish', 'Turkmen', 'Ukrainian', 'Urdu', 'Uyghur', 'Uzbek',
  'Vietnamese', 'Welsh', 'Xhosa', 'Yiddish', 'Yoruba', 'Zulu',
]

const language     = ref(user.value?.preferred_language ?? '')
const error        = ref('')
const loading      = ref(false)
const showDropdown = ref(false)
const { api }      = useApi()

const filteredLanguages = computed(() => {
  const query = language.value.trim().toLowerCase()
  if (!query) return []
  return VALID_LANGUAGES.filter(l => l.toLowerCase().startsWith(query)).slice(0, 8)
})

function onInput() {
  error.value        = ''
  showDropdown.value = filteredLanguages.value.length > 0
}

function selectLanguage(lang: string) {
  language.value     = lang
  showDropdown.value = false
}

function isValidLanguage() {
  return VALID_LANGUAGES.some(l => l.toLowerCase() === language.value.trim().toLowerCase())
}

async function saveLanguage() {
  error.value = ''
  if (!isValidLanguage()) {
    error.value = 'Please enter a valid language.'
    return
  }
  loading.value = true
  try {
    const response = await api.fetch('/api/account/update_language/', {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ preferred_language: language.value.trim() }),
    })
    if (!response.ok) throw new Error(`${response.status}`)
    emit('saved')
    emit('close')
  } catch (e) {
    console.error('saveLanguage error:', e)
    error.value = 'Failed to update language. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="fixed inset-0 flex items-center justify-center z-50" @click="$emit('close')">
    <div
      class="select-none relative bg-xrb-menu-background rounded-3xl min-w-[30rem] max-w-[30rem] h-[36rem] p-6 z-50 flex flex-col"
      @click.stop>
      <div class="relative flex rounded-3xl">
        <div @click="$emit('close')">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
            stroke="currentColor" class="size-8">
            <path stroke-linecap="round" stroke-linejoin="round"
              d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
          </svg>
        </div>
        <p class="text-2xl absolute left-1/2 -translate-x-1/2 whitespace-nowrap">Change Language</p>
      </div>

      <div class="mt-6 rounded-xl flex-1 min-h-0 overflow-auto">
        <div class="mt-2 relative w-full">
          <input
            v-model="language"
            @input="onInput"
            @blur="showDropdown = false"
            type="text"
            id="language"
            placeholder="Preferred Language"
            class="peer min-w-full border border-gray-300 rounded-md px-3 pt-2 pb-2 focus:outline-none focus:border-xrb-text-accent"
          />
          <label for="language"
            class="peer absolute left-2 -top-2 bg-xrb-menu-background px-1 text-sm text-xrb-text-secondary peer-focus:text-xrb-text-accent">
            Preferred Language
          </label>

          <ul v-if="showDropdown && filteredLanguages.length"
            class="absolute z-10 w-full bg-xrb-menu-background border border-gray-300 rounded-md mt-1 max-h-40 overflow-y-auto shadow-md">
            <li
              v-for="lang in filteredLanguages"
              :key="lang"
              @mousedown.prevent="selectLanguage(lang)"
              class="px-3 py-2 cursor-pointer hover:bg-xrb-menu-background-accent text-sm">
              {{ lang }}
            </li>
          </ul>
        </div>
        <p v-if="error" class="mt-3 text-sm text-xrb-text-warning-2">{{ error }}</p>
      </div>

      <div class="flex flex-row justify-end bottom-6 pt-6 rounded-3xl gap-2 w-full">
        <div @click="$emit('close')"
          class="hover:bg-xrb-menu-background-accent px-4 py-2 rounded-3xl flex items-center justify-center cursor-pointer text-xrb-accent-1">
          <p>Cancel</p>
        </div>
        <div @click="saveLanguage"
          class="px-4 py-2 rounded-3xl flex items-center justify-center cursor-pointer"
          :class="loading ? 'bg-xrb-accent-1/50 cursor-not-allowed' : 'bg-xrb-accent-1'">
          <p>{{ loading ? 'Saving...' : 'Save' }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>