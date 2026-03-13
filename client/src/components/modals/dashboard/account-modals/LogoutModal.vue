<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '@/composables/auth'

const emit = defineEmits<{
  (e: 'close'): void
}>()

const router = useRouter()
const { clearAccessToken } = useAuth()
const error   = ref('')
const loading = ref(false)

async function logout() {
  error.value   = ''
  loading.value = true
  try {
    await fetch('/api/account/logout/', { method: 'POST', credentials: 'include' })
    clearAccessToken()
    router.push('/')
  } catch (e) {
    console.error('logout error:', e)
    error.value = 'Failed to log out. Please try again.'
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
        <p class="text-2xl absolute left-1/2 -translate-x-1/2 whitespace-nowrap">Log Out</p>
      </div>
      <div class="justify-center rounded-xl flex-1 min-h-0 flex flex-col items-center overflow-auto">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1"
          stroke="currentColor" class="stroke-xrb-text-warning-1 size-36">
          <path stroke-linecap="round" stroke-linejoin="round"
            d="M8.25 9V5.25A2.25 2.25 0 0 1 10.5 3h6a2.25 2.25 0 0 1 2.25 2.25v13.5A2.25 2.25 0 0 1 16.5 21h-6a2.25 2.25 0 0 1-2.25-2.25V15m-3 0-3-3m0 0 3-3m-3 3H15" />
        </svg>
        <p class="mt-6 font-bold text-xl text-center">Are you sure you want to log out?</p>
        <p class="mt-2 text-center">You will need to log in again to access your account.</p>
        <p v-if="error" class="mt-3 text-sm text-xrb-text-warning-2">{{ error }}</p>
      </div>
      <div class="flex flex-row justify-end bottom-6 pt-6 rounded-3xl gap-2 w-full">
        <div @click="$emit('close')"
          class="hover:bg-xrb-menu-background-accent px-4 py-2 rounded-3xl cursor-pointer text-xrb-accent-1">
          <p>Cancel</p>
        </div>
        <div @click="logout"
          class="px-4 py-2 rounded-3xl cursor-pointer"
          :class="loading ? 'bg-xrb-text-warning-1/50 cursor-not-allowed' : 'bg-xrb-text-warning-1 hover:bg-xrb-text-warning-2'">
          <p>{{ loading ? 'Logging out...' : 'Log Out' }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>