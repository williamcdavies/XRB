<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const props = defineProps<{
  state: 'idle' | 'zoomed'
}>()

const emit = defineEmits(['done'])

const canvasRef = ref<HTMLCanvasElement | null>(null)

const U = 4

const C: Record<string, string> = {
  red1:     '#9b2016',
  red2:     '#67110c',
  red3:     '#600f08',
  orange1:  '#e66f32',
  orange2:  '#dc3910',
  orange3:  '#b82500',
  yellow1:  '#dfa75a',
  yellow2:  '#e49040',
  'xrb-bg': '#0e1116',
}

const TOP_ARCS = [
     { w: 320, h: 21.5,   bb: 10, bl: 24, br: 24, c: 'red3'    },
     { w: 278, h: 21,   bb: 6, bl: 7, br: 7, c: 'red3'    },
     { w: 264, h: 20.75,   bb: 6, bl: 7, br: 7, c: 'red2'    },
     { w: 250, h: 20.5,   bb: 6, bl: 6, br: 6, c: 'red1'    },
    { w: 240, h: 20,   bb: 6, bl: 6, br: 6, c: 'orange3' },
    { w: 232, h: 19,   bb: 6, bl: 6, br: 6, c: 'orange2' },
    { w: 224, h: 18,   bb: 6, bl: 6, br: 6, c: 'yellow2' },
    { w: 216, h: 17,   bb: 6, bl: 6, br: 6, c: 'orange1' },
    { w: 207, h: 16,   bb: 6, bl: 6, br: 6, c: 'orange2' },
    { w: 200, h: 15,   bb: 6, bl: 6, br: 6, c: 'orange3' },
    { w: 195, h: 14, bb: 2,  bl: 2,  br: 2,  c: 'orange2' },
    { w: 192, h: 13,   bb: 2,  bl: 2,  br: 2,  c: 'orange1' },
    { w: 189, h: 12,   bb: 2,  bl: 2,  br: 2,  c: 'orange2' },
    { w: 186, h: 11,   bb: 2,  bl: 2,  br: 2,  c: 'orange3' },
    { w: 183, h: 10,   bb: 2,  bl: 2,  br: 2,  c: 'red1'    },
    { w: 180, h: 9,   bb: 2,  bl: 2,  br: 2,  c: 'red2'    },
    { w: 177, h: 8,   bb: 2,  bl: 2,  br: 2,  c: 'red3'    },
    { w: 174, h: 7,   bb: 2,  bl: 2,  br: 2,  c: 'red1'    },
    { w: 171, h: 6,    bb: 2,  bl: 4,  br: 4,  c: 'red3'    },
    { w: 163, h: 5,    bb: 2,  bl: 1,  br: 1,  c: 'red2'    },
    { w: 161, h: 4,    bb: 1,  bl: 1,  br: 1,  c: 'red3'    },
]

const FILLED_CIRCLES = [
  { w: 186, c: 'orange3' },
  { w: 183, c: 'red1'    },
  { w: 180, c: 'red2'    },
  { w: 177, c: 'red2'    },
  { w: 177, c: 'red3'    },
  { w: 174, c: 'red1'    },
  { w: 171, c: 'red3'    },
  { w: 165, c: 'red3'    },
  { w: 163, c: 'red2'    },
  { w: 161, c: 'red3'    },
  { w: 159, c: 'red2'    },
  { w: 157, c: 'red2'    },
  { w: 155, c: 'red1'    },
  { w: 153, c: 'red2'    },
  { w: 151, c: 'red3'    },
  { w: 149, c: 'red2'    },
  { w: 147, c: 'red1'    },
  { w: 145, c: 'orange3' },
  { w: 143, c: 'orange2' },
  { w: 141, c: 'orange1' },
  { w: 139, c: 'orange2' },
  { w: 137, c: 'red1'    },
  { w: 135, c: 'red1'    },
  { w: 133, c: 'orange1' },
  { w: 131, c: 'orange2' },
  { w: 129, c: 'orange3' },
  { w: 127, c: 'red1'    },
  { w: 124, c: 'red2'    },
  { w: 121, c: 'orange1' },
  { w: 120, c: 'orange2' },
  { w: 119, c: 'orange1' },
  { w: 118, c: 'orange1' },
  { w: 117, c: 'orange3' },
  { w: 116, c: 'orange1' },
  { w: 115, c: 'orange1' },
  { w: 114, c: 'orange3' },
  { w: 113, c: 'orange1' },
  { w: 112, c: 'orange1' },
  { w: 111, c: 'red1'    },
  { w: 110, c: 'red2'    },
  { w: 109, c: 'red2'    },
  { w: 108, c: 'orange2' },
  { w: 107, c: 'orange1' },
  { w: 106, c: 'orange2' },
  { w: 105, c: 'orange3' },
  { w: 104, c: 'orange2' },
  { w: 103, c: 'orange1' },
  { w: 102, c: 'orange2' },
  { w: 101, c: 'orange2' },
  { w: 100, c: 'orange2' },
  { w: 99,  c: 'orange3' },
  { w: 98,  c: 'red2'    },
  { w: 97,  c: 'red1'    },
  { w: 96,  c: 'xrb-bg'  },  // innermost
]

const EXTRA_CIRCLES = [
  { w: 86, c: 'xrb-bg'  },
  { w: 70, c: 'yellow1' },
  { w: 70, c: 'xrb-bg'  },
]

const BOTTOM_ARCS = [
  { w: 320, h: 30,   bb: 10, bl: 24, br: 24, c: 'red3'    },
  { w: 278, h: 29,   bb: 6, bl: 7, br: 7, c: 'red3'    },
  { w: 264, h: 28,   bb: 6, bl: 7, br: 7, c: 'red2'    },
  { w: 250, h: 27,   bb: 6, bl: 6, br: 6, c: 'red1'    },
  { w: 240, h: 26,   bb: 6, bl: 6, br: 6, c: 'orange3' },
  { w: 232, h: 25,   bb: 6, bl: 6, br: 6, c: 'orange2' },
  { w: 224, h: 24,   bb: 6, bl: 6, br: 6, c: 'yellow2' },
  { w: 216, h: 23,   bb: 6, bl: 6, br: 6, c: 'orange1' },
  { w: 207, h: 22,   bb: 6, bl: 6, br: 6, c: 'orange2' },
  { w: 200, h: 20,   bb: 6, bl: 6, br: 6, c: 'orange3' },
  { w: 195, h: 17.5, bb: 2,  bl: 2,  br: 2,  c: 'orange2' },
  { w: 192, h: 16,   bb: 2,  bl: 2,  br: 2,  c: 'orange1' },
  { w: 189, h: 15,   bb: 2,  bl: 2,  br: 2,  c: 'orange2' },
  { w: 186, h: 14,   bb: 2,  bl: 2,  br: 2,  c: 'orange3' },
  { w: 183, h: 13,   bb: 2,  bl: 2,  br: 2,  c: 'red1'    },
  { w: 180, h: 12,   bb: 2,  bl: 2,  br: 2,  c: 'red2'    },
  { w: 177, h: 11,   bb: 2,  bl: 2,  br: 2,  c: 'red3'    },
  { w: 174, h: 10,   bb: 2,  bl: 2,  br: 2,  c: 'red1'    },
  { w: 171, h: 9,    bb: 2,  bl: 4,  br: 4,  c: 'red3'    },
  { w: 163, h: 8,    bb: 2,  bl: 1,  br: 1,  c: 'red2'    },
  { w: 161, h: 7,    bb: 1,  bl: 1,  br: 1,  c: 'red3'    },
]

function drawTopArc(
  ctx: CanvasRenderingContext2D,
  cx: number, cy: number,
  W: number, H: number,
  bt: number, bl: number, br: number,
  color: string,
) {
  ctx.save()

  // rotate 180° around the center
  ctx.translate(cx, cy)
  ctx.rotate(Math.PI)
  ctx.translate(-cx, -cy)

  drawBottomArc(ctx, cx, cy, W, H, bt, bl, br, color)

  ctx.restore()
}

function drawBottomArc(
  ctx: CanvasRenderingContext2D,
  cx: number, cy: number,
  W: number, H: number,
  bb: number, bl: number, br: number,
  color: string,
) {
  const outerA = W / 2
  const outerB = H

  const innerCx = cx + (bl - br) / 2
  const innerA  = (W - bl - br) / 2
  const innerB  = H - bb

  if (innerA <= 0 || innerB <= 0) return

  ctx.beginPath()
  ctx.ellipse(cx, cy, outerA, outerB, 0, Math.PI, 2 * Math.PI, false)
  ctx.ellipse(innerCx, cy, innerA, innerB, 0, 2 * Math.PI, Math.PI, true)
  ctx.closePath()
  ctx.fillStyle = C[color] ?? color
  ctx.fill()
}

function drawCircle(
  ctx: CanvasRenderingContext2D,
  cx: number, cy: number,
  w: number,
  color: string,
) {
  ctx.beginPath()
  ctx.arc(cx, cy, w / 2, 0, 2 * Math.PI)
  ctx.fillStyle = C[color] ?? color
  ctx.fill()
}

// stars
interface Star { x: number; y: number; r: number }
let stars: Star[] = []

function initStars(w: number, h: number) {
  stars = Array.from({ length: 400 }, () => ({
    x: Math.random() * w,
    y: Math.random() * h,
    r: Math.random() * 0.5 + 0.25,
  }))
}

function drawFrame(ctx: CanvasRenderingContext2D, W: number, H: number) {
  ctx.clearRect(0, 0, W, H)

  // Stars
  for (const s of stars) {
    ctx.beginPath()
    ctx.arc(s.x, s.y, s.r, 0, 2 * Math.PI)
    ctx.fillStyle = 'rgba(255,255,255,1)'
    ctx.fill()
  }

  const cx = W / 2
  const cy = H / 2

  ctx.save()
  ctx.translate(cx, cy)
  ctx.rotate(-70 * Math.PI / 180)
  ctx.translate(-cx, -cy)

  // 1 Top half arcs 
  for (const a of TOP_ARCS) {
    drawTopArc(ctx, cx, cy, a.w * U, a.h * U, a.bb * U, a.bl * U, a.br * U, a.c)
  }

  //2 Filled circles
  for (const fc of FILLED_CIRCLES) {
    drawCircle(ctx, cx, cy, fc.w * U, fc.c)
  }

  // 3 Extra circles
  for (const ec of EXTRA_CIRCLES) {
    drawCircle(ctx, cx, cy, ec.w * U, ec.c)
  }

  // 4 Bottom half arcs 
  for (const a of BOTTOM_ARCS) {
    drawBottomArc(ctx, cx, cy, a.w * U, a.h * U, a.bb * U, a.bl * U, a.br * U, a.c)
  }

  ctx.restore()
}

onMounted(() => {
  const canvas = canvasRef.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')!

    function resize() {
        canvas!.width  = window.innerWidth * 2
        canvas!.height = window.innerHeight * 2
        initStars(canvas!.width, canvas!.height)
    }

    resize()
  window.addEventListener('resize', resize)

  let rafId: number
  const loop = () => {
    drawFrame(ctx, canvas!.width, canvas!.height)
    rafId = requestAnimationFrame(loop)
  }
  rafId = requestAnimationFrame(loop)

  onUnmounted(() => {
    cancelAnimationFrame(rafId)
    window.removeEventListener('resize', resize)
  })
})

function onTransitionEnd(e: TransitionEvent) {
  if (e.propertyName !== 'transform') return
  if (props.state === 'zoomed') emit('done')
}
</script>

<template>
  <div
    class="absolute bh-responsive bh-transition"
    style="will-change: transform;"
    :class="{
      'bh-idle':   props.state === 'idle',
      'bh-zoomed': props.state === 'zoomed',
    }"
    @transitionend="onTransitionEnd"
  >
    <canvas
      ref="canvasRef"
      class="absolute pointer-events-none -z-10"
      style="transform: translate(-50%, -50%); top: 0; left: 0;"
    />
  </div>
</template>

<style scoped>
.bh-responsive {
  top:   var(--bh-top);
  left:  var(--bh-left);
  scale: var(--bh-scale);
}

@media (max-width: 749px) {
  .bh-responsive { --bh-top: 57%; --bh-left: 87.5%; --bh-scale: 0.8; }
}
@media (min-width: 750px) and (max-width: 849px) {
  .bh-responsive { --bh-top: 57%; --bh-left: 87.5%; --bh-scale: 1; }
}
@media (min-width: 850px) and (max-width: 1250px) {
  .bh-responsive { --bh-top: 57%; --bh-left: 87.5%; --bh-scale: 1.2; }
}
@media (min-width: 1251px) {
  .bh-responsive { --bh-top: 25%; --bh-left: 85%; --bh-scale: 1.7; }
}

.bh-idle   { transform: translate(-50%, -50%) scale(1) rotate(-135deg); }
.bh-zoomed { transform: translate(-50%, -50%) scale(8) rotate(-200deg); }

.bh-transition {
  transition:
    transform 1250ms cubic-bezier(0.6, 0, 0.1, 1),
    top       600ms ease,
    left      600ms ease,
    scale     600ms ease;
}
</style>