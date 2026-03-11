<script setup lang="ts">
    import      { watch } from 'vue'
    import type { Table } from '@/types/table'


    // Ref: https://vuejs.org/guide/components/events.html
    const prop = defineProps<{
        table: Table | null
    }>()


    watch(() => prop.table, (newTable) => {
        if(!newTable) return
    })
</script>


<template>
    <div class="h-full w-full overflow-auto">
        <table class="table table-pin-rows table-xs w-full">
            <thead>
                <tr class="bg-xrb-bg-2">
                    <th class="text-xs font-medium text-xrb-text-secondary px-3 py-2 border-b border-xrb-border">#</th>
                    <th v-for="header in prop.table?.headers" :key="header"
                        class="text-xs font-medium text-xrb-text-secondary px-3 py-2 border-b border-xrb-border">{{
                            header }}</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(row, i) in prop.table?.rows" :key="i" class="hover:bg-xrb-bg-2">
                    <td class="text-xs px-3 py-1.5 border-b border-xrb-border/50 whitespace-nowrap">{{ i + 1 }}</td>
                    <td v-for="(cell, j) in row" :key="j"
                        class="text-xs px-3 py-1.5 border-b border-xrb-border/50 whitespace-nowrap">{{ cell }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>


<style scoped>
</style>