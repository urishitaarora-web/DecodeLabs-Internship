const themeBtn=document.getElementById("themeBtn");

const savedTheme=localStorage.getItem("nova-theme");

if(savedTheme==="dark"){

    document.body.classList.add("dark");

    themeBtn.textContent="☀️";

}

else{

    themeBtn.textContent="🌙";

}

themeBtn.onclick=()=>{

    document.body.classList.toggle("dark");

    const dark=document.body.classList.contains("dark");

    themeBtn.textContent=dark ? "☀️" : "🌙";

    localStorage.setItem(
        "nova-theme",
        dark ? "dark" : "light"
    );

};