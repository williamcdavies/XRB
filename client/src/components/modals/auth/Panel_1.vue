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
                class="group btn btn-outline justify-start bg-xrb-bg-2 border-xrb-border text-xrb-text-1 hover:bg-xrb-text-1 hover:border-xrb-text-1 hover:text-xrb-bg-1">
                <span class="flex items-center justify-center h-full w-8">
                    <img class="h-4 w-4" src="../../../assets/icons/google.svg" />
                </span>
                <span class="text-xs tracking-wider">CONTINUE WITH GOOGLE</span>
            </button>

            <!-- Continue w/ email -->
            <button @click="emit('go-forward')"
                class="group btn btn-outline justify-start bg-xrb-bg-2 border-xrb-border text-xrb-text-1 hover:bg-xrb-text-1 hover:border-xrb-text-1 hover:text-xrb-bg-1">
                <span class="flex items-center justify-center h-full w-8">
                    <img class="h-5 w-5 group-hover:invert " src="../../../assets/icons/mail.svg" />
                </span>
                <span class="text-xs tracking-wider">CONTINUE WITH EMAIL</span>
            </button>

            <!-- Horizontal divider -->
            <div class="divider text-xs">OR</div>

            <!-- Continue as guest -->
            <button @click="emit('go-forward-as-guest')"
                class="group btn btn-outline justify-start bg-xrb-bg-2 border-xrb-border text-xrb-text-1 hover:bg-xrb-text-1 hover:border-xrb-text-1 hover:text-xrb-bg-1">
                <span class="flex items-center justify-center h-full w-8">
                    <img class="h-5 w-5 group-hover:invert " src="../../../assets/icons/users/user_1.svg" />
                </span>
                <span class="text-xs tracking-wider">CONTINUE AS GUEST</span>
            </button>

            <!-- Continue as student -->
            <button @click="emit('go-forward-as-student')"
                class="group btn btn-outline justify-start bg-xrb-bg-2 border-xrb-border text-xrb-text-1 hover:bg-xrb-text-1 hover:border-xrb-text-1 hover:text-xrb-bg-1">
                <span class="flex items-center justify-center h-full w-8">
                    <img class="h-5 w-5 group-hover:invert " src="../../../assets/icons/pencils/edit_pencil_1.svg" />
                </span>
                <span class="text-xs tracking-wider">CONTINUE AS STUDENT</span>
            </button>
        </div>
    </div>
</template>


<style scoped>
</style>