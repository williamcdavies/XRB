<script setup lang="ts">
    import { computed, ref } from 'vue';
    import { useAuth }       from '@/composables/auth';
    import { useRouter }     from 'vue-router';


    // Ref: https://vuejs.org/guide/components/events.html
    const prop = defineProps<{
        email: string
    }>()
    const emit = defineEmits<{
        (e: 'go-back'): void
    }>()


    // verify stuff
    const { setAccessToken } = useAuth()
    const router             = useRouter()
    const token              = ref('')


    // reactivity stuff
    const isTokenValid = computed<boolean>(() => !!token.value.match(/^\d{6}$/))
    const isInputValid = ref(true)

    
    async function verify(): Promise<boolean> {
        if(!prop.email.trim().toLowerCase() || !token.value.trim().toLowerCase()) {
            return false
        }

        try {
            const response = await fetch('/api/auth/verify/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    email: prop.email.trim().toLowerCase(),
                    token: token.value.trim().toLowerCase() 
                }),
                credentials: 'include'
            })

            if(!response.ok) {
                isInputValid.value = false
                
                console.error(response.status)

                return false
            }

            const data = await response.json()
            setAccessToken(data.access)
            
            return true
        } catch(err) {
            console.error(err)
            
            return false
        }
    }

    async function goToDashboard() {
        if(await verify()) {
            router.push('/dashboard')
        }
    }
</script>


<template>
    <div class="flex flex-col w-1/2 p-8 gap-8 text-xrb-text-1">
        <!-- Header -->
        <div class="flex flex-col gap-4">
            <div class="flex flex-row items-center">
                <button @click="emit('go-back')"
                    class="btn btn-ghost hover:bg-transparent hover:border-transparent hover:shadow-none pl-0">
                    <img class="h-4 w-4" src="../../../assets/icons/chevrons/chevron_left.svg" />
                </button>
                <span class="text-2xl font-bold">Continue with email</span>
            </div>
            <span class="text-xs">Almost there! We've sent a one-time login code to your email. Please submit the code to continue</span>
        </div>

        <!-- Body -->
        <div class="flex flex-col gap-4">
            <!-- Email fieldset -->
            <fieldset class="fieldset">
                <form @submit.prevent="goToDashboard" novalidate class="flex flex-col gap-4">
                    <div class="flex flex-col gap-2">
                        <label class="fieldset-legend pl-1 text-xs text-xrb-text-1" for="token">Email</label>
                        <input :value="prop.email" type="email" class="input btn-disabled bg-xrb-disabled"
                            placeholder="Type here" readonly />
                    </div>
                    <div class="flex flex-col gap-2">
                        <label class="fieldset-legend pl-1 text-xs text-xrb-text-1" for="token">One-time login code</label>
                        <input v-model="token" type="token" class="input bg-xrb-bg-3" :class="{'border-xrb-error': !isInputValid}" placeholder="XXXXXX" required />
                    </div>
                    <button type="submit" :disabled="!isTokenValid"
                        class="btn btn-outline bg-xrb-highlight border-xrb-border text-xrb-text-1 hover:bg-xrb-text-1 hover:border-xrb-text-1 hover:text-xrb-text-2" :class="{'bg-xrb-disabled': !isTokenValid}">
                        <span class="text-xs tracking-wider">CONTINUE</span>
                    </button>
                </form>
            </fieldset>
        </div>
    </div>
</template>


<style scoped>
</style>