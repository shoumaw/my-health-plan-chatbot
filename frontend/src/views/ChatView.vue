<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft, HeartPulse } from 'lucide-vue-next'
import { useChat } from '@/composables/useChat'
import ChatInterface from '@/components/chat/ChatInterface.vue'

const route = useRoute()
const router = useRouter()

const planId = route.params.planId as string
const planName = route.query.planName as string | undefined

const { messages, loading, error, send } = useChat(planId)
</script>

<template>
  <div class="h-screen bg-surface-subtle flex flex-col overflow-hidden">
    <!-- Chat header -->
    <header class="bg-white border-b border-slate-200 shrink-0" style="box-shadow: var(--shadow-card)">
      <div class="max-w-3xl mx-auto px-4 sm:px-6 h-14 flex items-center gap-3">
        <!-- Back -->
        <button
          class="p-1.5 -ml-1 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition-colors"
          aria-label="Go back"
          @click="router.back()"
        >
          <ArrowLeft class="w-5 h-5" />
        </button>

        <!-- Plan name + AI label -->
        <div class="flex-1 min-w-0">
          <p class="text-sm font-semibold text-slate-900 leading-tight truncate">
            {{ planName ?? 'Benefits Chat' }}
          </p>
          <p class="text-[11px] font-medium text-brand-600 leading-tight">AI Benefits Advisor</p>
        </div>

        <!-- Brand mark -->
        <div class="flex items-center gap-2 shrink-0">
          <div class="w-6 h-6 bg-gradient-to-br from-brand-400 to-brand-600 rounded-md flex items-center justify-center">
            <HeartPulse class="w-3.5 h-3.5 text-white" :stroke-width="2.5" />
          </div>
          <span class="text-xs font-bold text-slate-700 hidden sm:block">Vitable</span>
        </div>
      </div>
    </header>

    <!-- Chat panel — constrained width, fills remaining height -->
    <div class="flex-1 min-h-0 flex flex-col max-w-3xl w-full mx-auto bg-white sm:shadow-sm">
      <ChatInterface
        :messages="messages"
        :loading="loading"
        :error="error"
        class="h-full"
        @send="send"
      />
    </div>
  </div>
</template>

