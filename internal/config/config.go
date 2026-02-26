// Package config - Configuration avec Functional Options
package config

import (
	"time"
)

// Config - Configuration struct
type Config struct {
	APIBaseURL      string
	Timeout         time.Duration
	Domain          string
	DataDir         string
	EnableCache     bool
	CacheExpiration time.Duration
}

// Option - Functional option type
type Option func(*Config)

// Defaults
func Default() *Config {
	return &Config{
		APIBaseURL:      "https://api.mail.tm",
		Timeout:         30 * time.Second,
		Domain:          "", // auto-select
		DataDir:         "",
		EnableCache:     true,
		CacheExpiration: 5 * time.Minute,
	}
}

// Options
func WithAPIBaseURL(url string) Option {
	return func(c *Config) { c.APIBaseURL = url }
}

func WithTimeout(d time.Duration) Option {
	return func(c *Config) { c.Timeout = d }
}

func WithDomain(d string) Option {
	return func(c *Config) { c.Domain = d }
}

func WithDataDir(d string) Option {
	return func(c *Config) { c.DataDir = d }
}

func WithoutCache() Option {
	return func(c *Config) { c.EnableCache = false }
}

func WithCache(enabled bool) Option {
	return func(c *Config) { c.EnableCache = enabled }
}

// New - Create config with options
func New(opts ...Option) *Config {
	cfg := Default()
	for _, opt := range opts {
		opt(cfg)
	}
	return cfg
}
