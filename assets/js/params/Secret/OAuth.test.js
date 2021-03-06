/* globals describe, expect, it, jest */
import React from 'react'
import OAuth from './OAuth'
import { mount } from 'enzyme'

describe('OAuth', () => {
  const wrapper = (extraProps) => {
    return mount(
      <OAuth
        name='x'
        startCreateSecret={jest.fn()}
        deleteSecret={jest.fn()}
        secretMetadata={{ name: 'a secret' }}
        secretLogic={{ service: 'google' }}
        {...extraProps}
      />
    )
  }

  it('matches snapshot', () => {
    const w = wrapper({})
    expect(w).toMatchSnapshot()
  })

  it('renders without a secret', () => {
    const w = wrapper({ secretMetadata: null })
    expect(w.find('button.connect')).toHaveLength(1)
    w.find('button.connect').simulate('click')
    expect(w.prop('startCreateSecret')).toHaveBeenCalledWith('x')
  })

  it('disconnects', () => {
    const w = wrapper({ secretMetadata: { name: 'foo@example.org' } })
    w.find('button.disconnect').simulate('click')
    expect(w.prop('deleteSecret')).toHaveBeenCalledWith('x')
  })
})
