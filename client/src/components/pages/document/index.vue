<script setup lang="ts">
    import { ref } from 'vue';
    
    import Topbar  from './Topbar.vue';
    import Leftbar from './Leftbar.vue';
    import Handle  from './Handle.vue';
    import Graph   from './Graph.vue';


    const MIN_LEFTBAR_WIDTH = 200
    const MIN_GRAPH_WIDTH   = 200
    const HANDLE_WIDTH      = 4
    
    const leftbarWidth      = ref(200)


    function onMouseDown() {
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
        window.removeEventListener('mousemove', onMouseMove)
        window.removeEventListener('mouseup', onMouseUp)
    }
</script>


<template>
    <div class="grid grid-rows-[auto_1fr] h-screen w-screen"
        :style="{ gridTemplateColumns: `${leftbarWidth}px ${HANDLE_WIDTH}px 1fr` }">
        <Topbar class="col-span-3 h-10" />
        <Leftbar class="row-start-2 h-full" />
        <Handle @mousedown="onMouseDown" class="row-start-2 h-full" />
        <Graph class="row-start-2 h-full w-full" />
    </div>
</template>


<style scoped>
</style>