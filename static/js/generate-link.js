let btn = document.getElementById("make-invite")
btn.onclick = async (e) => {
    e = e || window.event
    let targ = e.target || e.srcElement
    console.log(targ.dataset.unique)
    try {
        await navigator.clipboard.writeText(`${window.location.protocol}//${window.location.host}/user/registration/${targ.dataset.unique}`)
    } catch (err) {
        console.error('Failed to copy: ', err)
    }
}