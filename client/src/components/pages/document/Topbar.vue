<script setup lang="ts">
    import { ref } from 'vue';

    // Ref: https://vuejs.org/guide/components/events.html
    const prop = defineProps<{
        headers:  string[]
        xColumn:  string | null
        yColumn:  string | null
    }>()
    const emit = defineEmits<{
        (e: 'clear-fit'):                              void
        (e: 'file-selected',     file:   File):        void
        (e: 'browse-files'):                           void
        (e: 'update:x-column',   column: string):      void
        (e: 'update:y-column',   column: string):      void
        (e: 'toggle-exponential'):                     void
        (e: 'toggle-linear'):                          void
        (e: 'toggle-logistic'):                        void
        (e: 'toggle-logarithmic'):                     void
        (e: 'toggle-polynomial', degree: number):      void
        (e: 'toggle-power'):                           void
        (e: 'toggle-sinusoidal'):                      void
    }>()


    // file input stuff
    const fileInput = ref<HTMLInputElement | null>(null)


    function handleFileInput(event: Event) {
        const input = event.target as HTMLInputElement
        const file  = input.files?.[0]

        if(!file) {
            return
        }

        emit('file-selected', file)
        input.value = ''
    }


    function targetFileInput() {
        fileInput.value?.click()
    }


    // axis column stuff
    function onXChange(e: Event) {
        emit('update:x-column', (e.target as HTMLSelectElement).value)
    }


    function onYChange(e: Event) {
        emit('update:y-column', (e.target as HTMLSelectElement).value)
    }


    // graph stuff
    function clearFit():                       void { emit('clear-fit')                 }
    function toggleExponential():              void { emit('toggle-exponential')        }
    function toggleLinear():                   void { emit('toggle-linear')             }
    function toggleLogistic():                 void { emit('toggle-logistic')           }
    function toggleLogarithmic():              void { emit('toggle-logarithmic')        }
    function togglePolynomial(degree: number): void { emit('toggle-polynomial', degree) }
    function togglePower():                    void { emit('toggle-power')              }
    function toggleSinusoidal():               void { emit('toggle-sinusoidal')         }
</script>


<template>
    <div class="flex flex-row items-center h-10 w-full bg-xrb-bg-2 border-b border-xrb-border px-3 gap-3">
        <input ref="fileInput" type="file" accept=".csv" class="hidden" @change="handleFileInput" />

        <!-- File actions -->
        <button class="btn btn-ghost btn-xs text-xrb-text-1 font-mono tracking-widest uppercase"
            @click="targetFileInput()">Import CSV</button>
        <button class="btn btn-ghost btn-xs text-xrb-text-1 font-mono tracking-widest uppercase"
            @click="emit('browse-files')">Browse Files</button>

        <div class="w-px h-5 bg-xrb-border" />

        <!-- Fit toggles dropdown -->
        <div class="dropdown">
            <button tabindex="0"
                class="btn btn-ghost btn-xs text-xrb-text-1 font-mono tracking-widest uppercase">Fit</button>
            <ul tabindex="0"
                class="dropdown-content menu bg-xrb-bg-2 border border-xrb-border rounded-box z-50 w-44 p-1 shadow-lg text-xrb-text-1 font-mono text-xs">
                <li><a @click="toggleLinear()">Linear</a></li>
                <li><a @click="toggleExponential()">Exponential</a></li>
                <li><a @click="toggleLogarithmic()">Logarithmic</a></li>
                <li><a @click="togglePower()">Power</a></li>
                <li><a @click="toggleSinusoidal()">Sinusoidal</a></li>
                <li><a @click="toggleLogistic()">Logistic</a></li>
                <li>
                    <details>
                        <summary>Polynomial</summary>
                        <ul>
                            <li><a @click="togglePolynomial(2)">Degree 2</a></li>
                            <li><a @click="togglePolynomial(3)">Degree 3</a></li>
                            <li><a @click="togglePolynomial(4)">Degree 4</a></li>
                            <li><a @click="togglePolynomial(5)">Degree 5</a></li>
                        </ul>
                    </details>
                </li>
            </ul>
        </div>

        <button class="btn btn-ghost btn-xs text-xrb-error font-mono tracking-widest uppercase"
            @click="clearFit()">Clear Fit</button>

        <div class="w-px h-5 bg-xrb-border" />

        <!-- Axis column selectors -->
        <div v-if="prop.headers.length > 0" class="flex items-center gap-2">
            <label class="text-xs font-mono uppercase tracking-widest text-xrb-text-secondary">X</label>
            <select
                class="select select-xs bg-xrb-bg-3 border border-xrb-border text-xrb-text-1 font-mono text-xs"
                :value="prop.xColumn ?? ''" @change="onXChange">
                <option v-for="h in prop.headers" :key="h" :value="h">{{ h }}</option>
            </select>
            <label class="text-xs font-mono uppercase tracking-widest text-xrb-text-secondary">Y</label>
            <select
                class="select select-xs bg-xrb-bg-3 border border-xrb-border text-xrb-text-1 font-mono text-xs"
                :value="prop.yColumn ?? ''" @change="onYChange">
                <option v-for="h in prop.headers" :key="h" :value="h">{{ h }}</option>
            </select>
        </div>
    </div>
</template>


<style scoped>
</style>
