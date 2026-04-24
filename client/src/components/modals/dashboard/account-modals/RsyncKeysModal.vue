<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRsyncKeys } from '@/composables/rsyncKeys'
import { useUser } from '@/composables/account'

defineEmits<{
    (e: 'close'): void
    (e: 'saved'): void
}>()

const { keys, fetchKeys, createKey, deleteKey } = useRsyncKeys()
const { user } = useUser()

const newName = ref('')
const newPublicKey = ref('')
const error = ref('')
const creating = ref(false)

onMounted(fetchKeys)

async function handleCreate() {
    error.value = ''
    if (!newName.value.trim()) {
        error.value = 'Name is required.'
        return
    }
    if (!newPublicKey.value.trim()) {
        error.value = 'Public key is required.'
        return
    }
    creating.value = true
    try {
        await createKey(newName.value.trim(), newPublicKey.value.trim())
        newName.value = ''
        newPublicKey.value = ''
    } catch (e: any) {
        error.value = e?.message ?? 'Failed to add key.'
    } finally {
        creating.value = false
    }
}

async function handleDelete(id: number) {
    try {
        await deleteKey(id)
    } catch (e: any) {
        error.value = e?.message ?? 'Failed to delete key.'
    }
}
</script>

<template>
    <div class="fixed inset-0 flex items-center justify-center z-50" @click="$emit('close')">
        <div class="select-none relative bg-xrb-menu-background rounded-3xl min-w-[36rem] max-w-[36rem] h-[44rem] p-6 z-50 flex flex-col"
            @click.stop>

            <div class="relative flex rounded-3xl">
                <div @click="$emit('close')" class="cursor-pointer">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="size-8">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                    </svg>
                </div>
                <p class="text-2xl absolute left-1/2 -translate-x-1/2 whitespace-nowrap">Rsync SSH Keys</p>
            </div>

            <div class="mt-6 rounded-xl flex-1 min-h-0 overflow-auto space-y-4">

                <div class="space-y-2">
                    <input v-model="newName" type="text" placeholder="Key name (e.g. laptop)"
                        class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:border-xrb-text-accent" />
                    <textarea v-model="newPublicKey" rows="4"
                        placeholder="Paste your public key here (contents of ~/.ssh/id_ed25519.pub)"
                        class="w-full border border-gray-300 rounded-md px-3 py-2 font-mono text-sm focus:outline-none focus:border-xrb-text-accent"></textarea>
                    <div class="flex justify-end">
                        <div @click="handleCreate"
                            class="px-4 py-2 rounded-3xl cursor-pointer flex items-center justify-center"
                            :class="creating ? 'bg-xrb-accent-1/50 cursor-not-allowed' : 'bg-xrb-accent-1'">
                            <p>{{ creating ? 'Adding...' : 'Add key' }}</p>
                        </div>
                    </div>
                </div>

                <p v-if="error" class="text-sm text-xrb-text-warning-2">{{ error }}</p>

                <div v-if="keys.length === 0" class="text-sm text-xrb-text-secondary">
                    No keys yet. Add one to start using rsync.
                </div>

                <ul v-else class="divide-y divide-xrb-border">
                    <li v-for="k in keys" :key="k.id" class="flex items-center py-3 gap-2">
                        <div class="flex-1 min-w-0">
                            <p class="font-bold truncate">{{ k.name }}</p>
                            <p class="text-sm text-xrb-text-secondary font-mono truncate">
                                {{ k.key_type }} · {{ k.fingerprint }}
                            </p>
                            <p class="text-xs text-xrb-text-secondary">
                                added {{ new Date(k.created_at).toLocaleDateString() }}
                            </p>
                        </div>
                        <div @click="handleDelete(k.id)"
                            class="px-3 py-1 rounded-3xl hover:bg-xrb-menu-background-accent cursor-pointer text-sm text-xrb-text-warning-2">
                            Delete
                        </div>
                    </li>
                </ul>

                <div class="mt-6 p-3 rounded-xl bg-xrb-menu-background-accent text-sm">
                    <p class="font-bold mb-1">Usage</p>
                    <code class="block break-all">
rsync -e 'ssh -p 2222 -i ~/.ssh/your-key' -av ./local_dir/ root@&lt;host&gt;:users/{{ user?.email ?? '&lt;email&gt;' }}/dest_dir/
                    </code>
                </div>

            </div>

            <div class="flex flex-row justify-end pt-6 rounded-3xl gap-2 w-full">
                <div @click="$emit('close')"
                    class="hover:bg-xrb-menu-background-accent px-4 py-2 rounded-3xl flex items-center justify-center cursor-pointer text-xrb-accent-1">
                    <p>Close</p>
                </div>
            </div>

        </div>
    </div>
</template>
