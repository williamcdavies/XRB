<script setup lang="ts">
    import { ref, computed }                        from 'vue'
    import { accountModals, type AccountModalType } from '../../../../modals/dashboard/account-modals'

    import TintLayer                                from '../../../../layers/TintLayer.vue'
    import AccountMenu                              from './AccountMenu.vue'
    
    const activeModal = ref<AccountModalType | null>(null)

    const ActiveModalComponent = computed(() =>
        activeModal.value ? accountModals[activeModal.value] : null
    )

    function closeModal() {
        activeModal.value = null
    }
</script>

<template>
    
    <AccountMenu @open-modal="activeModal = $event" />

    <Transition name="fade">
        <TintLayer v-if="activeModal" />
    </Transition>

    <Transition name="pop">
        <component v-if="ActiveModalComponent" :is="ActiveModalComponent" @close="closeModal" />
    </Transition>
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

    .pop-enter-active,
    .pop-leave-active {
        transition: opacity 0.33s ease, transform 0.33s ease;
    }

    .pop-enter-from,
    .pop-leave-to {
        opacity: 0;
        transform: scale(0.75);
    }

    .pop-enter-to,
    .pop-leave-from {
        opacity: 1;
        transform: scale(1);
    }
</style>