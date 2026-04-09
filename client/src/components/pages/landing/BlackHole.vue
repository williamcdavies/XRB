<script setup lang="ts">
const props = defineProps<{
    state: 'idle' | 'zoomed'
}>()

const emit = defineEmits(['done'])

// 1. Efficiency: 200 stars is plenty when bounds match the viewport exactly
const COUNT = 800

const stars = Array.from({ length: COUNT }, () => ({
    // 2. Bounds: -100 to 100 relative to the center (covers 2x screen size)
    // This handles the 90deg rotation and 40x zoom without gaps
    x: Math.random() * 250 - 125,
    y: Math.random() * 250 - 125,
    r: Math.random() * 2.5 + 0.5,
    opacity: Math.random() * 0.3 + 0.3,
    duration: Math.random() * 3 + 2,
    delay: Math.random() * 1
}))

function onTransitionEnd(e: TransitionEvent) {
    if (e.propertyName !== 'transform') return
    if (props.state === 'zoomed') {
        emit('done')
    }
}
</script>

<template>
    <div class="absolute bh-responsive bh-transition"
        style="will-change: transform;" :class="{
            'bh-idle': props.state === 'idle',
            'bh-zoomed': props.state === 'zoomed'
        }" @transitionend="onTransitionEnd">
        <div class="star-field-container">
            <div v-for="(star, i) in stars" :key="i" class="star" :style="{
                left: `${star.x}vw`,
                top: `${star.y}vh`,
                width: `${star.r}px`,
                height: `${star.r}px`,
                opacity: star.opacity,
                '--star-delay': `${star.delay}s`,
                '--star-duration': `${star.duration}s`
            }" />
        </div>

        <div class="rotate-45">
            <!-- blur layer -->
            <div class="absolute top-[calc(50%+1px)] left-1/2 -translate-x-1/2 -translate-y-full w-330 h-22.5 border-t-2 border-l-70 border-r-84 border-bh-red-3 bg-transparent blur-sm"
                style="border-radius: 50% 50% 0 0 / 100% 100% 0 0;">
            </div>

            <!-- top half of outer ring-->
            <div class="absolute top-[calc(50%+1px)] left-1/2 -translate-x-1/2 -translate-y-full w-320 h-22 border-t-2 border-l-86 border-r-86 border-bh-red-3 bg-t
ransparent"
                style="border-radius: 50% 50% 0 0 / 100% 100% 0 0;">
            </div>
            <div class="absolute top-[calc(50%+1px)] left-1/2 -translate-x-1/2 -translate-y-full w-278 h-21.75 border-t-2 border-l-30 border-r-30 border-bh-red-3 b
g-transparent"
                style="border-radius: 50% 50% 0 0 / 100% 100% 0 0;">
            </div>
            <div class="absolute top-[calc(50%+1px)] left-1/2 -translate-x-1/2 -translate-y-full w-264 h-21.5 border-t-2 border-l-30 border-r-30 border-bh-red-2 bg
-transparent"
                style="border-radius: 50% 50% 0 0 / 100% 100% 0 0;">
            </div>
            <div class="absolute top-[calc(50%+1px)] left-1/2 -translate-x-1/2 -translate-y-full w-250 h-21.25 border-t-2 border-l-22 border-r-22 border-bh-red-1 b
g-transparent"
                style="border-radius: 50% 50% 0 0 / 100% 100% 0 0;">
            </div>
            <div class="absolute top-[calc(50%+1px)] left-1/2 -translate-x-1/2 -translate-y-full w-240 h-21 border-t-2 border-l-20 border-r-20 border-bh-orange-3 b
g-transparent"
                style="border-radius: 50% 50% 0 0 / 100% 100% 0 0;">
            </div>
            <div class="absolute top-[calc(50%+1px)] left-1/2 -translate-x-1/2 -translate-y-full w-232 h-20.5 border-t-2 border-l-20 border-r-20 border-bh-orange-2
 bg-transparent  "
                style="border-radius: 50% 50% 0 0 / 100% 100% 0 0;">
            </div>
            <div class="absolute top-[calc(50%+1px)] left-1/2 -translate-x-1/2 -translate-y-full w-224 h-20 border-t-2 border-l-20 border-r-20 border-bh-yellow-2 b
g-transparent  "
                style="border-radius: 50% 50% 0 0 / 100% 100% 0 0;">
            </div>
            <div class="absolute top-[calc(50%+1px)] left-1/2 -translate-x-1/2 -translate-y-full w-216 h-19.5 border-t-2 border-l-20 border-r-20 border-bh-orange-1
 bg-transparent  "
                style="border-radius: 50% 50% 0 0 / 100% 100% 0 0;">
            </div>
            <div class="absolute top-[calc(50%+1px)] left-1/2 -translate-x-1/2 -translate-y-full w-207 h-19 border-t-2 border-l-16 border-r-16 border-bh-orange-2 b
g-transparent  "
                style="border-radius: 50% 50% 0 0 / 100% 100% 0 0;">
            </div>
            <div class="absolute top-[calc(50%+1px)] left-1/2 -translate-x-1/2 -translate-y-full w-200 h-18.5 border-t-2 border-l-12 border-r-12 border-bh-orange-3
 bg-transparent  "
                style="border-radius: 50% 50% 0 0 / 100% 100% 0 0;">
            </div>
            <div class="absolute top-[calc(50%+1px)] left-1/2 -translate-x-1/2 -translate-y-full w-195 h-18 border-t-2 border-l-8 border-r-8 border-bh-orange-2 bg-
transparent  "
                style="border-radius: 50% 50% 0 0 / 100% 100% 0 0;">
            </div>
            <div class="absolute top-[calc(50%+1px)] left-1/2 -translate-x-1/2 -translate-y-full w-192 h-17.5 border-t-2 border-l-8 border-r-8 border-bh-orange-1 b
g-transparent  "
                style="border-radius: 50% 50% 0 0 / 100% 100% 0 0;">
            </div>
            <div class="absolute top-[calc(50%+1px)] left-1/2 -translate-x-1/2 -translate-y-full w-189 h-17 border-t-2 border-l-8 border-r-8 border-bh-orange-2 bg-
transparent  "
                style="border-radius: 50% 50% 0 0 / 100% 100% 0 0;">
            </div>
            <div class="absolute top-[calc(50%+1px)] left-1/2 -translate-x-1/2 -translate-y-full w-186 h-16.5 border-t-2 border-l-8 border-r-8 border-bh-orange-3 b
g-transparent  "
                style="border-radius: 50% 50% 0 0 / 100% 100% 0 0;">
            </div>
            <div class="absolute top-[calc(50%+1px)] left-1/2 -translate-x-1/2 -translate-y-full w-183 h-16 border-t-2 border-l-8 border-r-8 border-bh-red-1 bg-tra
nsparent  "
                style="border-radius: 50% 50% 0 0 / 100% 100% 0 0;">
            </div>
            <div class="absolute top-[calc(50%+1px)] left-1/2 -translate-x-1/2 -translate-y-full w-180 h-15.5 border-t-2 border-l-8 border-r-8 border-bh-red-2 bg-t
ransparent  "
                style="border-radius: 50% 50% 0 0 / 100% 100% 0 0;">
            </div>
            <div class="absolute top-[calc(50%+1px)] left-1/2 -translate-x-1/2 -translate-y-full w-177 h-15 border-t-2 border-l-8 border-r-8 border-bh-red-3 bg-tra
nsparent  "
                style="border-radius: 50% 50% 0 0 / 100% 100% 0 0;">
            </div>
            <div class="absolute top-[calc(50%+1px)] left-1/2 -translate-x-1/2 -translate-y-full w-174 h-14.5 border-t-2 border-l-8 border-r-8 border-bh-red-1 bg-t
ransparent  "
                style="border-radius: 50% 50% 0 0 / 100% 100% 0 0;">
            </div>
            <div class="absolute top-[calc(50%+1px)] left-1/2 -translate-x-1/2 -translate-y-full w-171 h-14 border-t-2 border-l-6 border-r-6 border-bh-red-2 bg-tra
nsparent  "
                style="border-radius: 50% 50% 0 0 / 100% 100% 0 0;">
            </div>
            <div class="absolute top-[calc(50%+1px)] left-1/2 -translate-x-1/2 -translate-y-full w-169 h-13.5 border-t-2 border-l-6 border-r-6 border-bh-red-2 bg-t
ransparent  "
                style="border-radius: 50% 50% 0 0 / 100% 100% 0 0;">
            </div>
            <div class="absolute top-[calc(50%+1px)] left-1/2 -translate-x-1/2 -translate-y-full w-167 h-13 border-t-2 border-l-6 border-r-6 border-bh-red-3 bg-tra
nsparent  "
                style="border-radius: 50% 50% 0 0 / 100% 100% 0 0;">
            </div>

            <!-- Outer circles: blurry ring -->
            <div
                class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-186 h-186 rounded-full bg-bh-red-1 blur-2xl">
            </div>

            <div class="relative slow-spin">
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-186 h-186 rounded-t-full bg-bh-orange-3"
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-183 h-183 rounded-t-full bg-bh-red-1"
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-180 h-180 rounded-t-full bg-bh-red-2"
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-177 h-177 rounded-t-full bg-bh-red-2"
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-177 h-177 rounded-t-full bg-bh-red-3"
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-174 h-174 rounded-t-full bg-bh-red-1"
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-171 h-171 rounded-t-full bg-bh-red-3"
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-165 h-165 rounded-full bg-bh-red-3 "
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-163 h-163 rounded-full bg-bh-red-2 "
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-161 h-161 rounded-full bg-bh-red-3 "
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-159 h-159 rounded-full bg-bh-red-2 "
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-157 h-157 rounded-full bg-bh-red-2 "
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-155 h-155 rounded-full bg-bh-red-1 "
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-153 h-153 rounded-full bg-bh-red-2 "
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-151 h-151 rounded-full bg-bh-red-3 "
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-149 h-149 rounded-full bg-bh-red-2 "
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-147 h-147 rounded-full bg-bh-red-1 "
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-145 h-145 rounded-full bg-bh-orange-3 "
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-143 h-143 rounded-full bg-bh-orange-2 "
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-141 h-141 rounded-full bg-bh-orange-1 "
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-139 h-139 rounded-full bg-bh-orange-2 "
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-137 h-137 rounded-full bg-bh-red-1 "
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-135 h-135 rounded-full bg-bh-red-1 "
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-133 h-133 rounded-full bg-bh-orange-1 "
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-131 h-131 rounded-full bg-bh-orange-2 "
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-129 h-129 rounded-full bg-bh-orange-3 "
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-127 h-127 rounded-full bg-bh-red-1 "
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-124 h-124 rounded-full bg-bh-red-2 "
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-121 h-121 rounded-full bg-bh-orange-1 "
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-120 h-120 rounded-full bg-bh-orange-2 "
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-119 h-119 rounded-full bg-bh-orange-1 "
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-118 h-118 rounded-full bg-bh-orange-1 "
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-117 h-117 rounded-full bg-bh-orange-3 "
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-116 h-116 rounded-full bg-bh-orange-1 "
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-115 h-115 rounded-full bg-bh-orange-1 "
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-114 h-114 rounded-full bg-bh-orange-3 "
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-113 h-113 rounded-full bg-bh-orange-1 "
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-112 h-112 rounded-full bg-bh-orange-1 "
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-111 h-111 rounded-full bg-bh-red-1 "
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-110 h-110 rounded-full bg-bh-red-2 "
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-109 h-109 rounded-full bg-bh-red-2 "
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-108 h-108 rounded-full bg-bh-orange-2 "
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-107 h-107 rounded-full bg-bh-orange-1 "
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-106 h-106 rounded-full bg-bh-orange-2 "
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-105 h-105 rounded-full bg-bh-orange-3 "
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-104 h-104 rounded-full bg-bh-orange-2 "
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-103 h-103 rounded-full bg-bh-orange-1 "
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-102 h-102 rounded-full bg-bh-orange-2 "
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-101 h-101 rounded-full bg-bh-orange-2 "
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-100 h-100 rounded-full bg-bh-orange-2 "
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-99 h-99 rounded-full bg-bh-orange-3 "
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-98 h-98 rounded-full bg-bh-red-2 "
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-97 h-97 rounded-full bg-bh-red-1 "
                    style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
                <div
                    class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 rounded-full bg-xrb-bg-1">
                </div>
            </div>

            <!-- inner haze -->
            <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 rounded-full bg-bh-red-1/50 animate-pulse blur-lg"
                style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
            <div
                class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-90 h-90 rounded-full bg-xrb-bg-1 blur-sm">
            </div>

            <!-- Inner circle: Black -->
            <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-86 h-86 rounded-full bg-xrb-bg-1">
            </div>
            <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-70 h-70 rounded-full bg-bh-yellow-1 animate-pulse"
                style="border-radius: 49.5% 50.5% 50% 49.75% / 50% 50% 50% 50%;"></div>
            <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-70 h-70 rounded-full bg-xrb-bg-1">
            </div>

            <!-- bottom half of outer ring -->

            <!-- blur layer -->
             <!-- <div class="absolute top-1/2 left-1/2 -translate-x-1/2 w-360 h-40 border-b-34 border-l-84 border-r-84 border-bh-red-2 bg-transparent"
                style="border-radius: 0% 0% 50% 50% / 0% 0% 100% 100%;">
            </div> -->

            <div class="absolute top-1/2 left-1/2 -translate-x-1/2 w-330 h-31 border-b-48 border-l-86 border-r-86 border-bh-red-3 bg-transparent blur-sm"
                style="border-radius: 0% 0% 50% 50% / 0% 0% 100% 100%;">
            </div>
            <div class="absolute top-1/2 left-1/2 -translate-x-1/2 w-320 h-30 border-b-32 border-l-86 border-r-86 border-bh-red-3 bg-transparent  "
                style="border-radius: 0 0 50% 50% / 0 0 100% 100%;">
            </div>
            <div class="absolute top-1/2 left-1/2 -translate-x-1/2 w-278 h-29 border-b-28 border-l-30 border-r-30 border-bh-red-3 bg-transparent  "
                style="border-radius: 0 0 50% 50% / 0 0 100% 100%;">
            </div>
            <div class="absolute top-1/2 left-1/2 -translate-x-1/2 w-264 h-28 border-b-28 border-l-30 border-r-30 border-bh-red-2 bg-transparent  "
                style="border-radius: 0 0 50% 50% / 0 0 100% 100%;">
            </div>
            <div class="absolute top-1/2 left-1/2 -translate-x-1/2 w-250 h-27 border-b-28 border-l-22 border-r-22 border-bh-red-1 bg-transparent  "
                style="border-radius: 0 0 50% 50% / 0 0 100% 100%;">
            </div>
            <div class="absolute top-1/2 left-1/2 -translate-x-1/2 w-240 h-26 border-b-28 border-l-22 border-r-22 border-bh-orange-3 bg-transparent  "
                style="border-radius: 0 0 50% 50% / 0 0 100% 100%;">
            </div>
            <div class="absolute top-1/2 left-1/2 -translate-x-1/2 w-232 h-25 border-b-28 border-l-22 border-r-22 border-bh-orange-2 bg-transparent  "
            style="border-radius: 0 0 50% 50% / 0 0 100% 100%;">
            </div>
            <div class="absolute top-1/2 left-1/2 -translate-x-1/2 w-224 h-24 border-b-28 border-l-22 border-r-22 border-bh-yellow-2 bg-transparent  "
                style="border-radius: 0 0 50% 50% / 0 0 100% 100%;">
            </div>
            <div class="absolute top-1/2 left-1/2 -translate-x-1/2 w-216 h-23 border-b-20 border-l-22 border-r-22 border-bh-orange-1 bg-transparent  "
                style="border-radius: 0 0 50% 50% / 0 0 100% 100%;">
            </div>
            <div class="absolute top-1/2 left-1/2 -translate-x-1/2 w-207 h-22 border-b-16 border-l-18 border-r-18 border-bh-orange-2 bg-transparent  "
                style="border-radius: 0 0 50% 50% / 0 0 100% 100%;">
            </div>
            <div class="absolute top-1/2 left-1/2 -translate-x-1/2 w-200 h-20 border-b-16 border-l-18 border-r-18 border-bh-orange-3 bg-transparent  "
                style="border-radius: 0 0 50% 50% / 0 0 100% 100%;">
            </div>
            <div class="absolute top-1/2 left-1/2 -translate-x-1/2 w-195 h-17.5 border-b-6 border-l-8 border-r-8 border-bh-orange-2 bg-transparent  "
                style="border-radius: 0 0 50% 50% / 0 0 100% 100%;">
            </div>
            <div class="absolute top-1/2 left-1/2 -translate-x-1/2 w-192 h-16 border-b-6 border-l-8 border-r-8 border-bh-orange-1 bg-transparent  "
                style="border-radius: 0 0 50% 50% / 0 0 100% 100%;">
            </div>
            <div class="absolute top-1/2 left-1/2 -translate-x-1/2 w-189 h-15 border-b-6 border-l-8 border-r-8 border-bh-orange-2 bg-transparent  "
                style="border-radius: 0 0 50% 50% / 0 0 100% 100%;">
            </div>
            <div class="absolute top-1/2 left-1/2 -translate-x-1/2 w-186 h-14 border-b-6 border-l-8 border-r-8 border-bh-orange-3 bg-transparent  "
                style="border-radius: 0 0 50% 50% / 0 0 100% 100%;">
            </div>
            <div class="absolute top-1/2 left-1/2 -translate-x-1/2 w-183 h-13 border-b-6 border-l-8 border-r-8 border-bh-red-1 bg-transparent  "
                style="border-radius: 0 0 50% 50% / 0 0 100% 100%;">
            </div>
            <div class="absolute top-1/2 left-1/2 -translate-x-1/2 w-180 h-12 border-b-6 border-l-8 border-r-8 border-bh-red-2 bg-transparent  "
                style="border-radius: 0 0 50% 50% / 0 0 100% 100%;">
            </div>
            <div class="absolute top-1/2 left-1/2 -translate-x-1/2 w-177 h-11 border-b-6 border-l-8 border-r-8 border-bh-red-3 bg-transparent  "
                style="border-radius: 0 0 50% 50% / 0 0 100% 100%;">
            </div>
            <div class="absolute top-1/2 left-1/2 -translate-x-1/2 w-174 h-10 border-b-6 border-l-8 border-r-8 border-bh-red-1 bg-transparent  "
                style="border-radius: 0 0 50% 50% / 0 0 100% 100%;">
            </div>
            <div class="absolute top-1/2 left-1/2 -translate-x-1/2 w-171 h-9 border-b-6 border-l-6 border-r-6 border-bh-red-2 bg-transparent  "
                style="border-radius: 0 0 50% 50% / 0 0 100% 100%;">
            </div>
            <div class="absolute top-1/2 left-1/2 -translate-x-1/2 w-169 h-8 border-b-6 border-l-6 border-r-6 border-bh-red-2 bg-transparent  "
                style="border-radius: 0 0 50% 50% / 0 0 100% 100%;">
            </div>
            <div class="absolute top-1/2 left-1/2 -translate-x-1/2 w-167 h-7 border-b-4 border-l-6 border-r-6 border-bh-red-3 bg-transparent  "
                style="border-radius: 0 0 50% 50% / 0 0 100% 100%;">
            </div>
        </div>
    </div>

</template>
<style scoped>
.bh-responsive {
    top: var(--bh-top);
    left: var(--bh-left);
    scale: var(--bh-scale);
}


@media (max-width: 749px) {
    .bh-responsive {
        --bh-top: 57%;
        --bh-left: 87.5%;
        --bh-scale: 0.8;
    }
}

@media (min-width: 750px) and (max-width: 849px) {
    .bh-responsive {
        --bh-top: 57%;
        --bh-left: 87.5%;
        --bh-scale: 1;
    }
}

@media (min-width: 850px) and (max-width: 1250px) {
    .bh-responsive {
        --bh-top: 57%;
        --bh-left: 87.5%;
        --bh-scale: 1.2;
    }
}

@media (min-width: 1251px) {
    .bh-responsive {
        --bh-top: 25%;
        --bh-left: 85%;
        --bh-scale: 1.7;
    }
}

.star-field-container {
    position: absolute;
    /* Use a 0-size container at the center so children use vw/vh relative to center */
    top: 0;
    left: 0;
    width: 0;
    height: 0;
    pointer-events: none;
    z-index: -1;
}

.star {
    position: absolute;
    background: #fff;
    border-radius: 50%;
    /* Optimization: Only animate opacity. Scaling individual stars during 
       a parent 40x scale is redundant and costs CPU cycles. */
    will-change: opacity;
    animation: twinkle var(--star-duration) ease-in-out var(--star-delay) infinite alternate;
}

@keyframes twinkle {
    from {
        opacity: 0.2;
    }

    to {
        opacity: 0.5;
    }
}

/* Transitions */
.slow-spin {
    animation: spin 1s linear infinite;
}

@keyframes spin {
    from {
        transform: rotate(0deg);
    }

    to {
        transform: rotate(360deg);
    }
}

.bh-idle {
    transform: translate(-50%, -50%) scale(1) rotate(0deg);
}

.bh-zoomed {
    transform: translate(-50%, -50%) scale(40) rotate(-120deg);
}

.bh-transition {
    transition: transform 1250ms cubic-bezier(0.6, 0, 0.1, 1),
                top 600ms ease,
                left 600ms ease,
                scale 600ms ease;
}

.animate-pulse {
    animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

.rotate-45 {
    transform: rotate(-70deg);
}

@keyframes pulse {

    0%,
    100% {
        opacity: 1;
    }

    50% {
        opacity: .5;
    }
}
</style>
<style>
    /*  This is to prevent any scrolling */
    html, body {
        overflow: hidden;
        height: 100%;
    }
</style>