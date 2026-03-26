import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useCounterStore } from './counter'

describe('useCounterStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('initialises count at 0', () => {
    const store = useCounterStore()
    expect(store.count).toBe(0)
  })

  it('doubleCount is 0 initially', () => {
    const store = useCounterStore()
    expect(store.doubleCount).toBe(0)
  })

  it('increment increases count by 1', () => {
    const store = useCounterStore()
    store.increment()
    expect(store.count).toBe(1)
  })

  it('doubleCount always equals count × 2', () => {
    const store = useCounterStore()
    store.increment()
    store.increment()
    expect(store.doubleCount).toBe(4)
  })

  it('accumulates across multiple increment calls', () => {
    const store = useCounterStore()
    for (let i = 0; i < 5; i++) store.increment()
    expect(store.count).toBe(5)
    expect(store.doubleCount).toBe(10)
  })
})
