<script setup lang="ts">
    import { computed } from 'vue';


    // Ref: https://vuejs.org/guide/components/events.html
    const prop = defineProps<{
        email: string
        role:  'default' | 'student'
    }>()
    const emit = defineEmits<{
        (e: 'go-back'): void
        (e: 'go-forward'): void
        (e: 'update:email', value: string): void
    }>()

    
    // login stuff


    // reactivity stuff
    const isEmailValid = computed<boolean>(() => !!prop.email.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/))
    
        
    async function login() {
        if(!prop.email.trim().toLowerCase()) {
            return
        }

        emit('go-forward')

        try {
            const response = await fetch('/api/auth/login/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: prop.email.trim().toLowerCase(), role: prop.role }),
                credentials: 'include'
            })

            if(!response.ok) {
                console.error(response.status)
                return
            }
        } catch(err) {
            console.error(err)
        }

        return
    }


    
</script>


<template>
    <div class="flex flex-col w-1/2 p-8 gap-8 text-xrb-text-1">
        <!-- Header -->
        <div class="flex flex-col gap-4">
            <div class="flex flex-row items-center">
                <button @click="emit('go-back')"
                    class="btn btn-ghost hover:bg-transparent hover:border-transparent hover:shadow-none pl-0">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1" stroke="currentColor" class="size-5 text-xrb-text-secondary hover:text-xrb-text-primary">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5 8.25 12l7.5-7.5" />
                    </svg>
                </button>
                <span class="text-2xl font-bold">Continue with email</span>
            </div>
            <span class="text-xs">We'll check if you have an account, and help create one if you don't.</span>
        </div>

        <!-- Body -->
        <div class="flex flex-col gap-4">
            <!-- Email fieldset -->
            <fieldset class="fieldset">
                <form @submit.prevent="login" novalidate class="flex flex-col">
                    <label class="fieldset-legend text-xs text-xrb-text-1" for="token">Email</label>
                    <input :value="prop.email" @input="emit('update:email', ($event.target as HTMLInputElement).value)"
                        type="email" class="input bg-xrb-bg-3 mt-2" placeholder="Type here" required />
                    <button type="submit" :disabled="!isEmailValid"
                       class="btn btn-outline border-xrb-border text-xrb-text-1 hover:bg-xrb-menu-background-accent text-xrb-text-primary mt-4" :class="isEmailValid ? `bg-xrb-highlight` : `bg-xrb-disabled`">
                        <span class="text-xs tracking-wider">CONTINUE</span>
                    </button>
                </form>
            </fieldset>
        </div>
    </div>
</template>


<style scoped>
</style>