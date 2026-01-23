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
                expressions: true,
                logScales: true,
                xAxisScale: 'logarithmic',
                yAxisScale: 'logarithmic'
            }

            // initialize the calculator once the script is loaded
            const calculator = Desmos.GraphingCalculator(calculatorRef.value, options);
            
            // initialize array of expressions that will be filled with points of lrlx data
            var lrlxPoints = []

            fetchLRLXData().then((lrlxArray) => {
                // table defaults to hidden since we are already displaying points as expressions
                var lrColumn = {
                    latex: 'x',
                    hidden: true,
                    values: []
                }
                var lxColumn = {
                    latex: 'y',
                    hidden: true,
                    values: []
                }
                for (var i = 0 ; i < lrlxArray.length ; i++) {
                    const lrlxEntry = lrlxArray[i];

                    // add point to table
                    lrColumn.values.push(formatScientificToLatex(lrlxEntry.lr.toString()))
                    lxColumn.values.push(formatScientificToLatex(lrlxEntry.lx.toString()))

                    // add point as expression
                    lrlxPoints.push({ 
                        id: lrlxEntry.id, 
                        latex: `(${formatScientificToLatex(lrlxEntry.lr.toString())}, ${formatScientificToLatex(lrlxEntry.lx.toString())})` ,
                        label: lrlxEntry.name,
                        showLabel: true
                    })
                }

                const lrlxTable = {
                    type: 'table',
                    columns: [lrColumn, lxColumn]
                }
                calculator.setExpression(lrlxTable)
                calculator.setExpressions(lrlxPoints)
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