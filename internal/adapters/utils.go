package adapters

import (
	"math/rand"
	"time"
)

func generateRandomEmail(domain string) string {
	if domain == "" {
		domain = "example.com"
	}
	r := rand.New(rand.NewSource(time.Now().UnixNano()))
	const chars = "abcdefghijklmnopqrstuvwxyz0123456789"
	b := make([]byte, 12)
	for i := range b {
		b[i] = chars[r.Intn(len(chars))]
	}
	return string(b) + "@" + domain
}

func generatePassword() string {
	r := rand.New(rand.NewSource(time.Now().UnixNano()))
	const chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-"
	b := make([]byte, 16)
	for i := range b {
		b[i] = chars[r.Intn(len(chars))]
	}
	return string(b)
}
