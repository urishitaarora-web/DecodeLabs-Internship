/* ==========================================================
   NovaAI
   Text-to-Speech Module
========================================================== */
/* ==========================================================
   SPEAKER SETTINGS
========================================================== */

let speechEnabled =

JSON.parse(

localStorage.getItem("nova_speaker")

?? "true"

);

let synth = window.speechSynthesis;

/* ==========================================================
   SPEAK
========================================================== */

function speak(text){

    if(!speechEnabled)
        return;

    if(!("speechSynthesis" in window))
        return;

    // Stop any previous speech
    synth.cancel();

    const utterance = new SpeechSynthesisUtterance(text);

    utterance.lang = "en-US";

    utterance.rate = 1;

    utterance.pitch = 1;

    utterance.volume = 1;

    // Try to use a female English voice if available
    const voices = synth.getVoices();

    const preferredVoice = voices.find(voice =>
        voice.lang.startsWith("en") &&
        voice.name.toLowerCase().includes("female")
    );

    if(preferredVoice){

        utterance.voice = preferredVoice;

    }

    synth.speak(utterance);

}
/* ==========================================================
   SPEAKER TOGGLE
========================================================== */

function toggleSpeaker(){

    const button = document.getElementById("speakerBtn");

    speechEnabled = !speechEnabled;
    localStorage.setItem(

    "nova_speaker",

    speechEnabled

    );

    if(speechEnabled){

        button.textContent = "🔊";

    }

    else{

        speechSynthesis.cancel();

        button.textContent = "🔇";

    }

}
window.addEventListener(

    "DOMContentLoaded",

    ()=>{

        const btn=document.getElementById("speakerBtn");

        btn.textContent=

            speechEnabled

            ? "🔊"

            : "🔇";

    }

);