<script setup lang="ts">
    import      { VList } from 'virtua/vue'
    import      { ref   } from 'vue'
    import type { Table } from '@/types/table'

    // Ref: https://vuejs.org/guide/components/events.html
    const prop = defineProps<{
        table: Table | null
    }>()
    const emit = defineEmits<{
        (e: 'header', idx: number, name: string): void
    }>()


    // header stuff
    const subjectHeader = ref<number | null>(null)
    
    
    function startHeaderRename(idx: number): void {
        subjectHeader.value = idx
    }


    function finishHeaderRename(idx: number, name: string): void {
        emit('header', idx, name)

        subjectHeader.value = null
    }
</script>


<template>
    <div class="h-full w-full flex flex-col overflow-hidden">
        <!-- Header -->
        <div class="grid bg-xrb-bg-2 border-b border-xrb-border"
            :style="{ gridTemplateColumns: `3rem repeat(${prop.table?.headers.length ?? 0}, minmax(100px, 1fr))` }">
            <div class="text-xs px-3 py-1.5 font-semibold">#</div>
            <div v-for="(header, idx) in prop.table?.headers" :key="header"
                class="group flex items-center text-xs px-3 py-1.5">

                <!-- Editing state -->
                <input v-if="subjectHeader === idx"
                    class="h-full w-full bg-transparent font-semibold focus:outline-none" :value="header"
                    :ref="(el) => { if (el) (el as HTMLInputElement).select() }"
                    @blur="finishHeaderRename(idx, ($event.target as HTMLInputElement).value)"
                    @keydown.enter="finishHeaderRename(idx, ($event.target as HTMLInputElement).value)"
                    @keydown.escape="subjectHeader = null" />

                <!-- Default state -->
                <template v-else>
                    <span class="whitespace-nowrap overflow-hidden text-ellipsis font-semibold">{{ header }}</span>
                    <button
                        class="ml-1.5 shrink-0 opacity-0 group-hover:opacity-50 focus:opacity-100 hover:!opacity-100 transition-opacity duration-150"
                        @click="startHeaderRename(idx)" @keydown.enter.prevent="startHeaderRename(idx)"
                        @keydown.space.prevent="startHeaderRename(idx)">
                        <img src="@/assets/icons/pencils/edit_pencil_line_1.svg" class="w-3.5 h-3.5" />
                    </button>
                </template>
            </div>
        </div>

        <!-- Virtual rows -->
        <VList class="flex-1" :data="prop.table?.rows ?? []" #default="{ item, index }">
            <div class="grid hover:bg-xrb-bg-2 border-b border-xrb-border/50"
                :style="{ gridTemplateColumns: `3rem repeat(${prop.table?.headers.length ?? 0}, minmax(100px, 1fr))` }">
                <div class="text-xs px-3 py-1.5">{{ index + 1 }}</div>
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