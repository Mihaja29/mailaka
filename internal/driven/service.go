// Package driven - Application logic (use cases)
package driven

import (
	"context"
	"fmt"
	
	domainpkg "github.com/Mihaja29/mailaka/internal/domain"
	"github.com/Mihaja29/mailaka/internal/ports"
)

// InboxService - Logique métier des emails
type InboxService struct {
	api     ports.API
	storage ports.Storage
}

func NewInboxService(api ports.API, storage ports.Storage) *InboxService {
	return &InboxService{
		api:     api,
		storage: storage,
	}
}

func (s *InboxService) Create(ctx context.Context, domain string) (*domainpkg.Inbox, error) {
	inbox, err := s.api.CreateInbox(ctx, domain)
	if err != nil {
		return nil, fmt.Errorf("create inbox: %w", err)
	}
	
	if err := s.storage.SaveInbox(inbox); err != nil {
		return nil, fmt.Errorf("save inbox: %w", err)
	}
	
	return inbox, nil
}

func (s *InboxService) GetActive(ctx context.Context) (*domainpkg.Inbox, error) {
	// 1. Charger depuis stockage local
	inbox, err := s.storage.LoadInbox()
	if err != nil {
		return nil, fmt.Errorf("no active inbox: %w", err)
	}
	
	// 2. Vérifier expiration
	if inbox.IsExpired() {
		s.storage.DeleteInbox(inbox.ID)
		return nil, fmt.Errorf("inbox expired")
	}
	
	return inbox, nil
}

func (s *InboxService) ListMessages(ctx context.Context) ([]domainpkg.Message, error) {
	inbox, err := s.GetActive(ctx)
	if err != nil {
		return nil, err
	}
	
	// Optionnel: vérifier cache d'abord
	if cached, _ := s.storage.GetCachedMessages(inbox.ID); len(cached) > 0 {
		return cached, nil
	}
	
	// Fetch depuis API
	msgs, err := s.api.FetchMessages(ctx)
	if err != nil {
		return nil, fmt.Errorf("fetch messages: %w", err)
	}
	
	// Cacher pour prochaine fois
	_ = s.storage.CacheMessages(inbox.ID, msgs)
	
	return msgs, nil
}

func (s *InboxService) ReadMessage(ctx context.Context, id string) (*domainpkg.Message, error) {
	_, err := s.GetActive(ctx)
	if err != nil {
		return nil, err
	}
	
	return s.api.FetchMessage(ctx, id)
}

func (s *InboxService) Destroy(ctx context.Context) error {
	inbox, err := s.GetActive(ctx)
	if err != nil {
		return err
	}
	
	// Supprimer API + local
	_ = s.api.DeleteInbox(ctx, inbox.ID)
	return s.storage.DeleteInbox(inbox.ID)
}
