import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import { createRouter, createWebHashHistory } from 'vue-router'
import type { Plan } from '@/composables/usePlans'
import DashboardView from './DashboardView.vue'

// ── Mock composable ─────────────────────────────────────────────────────────
vi.mock('@/composables/usePlans')
import { usePlans } from '@/composables/usePlans'
const mockedUsePlans = vi.mocked(usePlans)

// ── Stub router (DashboardView uses useRouter) ───────────────────────────────
const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    { path: '/', component: DashboardView },
    { path: '/chat/:planId', name: 'chat', component: { template: '<div/>' } },
  ],
})

const mockPlans: Plan[] = [
  { id: 'p1', name: 'Gold Plan', description: 'Best coverage', provider: 'Vitable', plan_year: 2024 },
  { id: 'p2', name: 'Silver Plan', description: 'Mid coverage', provider: 'Vitable', plan_year: 2024 },
]

function makePlansState(overrides: Partial<ReturnType<typeof usePlans>>) {
  const { ref } = require('vue')
  return {
    plans: ref<Plan[]>([]),
    loading: ref(false),
    error: ref<string | null>(null),
    fetchPlans: vi.fn(),
    ...overrides,
  }
}

describe('DashboardView', () => {
  beforeEach(async () => {
    vi.clearAllMocks()
    router.push('/')
    await router.isReady()
  })

  it('shows loading skeletons while fetching plans', () => {
    const { ref } = require('vue')
    mockedUsePlans.mockReturnValue(makePlansState({ loading: ref(true) }))
    const wrapper = mount(DashboardView, { global: { plugins: [router] } })
    expect(wrapper.findAll('.animate-pulse').length).toBeGreaterThan(0)
  })

  it('shows error message when fetchPlans fails', () => {
    const { ref } = require('vue')
    mockedUsePlans.mockReturnValue(
      makePlansState({ error: ref('Failed to load plans. Please try again.') }),
    )
    const wrapper = mount(DashboardView, { global: { plugins: [router] } })
    expect(wrapper.text()).toContain('Failed to load plans. Please try again.')
  })

  it('shows empty state when there are no plans', () => {
    mockedUsePlans.mockReturnValue(makePlansState({}))
    const wrapper = mount(DashboardView, { global: { plugins: [router] } })
    expect(wrapper.text()).toContain('No plans found')
  })

  it('renders a card for each plan', () => {
    const { ref } = require('vue')
    mockedUsePlans.mockReturnValue(makePlansState({ plans: ref(mockPlans) }))
    const wrapper = mount(DashboardView, { global: { plugins: [router] } })
    for (const plan of mockPlans) {
      expect(wrapper.text()).toContain(plan.name)
    }
  })

  it('navigates to the chat route when "Chat about this plan" is clicked', async () => {
    const { ref } = require('vue')
    mockedUsePlans.mockReturnValue(makePlansState({ plans: ref(mockPlans) }))
    const wrapper = mount(DashboardView, { global: { plugins: [router] } })
    const chatButton = wrapper.findAll('button').find((b) => b.text().includes('Chat about'))
    await chatButton!.trigger('click')
    await flushPromises()
    expect(router.currentRoute.value.name).toBe('chat')
    expect(router.currentRoute.value.params.planId).toBe(mockPlans[0].id)
  })
})
