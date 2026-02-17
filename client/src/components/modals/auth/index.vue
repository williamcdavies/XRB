<script setup lang="ts">
    import { ref } from 'vue';
    import Panel_1 from './Panel_1.vue';
    import Panel_2 from './Panel_2.vue';
    import Panel_3 from './Panel_3.vue';

    // Ref: https://vuejs.org/guide/components/events.html
    const emit = defineEmits<{
        (e: 'close'): void
    }>()

    
    const email = ref('')
    
    type Panel = 'panel_1' | 'panel_2' | 'panel_3'
    const panels: Panel[] = ['panel_1', 'panel_2', 'panel_3']
    const activePanel = ref<Panel>('panel_1')
    

    // @go-back
    function goBack() {
        const i = panels.indexOf(activePanel.value)
        
        if (i > 0) {
            activePanel.value = panels[i - 1]!
        }
    }  


    // @go-forward
    function goForward() {
        const i = panels.indexOf(activePanel.value)
        
        if (i < panels.length - 1) {
            activePanel.value = panels[i + 1]!
        }
    }
</script>


<template>
    <div @click="emit('close')" class="fixed inset-0 flex items-center justify-center">
        <div @click.stop
            class="flex flex-row h-[36rem] w-[48rem] bg-xrb-bg-1 overflow-hidden rounded-xl">
            <!-- Left Panel -->
            <Transition name="slide" mode="out-in">
                <Panel_1 v-if="activePanel === 'panel_1'" @go-forward="goForward" />
                <Panel_2 v-else-if="activePanel === 'panel_2'" v-model:email="email" @go-forward="goForward"
                    @go-back="goBack" />
                <Panel_3 v-else-if="activePanel === 'panel_3'" :email="email" @go-back="goBack" />
            </Transition>

            <!-- Right Panel-->
            <div class="w-1/2 border-l border-xrb-border">
                <img src="../../../assets/images/steve-johnson-unsplash.jpg" class="h-full w-full object-cover">
            </div>
        </div>
    </div>
</template>


<style scoped>
    .slide-enter-active,
    .slide-leave-active {
        transition: opacity 0.22s ease, transform 0.22s ease;
    }

    .slide-enter-from,
    .slide-leave-to {
        opacity: 0;
        transform: translateX(-5%);
    }

    .slide-enter-to,
    .slide-leave-from {
        opacity: 1;
        transform: translateX(0);
    }
</style>