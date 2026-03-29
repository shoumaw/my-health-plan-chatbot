<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { MessageCircle, ShieldCheck, Sparkles, AlertCircle } from 'lucide-vue-next'
import { usePlans } from '@/composables/usePlans/usePlans'
import AppHeader from '@/components/AppHeader/AppHeader.vue'

type Tier = 'bronze' | 'silver' | 'gold' | 'default'

const router = useRouter()
const { plans, loading, error, fetchPlans } = usePlans()

onMounted(fetchPlans)

function getTier(name: string): Tier {
  const n = name.toLowerCase()
  if (n.includes('bronze')) return 'bronze'
  if (n.includes('silver')) return 'silver'
  if (n.includes('gold')) return 'gold'
  return 'default'
}

const tierBar: Record<Tier, string> = {
  bronze:  'from-amber-400 to-orange-400',
  silver:  'from-slate-300 to-slate-400',
  gold:    'from-yellow-400 to-amber-500',
  default: 'from-brand-400 to-brand-600',
}

const tierBadge: Record<Tier, string> = {
  bronze:  'bg-amber-50 text-amber-700 border-amber-200',
  silver:  'bg-slate-50  text-slate-600  border-slate-200',
  gold:    'bg-yellow-50 text-yellow-700 border-yellow-200',
  default: 'bg-brand-50  text-brand-700  border-brand-200',
}
</script>

<template>
  <div class="min-h-screen bg-surface-subtle">
    <AppHeader subtitle="Benefits Portal">
      <span class="text-sm text-slate-500 hidden sm:block">
        Welcome back, <span class="font-semibold text-slate-800">Alex</span>
      </span>
    </AppHeader>
    <div class="bg-white border-b border-slate-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div class="flex items-start justify-between gap-6">
          <div>
            <span class="inline-flex items-center gap-1.5 text-xs font-semibold text-brand-700 bg-brand-50 border border-brand-200 px-2.5 py-1 rounded-full mb-4">
              <Sparkles class="w-3 h-3" />
              AI-Powered Benefits Advisor
            </span>
            <h1 class="text-3xl font-bold text-slate-900 tracking-tight leading-tight">
              Your Enrolled Plans
            </h1>
            <p class="mt-2 text-slate-500 text-sm max-w-lg leading-relaxed">
              You are currently enrolled in the plans below. Start a chat and ask our AI assistant
              anything about your coverage — deductibles, copays, network providers, and more.
            </p>
          </div>
          <div class="hidden sm:flex items-center justify-center w-20 h-20 rounded-2xl bg-gradient-to-br from-brand-50 to-brand-100 border border-brand-200 shrink-0">
            <ShieldCheck class="w-10 h-10 text-brand-500" />
          </div>
        </div>
      </div>
    </div>
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <div v-if="loading" class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <div
          v-for="n in 3"
          :key="n"
          class="h-64 rounded-2xl bg-white border border-slate-200 animate-pulse"
          style="box-shadow: var(--shadow-card)"
        />
      </div>

      <div
        v-else-if="error"
        class="flex items-center gap-3 rounded-xl border border-red-200 bg-red-50 px-5 py-4 text-sm text-red-700"
      >
        <AlertCircle class="w-4 h-4 shrink-0" />
        {{ error }}
      </div>

      <div v-else-if="plans.length === 0" class="flex flex-col items-center justify-center py-24 gap-4 text-center">
        <div class="w-16 h-16 rounded-2xl bg-slate-100 flex items-center justify-center">
          <ShieldCheck class="w-8 h-8 text-slate-300" />
        </div>
        <div>
          <p class="font-semibold text-slate-600">No active enrollments found</p>
          <p class="text-sm text-slate-400 mt-1">Contact your HR team if you believe this is an error.</p>
        </div>
      </div>

      <template v-else>
        <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          <div
            v-for="plan in plans"
            :key="plan.id"
            class="bg-white rounded-2xl border border-slate-200 overflow-hidden flex flex-col"
            style="box-shadow: var(--shadow-card)"
          >
            <div :class="['h-1.5 bg-linear-to-r', tierBar[getTier(plan.name)]]" />

            <div class="p-6 flex flex-col flex-1 gap-4">
              <div>
                <div class="flex items-start justify-between gap-2 mb-1">
                  <h3 class="font-semibold text-slate-900 text-base leading-snug">
                    {{ plan.name }}
                  </h3>
                  <span :class="['text-[11px] font-semibold border rounded-full px-2 py-0.5 shrink-0', tierBadge[getTier(plan.name)]]">
                    {{ plan.plan_year }}
                  </span>
                </div>
                <p class="text-xs font-medium text-slate-400 uppercase tracking-wider">
                  {{ plan.provider }}
                </p>
              </div>

              <p class="text-sm text-slate-600 leading-relaxed line-clamp-3 flex-1">
                {{ plan.description || 'No description available for this plan.' }}
              </p>
            </div>
          </div>
        </div>

        <div class="mt-8 flex justify-center">
          <button
            class="flex items-center gap-2 rounded-xl bg-brand-500 hover:bg-brand-600 active:bg-brand-700 text-white text-sm font-semibold px-6 py-3 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-500 focus-visible:ring-offset-2"
            @click="router.push({ name: 'chat' })"
          >
            <MessageCircle class="w-4 h-4" />
            Chat with Benefits Advisor
          </button>
        </div>
      </template>
    </main>
  </div>
</template>

