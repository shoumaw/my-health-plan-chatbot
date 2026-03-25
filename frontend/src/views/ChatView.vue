<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'
import { useChat } from '@/composables/useChat'
import ChatInterface from '@/components/chat/ChatInterface.vue'

const route = useRoute()
const router = useRouter()

const planId = route.params.planId as string
const planName = route.query.planName as string | undefined

const { messages, loading, error, send } = useChat(planId)
</script>

<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <header class="bg-white border-b border-gray-200 shrink-0">
      <div class="max-w-3xl mx-auto px-4 sm:px-6 py-4 flex items-center gap-4">
        <button
          class="text-sm text-gray-500 hover:text-gray-800 transition"
          @click="router.back()"
        >
          ← Back
        </button>
        <h1 class="text-base font-semibold text-gray-900 truncate">
          {{ planName ?? 'Benefits Chat' }}
        </h1>
      </div>
    </header>

    <div class="flex-1 flex flex-col max-w-3xl w-full mx-auto bg-white shadow-sm">
      <ChatInterface
        :messages="messages"
        :loading="loading"
        :error="error"
        :plan-name="planName"
        class="flex-1"
        @send="send"
      />
    </div>
  </div>
</template>
