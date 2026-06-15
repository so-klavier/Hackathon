package main

import (
	"io"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
)

func main() {
	router := gin.Default()

	// serve static files from ./public directory
	// mount the whole public directory at the root so paths map directly
	// e.g. /street/index.html -> ./public/street/index.html
	router.Static("/", "./public")

	router.POST("/message", func(c *gin.Context) {
		// 1. HTTPクライアントの作成（タイムアウトを設定するのが安全です）
		client := &http.Client{
			Timeout: 10 * time.Second,
		}

		// 2. 外部APIへのGETリクエストを作成（例としてテスト用のパブリックAPIを使用）
		externalAPIURL := "http://127.0.0.1:8000/chat"
		req, err := http.NewRequest("POST", externalAPIURL, nil)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "リクエストの作成に失敗しました"})
			return
		}

		// (任意) ヘッダーの追加が必要な場合はここで行います
		// req.Header.Add("Authorization", "Bearer YOUR_TOKEN")
		// req.Header.Add("Content-Type", "application/json")

		// 3. リクエストの実行
		resp, err := client.Do(req)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "外部APIへの通信に失敗しました"})
			return
		}
		// 関数を抜けるときに必ずボディを閉じる
		defer resp.Body.Close()

		// 4. レスポンスボディの読み込み
		body, err := io.ReadAll(resp.Body)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "レスポンスの読み込みに失敗しました"})
			return
		}

		// 5. 取得したデータをそのままフロントエンド（クライアント）に返す
		// 外部APIがJSONを返している場合は、Data関数でそのまま流せます
		c.Data(resp.StatusCode, "application/json; charset=utf-8", body)
	})

	err := router.Run(":5002")
	if err != nil {
		return
	}
}
