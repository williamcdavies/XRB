<script setup lang="ts">

</script>


<template>
    <div class="fixed inset-0 flex items-center justify-center z-50" @click="$emit('close')">
        <div class="bg-[#181818] rounded-xl min-w-[48rem] max-w-[48rem] min-h-[36rem] max-h-[36rem] p-6 z-50"
            @click.stop>
            Edit Picture
        </div>
    </div>
</template>



<style scoped></style>