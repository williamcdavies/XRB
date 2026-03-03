<script setup lang="ts">
    import axios from 'axios';
    import { onMounted, ref, watch, computed } from 'vue';

    // Plain variable for Desmos calculator - NOT a Vue ref to avoid proxy issues
    let calculator: any = null;

    const DESMOS_API_KEY = '6d296d9af7c9474a830bc30e6ab595a3';
    const API_BASE_URL = 'http://localhost:8080';

    // Available data files
    const dataFiles = [
        { label: 'LRLX Data (Black Holes)', value: 'clean_data/lrlx_data_BH_CLEAN.csv' },
        { label: 'XRB Properties', value: 'clean_data/xrb_properties_CLEAN.csv' },
    ];

    // Regression types
    const regressionTypes = [
        { label: 'None', value: 'none' },
        { label: 'Linear (y = mx + b)', value: 'linear' },
        { label: 'Power Law (y = ax^b)', value: 'power' },
        { label: 'Exponential (y = ae^(bx))', value: 'exponential' },
        { label: 'Logarithmic (y = a + b·ln(x))', value: 'logarithmic' },
    ];

    // Reactive state - start with no file selected so user must choose
    const selectedFile = ref<string>('');
    const fileData = ref<any[]>([]);
    const columns = ref<string[]>([]);
    const columnStats = ref<Record<string, any>>({});
    const metadata = ref<any>(null);
    const isLoading = ref(false);
    const error = ref<string | null>(null);

    // Selected columns for plotting
    const xColumn = ref<string>('');
    const yColumn = ref<string>('');
    const labelColumn = ref<string>('');

    // Regression settings
    const regressionType = ref<string>('none');
    const regressionEquation = ref<string>('');

    // Store last plotted values for auto-zoom on scale change
    let lastPlottedX: number[] = [];
    let lastPlottedY: number[] = [];

    // Axis scale settings
    const xAxisScale = ref<string>('logarithmic');
    const yAxisScale = ref<string>('logarithmic');
    const scaleOptions = [
        { label: 'Linear', value: 'linear' },
        { label: 'Logarithmic', value: 'logarithmic' },
    ];

    // Filter to show only numeric columns for X and Y axes
    const numericColumns = computed(() => {
        return columns.value.filter(col => {
            const stats = columnStats.value[col];
            return stats?.is_numeric;
        });
    });

    // All columns for label selection
    const labelColumns = computed(() => {
        return ['(None)', ...columns.value];
    });

    async function fetchFileData(filePath: string) {
        isLoading.value = true;
        error.value = null;
        
        try {
            const response = await axios.get(`${API_BASE_URL}/api/data/file/`, {
                params: {
                    path: filePath,
                    include_stats: 'true',
                    include_metadata: 'true'
                }
            });
            
            const result = response.data;
            
            if (result.success) {
                fileData.value = result.data;
                columns.value = result.columns;
                const stats = result.column_stats || {};
                columnStats.value = stats;
                metadata.value = result.metadata;
                
                // Auto-select first two numeric columns if available
                const numCols = result.columns.filter((col: string) => stats[col]?.is_numeric);
                if (numCols.length >= 2) {
                    xColumn.value = numCols[0] ?? '';
                    yColumn.value = numCols[1] ?? '';
                } else if (numCols.length === 1) {
                    xColumn.value = numCols[0] ?? '';
                    yColumn.value = numCols[0] ?? '';
                }
                
                // Auto-select first non-numeric column as label, or first column
                const nonNumericCols = result.columns.filter((col: string) => !stats[col]?.is_numeric);
                labelColumn.value = nonNumericCols.length > 0 ? (nonNumericCols[0] ?? '(None)') : '(None)';
                
                // Show warnings if any
                if (metadata.value?.warning_count > 0) {
                    console.warn('Data warnings:', metadata.value.warnings);
                }
                
                // Explicitly update plot after data is loaded and auto-zoom
                const plotResult = updatePlot();
                if (plotResult) {
                    autoZoom(plotResult.xNumeric, plotResult.yNumeric);
                }
            } else {
                error.value = result.error || 'Failed to load data';
            }
        } catch (err: any) {
            error.value = err.response?.data?.error || err.message || 'Failed to fetch data';
            console.error('Error fetching file data:', err);
        } finally {
            isLoading.value = false;
        }
    }

    function formatScientificToLatex(value: number | string): string {
        if (value === null || value === undefined) return '';
        
        const numValue = typeof value === 'string' ? parseFloat(value) : value;
        
        if (isNaN(numValue) || !isFinite(numValue)) return '';
        
        // Convert to scientific notation string
        const sciStr = numValue.toExponential();
        const pair = sciStr.split('e');
        
        // Format exponent (remove leading + and zeros)
        let exponent = parseInt(pair[1] ?? '0', 10).toString();
        
        return `${pair[0]}*10^{${exponent}}`;
    }

    function getRegressionExpression(type: string): { latex: string; params: string[] } | null {
        switch (type) {
            case 'linear':
                return {
                    latex: 'y_1 \\sim m x_1 + b',
                    params: ['m', 'b']
                };
            case 'power':
                return {
                    latex: 'y_1 \\sim a x_1^{n}',
                    params: ['a', 'n']
                };
            case 'exponential':
                return {
                    latex: 'y_1 \\sim a e^{b x_1}',
                    params: ['a', 'b']
                };
            case 'logarithmic':
                return {
                    latex: 'y_1 \\sim a + b \\ln(x_1)',
                    params: ['a', 'b']
                };
            default:
                return null;
        }
    }

    // Generate distinct colors for points using HSL color wheel
    function getPointColor(index: number): string {
        // Use golden ratio for better color distribution
        const hue = (index * 137.508) % 360;
        const saturation = 70;
        const lightness = 50;
        return `hsl(${hue}, ${saturation}%, ${lightness}%)`;
    }

    function autoZoom(xValues: number[], yValues: number[]) {
        if (!calculator || xValues.length === 0 || yValues.length === 0) return;
        
        // Store for later use (e.g., when axis scales change)
        lastPlottedX = xValues;
        lastPlottedY = yValues;
        
        const xMin = Math.min(...xValues);
        const xMax = Math.max(...xValues);
        const yMin = Math.min(...yValues);
        const yMax = Math.max(...yValues);
        
        let bounds;
        
        if (xAxisScale.value === 'logarithmic' && yAxisScale.value === 'logarithmic') {
            // For log-log scale, add padding in log space
            const xLogMin = Math.log10(xMin);
            const xLogMax = Math.log10(xMax);
            const yLogMin = Math.log10(yMin);
            const yLogMax = Math.log10(yMax);
            
            const xPadding = Math.max((xLogMax - xLogMin) * 0.1, 0.5);
            const yPadding = Math.max((yLogMax - yLogMin) * 0.1, 0.5);
            
            bounds = {
                left: Math.pow(10, xLogMin - xPadding),
                right: Math.pow(10, xLogMax + xPadding),
                bottom: Math.pow(10, yLogMin - yPadding),
                top: Math.pow(10, yLogMax + yPadding)
            };
        } else {
            // For linear or mixed scales, add 10% padding
            const xRange = xMax - xMin;
            const yRange = yMax - yMin;
            const xPadding = Math.max(xRange * 0.1, 1);
            const yPadding = Math.max(yRange * 0.1, 1);
            
            bounds = {
                left: xAxisScale.value === 'logarithmic' ? Math.pow(10, Math.log10(xMin) - 0.5) : xMin - xPadding,
                right: xAxisScale.value === 'logarithmic' ? Math.pow(10, Math.log10(xMax) + 0.5) : xMax + xPadding,
                bottom: yAxisScale.value === 'logarithmic' ? Math.pow(10, Math.log10(yMin) - 0.5) : yMin - yPadding,
                top: yAxisScale.value === 'logarithmic' ? Math.pow(10, Math.log10(yMax) + 0.5) : yMax + yPadding
            };
        }
        
        calculator.setMathBounds(bounds);
    }

    function updatePlot() {
        if (!calculator) {
            console.log('Calculator not ready yet');
            return;
        }
        
        if (!xColumn.value || !yColumn.value) {
            console.log('No columns selected');
            return;
        }
        
        if (fileData.value.length === 0) {
            console.log('No data to plot');
            return;
        }
        
        // Clear existing expressions
        calculator.setBlank();
        
        // Re-apply axis scale settings after setBlank (which resets them)
        calculator.updateSettings({
            xAxisScale: xAxisScale.value,
            yAxisScale: yAxisScale.value
        });
        
        // Build table data and collect labels
        const xValues: string[] = [];
        const yValues: string[] = [];
        const labels: string[] = [];
        const xNumeric: number[] = [];
        const yNumeric: number[] = [];
        
        let validPointCount = 0;
        
        fileData.value.forEach((row) => {
            const xVal = row[xColumn.value];
            const yVal = row[yColumn.value];
            
            // Skip rows with invalid/null values for either axis
            if (xVal === null || yVal === null || xVal === undefined || yVal === undefined) {
                return;
            }
            
            // Skip non-numeric values
            if (typeof xVal !== 'number' || typeof yVal !== 'number') {
                return;
            }
            
            // Skip infinity, NaN, and non-positive values (for log scale)
            if (!isFinite(xVal) || !isFinite(yVal) || xVal <= 0 || yVal <= 0) {
                return;
            }
            
            const xLatex = formatScientificToLatex(xVal);
            const yLatex = formatScientificToLatex(yVal);
            
            if (!xLatex || !yLatex) return;
            
            xValues.push(xLatex);
            yValues.push(yLatex);
            xNumeric.push(xVal);
            yNumeric.push(yVal);
            
            // Get label if selected
            const labelVal = labelColumn.value !== '(None)' ? row[labelColumn.value] : '';
            labels.push(labelVal !== null && labelVal !== undefined ? String(labelVal) : '');
            
            validPointCount++;
        });
        
        console.log(`Plotting ${validPointCount} valid points out of ${fileData.value.length} rows`);
        
        // Create hidden table for regression (uses x_1 and y_1 variables)
        const regressionTable = {
            type: 'table',
            id: 'regression_table',
            columns: [
                { 
                    latex: 'x_1', 
                    values: xValues,
                    hidden: true
                },
                { 
                    latex: 'y_1', 
                    values: yValues,
                    hidden: true
                }
            ],
            secret: true  // Don't show in expression list
        };
        
        calculator.setExpression(regressionTable);
        
        // Create visible point expressions for each data point
        const pointExpressions: any[] = [];
        for (let i = 0; i < xValues.length; i++) {
            const label = labelColumn.value !== '(None)' && labels[i] ? labels[i] : '';
            pointExpressions.push({
                id: `point_${i}`,
                latex: `(${xValues[i]}, ${yValues[i]})`,
                color: getPointColor(i),
                pointSize: 9,
                pointStyle: 'POINT',
                label: label,
                showLabel: label !== ''
            });
        }
        
        if (pointExpressions.length > 0) {
            calculator.setExpressions(pointExpressions);
        }
        
        // Add regression
        updateRegression();
        
        // Return numeric values for potential auto-zoom
        return { xNumeric, yNumeric };
    }

    function updateRegression() {
        if (!calculator) return;
        
        // Save current math bounds to prevent view change
        const currentBounds = calculator.graphpaperBounds.mathCoordinates;
        
        // Remove existing regression
        calculator.removeExpression({ id: 'regression' });
        
        const regression = getRegressionExpression(regressionType.value);
        if (regression) {
            calculator.setExpression({
                id: 'regression',
                latex: regression.latex,
                color: '#c74440'
            });
            
            // Observe regression expression to get fitted parameters
            calculator.observe('expressionAnalysis', () => {
                const analysis = calculator.expressionAnalysis;
                if (analysis && analysis['regression']) {
                    // Get the helper expressions for the parameters
                    const params = regression.params;
                    const paramValues: string[] = [];
                    
                    params.forEach((param: string) => {
                        const helper = calculator.HelperExpression({ latex: param });
                        helper.observe('numericValue', () => {
                            if (helper.numericValue !== undefined) {
                                const val = helper.numericValue;
                                // Format the number nicely
                                const formatted = Math.abs(val) < 0.001 || Math.abs(val) > 10000 
                                    ? val.toExponential(4) 
                                    : val.toFixed(4);
                                paramValues.push(`${param} = ${formatted}`);
                                
                                if (paramValues.length === params.length) {
                                    regressionEquation.value = paramValues.join(', ');
                                }
                            }
                        });
                    });
                }
            });
        } else {
            regressionEquation.value = '';
        }
        
        // Restore math bounds to prevent view change
        calculator.setMathBounds({
            left: currentBounds.left,
            right: currentBounds.right,
            bottom: currentBounds.bottom,
            top: currentBounds.top
        });
    }

    // Watch for data column changes - these should trigger auto-zoom
    watch([xColumn, yColumn, labelColumn], () => {
        const result = updatePlot();
        if (result) {
            autoZoom(result.xNumeric, result.yNumeric);
        }
    });

    // Watch for regression changes - only update regression, not the entire plot
    watch(regressionType, () => {
        updateRegression();
    });

    // Watch for file changes to fetch new data
    watch(selectedFile, (newFile) => {
        if (newFile) {
            fetchFileData(newFile);
        }
    });

    // Watch for axis scale changes
    watch([xAxisScale, yAxisScale], () => {
        if (calculator) {
            calculator.updateSettings({
                xAxisScale: xAxisScale.value,
                yAxisScale: yAxisScale.value
            });
            // Re-run auto-zoom with stored values to fit new scale
            if (lastPlottedX.length > 0 && lastPlottedY.length > 0) {
                autoZoom(lastPlottedX, lastPlottedY);
            }
        }
    });

    onMounted(() => {
        // Load Desmos API script
        const script = document.createElement('script');
        script.src = `https://www.desmos.com/api/v1.11/calculator.js?apiKey=${DESMOS_API_KEY}`;

        script.onload = () => {
            // Get the calculator container element
            const elt = document.getElementById('desmos-calculator');
            if (!elt) {
                console.error('Calculator element not found');
                return;
            }

            // Set options for desmos calculator
            const options = {
                expressions: false,
                settingsMenu: false,
                zoomButtons: true,
                zoomFit: true,  // Enable auto-zoom button on tables
                logScales: true,
                xAxisScale: xAxisScale.value,
                yAxisScale: yAxisScale.value
            };

            // Initialize the calculator
            calculator = (window as any).Desmos.GraphingCalculator(elt, options);
        };

        document.head.appendChild(script);
    });
</script>

<template>
    <div class="min-h-screen bg-xrb-background-1 flex">
        <!-- Controls Panel -->
        <div class="w-80 p-6 border-r border-xrb-border-1 flex flex-col gap-6 overflow-y-auto">
            <h3 class="text-lg font-semibold text-white">Data Selection</h3>
            
            <!-- File Selection -->
            <div class="form-control w-full">
                <label class="label">
                    <span class="label-text text-white/70">Data File</span>
                </label>
                <select 
                    class="select select-bordered w-full bg-xrb-background-1 border-xrb-border-1" 
                    v-model="selectedFile" 
                    :disabled="isLoading"
                >
                    <option value="" disabled>Select a data file</option>
                    <option v-for="file in dataFiles" :key="file.value" :value="file.value">
                        {{ file.label }}
                    </option>
                </select>
            </div>
            
            <!-- Column Selection -->
            <div class="form-control w-full">
                <label class="label">
                    <span class="label-text text-white/70">X Axis</span>
                </label>
                <select 
                    class="select select-bordered w-full bg-xrb-background-1 border-xrb-border-1" 
                    v-model="xColumn" 
                    :disabled="isLoading || numericColumns.length === 0"
                >
                    <option v-for="col in numericColumns" :key="col" :value="col">
                        {{ col }}
                    </option>
                </select>
            </div>
            
            <div class="form-control w-full">
                <label class="label">
                    <span class="label-text text-white/70">Y Axis</span>
                </label>
                <select 
                    class="select select-bordered w-full bg-xrb-background-1 border-xrb-border-1" 
                    v-model="yColumn" 
                    :disabled="isLoading || numericColumns.length === 0"
                >
                    <option v-for="col in numericColumns" :key="col" :value="col">
                        {{ col }}
                    </option>
                </select>
            </div>
            
            <div class="form-control w-full">
                <label class="label">
                    <span class="label-text text-white/70">Point Labels</span>
                </label>
                <select 
                    class="select select-bordered w-full bg-xrb-background-1 border-xrb-border-1" 
                    v-model="labelColumn" 
                    :disabled="isLoading || columns.length === 0"
                >
                    <option v-for="col in labelColumns" :key="col" :value="col">
                        {{ col }}
                    </option>
                </select>
            </div>

            <!-- Divider -->
            <div class="divider divider-neutral my-0"></div>

            <!-- Axis Scale Section -->
            <h3 class="text-lg font-semibold text-white">Axis Scales</h3>

            <div class="flex gap-4">
                <div class="form-control flex-1">
                    <label class="label">
                        <span class="label-text text-white/70">X Axis</span>
                    </label>
                    <select 
                        class="select select-bordered select-sm w-full bg-xrb-background-1 border-xrb-border-1" 
                        v-model="xAxisScale"
                    >
                        <option v-for="scale in scaleOptions" :key="scale.value" :value="scale.value">
                            {{ scale.label }}
                        </option>
                    </select>
                </div>
                
                <div class="form-control flex-1">
                    <label class="label">
                        <span class="label-text text-white/70">Y Axis</span>
                    </label>
                    <select 
                        class="select select-bordered select-sm w-full bg-xrb-background-1 border-xrb-border-1" 
                        v-model="yAxisScale"
                    >
                        <option v-for="scale in scaleOptions" :key="scale.value" :value="scale.value">
                            {{ scale.label }}
                        </option>
                    </select>
                </div>
            </div>

            <!-- Divider -->
            <div class="divider divider-neutral my-0"></div>

            <!-- Regression Section -->
            <h3 class="text-lg font-semibold text-white">Regression</h3>
            
            <div class="form-control w-full">
                <label class="label">
                    <span class="label-text text-white/70">Regression Type</span>
                </label>
                <select 
                    class="select select-bordered w-full bg-xrb-background-1 border-xrb-border-1" 
                    v-model="regressionType" 
                    :disabled="isLoading || !selectedFile"
                >
                    <option v-for="type in regressionTypes" :key="type.value" :value="type.value">
                        {{ type.label }}
                    </option>
                </select>
            </div>

            <!-- Regression Equation -->
            <div v-if="regressionType !== 'none' && regressionEquation" class="bg-xrb-accent-2/20 rounded-lg p-4">
                <p class="text-white/50 text-xs mb-1">Fitted Parameters</p>
                <p class="text-white font-mono text-sm">{{ regressionEquation }}</p>
            </div>

            <!-- Divider -->
            <div class="divider divider-neutral my-0"></div>
            
            <!-- Data Info -->
            <div v-if="metadata" class="bg-xrb-accent-3/30 rounded-lg p-4 text-sm">
                <p class="text-white/70"><span class="font-medium text-white">Rows:</span> {{ metadata.row_count }}</p>
                <p class="text-white/70"><span class="font-medium text-white">Columns:</span> {{ metadata.column_count }}</p>
                <p v-if="metadata.warning_count > 0" class="text-xrb-accent-1 mt-2">
                    <span class="font-medium">{{ metadata.warning_count }}</span> data issues detected
                </p>
            </div>
            
            <!-- Loading State -->
            <div v-if="isLoading" class="flex items-center gap-2 text-white/70">
                <span class="loading loading-spinner loading-sm"></span>
                Loading data...
            </div>
            
            <!-- Error State -->
            <div v-if="error" class="alert alert-error text-sm">
                {{ error }}
            </div>
        </div>
        
        <!-- Desmos Calculator -->
        <div class="flex-1 p-4">
            <div id="desmos-calculator" class="w-full h-full rounded-lg overflow-hidden"></div>
        </div>
    </div>
</template>

<style scoped>
</style>
