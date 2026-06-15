const chat = document.getElementById('chat');
const sendBtn = document.getElementById('sendBtn');

sendBtn.addEventListener('click', () => {
    const message = chat.value;
    if (message.trim() !== '') {
        fetch('http://127.0.0.1:8000/chat',{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        }).then(response => response.json())
          .then(data => {
              console.log('サーバーからの応答:', data);
          })
          .catch(error => {
              console.error('エラー:', error);
          });


        console.log('送信されたメッセージ:', message);
        chat.value = ''; // メッセージ送信後にテキストエリアをクリア
    }
})