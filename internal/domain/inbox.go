// Package domain - Entités métier pures
package domain

import "time"

// Inbox - Email temporaire
type Inbox struct {
	ID        string    `json:"id"`
	Address   string    `json:"address"`
	Token     string    `json:"token"`
	CreatedAt time.Time `json:"created_at"`
	ExpiresAt time.Time `json:"expires_at"`
}

func (i *Inbox) IsExpired() bool {
	return time.Now().After(i.ExpiresAt)
}
