<script setup lang="ts">
    import      { onMounted, onUnmounted } from 'vue';
    import type { Table }                  from '@/types/table';


    // Ref: https://vuejs.org/guide/components/events.html
    const prop = defineProps<{
        table: Table | null
    }>()
    const emit = defineEmits<{
        (e: 'ready'): void
    }>()
    

    // desmos stuff
    const options         = {
        expressions: false
    }

    let   calculator: any = null


    function init() {
        const elt = document.getElementById('calculator')

        if(!elt || !(window as any).Desmos) {
            return
        }

        calculator = new (window as any).Desmos.GraphingCalculator(elt, options)
        
        calculator.setExpression({ id: 'graph', latex: 'y=x^2' })
        emit('ready')
    }


    // mounting stuff
    onMounted(() => {
        if((window as any).Desmos) {
            init()

            return
        }
        
        const script   = document.createElement('script')
        script.async   = true
        script.src     = "https://www.desmos.com/api/v1.11/calculator.js?apiKey=6d296d9af7c9474a830bc30e6ab595a3"
        script.onerror = () => {
            console.error("Failed to create element: `script` for Graph.vue")
        }
        script.onload  = init
    
        document.head.appendChild(script)
    })

    onUnmounted(() => {
        calculator?.destroy()
        calculator = null
    })
</script>


<template>
    <div class="h-full w-full">
        <div id="calculator" class="h-full w-full"></div>
    </div>
</template>


<style scoped>
</style>