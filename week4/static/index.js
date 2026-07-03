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
function getHotel(){
    //判斷輸入的ID是不是正整數
    let IdInput = document.querySelector("#id-input").value;
    let id = Number(IdInput);
    if (id<=0 || !Number.isInteger(id) || isNaN(id)){
        alert("請輸入正整數")
        return
    }
    window.location.href = `/hotel/${id}`;
}