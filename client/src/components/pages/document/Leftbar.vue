<script setup lang="ts">
    import      FilePreview from './FilePreview.vue';
    import type { Table }   from '@/types/table'

    
    // Ref: https://vuejs.org/guide/components/events.html
    const prop = defineProps<{
        table: Table | null
    }>()
    const emit = defineEmits<{
        (e: 'header', idx: number, name: string): void
    }>()
</script>


<template>
    <div class="h-full w-full overflow-hidden">
        <FilePreview :table="prop.table" @header="(idx, name) => emit('header', idx, name)" />
    </div>
</template>


<style scoped>
</style>