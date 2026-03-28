import { ref } from 'vue'
import { http } from '@/services/api'
import type { ChatMessage } from '@/components/ChatInterface/types'

export function useChat(planId: string) {
  const messages = ref<ChatMessage[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function send(message: string) {
    messages.value.push({
      id: crypto.randomUUID(),
      role: 'user',
      content: message,
    })

    loading.value = true
    error.value = null

    try {
      const history = messages.value
        .slice(0, -1)
        .map(m => ({ role: m.role, content: m.content }))

      const { data } = await http.post<{ reply: string }>('/chat/', {
        message,
        plan_id: planId,
        history,
      })

      messages.value.push({
        id: crypto.randomUUID(),
        role: 'assistant',
        content: data.reply,
      })
    } catch {
      error.value = 'Something went wrong. Please try again.'
    } finally {
      loading.value = false
    }
  }

  return { messages, loading, error, send }
}
