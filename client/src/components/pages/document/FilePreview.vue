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


    const openDropdown = ref<number | null>(null)


    function assign(i: number, axis: 'x' | 'y' | 'z' | null): void {
        if (xHeader.value === i) xHeader.value = null
        if (yHeader.value === i) yHeader.value = null
        if (zHeader.value === i) zHeader.value = null
        if (axis === 'x') xHeader.value = i
        if (axis === 'y') yHeader.value = i
        if (axis === 'z') zHeader.value = i
        openDropdown.value = null
    }


    function toggleDropdown(i: number): void {
        openDropdown.value = openDropdown.value === i ? null : i
    }


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
            <div v-for="(header, i) in prop.table?.headers" :key="header" class="relative">
                <!-- Header button -->
                <button
                    class="w-full text-left text-xs font-medium px-3 py-2 cursor-pointer select-none focus:outline-none focus:ring-1 focus:ring-inset focus:ring-xrb-border"
                    :class="{
                        'bg-blue-500/20   text-blue-400': xHeader === i,
                        'bg-green-500/20  text-green-400': yHeader === i,
                        'bg-orange-500/20 text-orange-400': zHeader === i,
                        'text-xrb-text-secondary hover:bg-xrb-bg-3': xHeader !== i && yHeader !== i && zHeader !== i
                    }"
                    :aria-label="`${header} column, ${xHeader === i ? 'X-Axis' : yHeader === i ? 'Y-Axis' : zHeader === i ? 'Z-Axis' : 'unassigned'}. Press Enter to change.`"
                    :aria-expanded="openDropdown === i" @click.stop="toggleDropdown(i)"
                    @keydown.enter.prevent="toggleDropdown(i)" @keydown.space.prevent="toggleDropdown(i)"
                    @keydown.escape="openDropdown = null">
                    <span>{{ header }}</span>
                    <span v-if="xHeader === i" class="ml-1 text-blue-400">(X)</span>
                    <span v-else-if="yHeader === i" class="ml-1 text-green-400">(Y)</span>
                    <span v-else-if="zHeader === i" class="ml-1 text-orange-400">(Z)</span>
                </button>
                <!-- Dropdown -->
                <div v-if="openDropdown === i"
                    class="absolute top-full left-0 z-50 min-w-full bg-xrb-bg-2 border border-xrb-border shadow-lg"
                    role="menu">
                    <button v-for="(option, label) in { X: 'x', Y: 'y', Z: 'z' }" :key="label"
                        class="w-full text-left text-xs px-3 py-2 hover:bg-xrb-bg-3 focus:outline-none focus:bg-xrb-bg-3"
                        :class="{
                            'text-blue-400': label === 'X',
                            'text-green-400': label === 'Y',
                            'text-orange-400': label === 'Z',
                        }" role="menuitem" @click.stop="assign(i, option as 'x' | 'y' | 'z')"
                        @keydown.enter.prevent="assign(i, option as 'x' | 'y' | 'z')">
                        {{ label }} axis
                    </button>
                    <button
                        class="w-full text-left text-xs px-3 py-2 text-xrb-text-secondary hover:bg-xrb-bg-3 focus:outline-none focus:bg-xrb-bg-3"
                        role="menuitem" @click.stop="assign(i, null)" @keydown.enter.prevent="assign(i, null)">
                        Unassign
                    </button>
                </div>
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