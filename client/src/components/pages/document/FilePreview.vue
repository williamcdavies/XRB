<script setup lang="ts">
    import      { ref, watch } from 'vue'
    import      { VList } from 'virtua/vue'
    import type { Table } from '@/types/table'


    // Ref: https://vuejs.org/guide/components/events.html
    const prop = defineProps<{
        table: Table | null
    }>()
    const emit = defineEmits<{
        (e: 'selected-headers', headers: { x: number | null, y: number | null, z: number | null }): void
    }>()


    const xHeader = ref<number | null>(0)
    const yHeader = ref<number | null>(1)
    const zHeader = ref<number | null>(2)


    function cycle(i: number): void {
        if      (xHeader.value != i && yHeader.value != i && zHeader.value != i) xHeader.value = i
        else if (xHeader.value == i)                                             { xHeader.value = null; yHeader.value = i }
        else if (yHeader.value == i)                                             { yHeader.value = null; zHeader.value = i }
        else                                                                     { zHeader.value = null;                   }
    }


    watch(() => prop.table, (newTable) => {
        if(!newTable) return

        xHeader.value = 0
        yHeader.value = 1
        zHeader.value = 2
    })


    watch([xHeader, yHeader, zHeader], () => {
        emit('selected-headers', { x: xHeader.value, y: yHeader.value, z: zHeader.value })
    })
</script>


<template>
    <div class="h-full w-full flex flex-col overflow-hidden">
        <!-- Header -->
        <div class="grid shrink-0 bg-xrb-bg-2 border-b border-xrb-border"
            :style="{ gridTemplateColumns: `3rem repeat(${prop.table?.headers.length ?? 0}, minmax(100px, 1fr))` }">
            <div class="text-xs font-medium text-xrb-text-secondary px-3 py-2">#</div>
            <div v-for="(header, i) in prop.table?.headers" :key="header"
                class="text-xs font-medium px-3 py-2 cursor-pointer select-none focus:outline-none focus:ring-1 focus:ring-inset focus:ring-xrb-border"
                :class="{
                    'bg-blue-500/20 text-blue-400': xHeader === i,
                    'bg-green-500/20 text-green-400': yHeader === i,
                    'bg-orange-500/20 text-orange-400': zHeader === i,
                    'text-xrb-text-secondary hover:bg-xrb-bg-3': xHeader !== i && yHeader !== i && zHeader !== i
                }" tabindex="0"
                :aria-label="`${header} column, ${xHeader === i ? 'X axis' : yHeader === i ? 'Y axis' : zHeader === i ? 'Z axis' : 'unassigned'}. Press Enter or Space to cycle.`"
                @click="cycle(i)" @keydown.enter.prevent="cycle(i)" @keydown.space.prevent="cycle(i)">
                <span>{{ header }}</span>
                <span v-if="xHeader === i" class="ml-1 text-blue-400">(X)</span>
                <span v-else-if="yHeader === i" class="ml-1 text-green-400">(Y)</span>
                <span v-else-if="zHeader === i" class="ml-1 text-orange-400">(Z)</span>
            </div>
        </div>

        <!-- Virtual rows -->
        <VList class="flex-1" :data="prop.table?.rows ?? []" #default="{ item, index }">
            <div class="grid hover:bg-xrb-bg-2 border-b border-xrb-border/50"
                :style="{ gridTemplateColumns: `3rem repeat(${prop.table?.headers.length ?? 0}, minmax(100px, 1fr))` }">
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