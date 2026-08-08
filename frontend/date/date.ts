import { chatEngine } from "../engine/engine.ts";
import { gsap } from "gsap"

const chatBox = document.getElementById("chat") as HTMLTextAreaElement | null;
const sendBtn = document.getElementById("sendBtn");
const chatPreview = document.getElementById("chat-preview") as HTMLParagraphElement | null;

const chat = new chatEngine(chatBox);

let userName = "ダパン";


// document.getElementsByName("chat")[0].addEventListener("keydown", async (e) => {
//     if(e.metaKey && e.key == "Enter" && chatBox) {
//         const res = await chat.generate(chatBox.value);
//         chat.showSerif(res);
//     }
// })

document.getElementsByName("chat")[0].addEventListener("focus", () => {
    if(chat.current_speaker == "AI"){
        chat.setSpeaker("User");
        chatPreview.innerText = chatBox.value.slice(0,9) + "...";
        chatBox.value = "";
    }
})

document.getElementById("sendBtn")?.addEventListener("click", async () => {
    const res = await chat.generate(chatBox.value);
    if(res){
        chatPreview.innerText = chatBox.value.slice(0,9) + "...";
        chat.showSerif(res);
        chatBox.blur();
    }
    
})
