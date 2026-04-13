<script setup lang="ts">
    import      { watch } from 'vue'
    import      { VList } from 'virtua/vue'
    import type { Table } from '@/types/table'


    // Ref: https://vuejs.org/guide/components/events.html
    const prop = defineProps<{
        table:      Table | null
        hiddenRows: Set<number>
    }>()
    const emit = defineEmits<{
        (e: 'toggle-row-hidden', index: number): void
    }>()


    watch(() => prop.table, (newTable) => {
        if(!newTable) return
    })
</script>


<template>
    <div class="h-full w-full flex flex-col overflow-hidden">
        <!-- Header -->
        <div class="grid shrink-0 bg-xrb-bg-2 border-b border-xrb-border"
            :style="{ gridTemplateColumns: `2rem 3rem repeat(${prop.table?.headers.length ?? 0}, minmax(100px, 1fr))` }">
            <div class="text-xs px-1 py-2"></div>
            <div class="text-xs font-medium text-xrb-text-secondary px-3 py-2">#</div>
            <div v-for="header in prop.table?.headers" :key="header"
                class="text-xs font-medium text-xrb-text-secondary px-3 py-2">
                {{ header }}
            </div>
        </div>

        <!-- Virtual rows -->
        <VList class="flex-1" :data="prop.table?.rows ?? []" #default="{ item, index }">
            <div class="grid border-b border-xrb-border/50"
                :class="prop.hiddenRows.has(index) ? 'opacity-30' : 'hover:bg-xrb-bg-2'"
                :style="{ gridTemplateColumns: `2rem 3rem repeat(${prop.table?.headers.length ?? 0}, minmax(100px, 1fr))` }">
                <button class="text-xs px-1 py-1.5 text-xrb-text-secondary hover:text-xrb-text-1 cursor-pointer"
                    @click="emit('toggle-row-hidden', index)">
                    {{ prop.hiddenRows.has(index) ? '○' : '●' }}
                </button>
                <div class="text-xs px-3 py-1.5 whitespace-nowrap">{{ index + 1 }}</div>
                <div v-for="(cell, j) in item" :key="j"
                    class="text-xs px-3 py-1.5 whitespace-nowrap overflow-hidden text-ellipsis">
                    {{ cell }}
                </div>
            </div>
        </VList>
    </div>
</template>


<style scoped>
</style>