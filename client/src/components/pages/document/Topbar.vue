<script setup lang="ts">
    import { ref } from 'vue';

    // Ref: https://vuejs.org/guide/components/events.html
    const emit = defineEmits<{
        (e: 'clear-fit'):                        void
        (e: 'file-selected',    file:   File):   void
        (e: 'fit-exponential'):                  void
        (e: 'fit-linear'):                       void
        (e: 'fit-logistic'):                     void
        (e: 'fit-logarithmic'):                  void
        (e: 'fit-polynomial',   degree: number): void
        (e: 'fit-power'):                        void
        (e: 'fit-sinusoidal'):                   void
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
    }


    function targetFileInput() {
        fileInput.value?.click()
    }


    // graph stuff
    function clearFit():                    void { emit('clear-fit')                   }
    function fitExponential():              void { emit('fit-exponential')             }
    function fitLinear():                   void { emit('fit-linear')                  }
    function fitLogistic():                 void { emit('fit-logistic')                }
    function fitLogarithmic():              void { emit('fit-logarithmic')             }
    function fitPolynomial(degree: number): void { emit('fit-polynomial', degree)      }
    function fitPower():                    void { emit('fit-power')                   }
    function fitSinusoidal():               void { emit('fit-sinusoidal')              }


    // menu stuff
    const isDropdownOpen  = ref(false)
    const isFitMenuOpen   = ref(false)
    const isPolyMenuOpen  = ref(false)

    function toggleDropdown(): void {
        isDropdownOpen.value = !isDropdownOpen.value
        
        if(!isDropdownOpen.value) {
            isPolyMenuOpen.value = false
            isFitMenuOpen.value  = false
        }
    }

    function closeAll(): void {
        isDropdownOpen.value = false
        isPolyMenuOpen.value = false
        isFitMenuOpen.value  = false
    }
</script>


<template>
    <div class="flex flex-row items-center h-10 w-full border-b border-xrb-border px-3 gap-2">
        <input ref="fileInput" type="file" accept=".csv" class="hidden" @change="handleFileInput" />
        <div class="dropdown">
            <button tabindex="0"
                class="btn btn-ghost btn-xs text-xrb-text-1 font-mono tracking-widest uppercase">Menu</button>
            <ul tabindex="0"
                class="dropdown-content menu bg-xrb-bg-2 border border-xrb-border rounded-box z-50 w-44 p-1 shadow-lg text-xrb-text-1 font-mono text-xs">
                <li><a @click="targetFileInput(); closeAll()">Import CSV</a></li>
                <li class="divider my-0.5" />
                <li>
                    <details>
                        <summary>Fit</summary>
                        <ul>
                            <li><a @click="fitLinear(); closeAll()">Linear</a></li>
                            <li><a @click="fitExponential(); closeAll()">Exponential</a></li>
                            <li><a @click="fitLogarithmic(); closeAll()">Logarithmic</a></li>
                            <li><a @click="fitPower(); closeAll()">Power</a></li>
                            <li><a @click="fitSinusoidal(); closeAll()">Sinusoidal</a></li>
                            <li><a @click="fitLogistic(); closeAll()">Logistic</a></li>
                            <li>
                                <details>
                                    <summary>Polynomial</summary>
                                    <ul>
                                        <li><a @click="fitPolynomial(2); closeAll()">Degree 2</a></li>
                                        <li><a @click="fitPolynomial(3); closeAll()">Degree 3</a></li>
                                        <li><a @click="fitPolynomial(4); closeAll()">Degree 4</a></li>
                                        <li><a @click="fitPolynomial(5); closeAll()">Degree 5</a></li>
                                    </ul>
                                </details>
                            </li>
                        </ul>
                    </details>
                </li>
                <li class="divider my-0.5" />
                <li><a class="text-xrb-error" @click="clearFit(); closeAll()">Clear Fit</a></li>
            </ul>
        </div>
    </div>
</template>


<style scoped>
</style>