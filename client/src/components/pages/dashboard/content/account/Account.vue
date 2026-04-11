<script setup lang="ts">
import { ref, computed } from 'vue'
import { accountModals, type AccountModalType } from '../../../../modals/dashboard/account-modals'
import AccountMenu   from './AccountMenu.vue'
import AdvancedMenu  from './AdvancedMenu.vue'
import { useUser }   from '@/composables/account'

const emit = defineEmits<{ tint: [value: boolean] }>()
const { fetchUser } = useUser()
const activeView  = ref<'main' | 'advanced'>('main')
const activeModal = ref<AccountModalType | null>(null)
const ActiveModalComponent = computed(() =>
  activeModal.value ? accountModals[activeModal.value] : null
)

function openModal(modal: AccountModalType) {
  activeModal.value = modal
  emit('tint', true)
}
function closeModal() {
  activeModal.value = null
  emit('tint', false)
}
</script>

<template>
  <AdvancedMenu v-if="activeView === 'advanced'"
    @open-modal="openModal"
    @change-view="activeView = $event"
  />
  <AccountMenu v-else
    @open-modal="openModal"
    @change-view="activeView = $event"
  />
  <!-- TintLayer removed from here -->
  <Teleport to="body">
  <Transition name="pop">
    <component
      v-if="ActiveModalComponent"
      :is="ActiveModalComponent"
      @close="closeModal"
      @saved="fetchUser(true)"
    />
  </Transition>
</Teleport>
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