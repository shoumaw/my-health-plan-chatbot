import { ref } from 'vue'
import { http } from '@/services/api'

export interface Plan {
  id: string
  name: string
  description: string
  provider: string
  plan_year: number
}

export function usePlans() {
  const plans = ref<Plan[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchPlans() {
    loading.value = true
    error.value = null
    try {
      const { data } = await http.get<Plan[]>('/v1/plans/')
      plans.value = data
    } catch {
      error.value = 'Failed to load plans. Please try again.'
    } finally {
      loading.value = false
    }
  }

  return { plans, loading, error, fetchPlans }
}
