/* ==========================================================
   NovaAI
   Professional Emoji Picker
========================================================== */

(() => {

    const emojiBtn = document.getElementById("emoji");
    const emojiPanel = document.getElementById("emojiPanel");
    const input = document.getElementById("message");

    const emojis = [

        "😀","😁","😂","🤣","😊","😍","🥰","😘",
        "😎","🤩","🥳","🤖","👋","👍","👏","🙌",
        "💖","❤️","💜","💙","💚","💛","🧡","🖤",
        "🔥","⭐","✨","⚡","💡","🚀","🎉","🎊",
        "💻","📱","📚","📝","🎵","🎮","🌍","☕",
        "🍕","🍔","🍎","🍩","🐶","🐱","🌸","🌈"

    ];

    /* ==========================================
       BUILD EMOJI PANEL
    ========================================== */

    function buildEmojiPanel(){

        emojiPanel.innerHTML = "";

        emojis.forEach(emoji => {

            const item = document.createElement("button");

            item.className = "emoji-item";

            item.type = "button";

            item.textContent = emoji;

            item.addEventListener("click", () => {

                insertEmoji(emoji);

            });

            emojiPanel.appendChild(item);

        });

    }

    /* ==========================================
       INSERT EMOJI
    ========================================== */

    function insertEmoji(emoji){

        const start = input.selectionStart;
        const end = input.selectionEnd;

        input.value =
            input.value.substring(0, start) +
            emoji +
            input.value.substring(end);

        input.focus();

        input.selectionStart =
        input.selectionEnd =
            start + emoji.length;

        emojiPanel.classList.remove("show");

    }

    /* ==========================================
       OPEN / CLOSE PANEL
    ========================================== */

    emojiBtn.addEventListener("click", function(e){

        e.stopPropagation();

        emojiPanel.classList.toggle("show");

    });

    /* ==========================================
       CLOSE WHEN CLICKING OUTSIDE
    ========================================== */

    document.addEventListener("click", function(e){

        if(
            !emojiPanel.contains(e.target) &&
            e.target !== emojiBtn
        ){

            emojiPanel.classList.remove("show");

        }

    });

    /* ==========================================
       ESC KEY CLOSES PANEL
    ========================================== */

    document.addEventListener("keydown", function(e){

        if(e.key === "Escape"){

            emojiPanel.classList.remove("show");

        }

    });

    /* ==========================================
       INITIALIZE
    ========================================== */

    buildEmojiPanel();

})();