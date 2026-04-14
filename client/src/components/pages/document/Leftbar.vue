<script setup lang="ts">
    import      FilePreview from './FilePreview.vue';
    import type { Table }   from '@/types/table'


    // Ref: https://vuejs.org/guide/components/events.html
    const prop = defineProps<{
        table:      Table | null
        hiddenRows: Set<number>
    }>()
    const emit = defineEmits<{
        (e: 'toggle-row-hidden', index: number): void
        (e: 'header', idx: number, name: string): void
    }>()
</script>


<template>
    <div class="h-full w-full overflow-hidden">
        <FilePreview :table="prop.table" :hidden-rows="prop.hiddenRows"
            @toggle-row-hidden="(i: number) => emit('toggle-row-hidden', i)"
            @header="(idx, name) => emit('header', idx, name)" />
    </div>
</template>


<style scoped>
</style>
