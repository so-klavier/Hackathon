package main

import (
	"fmt"
	"io"
	"net/http"

	"github.com/gin-gonic/gin"
)

func main() {
	router := gin.Default()

	router.Static("/", "./public")

	router.POST("/message", func(c *gin.Context) {
		bodyBytes, err := io.ReadAll(c.Request.Body)
		fmt.Println("受信したBody:", string(bodyBytes))
		if err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": "Failed to read body"})
			return
		}

		body, err := callapi("http://127.0.0.1:8000/chat", bodyBytes)
		if err != nil {
			c.Data(502, "application/json; charset=utf-8", body)
			return
		}

		//var bodyData map[string]any
		//
		//json.Unmarshal(body, &bodyData)
		//
		//emotion, err := callapi("http://127.0.0.1:8000/emotion", bodyBytes)
		//if err != nil {
		//	c.Data(502, "application/json; charset=utf-8", body)
		//	return
		//}
		//
		//var emotionData map[string]any
		//
		//json.Unmarshal(emotion, &emotionData)
		//
		//bodyData["emotion"] = emotionData
		//
		//body, _ = json.Marshal(bodyData)

		c.Data(200, "application/json; charset=utf-8", body)
	})

	router.POST("/emotion", func(c *gin.Context) {
		bodyBytes, err := io.ReadAll(c.Request.Body)
		fmt.Println("受信したBody:", string(bodyBytes))
		if err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": "Failed to read body"})
			return
		}

		body, err := callapi("http://127.0.0.1:8000/emotion", bodyBytes)
		if err != nil {
			c.Data(502, "application/json; charset=utf-8", body)
			return
		}
		c.Data(200, "application/json; charset=utf-8", body)
	})

	fmt.Println("Server is running on port http://127.0.0.1:5002")
	err := router.Run(":5002")
	if err != nil {
		return
	}
}
