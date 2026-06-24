package main

import (
	"bytes"
	"io"
	"net/http"
	"time"
)

func callapi(url string, bodyBytes []byte) ([]byte, error) {
	// 1. HTTPクライアントの作成（タイムアウトを設定するのが安全です）
	client := &http.Client{
		Timeout: 300 * time.Second,
	}

	// 2. 外部APIへのGETリクエストを作成（例としてテスト用のパブリックAPIを使用）
	externalAPIURL := "http://127.0.0.1:8000/chat"
	req, err := http.NewRequest("POST", externalAPIURL, bytes.NewBuffer(bodyBytes))
	if err != nil {
		return []byte(`{"error": "リクエストの作成に失敗しました"}`), err
	}

	// (任意) ヘッダーの追加が必要な場合はここで行います
	req.Header.Add("Authorization", "Bearer YOUR_TOKEN")
	req.Header.Add("Content-Type", "application/json")

	// 3. リクエストの実行
	resp, err := client.Do(req)
	if err != nil {
		return []byte(`{"error": "外部APIへの通信に失敗しました"}`), err
	}
	// 関数を抜けるときに必ずボディを閉じる
	defer resp.Body.Close()

	// 4. レスポンスボディの読み込み
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return []byte(`{"error": "レスポンスの読み込みに失敗しました"}`), err
	}

	return body, nil
}
