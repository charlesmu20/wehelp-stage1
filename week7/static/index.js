const signUp = document.querySelector("#signup");
signUp.addEventListener("submit",function(e){
    let name = document.querySelector("#signup-name").value.trim();
    let email = document.querySelector("#signup-email").value.trim();
    let password = document.querySelector("#signup-password").value.trim();
    if(name === "" || email === "" || password === ""){
        e.preventDefault();
        return
    }
})

const login = document.querySelector("#signin");
login.addEventListener("submit",function(e){
    let email = document.querySelector("#signin-email").value.trim();
    let password = document.querySelector("#signin-password").value.trim();
    if(email === "" || password === ""){
        e.preventDefault();
        return
    }
})
