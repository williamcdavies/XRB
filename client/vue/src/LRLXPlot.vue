<template>
    <div v-if="loading">
        <VueSpinner size="20" color="white" />
    </div>
    <div v-else-if="error">Error: {{ error }}</div>
    <div v-else id="lrlx-plot">
        <apexchart width="800px" type="scatter" :options="chartOptions" :series="series"></apexchart>
    </div>
</template>

<script>
import axios from 'axios'
import VueApexCharts from "vue3-apexcharts";
import {
    VueSpinner,
} from 'vue3-spinners';

export default {
    components: {
        apexchart: VueApexCharts,
        VueSpinner,
    },

    data() {
        return {
            lrlxs: [],
            loading: false,
            error: null,
            series: [],
            chartOptions: {
                chart: {
                    type: 'scatter',
                },
                title: {
                    text: 'Radio vs X-ray Luminosity',
                    style: {
                        color: '#e0e0e0'
                    }
                },
                xaxis: {
                    type: 'numeric',
                    decimalsInFloat: 4,
                    title: {
                        text: 'log(LR) [erg/s]',
                        style: {
                            color: '#e0e0e0'
                        }
                    },
                    labels: {
                        style: {
                            colors: '#e0e0e0'
                        }
                    }
                },
                yaxis: {
                    type: 'numeric',
                    decimalsInFloat: 4,
                    title: {
                        text: 'log(LX) [erg/s]',
                        style: {
                            color: '#e0e0e0'
                        }
                    },
                    labels: {
                        style: {
                            colors: '#e0e0e0'
                        }
                    }
                },
            },
        }
    },

    methods: {
        updateSeries() {
            const groupedLRLXs = this.lrlxs.reduce((acc, lrlx) => {
                const name = lrlx.name

                if (!acc[name]) {
                    acc[name] = []
                }
                
                acc[name].push(lrlx)
                
                return acc
            }, {})

            this.series = Object.entries(groupedLRLXs).map(function ([name, lrlxArray]) {
                return {
                    name: name,
                    data: lrlxArray.map(function (lrlx) {
                        return [Math.log10(lrlx.lr), Math.log10(lrlx.lx)]
                    })
                }
            })
        },

        async fetchLRLXs() {
            this.loading = true
            this.error = null

            try {
                const response = await axios.get('http://localhost:8080/api/lrlx/')
                this.lrlxs = response.data
                this.updateSeries()
            } catch (err) {
                this.error = err.message
                console.error('Error fetching LRLXs:', err)
            } finally {
                this.loading = false
            }
        }
    },

    mounted() {
        this.fetchLRLXs()
    }
}
</script>

<style scoped>
body {
    margin: 0;
    padding: 0;
    background-color: #202020 !important;
}

div {
    padding: 20px;
    text-align: center;
    font-size: 18px;
}

#lrlx-plot {
    background-color: #ffffff;
}
</style>