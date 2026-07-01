const signIn = document.querySelector("#signin")
signIn.addEventListener("submit",function(event){
    let checkbox = document.querySelector("#checkbox")
    if(!checkbox.checked){
        event.preventDefault()
        alert("請勾選同意條款")
        return
    }
    let email = document.querySelector("#signin-email").value
    let password = document.querySelector("#signin-password").value
    console.log(email,password)
})