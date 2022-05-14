
const imageForm = document.querySelector("#imageForm")
const imageInput = document.querySelector("#imageInput")

imageForm.addEventListener("submit", async event => {
  event.preventDefault()
  const image = imageInput.files[0]

  const formData = new FormData();
  formData.append("image", image)


  await fetch('http://127.0.0.1:8080/predict', {
    method: "PUT",
    body: formData
  })


})