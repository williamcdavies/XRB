<script setup lang="ts">
    import {ref} from 'vue';
    
    import Hero             from './Hero.vue';
    import Drawer           from './Drawer.vue';
    import HomeComponent    from './content/Home.vue'
    import GroupsComponent  from './content/Groups.vue'
    import AccountComponent from './content/account/Account.vue'

    const activeView = ref('home'); 

    const changeView = (view: string) => {
        activeView.value = view;
    };
</script>


<template>
    <div class="relative min-h-screen ">
        <!-- Z0 -->
        <Hero class="absolute inset-0 z-0" />

        <!-- Z1 -->
        <div class="flex flex-row relative z-1">
            <Drawer class="shrink-0 w-fit" @change-view="changeView" />
            
            <HomeComponent    v-if="activeView      === 'home'"    />
            <GroupsComponent  v-else-if="activeView === 'groups'"  />
            <AccountComponent v-else-if="activeView === 'account'" />
        </div>
    </div>
</template>


<style scoped>
</style>