<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const props = defineProps<{
    state: 'idle' | 'zoomed'
}>()

const emit = defineEmits(['done'])
const canvasRef = ref<HTMLCanvasElement | null>(null)
const BASE_U = 4
let refreshInterval: ReturnType<typeof setInterval> | null = null

// create stars off of seed 
function splitmix32(a: number) {
    return function() {
        a |= 0; a = a + 0x9e3779b9 | 0;
        let t = a ^ a >>> 16; t = Math.imul(t, 0x21f0aaad);
        t = t ^ t >>> 15; t = Math.imul(t, 0x735a2d97);
        return ((t = t ^ t >>> 15) >>> 0) / 4294967296;
    }
}

const C: Record<string, string> = {
    red1: '#9b2016', red2: '#67110c', red3: '#600f08',
    orange1: '#e66f32', orange2: '#dc3910', orange3: '#b82500',
    yellow1: '#dfa75a', yellow2: '#e49040', 'xrb-bg': '#0e1116',
}

const TOP_ARCS = [{ w: 320, h: 18, bb: 10, bl: 27, br: 27, c: 'red3' }, { w: 278, h: 18, bb: 6, bl: 10, br: 10, c: 'red3' }, { w: 264, h: 18, bb: 6, bl: 9, br: 9, c: 'red2' }, { w: 250, h: 18, bb: 6, bl: 6, br: 6, c: 'red1' }, { w: 240, h: 18, bb: 6, bl: 6, br: 6, c: 'orange3' }, { w: 232, h: 17, bb: 6, bl: 6, br: 6, c: 'orange2' }, { w: 224, h: 16, bb: 6, bl: 6, br: 6, c: 'yellow2' }, { w: 216, h: 15, bb: 6, bl: 6, br: 6, c: 'orange1' }, { w: 207, h: 14, bb: 6, bl: 6, br: 6, c: 'orange2' }, { w: 200, h: 13, bb: 6, bl: 6, br: 6, c: 'orange3' }, { w: 195, h: 12, bb: 2, bl: 2, br: 2, c: 'orange2' }, { w: 192, h: 11, bb: 2, bl: 2, br: 2, c: 'orange1' }, { w: 189, h: 10, bb: 2, bl: 2, br: 2, c: 'orange2' }, { w: 186, h: 9, bb: 2, bl: 2, br: 2, c: 'orange3' }, { w: 183, h: 8, bb: 2, bl: 2, br: 2, c: 'red1' }, { w: 180, h: 7, bb: 2, bl: 2, br: 2, c: 'red2' }, { w: 177, h: 6, bb: 2, bl: 2, br: 2, c: 'red3' }, { w: 174, h: 5, bb: 2, bl: 2, br: 2, c: 'red1' }, { w: 171, h: 4, bb: 2, bl: 4, br: 4, c: 'red3' }, { w: 163, h: 3, bb: 2, bl: 1, br: 1, c: 'red2' }, { w: 161, h: 2, bb: 1, bl: 1, br: 1, c: 'red3' }];
const FILLED_CIRCLES = [{ w: 186, c: 'orange3' }, { w: 183, c: 'red1' }, { w: 180, c: 'red2' }, { w: 177, c: 'red2' }, { w: 177, c: 'red3' }, { w: 174, c: 'red1' }, { w: 171, c: 'red3' }, { w: 165, c: 'red3' }, { w: 163, c: 'red2' }, { w: 161, c: 'red3' }, { w: 159, c: 'red2' }, { w: 157, c: 'red2' }, { w: 155, c: 'red1' }, { w: 153, c: 'red2' }, { w: 151, c: 'red3' }, { w: 149, c: 'red2' }, { w: 147, c: 'red1' }, { w: 145, c: 'orange3' }, { w: 143, c: 'orange2' }, { w: 141, c: 'orange1' }, { w: 139, c: 'orange2' }, { w: 137, c: 'red1' }, { w: 135, c: 'red1' }, { w: 133, c: 'orange1' }, { w: 131, c: 'orange2' }, { w: 129, c: 'orange3' }, { w: 127, c: 'red1' }, { w: 124, c: 'red2' }, { w: 121, c: 'orange1' }, { w: 120, c: 'orange2' }, { w: 119, c: 'orange1' }, { w: 118, c: 'orange1' }, { w: 117, c: 'orange3' }, { w: 116, c: 'orange1' }, { w: 115, c: 'orange1' }, { w: 114, c: 'orange3' }, { w: 113, c: 'orange1' }, { w: 112, c: 'orange1' }, { w: 111, c: 'red1' }, { w: 110, c: 'red2' }, { w: 109, c: 'red2' }, { w: 108, c: 'orange2' }, { w: 107, c: 'orange1' }, { w: 106, c: 'orange2' }, { w: 105, c: 'orange3' }, { w: 104, c: 'orange2' }, { w: 103, c: 'orange1' }, { w: 102, c: 'orange2' }, { w: 101, c: 'orange2' }, { w: 100, c: 'orange2' }, { w: 99, c: 'orange3' }, { w: 98, c: 'red2' }, { w: 97, c: 'red1' }, { w: 96, c: 'xrb-bg' }];
const EXTRA_CIRCLES = [{ w: 86, c: 'xrb-bg' }, { w: 70, c: 'yellow1' }, { w: 70, c: 'xrb-bg' }];
const BOTTOM_ARCS = [{ w: 320, h: 30, bb: 10, bl: 27, br: 27, c: 'red3' }, { w: 278, h: 29, bb: 6, bl: 10, br: 10, c: 'red3' }, { w: 264, h: 28, bb: 6, bl: 9, br: 9, c: 'red2' }, { w: 250, h: 27, bb: 6, bl: 6, br: 6, c: 'red1' }, { w: 240, h: 26, bb: 6, bl: 6, br: 6, c: 'orange3' }, { w: 232, h: 25, bb: 6, bl: 6, br: 6, c: 'orange2' }, { w: 224, h: 24, bb: 6, bl: 6, br: 6, c: 'yellow2' }, { w: 216, h: 23, bb: 6, bl: 6, br: 6, c: 'orange1' }, { w: 207, h: 22, bb: 6, bl: 6, br: 6, c: 'orange2' }, { w: 200, h: 20, bb: 6, bl: 6, br: 6, c: 'orange3' }, { w: 195, h: 17.5, bb: 2, bl: 2, br: 2, c: 'orange2' }, { w: 192, h: 16, bb: 2, bl: 2, br: 2, c: 'orange1' }, { w: 189, h: 15, bb: 2, bl: 2, br: 2, c: 'orange2' }, { w: 186, h: 14, bb: 2, bl: 2, br: 2, c: 'orange3' }, { w: 183, h: 13, bb: 2, bl: 2, br: 2, c: 'red1' }, { w: 180, h: 12, bb: 2, bl: 2, br: 2, c: 'red2' }, { w: 177, h: 11, bb: 2, bl: 2, br: 2, c: 'red3' }, { w: 174, h: 10, bb: 2, bl: 2, br: 2, c: 'red1' }, { w: 171, h: 9, bb: 2, bl: 4, br: 4, c: 'red3' }, { w: 163, h: 8, bb: 2, bl: 1, br: 1, c: 'red2' }, { w: 161, h: 7, bb: 1, bl: 1, br: 1, c: 'red3' }];

function drawTopArc(ctx: any, cx: any, cy: any, W: any, H: any, bt: any, bl: any, br: any, color: any, vibrateFactor: any) {
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(Math.PI); ctx.translate(-cx, -cy);
    drawBottomArc(ctx, cx, cy + 1, W, H, bt, bl, br, color, vibrateFactor); ctx.restore();
}
function drawBottomArc(ctx: any, cx: any, cy: any, W: any, H: any, bb: any, bl: any, br: any, color: any, vibrateFactor: any) {
    const rand = vibrateFactor; const outerA = (W / 2) * (1 + rand); const outerB = H * (1 + rand);
    const innerCx = cx + (bl - br) / 2; const innerA = ((W - bl - br) / 2) * (1 + rand); const innerB = (H - bb) * (1 + rand);
    if (innerA <= 0 || innerB <= 0) return;
    ctx.beginPath(); ctx.ellipse(cx, cy, outerA, outerB, 0, Math.PI, 2 * Math.PI, false);
    ctx.ellipse(innerCx, cy, innerA, innerB, 0, 2 * Math.PI, Math.PI, true);
    ctx.closePath(); ctx.fillStyle = C[color] ?? color; ctx.fill();
}
function drawCircle(ctx: any, cx: any, cy: any, w: any, color: any) {
    const rx = w / 2; const ry = rx * (0.995 + Math.random() * 0.005);
    ctx.beginPath(); ctx.ellipse(cx, cy, rx, ry, 0, 0, 2 * Math.PI);
    ctx.fillStyle = C[color] ?? color; ctx.fill();
}

interface Star { x: number; y: number; r: number }
let stars: Star[] = []
let starsInitialized = false

// Updated initStars to use seeded random and normalized coordinates
function initStars() {
    if (starsInitialized) return
    
    const seed = 41
    const random = splitmix32(seed)
    
    stars.length = 0
    const count = 2400 
    
    for (let i = 0; i < count; i++) {
        stars.push({
            x: random(), // Normalized 0 to 1
            y: random(), // Normalized 0 to 1
            r: random() * 0.8 + 0.2,
        })
    }
    starsInitialized = true
}

function drawFrame(ctx: CanvasRenderingContext2D, W: number, H: number, scaledU: number) {
    ctx.clearRect(0, 0, W, H)
    const cx = W / 2
    const cy = H / 2

    // Stars now use W and H to calculate actual position from percentage
    for (const s of stars) {
        ctx.beginPath(); 
        ctx.arc(s.x * W, s.y * H, s.r, 0, 2 * Math.PI);
        ctx.fillStyle = 'white'; 
        ctx.fill();
    }

    ctx.save()
    ctx.translate(cx, cy)
    ctx.rotate(-70 * Math.PI / 180)
    ctx.translate(-cx, -cy)

    const vibrate = 0.005
    const arcVibrations = TOP_ARCS.map(() => (Math.random() - 0.5) * vibrate)

    TOP_ARCS.forEach((a, i) => drawTopArc(ctx, cx, cy, a.w * scaledU, a.h * scaledU, a.bb * scaledU, a.bl * scaledU, a.br * scaledU, a.c, arcVibrations[i] ?? 0))
    for (const fc of FILLED_CIRCLES) drawCircle(ctx, cx, cy, fc.w * scaledU, fc.c)
    for (const ec of EXTRA_CIRCLES) drawCircle(ctx, cx, cy, ec.w * scaledU, ec.c)
    BOTTOM_ARCS.forEach((a, i) => drawBottomArc(ctx, cx, cy, a.w * scaledU, a.h * scaledU, a.bb * scaledU, a.bl * scaledU, a.br * scaledU, a.c, arcVibrations[i] ?? 0))

    ctx.restore()
}

onMounted(() => {
    const canvas = canvasRef.value
    if (!canvas) return
    const ctx = canvas.getContext('2d')!

    let currentScale = 1
    function resize() {
        if (!canvas) return

        const dpr = window.devicePixelRatio || 1
        const oversample = 2.5
        currentScale = Math.min(dpr * oversample, 3.0)

        const size = Math.max(window.innerWidth, window.innerHeight) * 1.5

        canvas.style.width = `${size}px`
        canvas.style.height = `${size}px`
        canvas.width = size * currentScale
        canvas.height = size * currentScale

        initStars()
    }

    window.addEventListener('resize', resize)
    resize()

    refreshInterval = setInterval(() => {
        window.location.reload()
    }, 60000) // refresh every minute to prevent lag

    let lastTime = 0
    const frameDuration = 1000 / 30
    const loop = (time: number) => {
        if (time - lastTime >= frameDuration) {
            lastTime = time - ((time - lastTime) % frameDuration)
            drawFrame(ctx, canvas.width, canvas.height, BASE_U * currentScale)
        }
        requestAnimationFrame(loop)
    }
    requestAnimationFrame(loop)
})

function onTransitionEnd(e: TransitionEvent) {
    if (e.propertyName === 'transform' && props.state === 'zoomed') emit('done')
}

onUnmounted(() => {
    if (refreshInterval) {
        clearInterval(refreshInterval)
        stars = []
    }
})

</script>

<template>
    <div class="bh-container bh-transition" :class="state" @transitionend="onTransitionEnd">
        <canvas ref="canvasRef" class="bh-canvas" />
    </div>
</template>

<style scoped>
.bh-container {
    position: absolute;
    top: var(--bh-top);
    left: var(--bh-left);
    will-change: transform;
}

.bh-canvas {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    pointer-events: none;
    z-index: -10;
}

@media (max-width: 749px) { 
    .bh-container { 
        --bh-top: 57%;
        --bh-left: 87.5%;
        --bh-scale: 0.8; 
    } 
}

@media (min-width: 750px) and (max-width: 849px) { 
    .bh-container {
         --bh-top: 57%; --bh-left: 87.5%; --bh-scale: 1; 
        } 
    }

@media (min-width: 850px) and (max-width: 1250px) { 
    .bh-container { 
        --bh-top: 57%;
        --bh-left: 87.5%;
        --bh-scale: 1.2; 
        } 
    }

@media (min-width: 1251px) {
    .bh-container { 
        --bh-top: 25%; 
        --bh-left: 85%; 
        --bh-scale: 1.7; 
    } 
}

.idle {
    transform:
        translate(-50%, -50%) 
        scale(var(--bh-scale)) 
        rotate(-135deg); 
}
.zoomed { 
    transform: 
    translate(-50%, -50%) 
    scale(calc(var(--bh-scale) * 8)) 
    rotate(-200deg); 
}

.bh-transition {
    transition: transform 1250ms cubic-bezier(0.6, 0, 0.1, 1), top 600ms ease, left 600ms ease;
}
</style>