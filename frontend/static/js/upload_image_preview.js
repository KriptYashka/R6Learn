function preview(input) {
    console.log("Вроде должно работать");
    frame.src = URL.createObjectURL(input.files[0]);
}

function clearImage() {
    document.getElementById('formFile').value = null;
    frame.src = "";
}