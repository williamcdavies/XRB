<script setup lang="ts">
    import      { DesmosGraphingCalculator }      from '@/dgclib';
    import      { onMounted, onUnmounted, watch } from 'vue';
    import type { Table }                         from '@/types/table';


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
    

    function clearFit(): void {
        if(!dgc) return
        
        dgc.clearFit()
    }

    function fitExponential(): void {
        if(!dgc) return
        dgc.fitExponential()
    }


    function fitLinear(): void {
        if(!dgc) return
        
        dgc.fitLinear()
    }


    function fitLogarithmic(): void {
        if(!dgc) return
        dgc.fitLogarithmic()
    }


    function fitLogistic(): void {
        if(!dgc) return
        dgc.fitLogistic()
    }


    function fitPolynomial(degree: number): void {
        if(!dgc) return
        dgc.fitPolynomial(degree)
    }


    function fitPower(): void {
        if(!dgc) return
        dgc.fitPower()
    }

    
    function fitSinusoidal(): void {
        if(!dgc) return
        dgc.fitSinusoidal()
    }

    
    defineExpose({ 
        clearFit, 
        fitExponential,
        fitLinear, 
        fitLogarithmic,
        fitLogistic,
        fitPolynomial,
        fitPower,
        fitSinusoidal
    })


    // mounting stuff
    onMounted(() => {
        const elt = document.getElementById('calculator')

        if(!elt) return

        dgc = new DesmosGraphingCalculator(elt, options)
        dgc.setXLabel('X');
        dgc.setYLabel('Y');

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

        dgc.load(x, 
                 y, 
                 newTable.headers[0], 
                 newTable.headers[1])
    })
</script>


<template>
    <div class="h-full w-full">
        <div id="calculator" class="h-full w-full"></div>
    </div>
</template>


<style scoped>
</style>