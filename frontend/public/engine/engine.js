class chatEngine {
    constructor(talking, firstSerif, serifElement) {
        this.currentTalking = talking; //value will be User or AI
        this.aiStatus;
        this.currentSerif = firstSerif;
        this.serifBox = serifElement;
    }

    set serif(s) {
        this.currentSerif = s;
        this.serifBox.value = s;
    }

    set speaker(s) {
        this.currentTalking = s;
    }

    async generate(speaker, serif) {
        this.serif = serif;
        this.speaker = speaker;
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
            return data;
        }
        return null;
    }
}
