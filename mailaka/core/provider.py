"""Email provider implementations."""

import json
import random
import string
import urllib.parse
import urllib.request
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

from .models import Inbox, Message
from ..utils.errors import ProviderError


def _http_get_json(url: str, headers: Optional[Dict[str, str]] = None) -> Any:
    """Make HTTP GET request and return JSON response.
    
    Args:
        url: URL to request
        headers: Optional HTTP headers
        
    Returns:
        Parsed JSON response
        
    Raises:
        ProviderError: If request fails
    """
    try:
        request = urllib.request.Request(url, headers=headers or {})
        with urllib.request.urlopen(request, timeout=15) as response:
            payload = response.read().decode("utf-8")
            return json.loads(payload)
    except Exception as e:
        raise ProviderError(f"HTTP GET failed: {e}")


def _http_post_json(
    url: str,
    data: Dict[str, Any],
    headers: Optional[Dict[str, str]] = None,
) -> Any:
    """Make HTTP POST request with JSON data and return JSON response.
    
    Args:
        url: URL to request
        data: Data to send as JSON
        headers: Optional HTTP headers
        
    Returns:
        Parsed JSON response
        
    Raises:
        ProviderError: If request fails
    """
    try:
        body = json.dumps(data).encode("utf-8")
        request = urllib.request.Request(
            url,
            data=body,
            headers={"Content-Type": "application/json", **(headers or {})},
        )
        with urllib.request.urlopen(request, timeout=15) as response:
            payload = response.read().decode("utf-8")
            return json.loads(payload)
    except Exception as e:
        raise ProviderError(f"HTTP POST failed: {e}")


def _random_local_part(length: int = 10) -> str:
    """Generate random email local part.
    
    Args:
        length: Length of random string
        
    Returns:
        Random string suitable for email local part
    """
    alphabet = string.ascii_lowercase + string.digits
    return "".join(random.choice(alphabet) for _ in range(length))


class Provider(ABC):
    """Abstract base class for email providers."""
    
    @abstractmethod
    def create_inbox(self) -> Inbox:
        """Create a new inbox.
        
        Returns:
            Inbox object
        """
        pass
    
    @abstractmethod
    def get_messages(
        self,
        inbox: Inbox,
        limit: Optional[int] = None,
        offset: int = 0,
    ) -> List[Message]:
        """Get messages for an inbox.
        
        Args:
            inbox: Inbox to get messages for
            limit: Optional maximum number of messages
            offset: Optional offset for pagination
            
        Returns:
            List of Message objects
        """
        pass
    
    @abstractmethod
    def read_message(self, inbox: Inbox, message_id: str) -> Message:
        """Read a specific message.
        
        Args:
            inbox: Inbox containing the message
            message_id: ID of message to read
            
        Returns:
            Message object with body populated
        """
        pass

    def get_attachments(self, inbox: Inbox, message_id: str) -> List[Dict[str, Any]]:
        """Get attachments for a message.
        
        Args:
            inbox: Inbox containing the message
            message_id: ID of message to get attachments for

        Returns:
            List of attachment dictionaries
        """
        raise ProviderError("Attachments not supported by this provider")

    def download_attachment(self, inbox: Inbox, message_id: str, attachment_id: str) -> bytes:
        """Download an attachment.

        Args:
            inbox: Inbox containing the message
            message_id: ID of message containing the attachment
            attachment_id: Attachment identifier (id or filename)

        Returns:
            Attachment content as bytes
        """
        raise ProviderError("Attachment download not supported by this provider")

    def delete_message(self, inbox: Inbox, message_id: str) -> None:
        """Delete a message.

        Args:
            inbox: Inbox containing the message
            message_id: ID of message to delete
        """
        raise ProviderError("Message deletion not supported by this provider")


class OneSecMailProvider(Provider):
    """1secmail.com provider implementation."""

    def delete_message(self, inbox: Inbox, message_id: str) -> None:
        """Delete a message (not supported by 1secmail API)."""
        raise ProviderError("Message deletion not supported by 1secmail")
    
    def create_inbox(self) -> Inbox:
        """Create a new 1secmail inbox."""
        domains = _http_get_json("https://www.1secmail.com/api/v1/?action=getDomainList")
        domain = random.choice(domains)
        login = _random_local_part()
        address = f"{login}@{domain}"
        
        return Inbox(
            provider="1secmail",
            address=address,
            login=login,
            domain=domain,
        )
    
    def get_messages(
        self,
        inbox: Inbox,
        limit: Optional[int] = None,
        offset: int = 0,
    ) -> List[Message]:
        """Get messages from 1secmail inbox."""
        url = (
            f"https://www.1secmail.com/api/v1/?action=getMessages&login="
            f"{urllib.parse.quote(inbox.login)}&domain={urllib.parse.quote(inbox.domain)}"
        )
        data = _http_get_json(url)

        if offset:
            data = data[offset:]
        if limit is not None:
            data = data[:limit]

        return [
            Message(
                id=str(msg["id"]),
                sender=msg["from"],
                subject=msg["subject"],
                date=msg.get("date"),
            )
            for msg in data
        ]
    
    def read_message(self, inbox: Inbox, message_id: str) -> Message:
        """Read a message from 1secmail inbox."""
        url = (
            f"https://www.1secmail.com/api/v1/?action=readMessage&login="
            f"{urllib.parse.quote(inbox.login)}&domain={urllib.parse.quote(inbox.domain)}"
            f"&id={urllib.parse.quote(message_id)}"
        )
        data = _http_get_json(url)
        
        body = data.get("textBody") or data.get("htmlBody") or ""
        
        return Message(
            id=message_id,
            sender=data.get("from"),
            subject=data.get("subject"),
            body=body,
            date=data.get("date"),
        )
    
    def get_attachments(self, inbox: Inbox, message_id: str) -> List[Dict[str, Any]]:
        """Get attachments for a message from 1secmail inbox.
        
        Args:
            inbox: Inbox containing the message
            message_id: ID of message to get attachments for
            
        Returns:
            List of attachment dictionaries with filename, size, contentType
        """
        url = (
            f"https://www.1secmail.com/api/v1/?action=readMessage&login="
            f"{urllib.parse.quote(inbox.login)}&domain={urllib.parse.quote(inbox.domain)}"
            f"&id={urllib.parse.quote(message_id)}"
        )
        data = _http_get_json(url)
        
        attachments = data.get("attachments", [])
        
        # Add download info to each attachment
        for att in attachments:
            att["message_id"] = message_id
            att["login"] = inbox.login
            att["domain"] = inbox.domain
        
        return attachments
    
    def download_attachment(self, inbox: Inbox, message_id: str, attachment_id: str) -> bytes:
        """Download an attachment from 1secmail inbox.
        
        Args:
            inbox: Inbox containing the message
            message_id: ID of message containing the attachment
            attachment_id: Attachment filename
            
        Returns:
            Attachment content as bytes
        """
        url = (
            f"https://www.1secmail.com/api/v1/?action=download&login="
            f"{urllib.parse.quote(inbox.login)}&domain={urllib.parse.quote(inbox.domain)}"
            f"&id={urllib.parse.quote(message_id)}&file={urllib.parse.quote(attachment_id)}"
        )
        
        try:
            request = urllib.request.Request(url)
            with urllib.request.urlopen(request, timeout=15) as response:
                return response.read()
        except Exception as e:
            raise ProviderError(f"Failed to download attachment: {e}")


class MailTmProvider(Provider):
    """mail.tm provider implementation."""

    def _auth_headers(self, inbox: Inbox) -> Dict[str, str]:
        """Build authorization headers for mail.tm."""
        token = self._get_token(inbox)
        return {"Authorization": f"Bearer {token}"}
    
    def create_inbox(self, domain: Optional[str] = None, local_part: Optional[str] = None) -> Inbox:
        """Create a new mail.tm inbox with optional custom local part."""
        try:
            # Get available domains if none specified
            if not domain:
                domain_payload = _http_get_json("https://api.mail.tm/domains?page=1")
                domains = domain_payload.get("hydra:member", [])
                if not domains:
                    raise ProviderError("No domains available for mail.tm")
                domain = random.choice(domains)["domain"]
            
            # Use custom local_part or generate random
            if local_part:
                # Sanitize local_part
                import re
                sanitized = re.sub(r'[^a-z0-9._-]', '', local_part.lower())[:30]
                if not sanitized:
                    sanitized = _random_local_part(10)
                local = sanitized
            else:
                local = _random_local_part()
            
            address = f"{local}@{domain}"
            password = _random_local_part(16)
            
            account_payload = _http_post_json(
                "https://api.mail.tm/accounts",
                {"address": address, "password": password},
            )
            
            return Inbox(
                provider="mailtm",
                address=account_payload["address"],
                password=password,
                account_id=account_payload["id"],
            )
        except Exception as e:
            raise ProviderError(f"Failed to create mail.tm inbox: {e}")
    
    def _get_token(self, inbox: Inbox) -> str:
        """Get authentication token for mail.tm."""
        token_payload = _http_post_json(
            "https://api.mail.tm/token",
            {"address": inbox.address, "password": inbox.password},
        )
        token = token_payload.get("token")
        
        if not token:
            raise ProviderError("Failed to get mail.tm token")
        
        return token
    
    def get_messages(
        self,
        inbox: Inbox,
        limit: Optional[int] = None,
        offset: int = 0,
    ) -> List[Message]:
        """Get messages from mail.tm inbox."""
        query = []
        if limit is not None:
            query.append("page=1")
            query.append(f"limit={limit}")
        url = "https://api.mail.tm/messages"
        if query:
            url = f"{url}?{'&'.join(query)}"
        messages_payload = _http_get_json(
            url,
            headers=self._auth_headers(inbox),
        )
        messages = messages_payload.get("hydra:member", [])

        if offset:
            messages = messages[offset:]
        if limit is not None:
            messages = messages[:limit]

        return [
            Message(
                id=msg["id"],
                sender=msg["from"]["address"],
                subject=msg["subject"],
                date=msg.get("createdAt"),
            )
            for msg in messages
        ]
    
    def read_message(self, inbox: Inbox, message_id: str) -> Message:
        """Read a message from mail.tm inbox."""
        data = _http_get_json(
            f"https://api.mail.tm/messages/{urllib.parse.quote(message_id)}",
            headers=self._auth_headers(inbox),
        )
        
        body = data.get("text") or data.get("html") or ""
        
        return Message(
            id=message_id,
            sender=data.get("from", {}).get("address"),
            subject=data.get("subject"),
            body=body,
            date=data.get("createdAt"),
        )

    def get_attachments(self, inbox: Inbox, message_id: str) -> List[Dict[str, Any]]:
        """Get attachments for a mail.tm message."""
        data = _http_get_json(
            f"https://api.mail.tm/messages/{urllib.parse.quote(message_id)}",
            headers=self._auth_headers(inbox),
        )
        attachments = data.get("attachments", [])
        # Debug: afficher toutes les clés de chaque attachment
        for attachment in attachments:
            attachment.setdefault("message_id", message_id)
            # Log debug
            print(f"DEBUG ATTACHMENT KEYS: {list(attachment.keys())}")
            print(f"DEBUG ATTACHMENT DATA: {attachment}")
        return attachments

    def download_attachment(self, inbox: Inbox, message_id: str, attachment_id: str) -> bytes:
        """Download an attachment from mail.tm."""
        # Ne pas revérifier - direct download avec l'ID
        token = self._get_token(inbox)
        url = f"https://api.mail.tm/messages/{urllib.parse.quote(message_id)}/attachments/{urllib.parse.quote(attachment_id)}"
        request = urllib.request.Request(url, headers={
            "Authorization": f"Bearer {token}",
            "Accept": "*/*"
        })
        try:
            with urllib.request.urlopen(request, timeout=15) as response:
                return response.read()
        except urllib.error.HTTPError as e:
            raise ProviderError(f"HTTP {e.code}: {e.reason}")
        except Exception as exc:
            raise ProviderError(f"Failed to download: {exc}")

    def delete_message(self, inbox: Inbox, message_id: str) -> None:
        """Delete a message from mail.tm."""
        request = urllib.request.Request(
            f"https://api.mail.tm/messages/{urllib.parse.quote(message_id)}",
            headers=self._auth_headers(inbox),
            method="DELETE",
        )
        try:
            with urllib.request.urlopen(request, timeout=15):
                return None
        except Exception as exc:
            raise ProviderError(f"Failed to delete message: {exc}")


class GuerrillaMailProvider(Provider):
    """guerrillamail.com provider implementation."""

    def delete_message(self, inbox: Inbox, message_id: str) -> None:
        """Delete a message (not supported by GuerrillaMail API)."""
        raise ProviderError("Message deletion not supported by GuerrillaMail")
    
    def create_inbox(self) -> Inbox:
        """Create a new guerrillamail inbox."""
        # Ajouter User-Agent pour éviter le 403
        headers = {"User-Agent": "Mozilla/5.0 (compatible; Mailaka/1.0)"}
        request = urllib.request.Request(
            "https://api.guerrillamail.com/ajax.php?f=get_email_address",
            headers=headers
        )
        try:
            with urllib.request.urlopen(request, timeout=15) as response:
                payload = json.loads(response.read().decode("utf-8"))
                return Inbox(
                    provider="guerrillamail",
                    address=payload["email_addr"],
                    token=payload["sid_token"],
                )
        except urllib.error.HTTPError as e:
            if e.code == 403:
                raise ProviderError("Guerrillamail est temporairement indisponible (rate limit). Réessayez dans quelques minutes ou choisissez un autre provider.")
            raise ProviderError(f"Failed to create inbox: {e}")
        except Exception as e:
            raise ProviderError(f"Failed to create inbox: {e}")
    
    def get_messages(
        self,
        inbox: Inbox,
        limit: Optional[int] = None,
        offset: int = 0,
    ) -> List[Message]:
        """Get messages from guerrillamail inbox."""
        url = (
            f"https://api.guerrillamail.com/ajax.php?f=get_email_list&offset={offset}&sid_token="
            f"{urllib.parse.quote(inbox.token)}"
        )
        headers = {"User-Agent": "Mozilla/5.0 (compatible; Mailaka/1.0)"}
        request = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=15) as response:
                payload = json.loads(response.read().decode("utf-8"))
                messages = payload.get("list", [])

                if limit is not None:
                    messages = messages[:limit]

                return [
                    Message(
                        id=msg["mail_id"],
                        sender=msg["mail_from"],
                        subject=msg["mail_subject"],
                        date=msg.get("mail_timestamp"),
                    )
                    for msg in messages
                ]
        except Exception as e:
            raise ProviderError(f"Failed to get messages: {e}")
    
    def read_message(self, inbox: Inbox, message_id: str) -> Message:
        """Read a message from guerrillamail inbox."""
        url = (
            f"https://api.guerrillamail.com/ajax.php?f=fetch_email&sid_token="
            f"{urllib.parse.quote(inbox.token)}&email_id={urllib.parse.quote(message_id)}"
        )
        headers = {"User-Agent": "Mozilla/5.0 (compatible; Mailaka/1.0)"}
        request = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=15) as response:
                data = json.loads(response.read().decode("utf-8"))
                return Message(
                    id=message_id,
                    sender=data.get("mail_from"),
                    subject=data.get("mail_subject"),
                    body=data.get("mail_body", ""),
                    date=data.get("mail_timestamp"),
                )
        except Exception as e:
            raise ProviderError(f"Failed to read message: {e}")


class TempMailIOProvider(Provider):
    """temp-mail.io provider implementation with custom domains."""
    
    API_BASE = "https://api.internal.temp-mail.io/api/v3"
    
    def _http_post_json(self, url: str, data: Dict[str, Any]) -> Any:
        """Make HTTP POST request with JSON data."""
        try:
            body = json.dumps(data).encode("utf-8")
            request = urllib.request.Request(
                url,
                data=body,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(request, timeout=15) as response:
                return json.loads(response.read().decode("utf-8"))
        except Exception as e:
            raise ProviderError(f"HTTP POST failed: {e}")
    
    def get_available_domains(self) -> List[str]:
        """Get list of available domains from temp-mail.io."""
        try:
            data = _http_get_json(f"{self.API_BASE}/domains")
            return [d["name"] for d in data.get("domains", [])]
        except Exception as e:
            raise ProviderError(f"Failed to get domains: {e}")
    
    def create_inbox(self, domain: Optional[str] = None) -> Inbox:
        """Create a new temp-mail.io inbox."""
        try:
            # If no domain specified, get available domains and pick one
            if not domain:
                domains = self.get_available_domains()
                if not domains:
                    raise ProviderError("No domains available")
                domain = domains[0]  # Pick first available
            
            data = self._http_post_json(
                f"{self.API_BASE}/email/new",
                {"domain": domain}
            )
            
            return Inbox(
                provider="tempmail_io",
                address=data["email"],
                token=data["token"],
            )
        except Exception as e:
            raise ProviderError(f"Failed to create inbox: {e}")
    
    def get_messages(self, inbox: Inbox, limit: Optional[int] = None, offset: int = 0) -> List[Message]:
        """Get messages from temp-mail.io inbox."""
        try:
            data = _http_get_json(
                f"{self.API_BASE}/email/{urllib.parse.quote(inbox.address)}/messages"
            )
            
            messages = [
                Message(
                    id=msg["id"],
                    sender=msg["from"],
                    subject=msg["subject"],
                    body=msg.get("body_text", ""),
                    date=msg.get("created_at", ""),
                )
                for msg in data
            ]
            
            if limit is not None:
                messages = messages[offset:offset + limit]
            
            return messages
        except Exception as e:
            raise ProviderError(f"Failed to get messages: {e}")
    
    def read_message(self, inbox: Inbox, message_id: str) -> Message:
        """Read a specific message from temp-mail.io."""
        try:
            messages = self.get_messages(inbox)
            for msg in messages:
                if msg.id == message_id:
                    return msg
            raise ProviderError(f"Message {message_id} not found")
        except Exception as e:
            raise ProviderError(f"Failed to read message: {e}")
    
    def delete_message(self, inbox: Inbox, message_id: str) -> None:
        """Delete a message from temp-mail.io."""
        try:
            request = urllib.request.Request(
                f"{self.API_BASE}/email/{urllib.parse.quote(inbox.address)}/messages/{urllib.parse.quote(message_id)}",
                method="DELETE"
            )
            with urllib.request.urlopen(request, timeout=15):
                return None
        except Exception as e:
            raise ProviderError(f"Failed to delete message: {e}")


class MailGwProvider(Provider):
    """mail.gw provider implementation - modern temporary email API."""
    
    API_BASE = "https://api.mail.gw"
    
    def _http_post_json(self, url: str, data: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> Any:
        """Make HTTP POST request with JSON data."""
        try:
            body = json.dumps(data).encode("utf-8")
            request = urllib.request.Request(
                url,
                data=body,
                headers={"Content-Type": "application/ld+json", **(headers or {})},
                method="POST"
            )
            with urllib.request.urlopen(request, timeout=15) as response:
                return json.loads(response.read().decode("utf-8"))
        except Exception as e:
            raise ProviderError(f"HTTP POST failed: {e}")
    
    def _http_get_json_auth(self, url: str, token: str) -> Any:
        """Make authenticated HTTP GET request."""
        try:
            request = urllib.request.Request(
                url,
                headers={"Authorization": f"Bearer {token}"}
            )
            with urllib.request.urlopen(request, timeout=15) as response:
                return json.loads(response.read().decode("utf-8"))
        except Exception as e:
            raise ProviderError(f"HTTP GET failed: {e}")
    
    def get_available_domains(self) -> List[str]:
        """Get list of available domains from mail.gw."""
        try:
            data = _http_get_json(f"{self.API_BASE}/domains")
            return [d["domain"] for d in data.get("hydra:member", [])]
        except Exception as e:
            raise ProviderError(f"Failed to get domains: {e}")
    
    def create_inbox(self, domain: Optional[str] = None, local_part: Optional[str] = None) -> Inbox:
        """Create a new mail.gw inbox with optional custom local part."""
        try:
            # Get available domains if none specified
            if not domain:
                domains = self.get_available_domains()
                if not domains:
                    raise ProviderError("No domains available")
                domain = domains[0]
            
            # Use custom local_part or generate random
            import secrets
            if local_part:
                # Sanitize local_part
                import re
                sanitized = re.sub(r'[^a-z0-9._-]', '', local_part.lower())[:30]
                if not sanitized:
                    sanitized = f"mailaka_{secrets.token_hex(8)}"
                username = sanitized
            else:
                username = f"mailaka_{secrets.token_hex(8)}"
            
            password = secrets.token_hex(12)
            address = f"{username}@{domain}"
            
            # Create account
            data = self._http_post_json(
                f"{self.API_BASE}/accounts",
                {"address": address, "password": password}
            )
            
            # Get auth token
            token_data = self._http_post_json(
                f"{self.API_BASE}/token",
                {"address": address, "password": password}
            )
            
            return Inbox(
                provider="mail_gw",
                address=data["address"],
                token=token_data["token"],
            )
        except Exception as e:
            raise ProviderError(f"Failed to create inbox: {e}")
    
    def get_messages(self, inbox: Inbox, limit: Optional[int] = None, offset: int = 0) -> List[Message]:
        """Get messages from mail.gw inbox."""
        try:
            data = self._http_get_json_auth(
                f"{self.API_BASE}/messages",
                inbox.token
            )
            
            messages = [
                Message(
                    id=msg["id"],
                    sender=msg["from"]["address"] if isinstance(msg["from"], dict) else msg["from"],
                    subject=msg.get("subject", ""),
                    date=msg.get("createdAt", ""),
                )
                for msg in data.get("hydra:member", [])
            ]
            
            if limit is not None:
                messages = messages[offset:offset + limit]
            
            return messages
        except Exception as e:
            raise ProviderError(f"Failed to get messages: {e}")
    
    def read_message(self, inbox: Inbox, message_id: str) -> Message:
        """Read a specific message from mail.gw."""
        try:
            data = self._http_get_json_auth(
                f"{self.API_BASE}/messages/{urllib.parse.quote(message_id)}",
                inbox.token
            )
            
            return Message(
                id=message_id,
                sender=data["from"]["address"] if isinstance(data["from"], dict) else data["from"],
                subject=data.get("subject", ""),
                body=data.get("text", "") or data.get("html", ""),
                date=data.get("createdAt", ""),
            )
        except Exception as e:
            raise ProviderError(f"Failed to read message: {e}")
    
    def delete_message(self, inbox: Inbox, message_id: str) -> None:
        """Delete a message from mail.gw."""
        try:
            request = urllib.request.Request(
                f"{self.API_BASE}/messages/{urllib.parse.quote(message_id)}",
                headers={"Authorization": f"Bearer {inbox.token}"},
                method="DELETE"
            )
            with urllib.request.urlopen(request, timeout=15):
                return None
        except Exception as e:
            raise ProviderError(f"Failed to delete message: {e}")


class DropMailProvider(Provider):
    """dropmail.me provider implementation using GraphQL."""
    
    API_URL = "https://dropmail.me/api/graphql"
    
    def _graphql_query(self, query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute GraphQL query/mutation."""
        try:
            payload = {"query": query}
            if variables:
                payload["variables"] = variables
            
            body = json.dumps(payload).encode("utf-8")
            request = urllib.request.Request(
                self.API_URL,
                data=body,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
            )
            
            with urllib.request.urlopen(request, timeout=15) as response:
                data = json.loads(response.read().decode("utf-8"))
                if "errors" in data:
                    raise ProviderError(f"GraphQL error: {data['errors']}")
                return data.get("data", {})
        except Exception as e:
            raise ProviderError(f"GraphQL request failed: {e}")
    
    def create_inbox(self, domain: Optional[str] = None) -> Inbox:
        """Create a new dropmail inbox via GraphQL."""
        query = """
        mutation {
            introduceSession {
                id
                addresses {
                    address
                }
            }
        }
        """
        
        data = self._graphql_query(query)
        session = data.get("introduceSession", {})
        
        if not session or not session.get("addresses"):
            raise ProviderError("Failed to create dropmail inbox: no address returned")
        
        address = session["addresses"][0]["address"]
        session_id = session["id"]
        
        return Inbox(
            provider="dropmail",
            address=address,
            token=session_id,
        )
    
    def get_messages(
        self,
        inbox: Inbox,
        limit: Optional[int] = None,
        offset: int = 0,
    ) -> List[Message]:
        """Get messages from dropmail inbox via GraphQL."""
        query = """
        query($sessionId: ID!) {
            session(id: $sessionId) {
                mails {
                    id
                    from
                    subject
                    timestamp
                }
            }
        }
        """
        
        data = self._graphql_query(query, {"sessionId": inbox.token})
        session = data.get("session", {})
        mails = session.get("mails", [])
        
        if limit is not None:
            mails = mails[offset:offset + limit]
        
        return [
            Message(
                id=mail["id"],
                sender=mail["from"],
                subject=mail.get("subject", ""),
                date=mail.get("timestamp"),
            )
            for mail in mails
        ]
    
    def read_message(self, inbox: Inbox, message_id: str) -> Message:
        """Read a specific message from dropmail."""
        query = """
        query($sessionId: ID!, $messageId: ID!) {
            session(id: $sessionId) {
                mail(id: $messageId) {
                    id
                    from
                    subject
                    text
                    html
                    timestamp
                }
            }
        }
        """
        
        data = self._graphql_query(query, {"sessionId": inbox.token, "messageId": message_id})
        session = data.get("session", {})
        mail = session.get("mail")
        
        if not mail:
            raise ProviderError(f"Message {message_id} not found")
        
        return Message(
            id=message_id,
            sender=mail["from"],
            subject=mail.get("subject", ""),
            body=mail.get("text") or mail.get("html", ""),
            date=mail.get("timestamp"),
        )
    
    def delete_message(self, inbox: Inbox, message_id: str) -> None:
        """Delete message (not supported by DropMail)."""
        raise ProviderError("Message deletion not supported by DropMail")
    
    def get_attachments(self, inbox: Inbox, message_id: str) -> List[Dict[str, Any]]:
        """Get attachments (not supported by DropMail)."""
        return []
    
    def download_attachment(self, inbox: Inbox, message_id: str, attachment_id: str) -> bytes:
        """Download attachment (not supported by DropMail)."""
        raise ProviderError("Attachments not supported by DropMail")


def validate_email_disify(email: str) -> Dict[str, Any]:
    """Validate email using Disify API (free, no auth).
    
    Args:
        email: Email address to validate
        
    Returns:
        Dict with validation results:
        - disposable: True if temporary email domain
        - dns: True if domain has MX records
        - format: True if format is valid
    """
    try:
        domain = email.split("@")[-1] if "@" in email else email
        url = f"https://www.disify.com/api/{urllib.parse.quote(domain)}"
        
        request = urllib.request.Request(url, headers={"Accept": "application/json"})
        
        with urllib.request.urlopen(request, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            return {
                "disposable": data.get("disposable", False),
                "dns": data.get("dns", False),
                "format": data.get("format", False),
                "domain": domain,
            }
    except Exception as e:
        return {
            "disposable": False,
            "dns": False,
            "format": False,
            "domain": email.split("@")[-1] if "@" in email else email,
            "error": str(e),
        }


class ProviderFactory:
    """Factory for creating provider instances."""
    
    PROVIDERS = {
        "1secmail": OneSecMailProvider,
        "mailtm": MailTmProvider,
        "guerrillamail": GuerrillaMailProvider,
        "tempmail_io": TempMailIOProvider,
        "mail_gw": MailGwProvider,
        "dropmail": DropMailProvider,
    }
    
    @classmethod
    def get_provider(cls, name: str) -> Provider:
        """Get a provider instance by name.
        
        Args:
            name: Provider name (1secmail, mailtm, guerrillamail)
            
        Returns:
            Provider instance
            
        Raises:
            ProviderError: If provider name is invalid
        """
        provider_class = cls.PROVIDERS.get(name.lower())
        
        if not provider_class:
            raise ProviderError(f"Unknown provider: {name}")
        
        return provider_class()
    
    @classmethod
    def get_all_provider_names(cls) -> List[str]:
        """Get list of all available provider names.
        
        Returns:
            List of provider names
        """
        return list(cls.PROVIDERS.keys())
