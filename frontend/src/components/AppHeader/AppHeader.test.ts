import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import AppHeader from './AppHeader.vue'

describe('AppHeader', () => {
  it('renders the Vitable Health brand name', () => {
    const wrapper = mount(AppHeader)
    expect(wrapper.text()).toContain('Vitable Health')
  })

  it('renders subtitle when the prop is provided', () => {
    const wrapper = mount(AppHeader, { props: { subtitle: 'Benefits Portal' } })
    expect(wrapper.text()).toContain('Benefits Portal')
  })

  it('does not render the subtitle element when the prop is absent', () => {
    const wrapper = mount(AppHeader)
    const subtitle = wrapper.find('p.text-\\[10px\\]')
    expect(subtitle.exists()).toBe(false)
  })

  it('renders default slot content', () => {
    const wrapper = mount(AppHeader, {
      slots: { default: '<span data-testid="slot">User Name</span>' },
    })
    expect(wrapper.html()).toContain('User Name')
  })
})
