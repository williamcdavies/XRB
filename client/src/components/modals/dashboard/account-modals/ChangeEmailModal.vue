<script setup lang="ts">
import { ref } from 'vue'
import { useApi } from '@/composables/api'
import { useUser } from '@/composables/account'

const { user } = useUser()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'saved'): void
}>()

const email   = ref(user.value?.email ?? '')
const error   = ref('')
const loading = ref(false)

const { api } = useApi()

async function saveEmail() {
  error.value   = ''

  //prevent malicious input
  const invalidChars = /[;"'<>()\\]/;
  if(invalidChars.test(email.value)) {
    error.value = 'Email contains invalid characters.'
    return
  }

  // prevent non-real email
  const validEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if(!validEmail.test(email.value)) {
    error.value = 'Please enter a valid email address.'
    return
  }

  loading.value = true
  try {
    const response = await api.fetch('/api/account/update_email/', {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email.value, username: email.value }),
    })

    const data = await response.json()

    if (!response.ok) {
      error.value = data.error + ' Please try again.' || 'Failed to update email. Please try again.'
      return
    }

    emit('saved')
    emit('close')
  } catch (e) {
    console.error('saveEmail error:', e)
    error.value = 'Failed to update email. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="fixed inset-0 flex items-center justify-center z-50" @click="$emit('close')">
    <div class="select-none relative bg-xrb-menu-background rounded-3xl min-w-[30rem] max-w-[30rem] h-[36rem] p-6 z-50 flex flex-col"
      @click.stop>

      <div class="relative flex rounded-3xl">
        <div @click="$emit('close')">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
            stroke="currentColor" class="size-8">
            <path stroke-linecap="round" stroke-linejoin="round"
              d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
          </svg>
        </div>
        <p class="text-2xl absolute left-1/2 -translate-x-1/2 whitespace-nowrap">Change Email</p>
      </div>

      <div class="mt-6 rounded-xl flex-1 min-h-0 overflow-auto">
        <div class="mt-2 relative w-full">
          <input v-model="email" type="email" id="email" placeholder="example@gmail.com"
            class="peer min-w-full border border-gray-300 rounded-md px-3 pt-2 pb-2 focus:outline-none focus:border-xrb-text-accent" />
          <label for="email"
            class="peer absolute left-2 -top-2 bg-xrb-menu-background px-1 text-sm text-xrb-text-secondary peer-focus:text-xrb-text-accent">
            Email
          </label>
        </div>

        <p v-if="error" class="mt-3 text-sm text-xrb-text-warning-2">{{ error }}</p>
      </div>

      <div class="flex flex-row justify-end bottom-6 pt-6 rounded-3xl gap-2 w-full">
        <div @click="$emit('close')"
          class="hover:bg-xrb-menu-background-accent px-4 py-2 rounded-3xl flex items-center justify-center cursor-pointer text-xrb-accent-1">
          <p>Cancel</p>
        </div>
        <div @click="saveEmail"
          class="px-4 py-2 rounded-3xl flex items-center justify-center cursor-pointer"
          :class="loading ? 'bg-xrb-accent-1/50 cursor-not-allowed' : 'bg-xrb-accent-1'">
          <p>{{ loading ? 'Saving...' : 'Save' }}</p>
        </div>
      </div>

    </div>
  </div>
</template>

<style scoped></style>