<script setup lang="ts">
import { ref } from 'vue'
import { useAuth }          from '@/composables/auth'
import TintLayer            from '@/components/layers/TintLayer.vue'
import Hero                 from './Hero.vue'
import Drawer               from './Drawer.vue'
import HomeComponent        from './content/Home.vue'
import GroupsComponent      from './content/Groups.vue'
import LearnComponent       from './content/Learn.vue'
import AccountComponent     from './content/account/Account.vue'
import FilesComponent       from '../files/index.vue'

const { accessToken } = useAuth()
const activeView = ref('home')
const tinted     = ref(false)                             

const changeView = (view: string) => { activeView.value = view }
</script>

<template>
  <div class="relative h-screen flex flex-col">
    <!-- Z0 -->
    <Hero class="absolute inset-0 z-0" />
    <!-- Z1 -->
    <div class="flex flex-row flex-1 min-h-0 relative z-1">
      <Drawer class="shrink-0 w-fit" @change-view="changeView" />
      <HomeComponent    v-if="activeView === 'home'" />
      <GroupsComponent  v-else-if="activeView === 'groups'   && accessToken" />
      <AccountComponent v-else-if="activeView === 'account'  && accessToken"
        @tint="tinted = $event"
      />
      <FilesComponent   v-else-if="activeView === 'files'" />
      <LearnComponent   v-else-if="activeView === 'learn'" />
      <!-- <LearnComponent   v-else-if="activeView === 'learn' && accessToken" />  -->
    </div>
    <Transition name="fade">
      <TintLayer v-if="tinted" class="absolute inset-0 z-2" />
    </Transition>
  </div>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.33s; }
.fade-enter-from,  .fade-leave-to      { opacity: 0; }
.fade-enter-to,    .fade-leave-from    { opacity: 1; }
</style>