<script setup lang="ts">
    import      { onBeforeUnmount, onMounted, ref } from 'vue';
    import type { Table }                           from '@/types/table';
    import      { parseCSV }                        from '@/utils/parse';
    
    import      ColorLayer                          from '@/components/layers/ColorLayer.vue';
    import      Topbar                              from './Topbar.vue';
    import      Leftbar                             from './Leftbar.vue';
    import      Handle                              from './Handle.vue';
    import      Graph                               from './Graph.vue';


    // pretty loading stuff
    const isContentReady = ref(false)
    

    // container adjustment stuff
    const MIN_LEFTBAR_WIDTH = 200
    const MIN_GRAPH_WIDTH   = 200
    const HANDLE_WIDTH      = 10
    
    const leftbarWidth      = ref(Math.floor(window.innerWidth / 2))
    const handleClass       = ref('bg-transparent')


    function onMouseDown() {
        handleClass.value = 'bg-xrb-bg-3'

        window.addEventListener('mousemove', onMouseMove)
        window.addEventListener('mouseup', onMouseUp)
    }


    function onMouseMove(e: MouseEvent) {
        leftbarWidth.value = Math.min(
            Math.max(MIN_LEFTBAR_WIDTH, e.clientX),
            window.innerWidth - MIN_GRAPH_WIDTH - HANDLE_WIDTH
        )
    }


    function onMouseUp() {
        handleClass.value = 'transparent'

        window.removeEventListener('mousemove', onMouseMove)
        window.removeEventListener('mouseup', onMouseUp)
    }


    function onWindowResize() {
        leftbarWidth.value = Math.min(
            leftbarWidth.value,
            window.innerWidth - MIN_GRAPH_WIDTH - HANDLE_WIDTH
        )
    }


    // data stuff
    const table = ref<Table | null>(null)

    
    async function onFileReceived(file: File) {
        const text  = await file.text()
        table.value = parseCSV(text)
    }


    // graph stuff
    const graph           = ref<InstanceType<typeof Graph> | null>(null)


    function clearFit():                       void { graph.value?.clearFit()               }
    function toggleExponential():              void { graph.value?.toggleExponential()      }
    function toggleLinear():                   void { graph.value?.toggleLinear()           }
    function toggleLogistic():                 void { graph.value?.toggleLogistic()         }
    function toggleLogarithmic():              void { graph.value?.toggleLogarithmic()      }
    function togglePolynomial(degree: number): void { graph.value?.togglePolynomial(degree) }
    function togglePower():                    void { graph.value?.togglePower()            }
    function toggleSinusoidal():               void { graph.value?.toggleSinusoidal()       }


    // header stuff
    const selectedHeaders = ref<{ x: number | null, y: number | null, z: number | null }>({ x: null, y: null, z: null })


    function onSelectedHeaders(headers: { x: number | null, y: number | null, z: number | null }): void {
        selectedHeaders.value = headers
    }
    

    // mounting stuff
    onMounted(() => {
        window.addEventListener('resize', onWindowResize)
    })

    
    onBeforeUnmount(() => {
        window.removeEventListener('resize', onWindowResize)
    })
</script>


<template>
    <div class="grid grid-rows-[auto_1fr] h-screen w-screen bg-xrb-bg-1"
        :style="{ gridTemplateColumns: `${leftbarWidth}px ${HANDLE_WIDTH}px 1fr` }">
        <!-- Z0 -->
        <Topbar @file-selected="onFileReceived" @clear-fit="clearFit" @toggle-exponential="toggleExponential"
            @toggle-linear="toggleLinear" @toggle-logistic="toggleLogistic" @toggle-logarithmic="toggleLogarithmic"
            @toggle-polynomial="togglePolynomial" @toggle-power="togglePower" @toggle-sinusoidal="toggleSinusoidal" class="col-span-3" />
        <Leftbar @selected-headers="onSelectedHeaders" :table="table" class="row-start-2" />
        <Handle @mousedown="onMouseDown" class="row-start-2" :class="handleClass" />
        <Graph ref="graph" :table="table" :selected-headers="selectedHeaders" @ready="isContentReady = true" class="row-start-2" />

        <!-- Z1 -->
        <transition name="fade">
            <ColorLayer v-if="!isContentReady" />
        </transition>
    </div>
</template>


<style scoped>
    .fade-enter-active,
    .fade-leave-active {
        transition: opacity 0.33s;
    }
    
    .fade-enter-from,
    .fade-leave-to {
        opacity: 0;
    }
    
    .fade-enter-to,
    .fade-leave-from {
        opacity: 1;
    }
</style>