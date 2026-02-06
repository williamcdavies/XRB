<script setup lang="ts">
</script>


<template>
    <div class="flex flex-col justify-center items-center space-y-6 rounded-none">
        <div class="flex text-2xl font-bold w-3/4 min-w-[36rem] max-w-[48rem]">Personal Information</div>
        <!-- <div class="flex text-l w-3/4 min-w-[36rem] max-w-[48rem]">Manage details that work best for you</div> Add maybe when I think of something better -->
        <ul
            class="list w-3/4 min-w-[36rem] max-w-[48rem] h-3/4 min-h-[36rem] max-h-[48rem] rounded-none hover:cursor-pointer">
            <li class="flex list-row h-full rounded-t-3xl rounded-b-none hover:bg-xrb-accent-4 hover:text-xrb-accent-1">
                <div class="flex justify-center items-center w-1/6">
                    <img class="w-20 h-20  rounded-full"
                        src="../../../../assets/images/profile-icons/profile-icon-3.jpg" alt="Rounded avatar">
                </div>
                <div class="flex flex-col w-5/6 justify-center h-full select-none">
                    <div class="font-bold text-lg">Ethan Claire</div>
                    <div class="py-0 text-md">Student</div>
                </div>
            </li>

            <li
                class="flex list-row h-full rounded-t-none rounded-b-none hover:bg-xrb-accent-4 hover:text-xrb-accent-1">
                <div class="flex justify-center items-center w-1/6">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z" />
                    </svg>
                </div>
                <div class="flex flex-col w-5/6 justify-center h-full select-none">
                    <div class="font-bold text-lg">Name</div>
                    <div class="py-0 text-md">Ethan Claire</div>
                </div>
            </li>

            <li
                class="flex list-row h-full rounded-t-none rounded-b-none hover:bg-xrb-accent-4 hover:text-xrb-accent-1">
                <div class="flex justify-center items-center w-1/6">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M4.26 10.147a60.438 60.438 0 0 0-.491 6.347A48.62 48.62 0 0 1 12 20.904a48.62 48.62 0 0 1 8.232-4.41 60.46 60.46 0 0 0-.491-6.347m-15.482 0a50.636 50.636 0 0 0-2.658-.813A59.906 59.906 0 0 1 12 3.493a59.903 59.903 0 0 1 10.399 5.84c-.896.248-1.783.52-2.658.814m-15.482 0A50.717 50.717 0 0 1 12 13.489a50.702 50.702 0 0 1 7.74-3.342M6.75 15a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Zm0 0v-3.675A55.378 55.378 0 0 1 12 8.443m-7.007 11.55A5.981 5.981 0 0 0 6.75 15.75v-1.5" />
                    </svg>
                </div>
                <div class="flex flex-col w-5/6 justify-center h-full select-none">
                    <div class="font-bold text-lg">Account Type</div>
                    <div class="py-0 text-md">Student</div>
                </div>
            </li>

            <li
                class="flex list-row h-full rounded-t-none rounded-b-none hover:bg-xrb-accent-4 hover:text-xrb-accent-1">
                <div class="flex justify-center items-center w-1/6">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="m10.5 21 5.25-11.25L21 21m-9-3h7.5M3 5.621a48.474 48.474 0 0 1 6-.371m0 0c1.12 0 2.233.038 3.334.114M9 5.25V3m3.334 2.364C11.176 10.658 7.69 15.08 3 17.502m9.334-12.138c.896.061 1.785.147 2.666.257m-4.589 8.495a18.023 18.023 0 0 1-3.827-5.802" />
                    </svg>
                </div>
                <div class="flex flex-col w-5/6 justify-center h-full select-none">
                    <div class="font-bold text-lg">Language</div>
                    <div class="py-0 text-md">English</div>
                </div>
            </li>

            <li
                class="flex list-row h-full rounded-t-none rounded-b-none hover:bg-xrb-accent-4 hover:text-xrb-accent-1">
                <div class="flex justify-center items-center w-1/6">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M21.75 6.75v10.5a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0 0 19.5 4.5h-15a2.25 2.25 0 0 0-2.25 2.25m19.5 0v.243a2.25 2.25 0 0 1-1.07 1.916l-7.5 4.615a2.25 2.25 0 0 1-2.36 0L3.32 8.91a2.25 2.25 0 0 1-1.07-1.916V6.75" />
                    </svg>
                </div>
                <div class="flex flex-col w-5/6 justify-center h-full select-none">
                    <div class="font-bold text-lg">Email</div>
                    <div class="py-0 text-md">eclaire@unr.edu</div>
                </div>
            </li>

            <li
                class="flex list-row h-full rounded-t-none rounded-b-3xl hover:bg-xrb-accent-4 hover:text-xrb-warning-1">
                <div class="flex justify-center items-center w-1/6">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
                    </svg>
                </div>
                <div class="flex flex-col w-5/6 justify-center h-full select-none">
                    <div class="font-bold text-lg">Delete Account</div>
                </div>
            </li>

        </ul>
    </div>
</template>


<style scoped></style>