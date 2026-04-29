<script setup lang="ts">
    import type { Group      } from '@/types/group'
    import      { VList         } from 'virtua/vue'
    import      { computed, ref } from 'vue'

    // Ref: https://vuejs.org/guide/components/events.html
    const prop = defineProps<{
        groups: Map<string, Group>
    }>()
    const emit = defineEmits<{
        (e: 'toggle-group-hidden', key: string): void
        (e: 'toggle-all-groups-hidden'):         void
    }>()

    // preview stuff
    const colCount = 2
    const gridCols = computed(() => `2rem 3rem repeat(${colCount}, minmax(100px, 1fr))`)

    // toggle stuff
    const allHidden = computed(() =>
        prop.groups.size > 0 &&
        [...prop.groups.values()].every(g => g.hidden)
    )
</script>


<template>
    <div class="h-full w-full overflow-x-auto">
        <div class="h-full flex flex-col" :style="{ minWidth: `calc(5rem + ${colCount} * 100px)` }">
            <!-- Header -->
            <div class="grid shrink-0 bg-xrb-bg-2 border-b border-xrb-border"
                :style="{ gridTemplateColumns: gridCols }">
                <button class="text-xs px-1 py-2 text-xrb-text-secondary hover:text-xrb-text-1 cursor-pointer"
                    @click="emit('toggle-all-groups-hidden')">
                    {{ allHidden ? '○' : '●' }}
                </button>
                <div class="text-xs font-medium text-xrb-text-secondary px-3 py-2">#</div>
                <div class="text-xs font-semibold px-3 py-2">Name</div>
                <div class="text-xs font-semibold px-3 py-2">Color</div>
            </div>
            <!-- Virtual rows -->
            <VList class="flex-1" :data="[...prop.groups.entries()]" #default="{ item: [key, entry], index }">
                <div class="grid border-b border-xrb-border/50"
                    :class="entry.hidden ? 'opacity-30' : 'hover:bg-xrb-bg-2'"
                    :style="{ gridTemplateColumns: gridCols }">
                    <button class="text-xs px-1 py-1.5 text-xrb-text-secondary hover:text-xrb-text-1 cursor-pointer"
                        @click="emit('toggle-group-hidden', key)">
                        {{ entry.hidden ? '○' : '●' }}
                    </button>
                    <div class="text-xs px-3 py-1.5 whitespace-nowrap">{{ index + 1 }}</div>
                    <div class="text-xs px-3 py-1.5 whitespace-nowrap">Group {{ index + 1 }}</div>
                    <div class="text-xs px-3 py-1.5 whitespace-nowrap flex items-center gap-2">
                        <div class="w-3 h-3 rounded-sm shrink-0" :style="{ backgroundColor: entry.colour }"></div>
                        {{ entry.colour }}
                    </div>
                </div>
            </VList>
        </div>
    </div>
</template>


<style scoped>
</style>
