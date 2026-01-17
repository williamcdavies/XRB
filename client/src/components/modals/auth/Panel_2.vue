<script setup lang="ts">
</script>


<template>
    <div class="flex flex-col w-1/2 p-8 gap-8">
        <!-- Header -->
        <div class="flex flex-col gap-4">
            <div class="flex flex-row items-center">
                <button class="btn btn-ghost hover:bg-transparent hover:border-transparent hover:shadow-none">
                    <img class="h-4 w-4" src="../../../assets/icons/chevrons/chevron_left.svg"/>
                </button>
                <span class="text-2xl font-bold">Continue with email</span>
            </div>
            <span class="text-xs">We'll check if you have an account, and help create one if you don't.</span>
        </div>
        <!-- Body -->
        <div class="flex flex-col gap-4">
            <!-- Fieldset -->
            <fieldset class="fieldset">
                <legend class="fieldset-legend text-xs">Email</legend>
                <input type="text" class="input" placeholder="Type here" />
            </fieldset>
            <!-- Continue -->
            <button class="btn btn-outline bg-[#dc8c64] border-white/25 text-[#181818] hover:bg-white hover:border-white hover:text-[#181818]">
                <span class="text-xs tracking-wider">CONTINUE</span>
            </button>
        </div>
    </div>
</template>


<style scoped>
</style>