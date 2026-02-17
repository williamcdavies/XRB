<script setup lang="ts">
    import { ref } from 'vue';
    
    import Topbar  from './Topbar.vue';
    import Leftbar from './Leftbar.vue';
    import Handle  from './Handle.vue';
    import Graph   from './Graph.vue';


    const MIN_LEFTBAR_WIDTH     = 200
    const MIN_GRAPH_WIDTH       = 200
    const HANDLE_WIDTH          = 10
    
    const leftbarWidth          = ref(200)
    const handleClass           = ref('bg-transparent')


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
</script>


<template>
    <div class="grid grid-rows-[auto_1fr] h-screen w-screen bg-xrb-bg-1"
        :style="{ gridTemplateColumns: `${leftbarWidth}px ${HANDLE_WIDTH}px 1fr` }">
        <Topbar class="col-span-3" />
        <Leftbar class="row-start-2" />
        <Handle @mousedown="onMouseDown" class="row-start-2" :class="handleClass" />
        <Graph class="row-start-2" />
    </div>
</template>


<style scoped>
</style>