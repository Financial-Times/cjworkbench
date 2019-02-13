import React from 'react'
import PropTypes from 'prop-types'
import Multicolumn from '../Multicolumn'

export default class JoinColumns extends React.PureComponent {
  static propTypes = {
    isReadOnly: PropTypes.bool.isRequired,
    onChange: PropTypes.func.isRequired, // func({ on: '...', right: '...' }) => undefined
    fieldId: PropTypes.string.isRequired, // <input id=...>
    name: PropTypes.string.isRequired, // <input name=...>
    label: PropTypes.string.isRequired,
    value: PropTypes.shape({
      on: PropTypes.string.isRequired, // column list
      right: PropTypes.string.isRequired // column list
    }).isRequired,
    inputColumns: PropTypes.arrayOf(PropTypes.shape({
      name: PropTypes.string.isRequired,
      type: PropTypes.oneOf([ 'text', 'number', 'datetime' ]).isRequired
    }).isRequired),
    tabs: PropTypes.arrayOf(PropTypes.shape({
      slug: PropTypes.string.isRequired,
      name: PropTypes.string.isRequired,
      outputColumns: PropTypes.arrayOf(PropTypes.shape({
        name: PropTypes.string.isRequired,
        type: PropTypes.oneOf([ 'text', 'number', 'datetime' ]).isRequired
      }).isRequired) // null while rendering
    }).isRequired).isRequired,
    selectedTab: PropTypes.string.isRequired // slug, may be ''
  }

  onChangeOn = (colnames) => {
    const { onChange, value } = this.props
    onChange({
      ...value,
      on: colnames
    })
  }

  onChangeRight = (colnames) => {
    const { onChange, value } = this.props
    onChange({
      ...value,
      right: colnames
    })
  }

  render () {
    const { isReadOnly, name, label, value, inputColumns, fieldId, tabs, selectedTab } = this.props
    const rightTab = tabs.find(({ slug }) => selectedTab === slug)

    const inputColnames = (inputColumns || []).map(({ name }) => name)

    // Empty/rendering tab? Empty options
    const rightColumns = rightTab && rightTab.outputColumns || []
    const bothColumns = rightColumns.filter(({ name }) => inputColnames.includes(name))

    return (
      <React.Fragment>
        <Multicolumn
          isReadOnly={isReadOnly}
          name={`${name}[on]`}
          fieldId={`${fieldId}_on`}
          onChange={this.onChangeOn}
          label='Join on'
          inputColumns={bothColumns}
          value={value.on}
        />
        <Multicolumn
          isReadOnly={isReadOnly}
          name={`${name}[right]`}
          fieldId={`${fieldId}_right`}
          onChange={this.onChangeRight}
          label='Add columns'
          inputColumns={rightColumns}
          value={value.right}
        />
      </React.Fragment>
    )
  }
}
