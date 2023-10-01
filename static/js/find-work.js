const updateActs = () => {
    let child = document.getElementById("acts").children;
    console.log(child)
    for (let i=0; i<child.length;i++) {
        if (child[i].dataset.type === selected) {
            child[i].classList.remove("none")
        } else {
            child[i].classList.add("none")
        }
    }
}

let selected = document.getElementById("select").value
console.log(selected)
updateActs()

document.getElementById("select").onchange = (event) => {
    selected = event.target.value
    updateActs()
    console.log(selected)
}