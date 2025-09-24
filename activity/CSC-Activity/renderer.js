const serverUrl = '' // Wala pa Server


const fileInput = document.getElementById('file')
const sendBtn = document.getElementById('send')
const resultDiv = document.getElementById('result')


sendBtn.onclick = async () => {
const file = fileInput.files[0]
if (!file) { alert('Choose a file'); return }


const form = new FormData()
form.append('file', file)
const filter = document.getElementById('filter').value
if (filter) form.append('filter', filter)
const blurVal = document.getElementById('blur_ksize').value
if (blurVal) form.append('blur_ksize', blurVal)
const flip = document.getElementById('flip').value
if (flip !== '') form.append('flip', flip)
const crop = document.getElementById('crop').value
if (crop) form.append('crop', crop)


try {
const res = await fetch(serverUrl, {
method: 'POST',
body: form
})
if (!res.ok) throw new Error('Server error')
const blob = await res.blob()
const url = URL.createObjectURL(blob)
resultDiv.innerHTML = `<img src="${url}">`
} catch (err) {
alert('Error: ' + err.message)
}
}