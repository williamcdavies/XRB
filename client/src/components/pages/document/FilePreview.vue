<script setup lang="ts">
    import type { Table         } from '@/types/table'
    import      { VList         } from 'virtua/vue'
    import      { computed, ref } from 'vue'

    // Ref: https://vuejs.org/guide/components/events.html
    const prop = defineProps<{
        table:      Table | null
        hiddenRows: Set<number>
    }>()
    const emit = defineEmits<{
        (e: 'toggle-row-hidden', index: number):  void
        (e: 'toggle-all-hidden'):                 void
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

    // preview stuff
    const colCount = computed(() => Math.max(prop.table?.headers.length ?? 0, 1))
    const gridCols = computed(() => `2rem 3rem repeat(${colCount.value}, minmax(100px, 1fr))`)

    // toggle stuff
    const allHidden = computed(() =>
        prop.table !== null && prop.table.rows.length > 0 &&
        prop.table.rows.every((_, i) => prop.hiddenRows.has(i))
    )
</script>


<template>
    <div class="h-full w-full overflow-x-auto">
        <div class="h-full flex flex-col" :style="{ minWidth: `calc(5rem + ${colCount} * 100px)` }">
            <!-- Header -->
            <div class="grid shrink-0 bg-xrb-bg-2 border-b border-xrb-border"
                :style="{ gridTemplateColumns: gridCols }">
                <button v-if="prop.table !== null" class="text-xs px-1 py-2 text-xrb-text-secondary hover:text-xrb-text-1 cursor-pointer"
                    @click="emit('toggle-all-hidden')">
                    {{ allHidden ? '○' : '●' }}
                </button>
                <div class="text-xs font-medium text-xrb-text-secondary px-3 py-2">#</div>
                <div v-for="(header, idx) in prop.table?.headers" :key="header"
                    class="group flex items-center text-xs px-3 py-2">
                    <input v-if="subjectHeader === idx"
                        class="h-full w-full bg-transparent font-semibold focus:outline-none" :value="header"
                        :ref="(el) => { if (el) (el as HTMLInputElement).select() }"
                        @blur="finishHeaderRename(idx, ($event.target as HTMLInputElement).value)"
                        @keydown.enter="finishHeaderRename(idx, ($event.target as HTMLInputElement).value)"
                        @keydown.escape="subjectHeader = null" />
                    <template v-else>
                        <span class="truncate font-semibold">{{ header }}</span>
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
                <div class="grid border-b border-xrb-border/50"
                    :class="prop.hiddenRows.has(index) ? 'opacity-30' : 'hover:bg-xrb-bg-2'"
                    :style="{ gridTemplateColumns: gridCols }">
                    <button class="text-xs px-1 py-1.5 text-xrb-text-secondary hover:text-xrb-text-1 cursor-pointer"
                        @click="emit('toggle-row-hidden', index)">
                        {{ prop.hiddenRows.has(index) ? '○' : '●' }}
                    </button>
                    <div class="text-xs px-3 py-1.5 whitespace-nowrap">{{ index + 1 }}</div>
                    <div v-for="(cell, j) in item" :key="j" class="text-xs px-3 py-1.5 truncate">
                        {{ cell }}
                    </div>
                </div>
            </VList>
        </div>
    </div>
</template>


<style scoped>
</style>
