<script setup lang="ts">
    import { ref, onMounted } from 'vue'
    import { useAuth }   from '@/composables/auth'
    import { useRouter } from 'vue-router'

    // Ref: https://vuejs.org/guide/components/events.html
    const emit = defineEmits<{
        (e: 'go-forward'):            void
        (e: 'go-forward-as-guest'):   void
        (e: 'go-forward-as-student'): void
    }>()

    const { initGoogleSignIn } = useAuth()
    const router                = useRouter()
    const googleButtonRef       = ref<HTMLElement>()

    onMounted(() => {
        if (googleButtonRef.value) {
            initGoogleSignIn(googleButtonRef.value, () => {
                router.push('/dashboard')
            })
        }
    })

    function handleGoogleClick() {
        const iframe = googleButtonRef.value?.querySelector('iframe')
        if (iframe) {
            iframe.contentWindow?.postMessage({ type: 'click' }, '*')
        }
        // Fallback: click the rendered Google button div
        const btn = googleButtonRef.value?.querySelector('[role="button"]') as HTMLElement | null
        btn?.click()
    }
</script>


<template>
    <div class="flex flex-col w-1/2 p-8 gap-8">
        <!-- Header -->
        <div class="flex flex-col gap-4">
            <span class="text-2xl font-bold">Log in or sign up</span>
        </div>

        <!-- Body -->
        <div class="flex flex-col gap-4">

            <!-- Continue w/ Google (hidden rendered button for cross-browser support) -->
            <div ref="googleButtonRef" class="hidden"></div>
            <button @click="handleGoogleClick"
                class="group btn btn-outline justify-start bg-xrb-bg-2 border-xrb-border text-xrb-text-1 hover:bg-xrb-menu-background-accent text-xrb-text-secondary hover:text-xrb-text-primary">
                <div class="flex justify-center items-center w-1/8">
                    <img class="h-4 w-4" src="../../../assets/icons/google.svg" />
                </div>
                <div class="flex justify-left items-left w-7/8">
                    <span class="text-xs tracking-wider">CONTINUE WITH GOOGLE</span>
                </div>
            </button>

            <!-- Continue w/ email -->
            <button @click="emit('go-forward')"
                class="group btn btn-outline justify-start bg-xrb-bg-2 border-xrb-border text-xrb-text-1 hover:bg-xrb-menu-background-accent text-xrb-text-secondary hover:text-xrb-text-primary">
                <div class="flex justify-center items-center w-1/8">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="text-xrb-text-primary size-5">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0 0 19.5 4.5h-15a2.25 2.25 0 0 0-2.25 2.25m19.5 0v.243a2.25 2.25 0 0 1-1.07 1.916l-7.5 4.615a2.25 2.25 0 0 1-2.36 0L3.32 8.91a2.25 2.25 0 0 1-1.07-1.916V6.75" />
                    </svg>
                </div>
                <div class="flex justify-left items-left w-7/8">
                    <span class="text-xs tracking-wider">CONTINUE WITH EMAIL</span>
                </div>
            </button>

            <!-- Horizontal divider -->
            <div class="divider text-xs">OR</div>

            <!-- Continue as guest -->
            <button @click="emit('go-forward-as-guest')"
                class="group btn btn-outline justify-start bg-xrb-bg-2 border-xrb-border text-xrb-text-1 hover:bg-xrb-menu-background-accent text-xrb-text-secondary hover:text-xrb-text-primary">
                <div class="flex justify-center items-center w-1/8">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="text-xrb-text-primary size-5">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z" />
                    </svg>
                </div>
                <div class="flex justify-left items-left w-7/8">
                    <span class="text-xs tracking-wider">CONTINUE AS GUEST</span>
                </div>
            </button>

            <!-- Continue as student -->
            <button @click="emit('go-forward-as-student')"
                class="group btn btn-outline justify-start bg-xrb-bg-2 border-xrb-border text-xrb-text-1 hover:bg-xrb-menu-background-accent text-xrb-text-secondary hover:text-xrb-text-primary">
                <div class="flex justify-center items-center w-1/8">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="text-xrb-text-primary size-5">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M4.26 10.147a60.438 60.438 0 0 0-.491 6.347A48.62 48.62 0 0 1 12 20.904a48.62 48.62 0 0 1 8.232-4.41 60.46 60.46 0 0 0-.491-6.347m-15.482 0a50.636 50.636 0 0 0-2.658-.813A59.906 59.906 0 0 1 12 3.493a59.903 59.903 0 0 1 10.399 5.84c-.896.248-1.783.52-2.658.814m-15.482 0A50.717 50.717 0 0 1 12 13.489a50.702 50.702 0 0 1 7.74-3.342M6.75 15a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Zm0 0v-3.675A55.378 55.378 0 0 1 12 8.443m-7.007 11.55A5.981 5.981 0 0 0 6.75 15.75v-1.5" />
                    </svg>
                </div>
                <div class="flex justify-left items-left w-7/8">
                    <span class="text-xs tracking-wider">CONTINUE AS STUDENT</span>
                </div>
            </button>
        </div>
    </div>
</template>


<style scoped>
</style>