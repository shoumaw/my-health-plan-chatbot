import { describe, it, expect, vi, beforeEach } from 'vitest'
import { useChat } from './useChat'
import { http } from '@/services/api'

vi.mock('@/services/api', () => ({
  http: { post: vi.fn() },
}))

const mockedPost = vi.mocked(http.post)

describe('useChat', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('initialises with empty messages, not loading, no error', () => {
    const { messages, loading, error } = useChat('plan-1')
    expect(messages.value).toEqual([])
    expect(loading.value).toBe(false)
    expect(error.value).toBeNull()
  })

  it('adds user message immediately on send (before await)', () => {
    mockedPost.mockResolvedValue({ data: { reply: 'Hello!' } })
    const { messages, send } = useChat('plan-1')
    const p = send('Hi there')
    expect(messages.value[0].role).toBe('user')
    expect(messages.value[0].content).toBe('Hi there')
    return p
  })

  it('appends assistant reply after successful API call', async () => {
    mockedPost.mockResolvedValue({ data: { reply: 'Your deductible is $500.' } })
    const { messages, send } = useChat('plan-1')
    await send('What is my deductible?')
    expect(messages.value).toHaveLength(2)
    expect(messages.value[1].role).toBe('assistant')
    expect(messages.value[1].content).toBe('Your deductible is $500.')
  })

  it('posts to /chat/ with the message and plan_id', async () => {
    mockedPost.mockResolvedValue({ data: { reply: 'ok' } })
    const { send } = useChat('plan-abc')
    await send('test message')
    expect(mockedPost).toHaveBeenCalledWith('/chat/', {
      message: 'test message',
      plan_id: 'plan-abc',
    })
  })

  it('sets error and keeps only the user message on API failure', async () => {
    mockedPost.mockRejectedValue(new Error('Network error'))
    const { messages, error, send } = useChat('plan-1')
    await send('test')
    expect(messages.value).toHaveLength(1)
    expect(error.value).toBe('Something went wrong. Please try again.')
  })

  it('resets loading to false after a successful call', async () => {
    mockedPost.mockResolvedValue({ data: { reply: 'ok' } })
    const { loading, send } = useChat('plan-1')
    await send('test')
    expect(loading.value).toBe(false)
  })

  it('resets loading to false after a failed call', async () => {
    mockedPost.mockRejectedValue(new Error('fail'))
    const { loading, send } = useChat('plan-1')
    await send('test')
    expect(loading.value).toBe(false)
  })

  it('clears the previous error before each new send', async () => {
    mockedPost
      .mockRejectedValueOnce(new Error('oops'))
      .mockResolvedValueOnce({ data: { reply: 'ok' } })
    const { error, send } = useChat('plan-1')
    await send('first')
    expect(error.value).not.toBeNull()
    await send('second')
    expect(error.value).toBeNull()
  })
})
