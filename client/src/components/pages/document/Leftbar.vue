<script setup lang="ts">
    import type { Table      } from '@/types/table'
    import type { Group      } from '@/types/group'
    import      { ref, watch } from 'vue'

    import      FilePreview  from './FilePreview.vue'
    import      GroupPreview from './GroupPreview.vue'
    

    // Ref: https://vuejs.org/guide/components/events.html
    const prop = defineProps<{
        table:      Table | null
        hiddenRows: Set<number>
        aColumn:    string | null
        groups:     Map<string, Group>
    }>()
    const emit = defineEmits<{
        (e: 'toggle-row-hidden', index: number):  void
        (e: 'toggle-all-rows-hidden'):            void
        (e: 'header', idx: number, name: string): void
        (e: 'toggle-group-hidden', key: string):  void
        (e: 'toggle-all-groups-hidden'):          void
    }>()

    const showGroups = ref(false)

    watch(() => prop.aColumn, (value) => {
        if (!value) showGroups.value = false
    })
</script>


<template>
    <div class="h-full w-full overflow-hidden">
        <FilePreview :table="prop.table" :hidden-rows="prop.hiddenRows"
            @toggle-row-hidden="(i: number) => emit('toggle-row-hidden', i)"
            @toggle-all-rows-hidden="emit('toggle-all-rows-hidden')" @header="(idx, name) => emit('header', idx, name)" />
        <GroupPreview :groups="prop.groups" @toggle-group-hidden="emit('toggle-group-hidden', $event)"
            @toggle-all-groups-hidden="emit('toggle-all-groups-hidden')" />
    </div>
</template>


<style scoped>
</style>
