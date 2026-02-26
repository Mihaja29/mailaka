package adapters

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	
	domainpkg "github.com/Mihaja29/mailaka/internal/domain"
	"github.com/Mihaja29/mailaka/internal/ports"
)

// LocalStorage - Stockage local JSON
type LocalStorage struct {
	dataDir string
}

func NewLocalStorage() ports.Storage {
	home, _ := os.UserHomeDir()
	return &LocalStorage{
		dataDir: filepath.Join(home, ".mailaka-v2"),
	}
}

func (l *LocalStorage) SaveInbox(inbox *domainpkg.Inbox) error {
	if err := os.MkdirAll(l.dataDir, 0755); err != nil {
		return err
	}
	
	path := filepath.Join(l.dataDir, "config.json")
	data, err := json.Marshal(inbox)
	if err != nil {
		return err
	}
	
	return os.WriteFile(path, data, 0600)
}

func (l *LocalStorage) LoadInbox() (*domainpkg.Inbox, error) {
	path := filepath.Join(l.dataDir, "config.json")
	data, err := os.ReadFile(path)
	if err != nil {
		if os.IsNotExist(err) {
			return nil, fmt.Errorf("no inbox found")
		}
		return nil, err
	}
	
	var inbox domainpkg.Inbox
	if err := json.Unmarshal(data, &inbox); err != nil {
		return nil, err
	}
	
	// Check expiration
	if inbox.IsExpired() {
		return nil, fmt.Errorf("inbox expired")
	}
	
	return &inbox, nil
}

func (l *LocalStorage) DeleteInbox(id string) error {
	path := filepath.Join(l.dataDir, "config.json")
	return os.Remove(path)
}

func (l *LocalStorage) CacheMessages(inboxID string, msgs []domainpkg.Message) error {
	return nil
}

func (l *LocalStorage) GetCachedMessages(inboxID string) ([]domainpkg.Message, error) {
	return nil, nil
}
