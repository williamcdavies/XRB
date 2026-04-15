<script setup lang="ts">
    import { ref, onMounted } from 'vue'


    const prop = defineProps<{
        defaultName: string
    }>()
    const emit = defineEmits<{
        (e: 'close'):              void
        (e: 'save', name: string): void
    }>()


    const name     = ref(prop.defaultName)
    const inputEl  = ref<HTMLInputElement | null>(null)


    function submit() {
        const trimmed = name.value.trim()
        if (trimmed) emit('save', trimmed)
    }


    onMounted(() => {
        inputEl.value?.select()
    })
</script>


<template>
    <div class="fixed inset-0 z-20 flex items-center justify-center bg-black/50" @click.self="emit('close')">
        <div class="bg-xrb-bg-1 border border-xrb-border rounded-lg shadow-xl w-[360px] max-w-[90vw]"
            @click.stop>
            <!-- Header -->
            <div class="flex items-center justify-between px-4 py-3 border-b border-xrb-border bg-xrb-bg-2 rounded-t-lg">
                <h3 class="text-xrb-text-1 font-mono text-sm uppercase tracking-widest">Save View</h3>
                <button type="button" class="btn btn-ghost btn-xs text-xrb-text-secondary"
                    @click="emit('close')">Close</button>
            </div>

            <!-- Body -->
            <form class="p-4 flex flex-col gap-4" @submit.prevent="submit">
                <label class="text-xs font-mono uppercase tracking-widest text-xrb-text-secondary">
                    View Name
                </label>
                <input
                    ref="inputEl"
                    v-model="name"
                    type="text"
                    class="input input-sm w-full bg-xrb-bg-3 border border-xrb-border text-xrb-text-1 font-mono text-sm"
                    placeholder="My View"
                    @keydown.escape="emit('close')" />

                <div class="flex justify-end gap-2">
                    <button type="button"
                        class="btn btn-ghost btn-sm text-xrb-text-secondary font-mono text-xs uppercase tracking-widest"
                        @click="emit('close')">Cancel</button>
                    <button type="submit"
                        class="btn btn-sm bg-xrb-bg-3 border border-xrb-border text-xrb-text-1 font-mono text-xs uppercase tracking-widest"
                        :disabled="!name.trim()">Save</button>
                </div>
            </form>
        </div>
    </div>
</template>


<style scoped>
</style>
