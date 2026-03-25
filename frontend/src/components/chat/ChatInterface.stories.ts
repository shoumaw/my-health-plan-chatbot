import type { Meta, StoryObj } from '@storybook/vue3'
import ChatInterface from './ChatInterface.vue'
import type { ChatMessage } from './types'

type ChatInterfaceArgs = {
  messages: ChatMessage[]
  loading?: boolean
  error?: string | null
  planName?: string
}

const meta: Meta<ChatInterfaceArgs> = {
  title: 'Chat/ChatInterface',
  component: ChatInterface,
  parameters: {
    layout: 'fullscreen',
  },
}

export default meta
type Story = StoryObj<ChatInterfaceArgs>

const conversation: ChatMessage[] = [
  { id: '1', role: 'user', content: 'What is my deductible for in-network care?' },
  {
    id: '2',
    role: 'assistant',
    content:
      'Based on your Silver Select plan, your in-network deductible is $1,500 for an individual and $3,000 for a family per plan year.',
  },
  { id: '3', role: 'user', content: 'Does it cover mental health visits?' },
  {
    id: '4',
    role: 'assistant',
    content:
      'Yes! Mental health outpatient visits are covered at the same cost-sharing as primary care. You pay a $30 copay per visit after your deductible is met.',
  },
]

export const Empty: Story = {
  args: {
    messages: [],
    planName: 'Silver Select — Aetna',
  },
}

export const WithConversation: Story = {
  args: {
    messages: conversation,
    planName: 'Silver Select — Aetna',
  },
}

export const Loading: Story = {
  args: {
    messages: conversation,
    loading: true,
    planName: 'Silver Select — Aetna',
  },
}

export const WithError: Story = {
  args: {
    messages: conversation,
    error: 'Something went wrong. Please try again.',
    planName: 'Silver Select — Aetna',
  },
}
