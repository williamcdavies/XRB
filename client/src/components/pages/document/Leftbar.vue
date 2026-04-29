<script setup lang="ts">
    import type { Table }    from '@/types/table'
    import type { Group }    from '@/types/group'
    import      FilePreview  from './FilePreview.vue'


    // Ref: https://vuejs.org/guide/components/events.html
    const prop = defineProps<{
        table:      Table | null
        hiddenRows: Set<number>
        aColumn:    string | null
        groups:     Map<string, Group>
    }>()
    const emit = defineEmits<{
        (e: 'toggle-row-hidden', index: number):                void
        (e: 'toggle-all-rows-hidden'):                          void
        (e: 'header', idx: number, name: string):               void
    }>()
</script>


<template>
    <div class="h-full w-full overflow-hidden">
        <FilePreview :table="prop.table" :hidden-rows="prop.hiddenRows"
            @toggle-row-hidden="(i: number) => emit('toggle-row-hidden', i)"
            @toggle-all-rows-hidden="emit('toggle-all-rows-hidden')" @header="(idx, name) => emit('header', idx, name)" />
    </div>
</template>


<style scoped>
</style>
