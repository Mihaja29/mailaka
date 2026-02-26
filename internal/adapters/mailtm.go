// Package adapters - Implémentation des ports (infrastructure)
package adapters

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"time"
	
	domainpkg "github.com/Mihaja29/mailaka/internal/domain"
	"github.com/Mihaja29/mailaka/internal/ports"
)

// MailTMAdapter - Implémentation de l'API mail.tm
type MailTMAdapter struct {
	client  *http.Client
	baseURL string
	token   string
}

func NewMailTMAdapter(timeout time.Duration) ports.API {
	return &MailTMAdapter{
		client:  &http.Client{Timeout: timeout},
		baseURL: "https://api.mail.tm",
	}
}

func (m *MailTMAdapter) CreateInbox(ctx context.Context, domain string) (*domainpkg.Inbox, error) {
	// Générer email random
	email := generateRandomEmail(domain)
	password := generatePassword()
	
	body, _ := json.Marshal(map[string]string{
		"address":  email,
		"password": password,
	})
	
	req, _ := http.NewRequestWithContext(ctx, "POST", m.baseURL+"/accounts", bytes.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	
	resp, err := m.client.Do(req)
	if err != nil {
		return nil, fmt.Errorf("create account: %w", err)
	}
	defer resp.Body.Close()
	
	if resp.StatusCode != http.StatusCreated {
		return nil, fmt.Errorf("create account failed: %d", resp.StatusCode)
	}
	
	// Get token
	token, err := m.getToken(ctx, email, password)
	if err != nil {
		return nil, err
	}
	
	return &domainpkg.Inbox{
		Address:   email,
		Token:     token,
		CreatedAt: time.Now(),
		ExpiresAt: time.Now().Add(24 * time.Hour),
	}, nil
}

func (m *MailTMAdapter) getToken(ctx context.Context, email, password string) (string, error) {
	body, _ := json.Marshal(map[string]string{
		"address":  email,
		"password": password,
	})
	
	req, _ := http.NewRequestWithContext(ctx, "POST", m.baseURL+"/token", bytes.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	
	resp, err := m.client.Do(req)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()
	
	var result struct {
		Token string `json:"token"`
	}
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return "", err
	}
	
	return result.Token, nil
}

// Autres méthodes avec Context pour cancellation...

func (m *MailTMAdapter) GetInbox(ctx context.Context) (*domainpkg.Inbox, error) {
	return nil, nil
}

func (m *MailTMAdapter) DeleteInbox(ctx context.Context, id string) error {
	return nil
}

func (m *MailTMAdapter) FetchMessages(ctx context.Context) ([]domainpkg.Message, error) {
	return nil, nil
}

func (m *MailTMAdapter) FetchMessage(ctx context.Context, id string) (*domainpkg.Message, error) {
	return nil, nil
}

func (m *MailTMAdapter) DownloadAttachment(ctx context.Context, url string) ([]byte, error) {
	return nil, nil
}
