<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useApi } from '@/composables/api'

const emit = defineEmits<{
  (e: 'close'): void
}>()

const router  = useRouter()
const { api } = useApi()
const error   = ref('')
const loading = ref(false)

async function deleteAccount() {
  error.value   = ''
  loading.value = true
  try {
    const response = await api.fetch('/api/account/delete_account/', {
      method: 'DELETE',
    })
    if (!response.ok) throw new Error(`${response.status}`)
    router.push('/')
  } catch (e) {
    console.error('deleteAccount error:', e)
    error.value = 'Failed to delete account. Please try again.'
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
        <p class="text-2xl absolute left-1/2 -translate-x-1/2 whitespace-nowrap">Delete Account</p>
      </div>

      <div class="justify-center rounded-xl flex-1 min-h-0 flex flex-col items-center overflow-auto">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1"
          stroke="currentColor" class="stroke-xrb-text-warning-1 size-36">
          <path stroke-linecap="round" stroke-linejoin="round"
            d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
        </svg>
        <p class="mt-6 font-bold text-xl text-center">Are you sure you want to delete your account?</p>
        <p class="mt-2 text-center">This action can not be undone.</p>
        <p v-if="error" class="mt-3 text-sm text-xrb-text-warning-2">{{ error }}</p>
      </div>

      <div class="flex flex-row justify-end bottom-6 pt-6 rounded-3x gap-2 w-full">
        <div @click="$emit('close')"
          class="hover:bg-xrb-menu-background-accent px-4 py-2 rounded-3xl cursor-pointer text-xrb-accent-1">
          <p>Cancel</p>
        </div>
        <div @click="deleteAccount"
          class="px-4 py-2 rounded-3xl cursor-pointer"
          :class="loading ? 'bg-xrb-text-warning-1/50 cursor-not-allowed' : 'bg-xrb-text-warning-1 hover:bg-xrb-text-warning-2'">
          <p>{{ loading ? 'Deleting...' : 'Delete Account' }}</p>
        </div>
      </div>
    </div>
  </div>
</template>



<style scoped></style>