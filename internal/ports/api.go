// Package ports - Interfaces (contrats)
package ports

import (
	"context"
	domainpkg "github.com/Mihaja29/mailaka/internal/domain"
)

// API - Port primaire (driven by application)
type API interface {
	CreateInbox(ctx context.Context, domain string) (*domainpkg.Inbox, error)
	GetInbox(ctx context.Context) (*domainpkg.Inbox, error)
	DeleteInbox(ctx context.Context, id string) error
	
	FetchMessages(ctx context.Context) ([]domainpkg.Message, error)
	FetchMessage(ctx context.Context, id string) (*domainpkg.Message, error)
	
	DownloadAttachment(ctx context.Context, url string) ([]byte, error)
}

// Storage - Port secondaire (driven by infrastructure)
type Storage interface {
	SaveInbox(inbox *domainpkg.Inbox) error
	LoadInbox() (*domainpkg.Inbox, error)
	DeleteInbox(id string) error
	
	CacheMessages(inboxID string, msgs []domainpkg.Message) error
	GetCachedMessages(inboxID string) ([]domainpkg.Message, error)
}
