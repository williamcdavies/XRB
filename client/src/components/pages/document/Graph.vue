<script setup lang="ts">
    import type { Group                             } from '@/types/group'
    import type { Table                             } from '@/types/table';
    import type { FitState, Viewport                } from '@/types/view';
    import      { DesmosGraphingCalculator, DGC_IDS } from '@/dgclib';
    import      { onMounted, onUnmounted, watch     } from 'vue';


    // Ref: https://vuejs.org/guide/components/events.html
    const prop = defineProps<{
        table:      Table | null
        hiddenRows: Set<number>
        xColumn:    string | null
        yColumn:    string | null
        aColumn:    string | null
        groups:     Map<string, Group>
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


    function getViewport(): Viewport | null {
        if (!dgc) return null
        return dgc.getViewport() ?? null
    }


    function setViewport(vp: Viewport): void {
        dgc?.setViewport(vp)
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
        getViewport,
        setViewport,
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
    watch([() => prop.table, () => prop.hiddenRows, () => prop.xColumn, () => prop.yColumn, () => prop.aColumn, () => prop.groups], () => {
        console.log('watch fired, groups size:', prop.groups.size)
        if(!prop.table || !dgc)            return
        if(!prop.xColumn || !prop.yColumn) return

        const xIdx = prop.table.headers.indexOf(prop.xColumn)
        const yIdx = prop.table.headers.indexOf(prop.yColumn)

        if(xIdx < 0 || yIdx < 0) return

        if(prop.aColumn) {
            const aIdx = prop.table.headers.indexOf(prop.aColumn)
            
            if(aIdx < 0) return

            // build groups from visible rows only, skipping hidden groups
            const groupData = new Map<string, { x: string[], y: string[] }>()
            
            prop.groups.forEach((_, key) => groupData.set(key, { x: [], y: [] }))

            for(let i = 0; i < prop.table.rows.length; i++) {
                if(prop.hiddenRows.has(i)) continue
                
                const row = prop.table.rows[i]!
                const key = row[aIdx] ?? '(empty)'
                
                groupData.get(key)?.x.push(row[xIdx]!)
                groupData.get(key)?.y.push(row[yIdx]!)
            }

            // combined table for fits (x_1/y_1)
            const allX: string[] = []
            const allY: string[] = []
            
            prop.groups.forEach((entry, key) => {
                if(entry.hidden) return
                
                const data = groupData.get(key)!
                
                allX.push(...data.x)
                allY.push(...data.y)
            })

            const viewport = dgc.getViewport()
            
            dgc.clear()
            dgc.addHidden(allX, allY)
            dgc.setXLabel(prop.xColumn)
            dgc.setYLabel(prop.yColumn)

            prop.groups.forEach((entry, key) => {
                if(entry.hidden) return
                
                const data = groupData.get(key)!
                
                if(data.x.length === 0) return
                
                dgc!.add(data.x, data.y, entry.colour, entry.index)
            })

            dgc.setViewport(viewport)
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
