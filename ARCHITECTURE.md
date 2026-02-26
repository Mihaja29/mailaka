# Mailaka v2 - Architecture Clean

## Structure

```
mailaka-v2/
├── cmd/mailaka/
│   └── main.go              # Point d'entrée, DI simple
├── internal/
│   ├── domain/
│   │   ├── inbox.go         # Entité Inbox
│   │   └── message.go       # Entité Message + Attachment
│   ├── ports/
│   │   └── api.go           # Interfaces API + Storage
│   ├── driven/
│   │   └── service.go       # Use cases (business logic)
│   ├── adapters/
│   │   ├── mailtm.go        # Implémentation API mail.tm
│   │   └── localstorage.go  # Stockage JSON local
│   └── config/
│       └── config.go        # Functional Options Pattern
└── pkg/                     # Libs partagées
```

## Patterns utilisés

### 1. Clean Architecture / Ports & Adapters
```
main.go → Service → Ports (API, Storage)
                    ↓
           Adapters (MailTM, LocalStorage)
```
- Testable: facile de mocker les interfaces
- Swappable: changer mail.tm par une autre API

### 2. Dependency Injection
```go
service := driven.NewInboxService(api, storage)
```
Pas de singletons, pas de globals.

### 3. Context Cancellation
```go
ctx, cancel := context.WithTimeout(parentCtx, 10*time.Second)
defer cancel()
```
Tous les appels HTTP passent par `context.Context`.

### 4. Functional Options
```go
cfg := config.New(
    config.WithTimeout(10*time.Second),
    config.WithDomain("gmail.com"),
)
```
API fluide et extensible.

### 5. Error Wrapping
```go
return fmt.Errorf("create inbox: %w", err)
// Peut être unwrap avec errors.Is()
```

## Flow Commande

```
main.go
  ↓ Parse args
  ↓ Create config (functional options)
  ↓ Inject dependencies (NewInboxService)
  ↓ Call Service method
  ↓ Service orchestrates API + Storage
```

## Avantages

| Aspect | Ancien | Nouveau |
|--------|--------|---------|
| Testable | ❌ Difficile | ✅ Interfaces mockables |
| Config | Hardcoded | Functional Options |
| Timeout | ❌ Non géré | ✅ Context cancellation |
| HTTP | Global client | Par instance, configurable |
| Swappable | ❌ Lié à mail.tm | ✅ Interface API |
| Separation | ❌ Mélange API/UI | ✅ Clean layers |

## Prochaines améliorations

1. **TUI**: Bubble Tea pour interface interactive
2. **Web**: Adapter HTTP avec même Service
3. **Cache**: Redis ou BoltDB
4. **Tests**: Mocks auto-générés (mockery)
5. **Tracing**: OpenTelemetry
