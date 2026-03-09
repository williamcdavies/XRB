<script setup lang="ts">
import { ref } from 'vue'
import { useApi } from '@/composables/api'
import { useUser } from '@/composables/account'

const { user } = useUser()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'saved'): void
}>()

const accountType = ref(user.value?.type ?? '')
const error       = ref('')
const loading     = ref(false)

const { api } = useApi()

async function saveType() {
  error.value   = ''
  loading.value = true
  try {
    const response = await api.fetch('/api/account/update_type/', {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ type: accountType.value }),
    })

    if (!response.ok) {
      throw new Error(`${response.status}`)
    }

    emit('saved')
    emit('close')
  } catch (e) {
    console.error('saveType error:', e)
    error.value = 'Failed to update account type. Please try again.'
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
        <p class="text-2xl absolute left-1/2 -translate-x-1/2 whitespace-nowrap">Change Account Type</p>
      </div>

      <div class="mt-6 rounded-xl flex-1 min-h-0 overflow-auto">
        <p class="mt-4 pl-4 font-semibold text-l">Account Type</p>
        <div class="p-4 space-y-4">

          <label class="flex items-center gap-2 cursor-pointer">
            <input v-model="accountType" type="radio" name="accountType" value="Researcher" class="peer hidden" />
            <span class="w-6 h-6 rounded-full border-2 border-gray-400"
              :class="accountType === 'Researcher' ? 'bg-xrb-accent-1 border-xrb-accent-1' : ''">
            </span>
            <p>Researcher</p>
          </label>

          <label class="flex items-center gap-2 cursor-pointer">
            <input v-model="accountType" type="radio" name="accountType" value="Student" class="peer hidden" />
            <span class="w-6 h-6 rounded-full border-2 border-gray-400"
              :class="accountType === 'Student' ? 'bg-xrb-accent-1 border-xrb-accent-1' : ''">
            </span>
            <p>Student</p>
          </label>

        </div>

        <p v-if="error" class="mt-3 px-4 text-sm text-xrb-text-warning-2">{{ error }}</p>
      </div>

      <div class="flex flex-row justify-end bottom-6 pt-6 rounded-3xl gap-2 w-full">
        <div @click="$emit('close')"
          class="hover:bg-xrb-menu-background-accent px-4 py-2 rounded-3xl flex items-center justify-center cursor-pointer text-xrb-accent-1">
          <p>Cancel</p>
        </div>
        <div @click="saveType"
          class="px-4 py-2 rounded-3xl flex items-center justify-center cursor-pointer"
          :class="loading ? 'bg-xrb-accent-1/50 cursor-not-allowed' : 'bg-xrb-accent-1'">
          <p>{{ loading ? 'Saving...' : 'Save' }}</p>
        </div>
      </div>

    </div>
  </div>
</template>

<style scoped></style>