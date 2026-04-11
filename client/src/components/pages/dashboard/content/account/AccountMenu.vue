<script setup lang="ts">
import type { AccountModalType } from '../../../../modals/dashboard/account-modals'
import { useAuth } from '@/composables/auth'
import { onMounted, computed } from 'vue'
import { useUser } from '@/composables/account'
import { useAppearance } from '@/composables/appearance'

const loading = computed(() => user.value === null)

import icon1 from '@/assets/images/profile-icons/profile-icon-1.jpg'
import icon2 from '@/assets/images/profile-icons/profile-icon-2.jpg'
import icon3 from '@/assets/images/profile-icons/profile-icon-3.jpg'
import icon4 from '@/assets/images/profile-icons/profile-icon-4.jpg'
import icon5 from '@/assets/images/profile-icons/profile-icon-5.jpg'
import icon6 from '@/assets/images/profile-icons/profile-icon-6.jpg'
import icon7 from '@/assets/images/profile-icons/profile-icon-7.jpg'
import icon8 from '@/assets/images/profile-icons/profile-icon-8.jpg'

const ICONS = [icon1, icon2, icon3, icon4, icon5, icon6, icon7, icon8]

// For navigation across the account menu and advanced menu
const emit = defineEmits<{
    (e: 'open-modal', modal: AccountModalType): void
    (e: 'change-view', view: 'main' | 'advanced'): void
}>()

const { user, fetchUser } = useUser()
const { isAuthenticated } = useAuth()
const { isDark, toggleTheme } = useAppearance()

const avatarSrc = computed(() => {
    const index = (user.value?.preferred_avatar ?? 1) - 1
    return ICONS[index] ?? ICONS[0]
})

// verify authentication and fetch user on mount
onMounted(async () => {
    const authenticated = await isAuthenticated()
    if (authenticated) {
        await fetchUser()
    } else {
        console.log('No valid token found')
    }
})
</script>

<template>
    <div class="flex flex-col min-h-screen hero justify-center items-center space-y-6 rounded-none">
        <div class="w-full min-w-[48rem] max-w-[48rem] mx-auto">
            <h1 class="text-3xl font-display mb-2 ml-3">
                <span v-if="loading" class="inline-block w-48 h-8 bg-xrb-text-secondary/20 rounded animate-pulse"></span>
                <span v-else>{{ user?.first_name ? `Hello, ${user.first_name}!` : 'Hello!' }}</span>
            </h1>
            <p class="font-sans text-m ml-3">Let's customize your personal information to make sure we work best for
                you.</p>
        </div>
        <ul
            class="list w-full min-w-[48rem] max-w-[48rem] h-full min-h-[36rem] max-h-[48rem] mx-auto rounded-none divide-y divide-xrb-border">

            <li @click="emit('open-modal', 'picture')"
                class="flex list-row h-full hover:bg-xrb-menu-background-accent text-xrb-text-secondary hover:text-xrb-text-primary rounded-none hover:cursor-pointer">
                <div class="flex justify-center items-center w-1/6">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M6.827 6.175A2.31 2.31 0 0 1 5.186 7.23c-.38.054-.757.112-1.134.175C2.999 7.58 2.25 8.507 2.25 9.574V18a2.25 2.25 0 0 0 2.25 2.25h15A2.25 2.25 0 0 0 21.75 18V9.574c0-1.067-.75-1.994-1.802-2.169a47.865 47.865 0 0 0-1.134-.175 2.31 2.31 0 0 1-1.64-1.055l-.822-1.316a2.192 2.192 0 0 0-1.736-1.039 48.774 48.774 0 0 0-5.232 0 2.192 2.192 0 0 0-1.736 1.039l-.821 1.316Z" />
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M16.5 12.75a4.5 4.5 0 1 1-9 0 4.5 4.5 0 0 1 9 0ZM18.75 10.5h.008v.008h-.008V10.5Z" />
                    </svg>
                </div>
                <div class="flex flex-col w-4/6 justify-center h-full select-none">
                    <h2 class="font-sans font-bold text-lg">Profile Picture</h2>
                </div>
                <div class="flex justify-center items-center w-1/6">
                    <div v-if="loading" class="w-20 h-20 rounded-full bg-xrb-text-secondary/20 animate-pulse" />
                    <img v-else class="w-20 h-20 rounded-full object-cover" :src="avatarSrc" alt="Rounded avatar">
                </div>
            </li>

            <li @click="emit('open-modal', 'name')"
                class="flex list-row h-full hover:bg-xrb-menu-background-accent text-xrb-text-secondary hover:text-xrb-text-primary rounded-none hover:cursor-pointer">
                <div class="flex justify-center items-center w-1/6">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z" />
                    </svg>
                </div>
                <div class="flex flex-col w-5/6 justify-center h-full select-none">
                    <h2 class="font-sans font-bold text-lg">Name</h2>
                    <p class="font-sans py-0 text-md">
                        <span v-if="loading"
                            class="inline-block w-32 h-4 bg-xrb-text-secondary/20 rounded animate-pulse"></span>
                        <span v-else>{{ user?.first_name ?? '' }} {{ user?.last_name ?? '' }}</span>
                    </p>
                </div>
            </li>

            <li @click="emit('open-modal', 'email')"
                class="flex list-row h-full hover:bg-xrb-menu-background-accent text-xrb-text-secondary hover:text-xrb-text-primary rounded-none hover:cursor-pointer">
                <div class="flex justify-center items-center w-1/6">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M21.75 6.75v10.5a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0 0 19.5 4.5h-15a2.25 2.25 0 0 0-2.25 2.25m19.5 0v.243a2.25 2.25 0 0 1-1.07 1.916l-7.5 4.615a2.25 2.25 0 0 1-2.36 0L3.32 8.91a2.25 2.25 0 0 1-1.07-1.916V6.75" />
                    </svg>
                </div>
                <div class="flex flex-col w-5/6 justify-center h-full select-none">
                    <h2 class="font-sans font-bold text-lg">Email</h2>
                    <p class="font-sans py-0 text-md">
                        <span v-if="loading"
                            class="inline-block w-32 h-4 bg-xrb-text-secondary/20 rounded animate-pulse"></span>
                        <span v-else>{{ user?.email ?? '' }}</span>
                    </p>
                </div>
            </li>

            <li class="flex list-row h-full hover:bg-xrb-menu-background-accent text-xrb-text-secondary hover:text-xrb-text-primary rounded-none">
                <div class="flex justify-center items-center w-1/6">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M9.53 16.122a3 3 0 0 0-5.78 1.128 2.25 2.25 0 0 1-2.4 2.245 4.5 4.5 0 0 0 8.4-2.245c0-.399-.078-.78-.22-1.128Zm0 0a15.998 15.998 0 0 0 3.388-1.62m-5.043-.025a15.994 15.994 0 0 1 1.622-3.395m3.42 3.42a15.995 15.995 0 0 0 4.764-4.648l3.876-5.814a1.151 1.151 0 0 0-1.597-1.597L14.146 6.32a15.996 15.996 0 0 0-4.649 4.763m3.42 3.42a6.776 6.776 0 0 0-3.42-3.42" />
                    </svg>
                </div>
                <div class="flex flex-col w-2/3 justify-center h-full select-none">
                    <h2 class="font-sans font-bold text-lg">Appearance</h2>
                    <p class="font-sans py-0 text-md">{{ isDark ? 'Dark' : 'Light' }}</p>
                </div>
                <div class="flex justify-center items-center w-1/6 h-full">
                    <label class="inline-flex items-center cursor-pointer">
                        <input type="checkbox" class="sr-only peer" :checked="!isDark" @change="toggleTheme">
                        <div
                            class="relative w-9 h-5 bg-xrb-blue peer-checked:bg-xrb-yellow peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-brand-soft dark:peer-focus:ring-brand-soft 
                            rounded-full peer peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-buffer after:content-[''] 
                            after:absolute after:top-[2px] after:start-[2px] after:bg-white after:rounded-full after:h-4 after:w-4 after:transition-all hover:cursor-pointer">
                        </div>
                    </label>
                </div>
            </li>

            <li @click.stop="emit('change-view', 'advanced')"
                class="flex list-row h-full hover:bg-xrb-menu-background-accent hover:border-xrb-text-warning-2 text-xrb-text-secondary hover:text-xrb-text-primary rounded-none hover:cursor-pointer">
                <div class="flex justify-center items-center w-1/6">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.325.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 0 1 1.37.49l1.296 2.247a1.125 1.125 0 0 1-.26 1.431l-1.003.827c-.293.241-.438.613-.43.992a7.723 7.723 0 0 1 0 .255c-.008.378.137.75.43.991l1.004.827c.424.35.534.955.26 1.43l-1.298 2.247a1.125 1.125 0 0 1-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.47 6.47 0 0 1-.22.128c-.331.183-.581.495-.644.869l-.213 1.281c-.09.543-.56.94-1.11.94h-2.594c-.55 0-1.019-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 0 1-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 0 1-1.369-.49l-1.297-2.247a1.125 1.125 0 0 1 .26-1.431l1.004-.827c.292-.24.437-.613.43-.991a6.932 6.932 0 0 1 0-.255c.007-.38-.138-.751-.43-.992l-1.004-.827a1.125 1.125 0 0 1-.26-1.43l1.297-2.247a1.125 1.125 0 0 1 1.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.086.22-.128.332-.183.582-.495.644-.869l.214-1.28Z" />
                        <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                    </svg>
                </div>
                <div class="flex flex-col w-5/6 justify-center h-full select-none">
                    <h2 class="font-sans font-bold text-lg">Advanced Settings</h2>
                </div>
            </li>

            <li @click="emit('open-modal', 'logout')"
                class="flex list-row h-full hover:bg-xrb-menu-background-accent hover:border-xrb-text-warning-2 text-xrb-text-secondary hover:text-xrb-text-primary rounded-none hover:cursor-pointer">
                <div class="flex justify-center items-center w-1/6">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 9V5.25A2.25 2.25 0 0 1 10.5 3h6a2.25 2.25 0 0 1 
                        2.25 2.25v13.5A2.25 2.25 0 0 1 16.5 21h-6a2.25 2.25 0 0 1-2.25-2.25V15m-3 0-3-3m0 0 3-3m-3 3H15" />
                    </svg>
                </div>
                <div class="flex flex-col w-5/6 justify-center h-full select-none">
                    <h2 class="font-sans font-bold text-lg">Log Out</h2>
                </div>
            </li>
        </ul>
    </div>
</template>