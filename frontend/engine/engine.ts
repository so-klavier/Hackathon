import { gsap } from "gsap"

export class chatEngine {
    private aiStatus: any;
    private serifBox: any;

    constructor(serifElement: any) {
        this.aiStatus;
        this.serifBox = serifElement;
    }

    set serif(s: any) {
        this.serifBox.value = s;
    }

    async generate(serif: string) {
        this.serif = serif;
        if (serif.trim() !== "") {
            const response = await fetch("http://127.0.0.1:5002/message", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ message: serif }),
            });

            const data = await response.json();
            this.serif = data.response;
            return data.response;
        }
        return null;
    }
}


document.getElementsByName("big-chat")[0].addEventListener("click", () => {
    shiftChatElement()
})

function shiftChatElement() {
    const chatElement = document.getElementsByName("big-chat")[0]
    let chatBox_tl = gsap.timeline();

    chatBox_tl.to(chatElement, {height: "10vh", width: "20vw", top: "50vh", ease:"power2.out"})
}