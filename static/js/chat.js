/* ==========================================================
   NovaAI
   Chat Engine
========================================================== */

const chatArea = document.getElementById("chatArea");
const messageInput = document.getElementById("message");

const STORAGE_KEY = "nova_chat_history";

let chatHistory = [];

/* ==========================================================
   LOAD HISTORY ON START
========================================================== */

window.addEventListener("DOMContentLoaded", () => {

    loadHistory();

});

/* ==========================================================
   SAVE HISTORY
========================================================== */

function saveHistory(){

    localStorage.setItem(
        STORAGE_KEY,
        JSON.stringify(chatHistory)
    );

}

/* ==========================================================
   LOAD HISTORY
========================================================== */

function loadHistory(){

    const saved = localStorage.getItem(STORAGE_KEY);

    if(!saved){

        chatArea.innerHTML = `

            <div class="bot">

                <img src="/static/images/nova-avatar.png">

                <div class="bubble">

                    <h3>Hello 👋</h3>

                    <p>

                        I'm NovaAI.

                        How can I help you today?

                    </p>

                    <div class="message-footer">

                        <span class="time">

                            ${getCurrentTime()}

                        </span>

                    </div>

                </div>

            </div>

        `;

        return;

    }

    chatHistory = JSON.parse(saved);

    chatArea.innerHTML = "";

    chatHistory.forEach(message=>{

        if(message.sender==="user"){

            createUserMessage(message.text);

        }

        else{

            createBotMessage(message.text);

        }

    });

    scrollBottom();

}

/* ==========================================================
   CURRENT TIME
========================================================== */

function getCurrentTime(){

    return new Date().toLocaleTimeString([],{

        hour:"2-digit",

        minute:"2-digit"

    });

}

/* ==========================================================
   USER MESSAGE
========================================================== */

function createUserMessage(text){

    const div = document.createElement("div");

    div.className = "user";

    div.innerHTML = `

        <div class="bubble">

            <p>${text}</p>

            <div class="message-footer">

                <span class="time">

                    ${getCurrentTime()}

                </span>

            </div>

        </div>

    `;

    chatArea.appendChild(div);

}

/* ==========================================================
   BOT MESSAGE
========================================================== */

function createBotMessage(text){

    const div = document.createElement("div");

    div.className = "bot";

    div.innerHTML = `

        <img src="/static/images/nova-avatar.png">

        <div class="bubble">

            <p>${text}</p>

            <div class="message-footer">

                <button class="copy-btn">

                    <i class="fa-regular fa-copy"></i>

                </button>

                <span class="time">

                    ${getCurrentTime()}

                </span>

            </div>

        </div>

    `;

    chatArea.appendChild(div);

    const copyButton = div.querySelector(".copy-btn");

    copyButton.addEventListener("click", async()=>{

        try{

            await navigator.clipboard.writeText(text);

            copyButton.innerHTML =
                '<i class="fa-solid fa-check"></i>';

            setTimeout(()=>{

                copyButton.innerHTML =
                    '<i class="fa-regular fa-copy"></i>';

            },2000);

        }

        catch{

            alert("Unable to copy text.");

        }

    });

}

/* ==========================================================
   SCROLL
========================================================== */

function scrollBottom(){

    chatArea.scrollTop = chatArea.scrollHeight;

}

/* ==========================================================
   SEND MESSAGE
========================================================== */

async function sendMessage(){

    if(window.speechSynthesis){

        speechSynthesis.cancel();

    }

    const text = messageInput.value.trim();

    if(text==="") return;
    const sendBtn = document.getElementById("send");
    const voiceBtn = document.getElementById("voice");

    sendBtn.disabled = true;
    voiceBtn.disabled = true;
    sendBtn.innerHTML = `
    <i class="fa-solid fa-spinner fa-spin"></i>
    `;

    createUserMessage(text);

    chatHistory.push({

        sender:"user",

        text:text

    });

    saveHistory();

    scrollBottom();

    messageInput.value = "";

    showTyping();

    try{

        const response = await fetch("/chat",{

            method:"POST",

            headers:{

                "Content-Type":"application/json"

            },

            body:JSON.stringify({

                message:text

            })

        });

        const data = await response.json();

        hideTyping();

        sendBtn.disabled = false;
        voiceBtn.disabled = false;

        sendBtn.innerHTML = `
        <i class="fa-solid fa-paper-plane"></i>
        `;

        createBotMessage(data.reply);

        if(typeof speak==="function"){

            speak(data.reply);

        }

        chatHistory.push({

            sender:"bot",

            text:data.reply

        });

        saveHistory();

        scrollBottom();

    }

    catch(error){

        hideTyping();

        createBotMessage("⚠ Unable to connect to NovaAI.");
        sendBtn.disabled = false;
        voiceBtn.disabled = false;

        sendBtn.innerHTML = `
        <i class="fa-solid fa-paper-plane"></i>
        `;

    }

}
/* ==========================================================
   TYPING INDICATOR
========================================================== */

function showTyping(){

    document.getElementById("typing").style.display = "flex";

    scrollBottom();

}

function hideTyping(){

    document.getElementById("typing").style.display = "none";

}

/* ==========================================================
   ENTER KEY
========================================================== */

messageInput.addEventListener("keydown",(e)=>{

    if(e.key==="Enter"){

        e.preventDefault();

        sendMessage();

    }

});

/* ==========================================================
   DOWNLOAD CHAT
========================================================== */

function downloadChat(){

    if(chatHistory.length===0){

        alert("No conversation to download.");

        return;

    }

    let content="";

    content+="=========================================\n";
    content+="          NovaAI Conversation\n";
    content+="=========================================\n\n";

    chatHistory.forEach(message=>{

        if(message.sender==="user"){

            content+="You:\n";

        }

        else{

            content+="NovaAI:\n";

        }

        content+=message.text+"\n\n";

    });

    content+="=========================================\n";
    content+="Generated by NovaAI\n";
    content+="=========================================\n";

    const blob = new Blob([content],{

        type:"text/plain"

    });

    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");

    a.href = url;

    a.download = "NovaAI_Chat.txt";

    document.body.appendChild(a);

    a.click();

    a.remove();

    URL.revokeObjectURL(url);

}

/* ==========================================================
   CLEAR CHAT
========================================================== */

function clearChat(){

    if(!confirm("Are you sure you want to clear the conversation?")){

        return;

    }

    chatHistory=[];

    localStorage.removeItem(STORAGE_KEY);

    chatArea.innerHTML=`

        <div class="bot">

            <img src="/static/images/nova-avatar.png">

            <div class="bubble">

                <h3>Hello 👋</h3>

                <p>

                    I'm NovaAI.

                    How can I help you today?

                </p>

                <div class="message-footer">

                    <span class="time">

                        ${getCurrentTime()}

                    </span>

                </div>

            </div>

        </div>

    `;

    scrollBottom();

}

/* ==========================================================
   VOICE RECOGNITION
========================================================== */

const SpeechRecognition =
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;

let recognition = null;

if(SpeechRecognition){

    recognition = new SpeechRecognition();

    recognition.lang = "en-US";

    recognition.continuous = false;

    recognition.interimResults = false;

}

function startVoiceRecognition(){

    if(!recognition){

        alert("Speech Recognition is not supported in this browser.");

        return;

    }

    const voiceBtn = document.getElementById("voice");

    voiceBtn.classList.add("listening");

    recognition.start();

    recognition.onresult = function(event){

        const transcript = event.results[0][0].transcript;

        messageInput.value = transcript;

        voiceBtn.classList.remove("listening");

        sendMessage();

    };

    recognition.onerror = function(){

        voiceBtn.classList.remove("listening");

    };

    recognition.onend = function(){

        voiceBtn.classList.remove("listening");

    };

}

/* ==========================================================
   BUTTON EVENTS
========================================================== */

document.getElementById("send").addEventListener(

    "click",

    sendMessage

);

document.getElementById("voice").addEventListener(

    "click",

    startVoiceRecognition

);

document.getElementById("download").addEventListener(

    "click",

    downloadChat

);

document.getElementById("clear").addEventListener(

    "click",

    clearChat

);

/* ==========================================================
   AUTO SCROLL
========================================================== */

const observer = new MutationObserver(()=>{

    scrollBottom();

});

observer.observe(chatArea,{

    childList:true,

    subtree:true

});

/* ==========================================================
   WINDOW FOCUS
========================================================== */

window.addEventListener("focus",()=>{

    scrollBottom();

});
