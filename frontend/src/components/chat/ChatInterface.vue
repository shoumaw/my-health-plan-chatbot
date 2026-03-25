<script setup lang="ts">
import { ref, nextTick, watch } from 'vue'
import { Button } from '@/components/ui/button'
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
  <div class="flex flex-col h-full">
    <div v-if="planName" class="px-4 py-3 border-b border-gray-200 bg-white">
      <p class="text-sm font-medium text-gray-700">{{ planName }}</p>
    </div>

    <div
      ref="scrollRef"
      class="flex-1 overflow-y-auto px-4 py-6 space-y-4"
    >
      <div
        v-if="messages.length === 0 && !loading"
        class="flex items-center justify-center h-full text-sm text-gray-400"
      >
        Ask anything about your health plan benefits.
      </div>

      <div
        v-for="msg in messages"
        :key="msg.id"
        class="flex"
        :class="msg.role === 'user' ? 'justify-end' : 'justify-start'"
      >
        <div
          class="max-w-[75%] rounded-2xl px-4 py-2.5 text-sm leading-relaxed whitespace-pre-wrap"
          :class="
            msg.role === 'user'
              ? 'bg-primary text-primary-foreground rounded-br-sm'
              : 'bg-muted text-foreground rounded-bl-sm'
          "
        >
          {{ msg.content }}
        </div>
      </div>

      <div v-if="loading" class="flex justify-start">
        <div class="bg-muted rounded-2xl rounded-bl-sm px-4 py-3 flex gap-1 items-center">
          <span
            v-for="n in 3"
            :key="n"
            class="w-1.5 h-1.5 rounded-full bg-gray-400 animate-bounce"
            :style="{ animationDelay: `${(n - 1) * 0.15}s` }"
          />
        </div>
      </div>
    </div>

    <div
      v-if="error"
      class="mx-4 mb-2 rounded-lg border border-red-200 bg-red-50 px-4 py-2 text-sm text-red-700"
    >
      {{ error }}
    </div>

    <!-- Input area -->
    <div class="border-t border-gray-200 bg-white px-4 py-3">
      <div class="flex gap-2 items-end">
        <textarea
          v-model="input"
          rows="1"
          placeholder="Type your question…"
          class="flex-1 resize-none rounded-xl border border-gray-300 bg-gray-50 px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary transition max-h-36"
          :disabled="loading"
          @keydown="onKeydown"
        />
        <Button
          :disabled="!input.trim() || loading"
          class="shrink-0"
          @click="submit"
        >
          Send
        </Button>
      </div>
    </div>
  </div>
</template>
