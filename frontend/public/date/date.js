const chatBox = document.getElementById("chat");
const dynamicChatBoxParent = document.getElementById("ui-animation-layer")
const sendBtn = document.getElementById("sendBtn");

const chat = new chatEngine("User", "",chatBox);
const messageManager = new insertMessage(chatBox, dynamicChatBoxParent)

sendBtn.addEventListener("click", async () => {
    const message = chatBox.value;
    const res = await chat.generate("User", message);

    messageManager.insert(res)
    let anime =  messageManager.beSmall(res)

    console.log(res);
});
