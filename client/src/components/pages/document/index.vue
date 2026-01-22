<script setup lang="ts">
    import Desmos from 'desmos';
    import { useTemplateRef, onMounted } from 'vue';

    const calculatorRef = useTemplateRef('calculator');
    // Replace 'dcb31709b452b1cf9dc26972add0fda6' with your own production API key.
    const API_KEY = '6d296d9af7c9474a830bc30e6ab595a3';

    onMounted(() => {
        // TODO look at using vue-meta for cleaner handling of head tag
        const script = document.createElement('script');
        script.src = `https://www.desmos.com/api/v1.11/calculator.js?apiKey=` + API_KEY;

        script.onload = () => {
            // initialize the calculator once the script is loaded
            const calculator = Desmos.GraphingCalculator(calculatorRef.value);
            calculator.setExpression({ id: 'graph1', latex: 'y=x^2' });
        };

        // Add the Desmos CDN to the top of the page
        document.head.appendChild(script);
    });
</script>

<template>
    <div ref="calculator" style="width: 600px; height: 600px;"></div>
</template>


<style scoped></style>