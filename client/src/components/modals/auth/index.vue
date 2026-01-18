<script setup lang="ts">
    import { ref } from 'vue';
    import Panel_1 from './Panel_1.vue';
    import Panel_2 from './Panel_2.vue';

    // Ref: https://vuejs.org/guide/components/events.html
    const emit = defineEmits<{
        (e: 'close'): void
    }>()

    type Panel = 'panel_1' | 'panel_2'
    const activePanel = ref<Panel>('panel_1')
</script>


<template>
    <div @click="emit('close')" class="fixed inset-0 flex items-center justify-center">
        <div @click.stop class="flex flex-row min-h-[36rem] max-h-[36rem] min-w-[48rem] max-w-[48rem] bg-[#181818] overflow-hidden rounded-xl">
            <!-- Left Panel -->
            <Transition name="slide" mode="out-in">
                <Panel_1 v-if="activePanel === 'panel_1'" key="panel_1" @continue-with-email="activePanel = 'panel_2'" />
                <Panel_2 v-else-if="activePanel === 'panel_2'" key="panel_2" @go-back="activePanel = 'panel_1'" />
            </Transition>

            <!-- Right Panel-->
            <div class="w-1/2">
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