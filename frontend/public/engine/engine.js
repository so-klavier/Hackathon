class chatEngine {
    constructor(talking, firstSerif, serifElement) {
        this.currentTalking = talking; //value will be User or AI
        this.aiStatus;
        this.currentSerif = firstSerif;
        this.serifBox = serifElement;
    }

    async generate(speaker, serif) {
        console.log(speaker);
        console.log(serif);
        this.currentSerif = serif;
        this.currentTalking = speaker;
        if (serif.trim() !== "") {
            const response = await fetch("http://127.0.0.1:5002/message", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ message: serif }),
            });

            const data = await response.json();
            this.currentSerif = data.response;
            console.log(data);
            return data.response;
        }
        return null;
    }
}

class insertMessage {
    constructor(chatBox, dynamicChatBoxParent) {
        this.chatBox = chatBox;
        this.dynamicChatBoxParent = dynamicChatBoxParent;
    }

    insert(message) {
        this.dynamicChatBoxParent.lastElementChild.innerHTML = message;
        this.chatBox.value = "";
    }

    async beSmall() {
        const elementTemp = this.dynamicChatBoxParent.lastElementChild.outerHTML;
        console.log(this.dynamicChatBoxParent.firstElementChild);
        this.dynamicChatBoxParent.firstElementChild.remove();

        this.dynamicChatBoxParent.lastElementChild.classList.remove("big-chat");
        this.dynamicChatBoxParent.lastElementChild.classList.add("small-chat");
        this.dynamicChatBoxParent.lastElementChild.classList.add("get-small");

        await new Promise(resolve => setTimeout(resolve, 1000));

        this.dynamicChatBoxParent.firstElementChild.classList.remove("get-small")
        this.dynamicChatBoxParent.innerHTML += elementTemp

        return true;
    }
}
