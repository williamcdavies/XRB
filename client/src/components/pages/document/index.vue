<script setup lang="ts">
    import      { useApi                                              } from '@/composables/api';
    import      { useDocumentViews                                    } from '@/composables/views';
    import type { Table                                               } from '@/types/table';
    import      { parseCSV                                            } from '@/utils/parse';
    import      { computed, nextTick, onBeforeUnmount, onMounted, ref } from 'vue';

    import      ColorLayer                                              from '@/components/layers/ColorLayer.vue';
    import      FileBrowser                                             from './FileBrowser.vue';
    import      Graph                                                   from './Graph.vue';
    import      Handle                                                  from './Handle.vue';
    import      Leftbar                                                 from './Leftbar.vue';
    import      SaveViewModal                                           from './SaveViewModal.vue';
    import      Topbar                                                  from './Topbar.vue';


    const { api }                                                                               = useApi()
    const { views, save: saveView, overwrite: overwriteView, remove: removeView, get: getView } = useDocumentViews()


    // pretty loading stuff
    const isContentReady = ref(false)


    // container adjustment stuff
    const MIN_LEFTBAR_WIDTH = 200
    const MIN_GRAPH_WIDTH   = 200
    const HANDLE_WIDTH      = 10

    const leftbarWidth      = ref(Math.floor(window.innerWidth / 2))
    const handleClass       = ref('bg-transparent')


    function onMouseDown() {
        handleClass.value = 'bg-xrb-bg-3'

        window.addEventListener('mousemove', onMouseMove)
        window.addEventListener('mouseup', onMouseUp)
    }


    function onMouseMove(e: MouseEvent) {
        leftbarWidth.value = Math.min(
            Math.max(MIN_LEFTBAR_WIDTH, e.clientX),
            window.innerWidth - MIN_GRAPH_WIDTH - HANDLE_WIDTH
        )
    }


    function onMouseUp() {
        handleClass.value = 'transparent'

        window.removeEventListener('mousemove', onMouseMove)
        window.removeEventListener('mouseup', onMouseUp)
    }


    function onWindowResize() {
        leftbarWidth.value = Math.min(
            leftbarWidth.value,
            window.innerWidth - MIN_GRAPH_WIDTH - HANDLE_WIDTH
        )
    }


    // data stuff
    const table           = ref<Table | null>(null)
    const hiddenRows      = ref<Set<number>>(new Set())
    const xColumn         = ref<string | null>(null)
    const yColumn         = ref<string | null>(null)
    const loadError       = ref<string | null>(null)
    const showBrowser     = ref(false)
    const currentViewId   = ref<string | null>(null)
    const currentViewName = computed(() => {
        if (!currentViewId.value) return null
        return getView(currentViewId.value)?.name ?? null
    })


    function applyTable(newTable: Table) {
        table.value         = newTable
        hiddenRows.value    = new Set()
        xColumn.value       = newTable.headers[0] ?? null
        yColumn.value       = newTable.headers[1] ?? newTable.headers[0] ?? null
        currentViewId.value = null
    }


    function toggleRowHidden(index: number) {
        const next = new Set(hiddenRows.value)
        if (next.has(index)) next.delete(index)
        else                 next.add(index)
        hiddenRows.value = next
    }


    async function onFileReceived(file: File) {
        loadError.value = null
        const text = await file.text()
        applyTable(parseCSV(text))
    }


    async function loadServerFile(path: string) {
        loadError.value   = null
        showBrowser.value = false
        try {
            const res = await api.fetch(`/api/data/preview/table/?path=${encodeURIComponent(path)}`)
            if (!res.ok) {
                const data      = await res.json().catch(() => ({}))
                loadError.value = data.error || `Error ${res.status}`
                
                return
            }
            const data     = await res.json()
            const fileName = path.split('/').pop() ?? path
            applyTable({
                headers: data.headers ?? [],
                rows:    data.rows    ?? [],
                source:  { name: fileName, type: 'csv' },
            })
        } catch (e) {
            loadError.value = e instanceof Error ? e.message : 'Failed to load file'
        }
    }


    function onXColumn(col: string) { xColumn.value = col }
    function onYColumn(col: string) { yColumn.value = col }


    // view stuff
    const showSaveModal    = ref(false)
    const saveModalDefault = ref('')


    function buildViewData() {
        return {
            name:       '',
            table:      table.value!,
            hiddenRows: [...hiddenRows.value],
            xColumn:    xColumn.value,
            yColumn:    yColumn.value,
            fits:       graph.value?.getFitState() ?? {
                linear: false, exponential: false, logarithmic: false,
                logistic: false, polynomial: false, power: false, sinusoidal: false,
            },
        }
    }


    function onSaveView() {
        if (!table.value || !currentViewId.value) return
        overwriteView(currentViewId.value, buildViewData())
    }


    function onSaveViewAs() {
        if (!table.value) return
        const current = currentViewId.value ? getView(currentViewId.value) : null
        saveModalDefault.value = current?.name ?? table.value.source?.name ?? ''
        showSaveModal.value = true
    }


    function onSaveModalConfirm(name: string) {
        if (!table.value) return
        showSaveModal.value = false
        const data  = buildViewData()
        data.name   = name
        const entry = saveView(data)
        currentViewId.value = entry.id
    }


    function onLoadView(id: string) {
        const view = getView(id)
        if (!view) return
        table.value         = view.table
        hiddenRows.value    = new Set(view.hiddenRows)
        xColumn.value       = view.xColumn
        yColumn.value       = view.yColumn
        currentViewId.value = view.id

        if (view.fits) {
            nextTick(() => graph.value?.restoreFits(view.fits))
        }
    }


    function onDeleteView(id: string) {
        removeView(id)
        if (currentViewId.value === id) currentViewId.value = null
    }


    // header stuff
    function onHeader(idx: number, name: string): void {
        if (!table.value) return

        table.value.headers[idx] = name
    }


    // graph stuff
    const graph = ref<InstanceType<typeof Graph> | null>(null)


    function clearFit():                       void { graph.value?.clearFit()               }
    function toggleExponential():              void { graph.value?.toggleExponential()      }
    function toggleLinear():                   void { graph.value?.toggleLinear()           }
    function toggleLogistic():                 void { graph.value?.toggleLogistic()         }
    function toggleLogarithmic():              void { graph.value?.toggleLogarithmic()      }
    function togglePolynomial(degree: number): void { graph.value?.togglePolynomial(degree) }
    function togglePower():                    void { graph.value?.togglePower()            }
    function toggleSinusoidal():               void { graph.value?.toggleSinusoidal()       }


    // mounting stuff
    onMounted(() => {
        window.addEventListener('resize', onWindowResize)
    })


    onBeforeUnmount(() => {
        window.removeEventListener('resize', onWindowResize)
    })
</script>


<template>
    <div class="grid grid-rows-[auto_1fr] h-screen w-screen bg-xrb-bg-1"
        :style="{ gridTemplateColumns: `${leftbarWidth}px ${HANDLE_WIDTH}px 1fr` }">
        <!-- Z0 -->
        <Topbar :headers="table?.headers ?? []" :x-column="xColumn" :y-column="yColumn" :saved-views="views"
            :has-table="!!table" :current-view-id="currentViewId" :current-view-name="currentViewName"
            @file-selected="onFileReceived" @browse-files="showBrowser = true" @update:x-column="onXColumn"
            @update:y-column="onYColumn" @clear-fit="clearFit" @toggle-exponential="toggleExponential"
            @toggle-linear="toggleLinear" @toggle-logistic="toggleLogistic" @toggle-logarithmic="toggleLogarithmic"
            @toggle-polynomial="togglePolynomial" @toggle-power="togglePower" @toggle-sinusoidal="toggleSinusoidal"
            @save-view="onSaveView" @save-view-as="onSaveViewAs" @load-view="onLoadView" @delete-view="onDeleteView"
            class="col-span-3" />
        <Leftbar :table="table" :hidden-rows="hiddenRows" @toggle-row-hidden="toggleRowHidden" @header="onHeader"
            class="row-start-2" />
        <Handle @mousedown="onMouseDown" class="row-start-2" :class="handleClass" />
        <Graph ref="graph" :table="table" :hidden-rows="hiddenRows" :x-column="xColumn" :y-column="yColumn"
            @ready="isContentReady = true" class="row-start-2" />

            
            <!-- File browser modal -->
            <FileBrowser v-if="showBrowser" @close="showBrowser = false" @select="loadServerFile" />
            
            <!-- Save view modal -->
            <SaveViewModal v-if="showSaveModal" :default-name="saveModalDefault" @close="showSaveModal = false"
            @save="onSaveModalConfirm" />
            
            <!-- Load error toast -->
            <div v-if="loadError"
            class="fixed bottom-4 right-4 z-30 bg-xrb-bg-2 border border-xrb-error text-xrb-error text-sm px-4 py-2 rounded shadow-lg flex items-center gap-3">
            <span>{{ loadError }}</span>
            <button type="button" class="text-xrb-text-secondary hover:text-xrb-text-1"
            @click="loadError = null">&times;</button>

            <!-- Z1 -->
            <transition name="fade">
                <ColorLayer v-if="!isContentReady" />
            </transition>
        </div>
    </div>
</template>


<style scoped>
    .fade-enter-active,
    .fade-leave-active {
        transition: opacity 0.33s;
    }

    .fade-enter-from,
    .fade-leave-to {
        opacity: 0;
    }

    .fade-enter-to,
    .fade-leave-from {
        opacity: 1;
    }
</style>
