<script setup lang="ts">
    import { ref } from 'vue';

    // Ref: https://vuejs.org/guide/components/events.html
    const prop = defineProps<{
        email: string
    }>()
    const emit = defineEmits<{
        (e: 'go-back'): void
    }>()

    
    const accessToken = ref<string | null>(null)


    // verify
    const token = ref('')

    async function verify() {
        if(!prop.email.trim().toLowerCase() || !token.value.trim().toLowerCase()) {
            return
        }

        try {
            const response = await fetch('http://localhost:8000/api/auth/verify/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    email: prop.email.trim().toLowerCase(),
                    token: token.value.trim().toLowerCase() 
                }),
                credentials: 'include'
            })

            if(!response.ok) {
                console.error(response.status)
                return
            }

            const data = await response.json()
            accessToken.value = data.access
        } catch(err) {
            console.error(err)
        }

        return
    }
</script>


<template>
    <div class="flex flex-col w-1/2 p-8 gap-8">
        <!-- Header -->
        <div class="flex flex-col gap-4">
            <div class="flex flex-row items-center">
                <button @click="emit('go-back')" class="btn btn-ghost hover:bg-transparent hover:border-transparent hover:shadow-none">
                    <img class="h-4 w-4" src="../../../assets/icons/chevrons/chevron_left.svg"/>
                </button>
                <span class="text-2xl font-bold">Continue with email</span>
            </div>
            <span class="text-xs">We'll check if you have an account, and help create one if you don't.</span>
        </div>
        
        <!-- Body -->
        <div class="flex flex-col gap-4">
            <!-- Email fieldset -->
            <fieldset class="fieldset">
                <form @submit.prevent="verify" novalidate class="flex flex-col gap-4">
                    <div class="flex flex-col gap-2">
                        <label class="fieldset-legend pl-1 text-xs" for="token">Email</label>
                        <input
                            :value="prop.email"
                            type="email"
                            class="input"
                            placeholder="Type here"
                            readonly
                        />
                    </div>
                    <div class="flex flex-col gap-2">
                        <label class="fieldset-legend pl-1 text-xs" for="token">Password</label>
                        <input
                            v-model="token"
                            type="token"
                            class="input"
                            placeholder="XXXXXX"
                            required
                        />
                    </div>
                    <button
                        type="submit"
                        :disabled="!token.match(/^\d{6}$/)"
                        class="btn btn-outline bg-[#dc8c64] border-white/25 text-[#181818] hover:bg-white hover:border-white hover:text-[#181818]"
                    >
                        <span class="text-xs tracking-wider">CONTINUE</span>
                    </button>
                </form>
            </fieldset>
        </div>
    </div>
</template>


<style scoped>
</style>