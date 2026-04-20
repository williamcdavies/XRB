<script setup lang="ts">
import type { DocumentView} from '@/types/view';
import { useRouter } from 'vue-router';
import { ref } from 'vue';

const router = useRouter();

    // Ref: https://vuejs.org/guide/components/events.html
    const prop = defineProps<{
        headers:         string[]
        xColumn:         string | null
        yColumn:         string | null
        aColumn:         string | null
        savedViews:      DocumentView[]
        hasTable:        boolean
        currentViewId:   string | null
        currentViewName: string | null
    }>()
    const emit = defineEmits<{
        (e: 'clear-fit'):                         void
        (e: 'file-selected',     file:   File):   void
        (e: 'browse-files'):                      void
        (e: 'update:x-column',   column: string): void
        (e: 'update:y-column',   column: string): void
        (e: 'update:a-column',   column: string): void
        (e: 'toggle-exponential'):                void
        (e: 'toggle-linear'):                     void
        (e: 'toggle-logistic'):                   void
        (e: 'toggle-logarithmic'):                void
        (e: 'toggle-polynomial', degree: number): void
        (e: 'toggle-power'):                      void
        (e: 'toggle-sinusoidal'):                 void
        (e: 'save-view'):                         void
        (e: 'save-view-as'):                      void
        (e: 'load-view',         id:   string):   void
        (e: 'delete-view',       id:   string):   void
    }>()


// file stuff
const fileInput = ref<HTMLInputElement | null>(null)


function handleFileInput(event: Event) {
    const input = event.target as HTMLInputElement
    const file = input.files?.[0]

    if (!file) {
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


    function onAChange(e: Event) {
        emit('update:a-column', (e.target as HTMLSelectElement).value)
    }


// graph stuff
function clearFit(): void { emit('clear-fit') }
function toggleExponential(): void { emit('toggle-exponential') }
function toggleLinear(): void { emit('toggle-linear') }
function toggleLogistic(): void { emit('toggle-logistic') }
function toggleLogarithmic(): void { emit('toggle-logarithmic') }
function togglePolynomial(degree: number): void { emit('toggle-polynomial', degree) }
function togglePower(): void { emit('toggle-power') }
function toggleSinusoidal(): void { emit('toggle-sinusoidal') }
</script>


<template>
    <div class="flex flex-row items-center h-10 w-full bg-xrb-bg-2 border-b border-xrb-border px-3 gap-3">
        <input ref="fileInput" type="file" accept=".csv" class="hidden" @change="handleFileInput" />

        <button @click="router.push('/dashboard');"
            text-xrb-text-secondary hover:text-xrb-text-primary
            class="rounded-none tooltip tooltip-bottom tooltip-neutral group" data-tip="Home">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1"
                stroke="currentColor" class="size-6">
                <path stroke-linecap="round" stroke-linejoin="round"
                    d="m2.25 12 8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
            </svg>
        </button>

        <button class="btn btn-ghost btn-xs text-xrb-text-1 font-mono tracking-widest uppercase"
            @click="emit('browse-files')">Browse Files</button>
        <button class="btn btn-ghost btn-xs text-xrb-text-1 font-mono tracking-widest uppercase"
            @click="targetFileInput()">Import CSV</button>

        <div class="w-px h-5 bg-xrb-border" />

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

        <div v-if="prop.headers.length > 0" class="flex items-center gap-2">
            <label class="text-xs font-mono uppercase tracking-widest text-xrb-text-secondary">X</label>
            <select class="select select-xs bg-xrb-bg-3 border border-xrb-border text-xrb-text-1 font-mono text-xs"
                :value="prop.xColumn ?? ''" @change="onXChange">
                <option v-for="h in prop.headers" :key="h" :value="h">{{ h }}</option>
            </select>
            <label class="text-xs font-mono uppercase tracking-widest text-xrb-text-secondary">Y</label>
            <select class="select select-xs bg-xrb-bg-3 border border-xrb-border text-xrb-text-1 font-mono text-xs"
                :value="prop.yColumn ?? ''" @change="onYChange">
                <option v-for="h in prop.headers" :key="h" :value="h">{{ h }}</option>
            </select>
            <label class="text-xs font-mono uppercase tracking-widest text-xrb-text-secondary">A</label>
            <select class="select select-xs bg-xrb-bg-3 border border-xrb-border text-xrb-text-1 font-mono text-xs"
                :value="prop.aColumn ?? ''" @change="onAChange">
                <option value="">none</option>
                <option v-for="h in prop.headers" :key="h" :value="h">{{ h }}</option>
            </select>
        </div>

        <div class="flex-1" />

        <span v-if="prop.currentViewName" class="text-xs font-mono text-xrb-text-secondary truncate max-w-48">
            {{ prop.currentViewName }}
        </span>

        <template v-if="prop.hasTable && prop.currentViewId">
            <button class="btn btn-ghost btn-xs text-xrb-text-1 font-mono tracking-widest uppercase"
                @click="emit('save-view')">Save</button>
            <button class="btn btn-ghost btn-xs text-xrb-text-1 font-mono tracking-widest uppercase"
                @click="emit('save-view-as')">Save As</button>
        </template>
        <button v-else-if="prop.hasTable"
            class="btn btn-ghost btn-xs text-xrb-text-1 font-mono tracking-widest uppercase"
            @click="emit('save-view-as')">Save As New</button>

        <div v-if="prop.savedViews.length > 0" class="dropdown dropdown-end">
            <button tabindex="0" class="btn btn-ghost btn-xs text-xrb-text-1 font-mono tracking-widest uppercase">
                Saved Views
                <span class="badge badge-xs badge-neutral ml-1">{{ prop.savedViews.length }}</span>
            </button>
            <ul tabindex="0"
                class="dropdown-content menu bg-xrb-bg-2 border border-xrb-border rounded-box z-50 w-64 p-1 shadow-lg text-xrb-text-1 font-mono text-xs">
                <li v-for="view in prop.savedViews" :key="view.id">
                    <a class="flex justify-between items-center" @click="emit('load-view', view.id)">
                        <span class="truncate">{{ view.name }}</span>
                        <button class="btn btn-ghost btn-xs text-xrb-error px-1"
                            @click.stop="emit('delete-view', view.id)">
                            &times;
                        </button>
                    </a>
                </li>
            </ul>
        </div>
    </div>
</template>


<style scoped></style>
