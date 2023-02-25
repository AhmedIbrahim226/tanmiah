console.log("file is loaded")

let pointFunctionTotalForms = 1;
let pointFunctionWhenElements = [];

window.onload = () => {
    pointFunctionTotalForms = document.querySelector('#id_point_functions-TOTAL_FORMS').value
    let retFunc = pointFunctionsWhenElements()
    changePointFunctionsWhenElements(retFunc)
}

document.onclick = function () {
    pointFunctionTotalForms = document.querySelector('#id_point_functions-TOTAL_FORMS').value
    pointFunctionsWhenElements()
}

let pointFunctionsWhenElements = () => {
    let passing = [];
    if (pointFunctionTotalForms !== 0) {
        for (let i = 0; i < pointFunctionTotalForms; i++) {
            passing.push(document.querySelector(`#id_point_functions-${i}-when`))
        }
    }
    pointFunctionWhenElements = passing
    valOfPointFunctionWhenElements(pointFunctionWhenElements)
    return pointFunctionWhenElements;
}

let changePointFunctionsWhenElements = (retFunc) => {
    for (const pointFunctionWhenElementsKey of pointFunctionWhenElements) {
        let splitKey = pointFunctionWhenElementsKey.id.split('-')
        let hiddenSpecificPostEl = document.querySelector(`#${splitKey[0] + '-' + splitKey[1]}-comment_on_post`)
        if (pointFunctionWhenElementsKey.value === '3'){
            hiddenSpecificPostEl.removeAttribute('hidden')
        }
    }
}

let valOfPointFunctionWhenElements = (pointFunctionWhenElements) => {
    for (const pointFunctionWhenElementsKey of pointFunctionWhenElements) {
        let splitKey = pointFunctionWhenElementsKey.id.split('-')
        let hiddenSpecificPostEl = document.querySelector(`#${splitKey[0] + '-' + splitKey[1]}-comment_on_post`)
        pointFunctionWhenElementsKey.addEventListener('change', (e) => {
            if (e.target.value === '3') {
                hiddenSpecificPostEl.removeAttribute('hidden')
            }else {
                hiddenSpecificPostEl.setAttribute('hidden', 'hidden')
            }
        })
    }
}
