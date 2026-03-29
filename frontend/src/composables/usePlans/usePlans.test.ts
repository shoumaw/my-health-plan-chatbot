import { describe, it, expect, vi, beforeEach } from 'vitest'
import { usePlans } from './usePlans'
import { http } from '@/services/api'

vi.mock('@/services/api', () => ({
  http: { get: vi.fn() },
}))

const mockedGet = vi.mocked(http.get)

const mockPlans = [
  { id: '1', name: 'Gold Plan', description: 'Best coverage', provider: 'Vitable Health', plan_year: 2024 },
  { id: '2', name: 'Silver Plan', description: 'Mid coverage', provider: 'Vitable Health', plan_year: 2024 },
]

describe('usePlans', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('initialises with empty plans, not loading, no error', () => {
    const { plans, loading, error } = usePlans()
    expect(plans.value).toEqual([])
    expect(loading.value).toBe(false)
    expect(error.value).toBeNull()
  })

  it('populates plans on a successful fetchPlans call', async () => {
    mockedGet.mockResolvedValue({ data: mockPlans })
    const { plans, fetchPlans } = usePlans()
    await fetchPlans()
    expect(plans.value).toEqual(mockPlans)
  })

  it('requests /v1/plans/', async () => {
    mockedGet.mockResolvedValue({ data: [] })
    const { fetchPlans } = usePlans()
    await fetchPlans()
    expect(mockedGet).toHaveBeenCalledWith('/v1/plans/')
  })

  it('sets error and keeps plans empty on failure', async () => {
    mockedGet.mockRejectedValue(new Error('Network error'))
    const { plans, error, fetchPlans } = usePlans()
    await fetchPlans()
    expect(plans.value).toEqual([])
    expect(error.value).toBe('Failed to load plans. Please try again.')
  })

  it('resets loading to false after a successful fetch', async () => {
    mockedGet.mockResolvedValue({ data: [] })
    const { loading, fetchPlans } = usePlans()
    await fetchPlans()
    expect(loading.value).toBe(false)
  })

  it('resets loading to false after a failed fetch', async () => {
    mockedGet.mockRejectedValue(new Error('fail'))
    const { loading, fetchPlans } = usePlans()
    await fetchPlans()
    expect(loading.value).toBe(false)
  })

  it('clears a previous error before each new fetch', async () => {
    mockedGet
      .mockRejectedValueOnce(new Error('oops'))
      .mockResolvedValueOnce({ data: [] })
    const { error, fetchPlans } = usePlans()
    await fetchPlans()
    expect(error.value).not.toBeNull()
    await fetchPlans()
    expect(error.value).toBeNull()
  })
})
