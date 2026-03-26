<script setup lang="ts">
import { ref, nextTick, watch } from 'vue'
import { Sparkles, MessageCircle, Send } from 'lucide-vue-next'
import type { ChatMessage } from './types'

const props = defineProps<{
  messages: ChatMessage[]
  loading?: boolean
  error?: string | null
  planName?: string
}>()

const emit = defineEmits<{
  send: [message: string]
}>()

const input = ref('')
const scrollRef = ref<HTMLElement | null>(null)

function submit() {
  const text = input.value.trim()
  if (!text || props.loading) return
  emit('send', text)
  input.value = ''
}

function onKeydown(e: KeyboardEvent) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    submit()
  }
}

watch(
  () => props.messages.length,
  async () => {
    await nextTick()
    if (scrollRef.value) {
      scrollRef.value.scrollTop = scrollRef.value.scrollHeight
    }
  },
)
</script>

<template>
  <div class="flex flex-col h-full bg-surface-subtle">
    <div
      ref="scrollRef"
      class="flex-1 min-h-0 overflow-y-auto px-4 py-6 space-y-5"
    >
      <div
        v-if="messages.length === 0 && !loading"
        class="flex flex-col items-center justify-center h-full gap-4 text-center px-4"
      >
        <div class="w-16 h-16 rounded-2xl bg-linear-to-br from-brand-50 to-brand-100 border border-brand-200 flex items-center justify-center">
          <MessageCircle class="w-8 h-8 text-brand-400" />
        </div>
        <div>
          <p class="font-semibold text-slate-700 mb-1">Ask me anything about your plan</p>
          <p class="text-sm text-slate-400 leading-relaxed max-w-xs">
            I can help with deductibles, copays, in-network providers, coverage limits, and more.
          </p>
        </div>
      </div>

      <template v-else>
        <div
          v-for="msg in messages"
          :key="msg.id"
          class="flex gap-2.5"
          :class="msg.role === 'user' ? 'justify-end' : 'justify-start'"
        >
          <div
            v-if="msg.role === 'assistant'"
            class="w-7 h-7 rounded-full bg-linear-to-br from-brand-400 to-brand-600 flex items-center justify-center shrink-0 mt-0.5"
          >
            <Sparkles class="w-3.5 h-3.5 text-white" />
          </div>

          <div
            class="max-w-[78%] rounded-2xl px-4 py-2.5 text-sm leading-relaxed whitespace-pre-wrap"
            :class="
              msg.role === 'user'
                ? 'bg-brand-500 text-white rounded-tr-sm shadow-sm'
                : 'bg-white text-slate-800 border border-slate-200 rounded-tl-sm shadow-sm'
            "
          >
            {{ msg.content }}
          </div>
        </div>

        <div v-if="loading" class="flex items-start gap-2.5">
          <div class="w-7 h-7 rounded-full bg-gradient-to-br from-brand-400 to-brand-600 flex items-center justify-center shrink-0">
            <Sparkles class="w-3.5 h-3.5 text-white" />
          </div>
          <div class="bg-white border border-slate-200 rounded-2xl rounded-tl-sm px-4 py-3 flex gap-1.5 items-center shadow-sm">
            <span
              v-for="n in 3"
              :key="n"
              class="w-1.5 h-1.5 rounded-full bg-brand-400 animate-bounce"
              :style="{ animationDelay: `${(n - 1) * 0.18}s` }"
            />
          </div>
        </div>
      </template>
    </div>

    <div
      v-if="error"
      class="mx-4 mb-2 rounded-xl border border-red-200 bg-red-50 px-4 py-2.5 text-sm text-red-700 flex items-center gap-2"
    >
      <span class="shrink-0">⚠</span>
      {{ error }}
    </div>

    <div
      class="bg-white border-t border-slate-200 px-4 py-3"
      style="box-shadow: var(--shadow-chat-input)"
    >
      <div class="flex gap-2 items-end">
        <textarea
          v-model="input"
          rows="1"
          placeholder="Ask about your plan coverage…"
          class="flex-1 resize-none rounded-xl border border-slate-200 bg-slate-50 px-4 py-2.5 text-sm text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-brand-400/40 focus:border-brand-400 transition max-h-36 leading-relaxed"
          :disabled="loading"
          @keydown="onKeydown"
        />
        <button
          :disabled="!input.trim() || loading"
          class="shrink-0 w-10 h-10 flex items-center justify-center rounded-xl bg-brand-500 hover:bg-brand-600 active:bg-brand-700 text-white transition-colors disabled:opacity-40 disabled:cursor-not-allowed focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-500 focus-visible:ring-offset-2"
          aria-label="Send message"
          @click="submit"
        >
          <Send class="w-4 h-4" />
        </button>
      </div>
      <p class="text-[10px] text-slate-400 mt-2 text-center">
        AI responses are based on your plan documents. Always verify with your insurer.
      </p>
    </div>
  </div>
</template>

