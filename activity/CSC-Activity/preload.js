const { contextBridge, ipcRenderer } = require('electron')


contextBridge.exposeInMainWorld('electronAPI', {
invokeProcess: (formDataObj) => ipcRenderer.invoke('process-image', formDataObj)
})