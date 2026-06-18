const chatBox = document.getElementById("chat");
const sendBtn = document.getElementById("sendBtn");

const chat = new chatEngine("User", "",chatBox);

sendBtn.addEventListener("click", async () => {
    const message = chatBox.value;
    const res = await chat.generate("User", message);

    console.log(res)
});
