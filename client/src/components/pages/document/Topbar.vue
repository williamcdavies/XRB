<script setup lang="ts">
    import { ref } from 'vue';

    // Ref: https://vuejs.org/guide/components/events.html
    const emit = defineEmits<{
        (e: 'file-selected', file: File): void
    }>()


    // file input stuff
    const fileInput = ref<HTMLInputElement | null>(null)

        
    function handleFileInput(event: Event) {
        const input = event.target as HTMLInputElement
        const file  = input.files?.[0]

        if(!file) {
            return
        }

        emit('file-selected', file)
    }


    function targetFileInput() {
        fileInput.value?.click()
    }
</script>


<template>
    <div class="flex flex-col h-10 w-full border-b border-xrb-border">
        <!-- hidden file input trigger -->
        <input ref="fileInput" type="file" accept=".csv" class="hidden" @change="handleFileInput" />
        <button @click="targetFileInput">Import CSV</button>
    </div>
</template>


<style scoped>
</style>