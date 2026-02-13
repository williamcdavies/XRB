<script setup lang="ts">
    import { onMounted } from 'vue';

    
    let calculator: any = null
    let options = {
        expressions: false
    }


    onMounted(async () => {
        const script   = document.createElement('script')
        script.async   = true
        script.src     = "https://www.desmos.com/api/v1.11/calculator.js?apiKey=6d296d9af7c9474a830bc30e6ab595a3"
        script.onerror = () => {
            console.error("Failed to create element: `script` for Graph.vue")
        }
        script.onload = () => {
            const elt = document.getElementById('calculator')
            if(elt) {
                calculator = new (window as any).Desmos.GraphingCalculator(elt, options)
                calculator.setExpression({ id: 'graph1', latex: 'y=x^2' })
            }
        }
    
        document.head.appendChild(script)
    })
</script>


<template>
    <div class="h-full w-full">
        <div id="calculator" class="h-full w-full"></div>
    </div>
</template>


<style scoped>
</style>