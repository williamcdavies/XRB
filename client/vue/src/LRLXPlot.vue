<template>
    <div v-if="loading">
        <VueSpinner size="20" color="white" />
    </div>
    <div v-else-if="error">Error: {{ error }}</div>
    <div v-else>
        <apexchart ref="scatterplot" id="scatterplot" width="800px" type="scatter" :options="chartOptions" :series="series"></apexchart>
        <button @click="savePlot">Save to PDF</button>
    </div>
</template>

<script>
import axios from 'axios'
import VueApexCharts from "vue3-apexcharts";
import {
    VueSpinner,
} from 'vue3-spinners';
import { jsPDF } from 'jspdf';

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
            chartImage: null,
            chartOptions: {
                chart: {
                    type: 'scatter',
                    background: '#ffffff',
                    toolbar: {
                        show: true,
                        offsetX: 0,
                        offsetY: 0,
                        tools: {
                            download: false,
                            selection: true,
                            zoom: true,
                            zoomin: true,
                            zoomout: true,
                            pan: true,
                        },
                        autoSelected: 'none'
                    },
                },
                title: {
                    text: 'Radio vs X-ray Luminosity',
                    style: {
                        fontSize: '24px'
                    }
                },
                xaxis: {
                    type: 'numeric',
                    decimalsInFloat: 4,
                    title: {
                        text: 'log(LR) [erg/s]',
                    },
                    crosshairs: {
                        show: false
                    },
                    tooltip: {
                        enabled: false
                    }
                },
                yaxis: {
                    type: 'numeric',
                    decimalsInFloat: 4,
                    title: {
                        text: 'log(LX) [erg/s]',
                    },
                    crosshairs: {
                        show: false
                    },
                    tooltip: {
                        enabled: false
                    }
                },
                tooltip: {
                    enabled: true,
                    custom: ({ seriesIndex, dataPointIndex, w }) => {
                        // Use w.config.series to access the series data
                        const point = w.config.series[seriesIndex].data[dataPointIndex]

                        return `
                        <div style="padding: 10px; background: #333; border-radius: 4px;">
                            <strong>${w.config.series[seriesIndex].name}</strong><br/>
                            log(LR): ${point[0]}<br/>
                            log(LX): ${point[1]}
                        </div>
                        `
                    }
                }
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

            this.series = Object.entries(groupedLRLXs).map(([name, lrlxArray], index) => {
                return {
                    name: name,
                    hidden: index != 0,
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
                alert('Error fetching LRLX data!')
                console.error('Error fetching LRLXs:', err)
            } finally {
                this.loading = false
            }
        },

        async savePlot() {
            const { imgURI } = await this.$refs.scatterplot.dataURI()

            // create an image element to get dimensions
            const img = new Image()
            img.src = imgURI

            // load base64
            await new Promise((resolve) => {
                img.onload = resolve
            })
            const width = img.width
            const height = img.height

            // create PDF doc matching image size
            const doc = new jsPDF({
                orientation: "landscape",
                unit: 'px',
                format: [width, height]
            })
            doc.addImage(imgURI, "PNG", 20, 20, width - 40, height - 40)
            doc.save("lrlx-plot.pdf")
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
</style>