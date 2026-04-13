<script setup lang="ts">
    import type { Table                             } from '@/types/table';
    import      { DesmosGraphingCalculator, DGC_IDS } from '@/dgclib';
    import      { onMounted, onUnmounted, watch     } from 'vue';


    // Ref: https://vuejs.org/guide/components/events.html
    const prop = defineProps<{
        table: Table | null
    }>()
    const emit = defineEmits<{
        (e: 'ready'): void
    }>()
    

    // desmos stuff
    const options                              = {
        expressions: false
    }

    let   dgc: DesmosGraphingCalculator | null = null
    

    function clearFit(): void {
        if(!dgc) return
        
        dgc.clearFit()
    }

    function toggleExponential(): void {
        if(!dgc) return
        
        if (!dgc.hasFit(DGC_IDS.FIT_EXPONENTIAL)) dgc.fitExponential()
        else                                      dgc.clearExponential()
    }


    function toggleLinear(): void {
        if(!dgc) return
        
        if (!dgc.hasFit(DGC_IDS.FIT_LINEAR)) dgc.fitLinear()
        else                                 dgc.clearLinear()
    }


    function toggleLogarithmic(): void {
        if(!dgc) return
        
        if (!dgc.hasFit(DGC_IDS.FIT_LOGARITHMIC)) dgc.fitLogarithmic()
        else                                      dgc.clearLogarithmic()
    }


    function toggleLogistic(): void {
        if(!dgc) return
        
        if (!dgc.hasFit(DGC_IDS.FIT_LOGISTIC)) dgc.fitLogistic()
        else                                   dgc.clearLogistic()
    }


    function togglePolynomial(degree: number): void {
        if(!dgc) return
        
        if (!dgc.hasFit(DGC_IDS.FIT_POLYNOMIAL)) dgc.fitPolynomial(degree)
        else                                     dgc.clearPolynomial()
    }


    function togglePower(): void {
        if(!dgc) return
        
        if (!dgc.hasFit(DGC_IDS.FIT_POWER)) dgc.fitPower()
        else                                dgc.clearPower()
    }

    
    function toggleSinusoidal(): void {
        if(!dgc) return
        
        if (!dgc.hasFit(DGC_IDS.FIT_SINUSOIDAL)) dgc.fitSinusoidal()
        else                                     dgc.clearSinusoidal()
    }

    
    defineExpose({ 
        clearFit, 
        toggleExponential,
        toggleLinear, 
        toggleLogarithmic,
        toggleLogistic,
        togglePolynomial,
        togglePower,
        toggleSinusoidal
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