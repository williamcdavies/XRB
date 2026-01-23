<script setup lang="ts">
    import axios from 'axios';
    import { useTemplateRef, onMounted } from 'vue';

    const calculatorRef = useTemplateRef('calculator');

    const DESMOS_API_KEY = '6d296d9af7c9474a830bc30e6ab595a3';

    async function fetchLRLXData() {
        const response = await axios.get('http://localhost:8080/api/lrlx');
        return response.data;
    }

    function formatScientificToLatex(value) {
        // start by splitting the value at 'e'
        const pair = value.split('e')
        
        // return scientific notation in latex
        return `${pair[0]}*10^{${pair[1]}}`
    }

    onMounted(() => {
        // TODO look at using vue-meta for cleaner handling of head tag
        const script = document.createElement('script');
        script.src = `https://www.desmos.com/api/v1.11/calculator.js?apiKey=` + DESMOS_API_KEY;

        script.onload = () => {
            // set options for desmos calculator
            const options = {
                expressions: false,
                logScales: true
            }

            // initialize the calculator once the script is loaded
            const calculator = Desmos.GraphingCalculator(calculatorRef.value, options);

            fetchLRLXData().then((lrlxArray) => {
                for (var i = 0 ; i < lrlxArray.length ; i++) {
                    const lrlxEntry = lrlxArray[i];
                    calculator.setExpression({ 
                        id: lrlxEntry.id, 
                        latex: `(${formatScientificToLatex(lrlxEntry.lr.toString())}, ${formatScientificToLatex(lrlxEntry.lx.toString())})` ,
                        label: lrlxEntry.name,
                        showLabel: true
                    })
                }
                calculator.focusFirstExpression();
            });
        };

        // Add the Desmos CDN to the top of the page
        document.head.appendChild(script);
    });
</script>

<template>
    <div ref="calculator" style="width: 1200px; height: 800px;"></div>
</template>


<style scoped></style>