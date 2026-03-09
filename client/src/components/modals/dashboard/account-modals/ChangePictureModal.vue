<script setup lang="ts">
import { ref } from 'vue'
import { useApi } from '@/composables/api'
import { useUser } from '@/composables/account'

import icon1 from '@/assets/images/profile-icons/profile-icon-1.jpg'
import icon2 from '@/assets/images/profile-icons/profile-icon-2.jpg'
import icon3 from '@/assets/images/profile-icons/profile-icon-3.jpg'
import icon4 from '@/assets/images/profile-icons/profile-icon-4.jpg'
import icon5 from '@/assets/images/profile-icons/profile-icon-5.jpg'
import icon6 from '@/assets/images/profile-icons/profile-icon-6.jpg'
import icon7 from '@/assets/images/profile-icons/profile-icon-7.jpg'
import icon8 from '@/assets/images/profile-icons/profile-icon-8.jpg'

const ICONS = [icon1, icon2, icon3, icon4, icon5, icon6, icon7, icon8]

const { user } = useUser()
const emit = defineEmits<{
  (e: 'close'): void
  (e: 'saved'): void
}>()

const selected = ref<number>(user.value?.preferred_avatar ?? 1)
const error    = ref('')
const loading  = ref(false)
const { api }  = useApi()

function currentIcon() {
  return ICONS[selected.value - 1]
}

async function saveAvatar() {
  error.value   = ''
  loading.value = true
  try {
    const response = await api.fetch('/api/account/update_avatar/', {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ preferred_avatar: selected.value }),
    })
    if (!response.ok) throw new Error(`${response.status}`)
    emit('saved')
    emit('close')
  } catch (e) {
    console.error('saveAvatar error:', e)
    error.value = 'Failed to update profile picture. Please try again.'
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
        <h2 class="justify-center items-center text-2xl absolute left-1/2 -translate-x-1/2 whitespace-nowrap">
          Profile Picture
        </h2>
      </div>

      <div class="mt-6 rounded-xl flex-1 min-h-0 overflow-auto flex flex-col items-center justify-center space-y-4">
        <!-- Main preview -->
        <img
          class="w-48 h-48 rounded-full object-cover"
          :src="currentIcon()"
          alt="Selected avatar"
        />

        <!-- Row 1: icons 1-4 -->
        <div class="flex flex-row gap-4">
          <img
            v-for="i in [1, 2, 3, 4]"
            :key="i"
            class="w-18 h-18 rounded-full object-cover cursor-pointer transition-all"
            :class="selected === i ? 'ring-2 ring-white' : 'ring-2 ring-transparent'"
            :src="ICONS[i - 1]"
            :alt="`Profile icon ${i}`"
            @click="selected = i"
          />
        </div>

        <!-- Row 2: icons 5-8 -->
        <div class="flex flex-row gap-4">
          <img
            v-for="i in [5, 6, 7, 8]"
            :key="i"
            class="w-18 h-18 rounded-full object-cover cursor-pointer transition-all"
            :class="selected === i ? 'ring-2 ring-white' : 'ring-2 ring-transparent'"
            :src="ICONS[i - 1]"
            :alt="`Profile icon ${i}`"
            @click="selected = i"
          />
        </div>

        <p v-if="error" class="mt-3 text-sm text-xrb-text-warning-2">{{ error }}</p>
      </div>

      <div class="flex flex-row justify-end bottom-6 pt-6 rounded-3xl gap-2 w-full">
        <div @click="$emit('close')"
          class="hover:bg-xrb-menu-background-accent px-4 py-2 rounded-3xl flex items-center justify-center cursor-pointer text-xrb-accent-1">
          <p>Cancel</p>
        </div>
        <div @click="saveAvatar"
          class="px-4 py-2 rounded-3xl flex items-center justify-center cursor-pointer"
          :class="loading ? 'bg-xrb-accent-1/50 cursor-not-allowed' : 'bg-xrb-accent-1'">
          <p>{{ loading ? 'Saving...' : 'Save' }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>