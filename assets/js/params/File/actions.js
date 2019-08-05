const FILE_UPLOAD = 'FILE_UPLOAD'
const FILE_UPLOAD_CANCEL = 'FILE_UPLOAD_CANCEL'
const FILE_UPLOAD_PROGRESS = 'FILE_UPLOAD_PROGRESS'
const API_TOKEN_NO_OP = 'API_TOKEN_NO_OP'

/**
 * Begin uploading the File in question.
 *
 * File docs: https://developer.mozilla.org/en-US/docs/Web/API/File
 */
export function upload (wfModuleId, file) {
  return (dispatch, getState, api) => {
    const onProgress = (nBytesUploaded) => dispatch(setProgress(wfModuleId, nBytesUploaded))
    return dispatch({
      type: FILE_UPLOAD,
      payload: {
        // `api.uploadFile` will never error. At worst, it will retry indefinitely.
        promise: api.uploadFile(wfModuleId, file, onProgress)
          .then(result => ({
            wfModuleId,
            uuid: result === null ? null : result.uuid
          })),
        data: { wfModuleId, name: file.name, size: file.size }
      }
    })
  }
}

/**
 * Modify wfModule.inProgressUpload in `state`.
 */
function updateWfModuleInProgressFileUpload (state, wfModuleId, updateOrNull) {
  const { wfModules } = state
  const wfModule = wfModules[String(wfModuleId)]
  return {
    ...state,
    wfModules: {
      ...wfModules,
      [wfModuleId]: {
        ...wfModule,
        inProgressUpload: updateOrNull === null ? null : {
          ...(wfModule.inProgressUpload || {}),
          ...updateOrNull
        }
      }
    }
  }
}

function reduceUploadPending (state, action) {
  const { wfModuleId, name, size } = action.payload
  // `nBytesUploaded === null` will render as an "indeterminate" progressbar.
  return updateWfModuleInProgressFileUpload(state, wfModuleId, { name, size, nBytesUploaded: null })
}

function reduceUploadFulfilled (state, action) {
  const { wfModuleId } = action.payload
  return updateWfModuleInProgressFileUpload(state, wfModuleId, null)
}

/**
 * Cancel any upload on `wfModule`.
 */
export function cancel (wfModuleId) {
  return (dispatch, getState, api) => {
    const hasUpload = !!getState().wfModules[String(wfModuleId)].inProgressUpload
    return dispatch({
      type: FILE_UPLOAD_CANCEL,
      payload: {
        promise: (hasUpload ? api.cancelFileUpload(wfModuleId) : Promise.resolve(null)).then(() => ({ wfModuleId })),
        data: { wfModuleId }
      }
    })
  }
}

function reduceCancelPending (state, action) {
  const { wfModuleId } = action.payload
  // `nBytesUploaded === null` will render as an "indeterminate" progressbar.
  return updateWfModuleInProgressFileUpload(state, wfModuleId, { nBytesUploaded: null })
}

function reduceCancelFulfilled (state, action) {
  const { wfModuleId } = action.payload
  return updateWfModuleInProgressFileUpload(state, wfModuleId, null)
}

/**
 * Mark a File upload as progressing.
 */
export function setProgress (wfModuleId, nBytesUploaded) {
  return {
    type: FILE_UPLOAD_PROGRESS,
    payload: { wfModuleId, nBytesUploaded }
  }
}

function reduceSetProgress (state, action) {
  const { wfModuleId, nBytesUploaded } = action.payload
  return updateWfModuleInProgressFileUpload(state, wfModuleId, { nBytesUploaded })
}

/**
 * Call API method to get API token.
 *
 * API token is not stored in Redux state because Redux state is the same for
 * all users, even users without write permission.
 *
 * Return a url-safe string.
 */
export function getApiToken (wfModuleId) {
  return (dispatch, getState, api) => {
    return dispatch({
      type: API_TOKEN_NO_OP,
      payload: {
        promise: api.getWfModuleFileUploadApiToken(wfModuleId)
      }
    })
  }
}

/**
 * Call API method to set a new API token.
 *
 * API token is not stored in Redux state because Redux state is the same for
 * all users, even users without write permission.
 *
 * Return a url-safe string.
 */
export function resetApiToken (wfModuleId) {
  return (dispatch, getState, api) => {
    return dispatch({
      type: API_TOKEN_NO_OP,
      payload: {
        promise: api.resetWfModuleFileUploadApiToken(wfModuleId)
      }
    })
  }
}

/**
 * Call API method to disallow API file uploads.
 *
 * API token is not stored in Redux state because Redux state is the same for
 * all users, even users without write permission.
 */
export function clearApiToken (wfModuleId) {
  return (dispatch, getState, api) => {
    return dispatch({
      type: API_TOKEN_NO_OP,
      payload: {
        promise: api.clearWfModuleFileUploadApiToken(wfModuleId)
      }
    })
  }
}

export const reducerFunctions = {
  [FILE_UPLOAD + '_PENDING']: reduceUploadPending,
  [FILE_UPLOAD + '_FULFILLED']: reduceUploadFulfilled,
  [FILE_UPLOAD_CANCEL + '_PENDING']: reduceCancelPending,
  [FILE_UPLOAD_CANCEL + '_FULFILLED']: reduceCancelFulfilled,
  [FILE_UPLOAD_PROGRESS]: reduceSetProgress
  // No reducers for API_TOKEN_NO_OP -- state doesn't change.
}
