<script setup lang="ts">
    import type { Table } from '@/types/table'
    import FilePreview    from './FilePreview.vue';

    
    // Ref: https://vuejs.org/guide/components/events.html
    const prop = defineProps<{
        table: Table | null
    }>()
    const emit = defineEmits<{
        (e: 'selected-headers', headers: { x: number | null, y: number | null, z: number | null }): void
    }>()
</script>


<template>
    <div class="h-full w-full overflow-hidden">
        <FilePreview :table="prop.table" @selected-headers="emit('selected-headers', $event)" />
    </div>
</template>


<style scoped>
</style>