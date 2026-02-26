package domain

import "time"

type Message struct {
	ID          string       `json:"id"`
	Subject     string       `json:"subject"`
	From        Address      `json:"from"`
	Body        string       `json:"body"`
	Attachments []Attachment `json:"attachments"`
	CreatedAt   time.Time    `json:"created_at"`
	IsRead      bool         `json:"is_read"`
}

type Address struct {
	Name    string `json:"name"`
	Address string `json:"address"`
}

type Attachment struct {
	Filename    string `json:"filename"`
	Size        int64  `json:"size"`
	ContentType string `json:"content_type"`
	URL         string `json:"url"`
}
