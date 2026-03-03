<script setup lang="ts">
    import { computed } from 'vue';

    const props = withDefaults(
        defineProps<{
            path: string;
            rootPath: string;
            rootLabel: string;
        }>(),
        { rootPath: '', rootLabel: 'Data' }
    );

    const emit = defineEmits<{
        (e: 'navigate', path: string): void;
    }>();

    const segments = computed(() => {
        const root = props.rootPath ? { name: props.rootLabel, path: props.rootPath } : { name: 'Data', path: '' };
        if (!props.path || props.path === props.rootPath) return [root];
        const rest = props.rootPath
            ? props.path.slice(props.rootPath.length).replace(/^\//, '').split('/').filter(Boolean)
            : props.path.split('/').filter(Boolean);
        const result = [root];
        let acc = props.rootPath;
        for (const p of rest) {
            acc = acc ? `${acc}/${p}` : p;
            result.push({ name: p, path: acc });
        }
        return result;
    });
</script>

<template>
    <div class="flex items-center gap-1 flex-wrap border-b border-xrb-border bg-xrb-bg-2 px-4 py-2 text-sm text-xrb-text-1">
        <template v-for="(seg, i) in segments" :key="seg.path">
            <button
                v-if="i > 0"
                type="button"
                class="text-xrb-text-secondary cursor-default"
                disabled
                aria-hidden="true"
            >
                /
            </button>
            <button
                type="button"
                class="rounded px-2 py-1 hover:bg-xrb-bg-3 hover:text-xrb-accent-1 transition-colors truncate max-w-[8rem]"
                :class="{ 'text-xrb-accent-1 font-medium': i === segments.length - 1 }"
                @click="emit('navigate', seg.path)"
            >
                {{ seg.name }}
            </button>
        </template>
    </div>
</template>
