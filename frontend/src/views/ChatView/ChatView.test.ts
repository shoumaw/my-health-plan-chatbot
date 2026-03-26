import { describe, it, expect, vi, beforeEach } from 'vitest'
import { ref } from 'vue'
import { mount } from '@vue/test-utils'
import { createRouter, createWebHistory } from 'vue-router'
import ChatView from './ChatView.vue'
import { useChat } from '@/composables/useChat/useChat'

vi.mock('@/composables/useChat/useChat')
vi.mock('lucide-vue-next', () => ({
  ArrowLeft: { template: '<svg />' },
  HeartPulse: { template: '<svg />' },
  Sparkles: { template: '<svg />' },
}))
vi.mock('@/components/ChatInterface/ChatInterface.vue', () => ({
  default: {
    name: 'ChatInterface',
    props: ['messages', 'loading', 'error'],
    emits: ['send'],
    template: '<div data-testid="chat-interface" @click="$emit(\'send\', \'test\')" />',
  },
}))

const mockSend = vi.fn()
const mockUseChat = vi.mocked(useChat)

function makeRouter(planId = 'plan-123', planName = 'Bronze Essential') {
  const router = createRouter({
    history: createWebHistory(),
    routes: [{ path: '/chat/:planId', component: ChatView }],
  })
  router.push({ path: `/chat/${planId}`, query: { planName } })
  return router
}

beforeEach(() => {
  vi.clearAllMocks()
  mockUseChat.mockReturnValue({
    messages: ref([]),
    loading: ref(false),
    error: ref(null),
    send: mockSend,
  })
})

describe('ChatView', () => {
  it('renders the plan name from query param', async () => {
    const router = makeRouter('plan-123', 'Bronze Essential')
    await router.isReady()
    const wrapper = mount(ChatView, { global: { plugins: [router] } })
    expect(wrapper.text()).toContain('Bronze Essential')
  })

  it('falls back to "Benefits Chat" when planName query param is absent', async () => {
    const router = createRouter({
      history: createWebHistory(),
      routes: [{ path: '/chat/:planId', component: ChatView }],
    })
    router.push('/chat/plan-123')
    await router.isReady()
    const wrapper = mount(ChatView, { global: { plugins: [router] } })
    expect(wrapper.text()).toContain('Benefits Chat')
  })

  it('initialises useChat with the planId route param', async () => {
    const router = makeRouter('plan-abc', 'Silver Select')
    await router.isReady()
    mount(ChatView, { global: { plugins: [router] } })
    expect(mockUseChat).toHaveBeenCalledWith('plan-abc')
  })

  it('navigates back when the back button is clicked', async () => {
    const router = makeRouter()
    await router.isReady()
    const backSpy = vi.spyOn(router, 'back')
    const wrapper = mount(ChatView, { global: { plugins: [router] } })
    await wrapper.find('button[aria-label="Go back"]').trigger('click')
    expect(backSpy).toHaveBeenCalled()
  })

  it('forwards the send event from ChatInterface to useChat.send', async () => {
    const router = makeRouter()
    await router.isReady()
    const wrapper = mount(ChatView, { global: { plugins: [router] } })
    await wrapper.find('[data-testid="chat-interface"]').trigger('click')
    expect(mockSend).toHaveBeenCalledWith('test')
  })
})
