/* ==========================================================
   NovaAI
   Main Controller
========================================================== */

const sendBtn=document.getElementById("send");
const downloadBtn=document.getElementById("download");
const clearBtn=document.getElementById("clear");
const voiceBtn=document.getElementById("voice");
const speakerBtn=document.getElementById("speakerBtn");

sendBtn.addEventListener("click",sendMessage);
downloadBtn.addEventListener("click",downloadChat);
clearBtn.addEventListener("click",clearChat);
voiceBtn.addEventListener("click",startVoiceRecognition);
speakerBtn.addEventListener("click",toggleSpeaker);