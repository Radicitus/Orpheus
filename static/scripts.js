function increaseBPM() {
    let old = document.getElementById("bpm").value
    document.getElementById("bpm").value = Number(old) + 1
}

function decreaseBPM() {
    let old = document.getElementById("bpm").value
    document.getElementById("bpm").value = Number(old) - 1
}