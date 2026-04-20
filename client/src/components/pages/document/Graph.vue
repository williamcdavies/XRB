<script setup lang="ts">
    import type { Table                             } from '@/types/table';
    import type { FitState                          } from '@/types/view';
    import      { DesmosGraphingCalculator, DGC_IDS } from '@/dgclib';
    import      { onMounted, onUnmounted, watch     } from 'vue';


    // Ref: https://vuejs.org/guide/components/events.html
    const prop = defineProps<{
        table:      Table | null
        hiddenRows: Set<number>
        xColumn:    string | null
        yColumn:    string | null
        aColumn:    string | null
    }>()
    const emit = defineEmits<{
        (e: 'ready'): void
    }>()


    // desmos stuff
    const options = {
        expressions: false
    }

    let dgc: DesmosGraphingCalculator | null = null
    let lastPolyDegree: number               = 2


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

        if (!dgc.hasFit(DGC_IDS.FIT_POLYNOMIAL)) {
            lastPolyDegree = degree
            dgc.fitPolynomial(degree)
        }
        else dgc.clearPolynomial()
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


    function getFitState(): FitState {
        return {
            linear:          !!dgc?.hasFit(DGC_IDS.FIT_LINEAR),
            exponential:     !!dgc?.hasFit(DGC_IDS.FIT_EXPONENTIAL),
            logarithmic:     !!dgc?.hasFit(DGC_IDS.FIT_LOGARITHMIC),
            logistic:        !!dgc?.hasFit(DGC_IDS.FIT_LOGISTIC),
            polynomial:      !!dgc?.hasFit(DGC_IDS.FIT_POLYNOMIAL),
            polynomialDegree: lastPolyDegree,
            power:           !!dgc?.hasFit(DGC_IDS.FIT_POWER),
            sinusoidal:      !!dgc?.hasFit(DGC_IDS.FIT_SINUSOIDAL),
        }
    }


    function restoreFits(fits: FitState): void {
        if (!dgc) return

        dgc.clearFit()

        if (fits.linear)      dgc.fitLinear()
        if (fits.exponential) dgc.fitExponential()
        if (fits.logarithmic) dgc.fitLogarithmic()
        if (fits.logistic)    dgc.fitLogistic()
        if (fits.power)       dgc.fitPower()
        if (fits.sinusoidal)  dgc.fitSinusoidal()
        if (fits.polynomial) {
            lastPolyDegree = fits.polynomialDegree ?? 2
            dgc.fitPolynomial(lastPolyDegree)
        }
    }


    defineExpose({
        clearFit,
        toggleExponential,
        toggleLinear,
        toggleLogarithmic,
        toggleLogistic,
        togglePolynomial,
        togglePower,
        toggleSinusoidal,
        getFitState,
        restoreFits,
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
    watch([() => prop.table, () => prop.hiddenRows, () => prop.xColumn, () => prop.yColumn], () => {
        if(!prop.table || !dgc)            return
        if(!prop.xColumn || !prop.yColumn) return

        const xIdx = prop.table.headers.indexOf(prop.xColumn)
        const yIdx = prop.table.headers.indexOf(prop.yColumn)
        
        if(xIdx < 0 || yIdx < 0) return

        const x: string[] = []
        const y: string[] = []

        for(let i = 0; i < prop.table.rows.length; i++) {
            if(prop.hiddenRows.has(i)) continue
            
            const row = prop.table.rows[i]!
            
            x.push(row[xIdx]!)
            y.push(row[yIdx]!)
        }

        dgc.load(x,
                 y,
                 prop.xColumn,
                 prop.yColumn)
    }, { deep: true })

    watch([() => prop.table, () => prop.hiddenRows, () => prop.xColumn, () => prop.yColumn, () => prop.aColumn], () => {
    if(!prop.table || !dgc) return
    if(!prop.xColumn || !prop.yColumn) return

    const xIdx = prop.table.headers.indexOf(prop.xColumn)
    const yIdx = prop.table.headers.indexOf(prop.yColumn)

    if(xIdx < 0 || yIdx < 0) return

    if(prop.aColumn) {
        const aIdx = prop.table.headers.indexOf(prop.aColumn)
        
        if(aIdx < 0) return

        // select distinct values from aColumn
        const distinctKeys = [...new Set(
            prop.table.rows.map(row => row[aIdx] ?? '(empty)')
        )]

        // map distinct values to colours
        const colorMap = new Map<string, string>()
        
        distinctKeys.forEach((key, i) => {
            colorMap.set(key, `hsl(${Math.round((i / distinctKeys.length) * 360)}, 50%, 50%)`)
        })

        // build groups from visible rows only
        const groups = new Map<string, { x: string[], y: string[] }>()
        
        distinctKeys.forEach(key => groups.set(key, { x: [], y: [] }))

        for(let i = 0; i < prop.table.rows.length; i++) {
            if(prop.hiddenRows.has(i)) continue

            const row = prop.table.rows[i]!
            const key = row[aIdx] ?? '(empty)'

            groups.get(key)!.x.push(row[xIdx]!)
            groups.get(key)!.y.push(row[yIdx]!)
        }

        const allX: string[] = []
        const allY: string[] = []
        groups.forEach((data) => { allX.push(...data.x); allY.push(...data.y) })

        const viewport = dgc.getViewport()
        dgc.clear()
        dgc.setViewport(viewport)
        
        dgc.add(allX, allY)

        let varIndex = 2

        groups.forEach((data, key) => {
            if(data.x.length === 0) return
            
            dgc!.add(data.x, data.y, colorMap.get(key), varIndex++)
        })
    } else {
        const x: string[] = []
        const y: string[] = []

        for(let i = 0; i < prop.table.rows.length; i++) {
            if(prop.hiddenRows.has(i)) continue

            const row = prop.table.rows[i]!

            x.push(row[xIdx]!)
            y.push(row[yIdx]!)
        }

        dgc.load(x, y, prop.xColumn, prop.yColumn)
    }
}, { deep: true })
</script>


<template>
    <div class="h-full w-full">
        <div id="calculator" class="h-full w-full"></div>
    </div>
</template>


<style scoped>
</style>
