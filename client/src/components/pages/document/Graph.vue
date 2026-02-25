<script setup lang="ts">
    import      { DesmosGraphingCalculator }      from '@/dgclib';
    import      { onMounted, onUnmounted, watch } from 'vue';
    import type { Table }                         from '@/dgclib/types';


    // Ref: https://vuejs.org/guide/components/events.html
    const prop = defineProps<{
        table: Table | null
    }>()
    const emit = defineEmits<{
        (e: 'ready'): void
    }>()
    

    // desmos stuff
    const options                            = {
        expressions: false
    }

    let dgc: DesmosGraphingCalculator | null = null
    

    // mounting stuff
    onMounted(() => {
        const elt = document.getElementById('calculator')

        if(!elt) return

        dgc = new DesmosGraphingCalculator(elt, options)

        emit('ready')
    })


    onUnmounted(() => {
        dgc?.destroy()
        dgc = null
    })


    // watching
    watch(() => prop.table, (newTable) => {
        if(!newTable || !dgc) return

        const x = newTable.rows.map(r => Number(r[0]))
        const y = newTable.rows.map(r => Number(r[1]))

        dgc.populate(x, 
                     y, 
                     newTable.headers[0] ?? 'X', 
                     newTable.headers[1] ?? 'Y')
    })
</script>


<template>
    <div class="h-full w-full">
        <div id="calculator" class="h-full w-full"></div>
    </div>
</template>


<style scoped>
</style>