<script setup lang="ts">
import type { AccountModalType } from '../../../../modals/dashboard/account-modals'
import { useAuth } from '@/composables/auth'
import { onMounted, computed } from 'vue'
import { useUser } from '@/composables/account'

const loading = computed(() => user.value === null)

const emit = defineEmits<{
    (e: 'open-modal', modal: AccountModalType): void
}>()

const { user, fetchUser } = useUser()
const { isAuthenticated } = useAuth()

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
                <span>Advanced Settings</span>
            </h1>
        </div>
        <ul class="list w-full min-w-[48rem] max-w-[48rem] h-full min-h-[36rem] max-h-[48rem] mx-auto rounded-none divide-y divide-xrb-border hover:cursor-pointer">

            <li @click="emit('open-modal', 'name')"
                class="flex list-row h-full hover:bg-xrb-menu-background-accent text-xrb-text-secondary hover:text-xrb-text-primary rounded-none">
                <div class="flex justify-center items-center w-1/6">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M9 15 3 9m0 0 6-6M3 9h12a6 6 0 0 1 0 12h-3" />
                    </svg>
                </div>
                <div class="flex flex-col w-5/6 justify-center h-full select-none">
                    <h2 class="font-sans font-bold text-lg">Go Back</h2>
                </div>
            </li>

            <li @click="emit('open-modal', 'type')"
                class="flex list-row h-full hover:bg-xrb-menu-background-accent text-xrb-text-secondary hover:text-xrb-text-primary rounded-none">
                <div class="flex justify-center items-center w-1/6">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M4.26 10.147a60.438 60.438 0 0 0-.491 6.347A48.62 48.62 0 0 1 12 20.904a48.62 48.62 0 0 1 8.232-4.41 60.46 60.46 0 0 0-.491-6.347m-15.482 0a50.636 50.636 0 0 0-2.658-.813A59.906 59.906 0 0 1 12 3.493a59.903 59.903 0 0 1 10.399 5.84c-.896.248-1.783.52-2.658.814m-15.482 0A50.717 50.717 0 0 1 12 13.489a50.702 50.702 0 0 1 7.74-3.342M6.75 15a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Zm0 0v-3.675A55.378 55.378 0 0 1 12 8.443m-7.007 11.55A5.981 5.981 0 0 0 6.75 15.75v-1.5" />
                    </svg>
                </div>
                <div class="flex flex-col w-5/6 justify-center h-full select-none">
                    <h2 class="font-sans font-bold text-lg">Account Type</h2>
                    <p class="font-sans py-0 text-md">
                        <span v-if="loading"
                            class="inline-block w-32 h-4 bg-xrb-text-secondary/20 rounded animate-pulse"></span>
                        <span v-else>{{ user?.type ?? '' }}</span>
                    </p>
                </div>
            </li>

            <li @click="emit('open-modal', 'language')"
                class="flex list-row h-full hover:bg-xrb-menu-background-accent text-xrb-text-secondary hover:text-xrb-text-primary rounded-none">
                <div class="flex justify-center items-center w-1/6">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="m10.5 21 5.25-11.25L21 21m-9-3h7.5M3 5.621a48.474 48.474 0 0 1 6-.371m0 0c1.12 0 2.233.038 3.334.114M9 5.25V3m3.334 2.364C11.176 10.658 7.69 15.08 3 17.502m9.334-12.138c.896.061 1.785.147 2.666.257m-4.589 8.495a18.023 18.023 0 0 1-3.827-5.802" />
                    </svg>
                </div>
                <div class="flex flex-col w-5/6 justify-center h-full select-none">
                    <h2 class="font-sans font-bold text-lg">Language</h2>
                    <p class="font-sans py-0 text-md">
                        <span v-if="loading"
                            class="inline-block w-32 h-4 bg-xrb-text-secondary/20 rounded animate-pulse"></span>
                        <span v-else>{{ user?.preferred_language ?? '' }}</span>
                    </p>
                </div>
            </li>

            <li @click="emit('open-modal', 'delete')"
                class="flex list-row h-full hover:bg-xrb-menu-background-accent hover:border-xrb-text-warning-2 text-xrb-text-secondary hover:text-xrb-text-primary rounded-none">
                <div class="flex justify-center items-center w-1/6">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
                    </svg>
                </div>
                <div class="flex flex-col w-5/6 justify-center h-full select-none">
                    <h2 class="font-sans font-bold text-lg">Delete Account</h2>
                </div>
            </li>

        </ul>
    </div>
</template>