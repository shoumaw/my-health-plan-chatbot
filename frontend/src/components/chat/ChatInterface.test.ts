import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import ChatInterface from './ChatInterface.vue'
import type { ChatMessage } from './types'

const userMsg: ChatMessage = { id: '1', role: 'user', content: 'What is my deductible?' }
const assistantMsg: ChatMessage = { id: '2', role: 'assistant', content: 'Your deductible is $500.' }

describe('ChatInterface', () => {
  it('renders user messages on the right', () => {
    const wrapper = mount(ChatInterface, {
      props: { messages: [userMsg] },
    })
    expect(wrapper.html()).toContain('What is my deductible?')
    const row = wrapper.find('.justify-end')
    expect(row.exists()).toBe(true)
    expect(row.text()).toContain('What is my deductible?')
  })

  it('renders assistant messages on the left', () => {
    const wrapper = mount(ChatInterface, {
      props: { messages: [assistantMsg] },
    })
    expect(wrapper.html()).toContain('Your deductible is $500.')
    const row = wrapper.find('.justify-start')
    expect(row.exists()).toBe(true)
    expect(row.text()).toContain('Your deductible is $500.')
  })

  it('emits send with the input text when Send is clicked', async () => {
    const wrapper = mount(ChatInterface, { props: { messages: [] } })
    const textarea = wrapper.find('textarea')
    await textarea.setValue('Hello')
    await wrapper.find('button').trigger('click')
    expect(wrapper.emitted('send')).toEqual([['Hello']])
  })

  it('emits send when Enter is pressed (without Shift)', async () => {
    const wrapper = mount(ChatInterface, { props: { messages: [] } })
    const textarea = wrapper.find('textarea')
    await textarea.setValue('Enter test')
    await textarea.trigger('keydown', { key: 'Enter', shiftKey: false })
    expect(wrapper.emitted('send')).toEqual([['Enter test']])
  })

  it('does not emit send on Shift+Enter', async () => {
    const wrapper = mount(ChatInterface, { props: { messages: [] } })
    const textarea = wrapper.find('textarea')
    await textarea.setValue('Multiline')
    await textarea.trigger('keydown', { key: 'Enter', shiftKey: true })
    expect(wrapper.emitted('send')).toBeUndefined()
  })

  it('disables the Send button when input is empty', async () => {
    const wrapper = mount(ChatInterface, { props: { messages: [] } })
    const btn = wrapper.find('button')
    expect(btn.attributes('disabled')).toBeDefined()
  })

  it('disables textarea and button while loading', async () => {
    const wrapper = mount(ChatInterface, { props: { messages: [], loading: true } })
    expect(wrapper.find('textarea').attributes('disabled')).toBeDefined()
    expect(wrapper.find('button').attributes('disabled')).toBeDefined()
  })

  it('shows error banner when error prop is set', () => {
    const wrapper = mount(ChatInterface, {
      props: { messages: [], error: 'Something went wrong.' },
    })
    expect(wrapper.html()).toContain('Something went wrong.')
  })

  it('shows typing indicator while loading', () => {
    const wrapper = mount(ChatInterface, { props: { messages: [], loading: true } })
    // Three bounce dots are rendered
    expect(wrapper.findAll('.animate-bounce').length).toBe(3)
  })

  it('shows empty state when there are no messages', () => {
    const wrapper = mount(ChatInterface, { props: { messages: [] } })
    expect(wrapper.html()).toContain('Ask me anything about your plan')
  })

  it('clears input after send', async () => {
    const wrapper = mount(ChatInterface, { props: { messages: [] } })
    const textarea = wrapper.find('textarea')
    await textarea.setValue('Clear me')
    await wrapper.find('button').trigger('click')
    expect((textarea.element as HTMLTextAreaElement).value).toBe('')
  })
})
