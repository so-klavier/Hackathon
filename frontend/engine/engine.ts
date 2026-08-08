// import { gsap } from "gsap"

export class chatEngine {
    private aiStatus: any;
    private serifBox: any;
    public current_speaker: string;
    private speakerNameBox: any;

    constructor(serifElement: any) {
        this.aiStatus;
        this.serifBox = serifElement;
        this.speakerNameBox = document.getElementById("speaker-name");
        this.current_speaker = "User";
    }

    async generate(serif: string) {
        if (serif.trim() !== "" && this.current_speaker == "User") {
            this.setSpeaker("AI");
            const response = await fetch("http://127.0.0.1:8000/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ message: serif }),
            });

            const data = await response.json();
            return data.response;
        }
        return null;
    }

    setSpeaker(s: string) {
        this.speakerNameBox.innerText = "| " + s + " |";
        this.current_speaker = s;
        return true
    }

    showSerif(s: string) {
        this.serifBox.value = s;
        this.setSpeaker("AI");
        return true
    }
}


// document.getElementsByName("big-chat")[0].addEventListener("click", () => {
//     shiftChatElement()
// })

// function shiftChatElement() {
//     const chatElement = document.getElementsByName("big-chat")[0]
//     let chatBox_tl = gsap.timeline();

//     chatBox_tl.to(chatElement, {height: "10vh", width: "20vw", top: "50vh", ease:"power2.out"})
// }