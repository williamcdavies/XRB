<script setup lang="ts">
    import type { Table } from '@/types/table'
    import FilePreview    from './FilePreview.vue';

    
    // Ref: https://vuejs.org/guide/components/events.html
    const prop = defineProps<{
        table: Table | null
    }>()
</script>


<template>
    <div class="h-full w-full overflow-hidden">
        <FilePreview :table="prop.table" />
    </div>
</template>


<style scoped>
</style>