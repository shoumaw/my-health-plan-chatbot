<script setup lang="ts">
import { HeartPulse } from 'lucide-vue-next'

defineProps<{
  subtitle?: string
}>()
</script>

<template>
  <header class="sticky top-0 z-30 bg-white border-b border-slate-200/80" style="box-shadow: var(--shadow-card)">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between gap-4">
      <div class="flex items-center gap-3 shrink-0">
        <div class="w-8 h-8 bg-gradient-to-br from-brand-400 to-brand-600 rounded-lg flex items-center justify-center">
          <HeartPulse class="w-4 h-4 text-white" :stroke-width="2.5" />
        </div>
        <div class="leading-tight">
          <p class="text-sm font-bold text-slate-900 tracking-tight">
            Vitable <span class="text-brand-600">Health</span>
          </p>
          <p v-if="subtitle" class="text-[10px] font-semibold text-slate-400 uppercase tracking-widest">
            {{ subtitle }}
          </p>
        </div>
      </div>
      <slot />
    </div>
  </header>
</template>
