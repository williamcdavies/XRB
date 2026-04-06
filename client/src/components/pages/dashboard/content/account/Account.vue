<script setup lang="ts">
import { ref, computed }                        from 'vue'
import { accountModals, type AccountModalType } from '../../../../modals/dashboard/account-modals'
import TintLayer                                from '../../../../layers/TintLayer.vue'
import AccountMenu                              from './AccountMenu.vue'
import { useUser }                              from '@/composables/account'
import AdvancedMenu from './AdvancedMenu.vue'

const { fetchUser } = useUser()

const activeView = ref<'main' | 'advanced'>('main')

const activeModal = ref<AccountModalType | null>(null)
const ActiveModalComponent = computed(() =>
    activeModal.value ? accountModals[activeModal.value] : null
)

function closeModal() {
    activeModal.value = null
}
</script>

<template>
    <AdvancedMenu
        v-if="activeView === 'advanced'"
        @open-modal="activeModal = $event"
        @change-view="activeView = $event"
    />
    <AccountMenu
        v-else
        @open-modal="activeModal = $event"
        @change-view="activeView = $event"
    />
    <Transition name="fade">
        <TintLayer v-if="activeModal" />
    </Transition>
    <Transition name="pop">
        <component
            v-if="ActiveModalComponent"
            :is="ActiveModalComponent"
            @close="closeModal"
            @saved="fetchUser(true)"
        />
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