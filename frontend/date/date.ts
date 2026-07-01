// import { chatEngine } from "../engine/engine.ts";
import { gsap } from "gsap"

const chatBox  = document.getElementById("chat");
const sendBtn = document.getElementById("sendBtn");

// const chat = new chatEngine(chatBox);

if(sendBtn && chatBox) {
    sendBtn.addEventListener("click", async () => {
        // // @ts-ignore
        // const message = chatBox.value;
        // const res = await chat.generate(message);
        //
        // console.log(res);

        shiftChatElement()
        console.log("hello")
    });
}

document.getElementsByName("big-chat")[0].addEventListener("click", () => {
    shiftChatElement()
})

function shiftChatElement() {
    const chatElement = document.getElementsByName("big-chat")[0]
    let chatBox_tl = gsap.timeline();

    chatBox_tl.to(chatElement, {duration:0.5, height: "10%", width: "20%", top: "50%", ease:"power2.out"})
}