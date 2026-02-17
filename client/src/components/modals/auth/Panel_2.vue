<script setup lang="ts">
    // Ref: https://vuejs.org/guide/components/events.html
    const prop = defineProps<{
        email: string
    }>()
    const emit = defineEmits<{
        (e: 'go-back'): void
        (e: 'go-forward'): void
        (e: 'update:email', value: string): void
    }>()

    
    // login
    async function login() {
        if(!prop.email.trim().toLowerCase()) {
            return
        }

        try {
            const response = await fetch('http://localhost:8000/api/auth/login/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: prop.email.trim().toLowerCase() }),
                credentials: 'include'
            })

            if(!response.ok) {
                console.error(response.status)
                return
            }
        } catch(err) {
            console.error(err)
        }

        emit('go-forward')
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
                    <img class="h-4 w-4" src="../../../assets/icons/chevrons/chevron_left.svg" />
                </button>
                <span class="text-2xl font-bold">Continue with email</span>
            </div>
            <span class="text-xs">We'll check if you have an account, and help create one if you don't.</span>
        </div>

        <!-- Body -->
        <div class="flex flex-col gap-4">
            <!-- Email fieldset -->
            <fieldset class="fieldset">
                <form @submit.prevent="login" novalidate class="flex flex-col gap-4">
                    <label class="fieldset-legend text-xs text-xrb-text-1" for="token">Email</label>
                    <input :value="prop.email" @input="emit('update:email', ($event.target as HTMLInputElement).value)"
                        type="email" class="input bg-xrb-bg-3" placeholder="Type here" required />
                    <button type="submit" :disabled="!prop.email.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)"
                        class="btn btn-outline bg-xrb-highlight border-xrb-border text-xrb-text-1 hover:bg-xrb-text-1 hover:border-xrb-text-1 hover:text-xrb-text-2">
                        <span class="text-xs tracking-wider">CONTINUE</span>
                    </button>
                </form>
            </fieldset>
        </div>
    </div>
</template>


<style scoped>
</style>