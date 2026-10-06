from __future__ import annotations

from dataclasses import dataclass
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

import requests


MAX_POLICY_BYTES = 1_000_000
REQUEST_TIMEOUT_SECONDS = 8


KNOWN_POLICY_URLS = {
    "instagram": "https://privacycenter.instagram.com/policy/",
    "facebook": "https://www.facebook.com/privacy/policy/",
    "whatsapp": "https://www.whatsapp.com/legal/privacy-policy",
    "google maps": "https://policies.google.com/privacy",
    "google": "https://policies.google.com/privacy",
    "netflix": "https://help.netflix.com/legal/privacy",
    "spotify": "https://www.spotify.com/legal/privacy-policy/",
    "snapchat": "https://values.snap.com/privacy/privacy-policy",
    "uber": "https://www.uber.com/legal/en/document/?name=privacy-notice",
    "amazon": "https://www.amazon.com/gp/help/customer/display.html?nodeId=GX7NJQ4ZB8MHFRNJ",
}


@dataclass
class PolicyDiscoveryResult:
    success: bool
    policy_text: str | None = None
    source_url: str | None = None
    error: str | None = None


class _TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self._ignored = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() in {"script", "style", "noscript"}:
            self._ignored += 1

    def handle_endtag(self, tag):
        if tag.lower() in {"script", "style", "noscript"}:
            self._ignored = max(0, self._ignored - 1)

    def handle_data(self, data):
        if self._ignored:
            return

        text = " ".join(data.split())

        if text:
            self.parts.append(text)


class _LinkExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() != "a":
            return

        attributes = dict(attrs)
        href = attributes.get("href")

        if href:
            self.links.append(href)


def _normalize_application_name(name: str) -> str:
    return " ".join(name.strip().lower().split())


def _is_safe_http_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def _fetch_url(url: str) -> str:
    if not _is_safe_http_url(url):
        raise ValueError("Unsupported policy URL.")

    response = requests.get(
        url,
        timeout=REQUEST_TIMEOUT_SECONDS,
        allow_redirects=True,
        headers={
            "User-Agent": (
                "FDO-Privacy academic policy discovery/1.0"
            )
        },
    )
    response.raise_for_status()

    content = response.content[:MAX_POLICY_BYTES]
    encoding = response.encoding or "utf-8"

    return content.decode(encoding, errors="replace")


def _html_to_text(html: str) -> str:
    parser = _TextExtractor()
    parser.feed(html)
    return "\n".join(parser.parts)


def _extract_privacy_links(
    html: str,
    base_url: str,
) -> list[str]:
    parser = _LinkExtractor()
    parser.feed(html)

    links = []

    for href in parser.links:
        candidate = urljoin(base_url, href)
        parsed = urlparse(candidate)

        if "privacy" not in candidate.lower():
            continue

        if parsed.scheme not in {"http", "https"}:
            continue

        links.append(candidate)

    return links[:3]


def _candidate_homepage(application_name: str) -> str | None:
    normalized = _normalize_application_name(application_name)

    if not normalized:
        return None

    if any(char in normalized for char in "/:@"):
        return None

    compact = normalized.replace(" ", "")

    if not compact.isalnum():
        return None

    return f"https://www.{compact}.com"


def _is_usable_policy_text(text: str) -> bool:
    normalized = text.lower()
    return (
        len(text.split()) >= 80
        and "privacy" in normalized
        and any(
            phrase in normalized
            for phrase in (
                "personal information",
                "personal data",
                "information we collect",
                "data we collect",
            )
        )
    )


def discover_privacy_policy(
    application_name: str,
) -> PolicyDiscoveryResult:
    normalized = _normalize_application_name(application_name)
    candidates = []

    if normalized in KNOWN_POLICY_URLS:
        candidates.append(KNOWN_POLICY_URLS[normalized])

    homepage = _candidate_homepage(application_name)

    if homepage:
        candidates.append(homepage)

    for url in candidates:
        try:
            html = _fetch_url(url)
        except Exception:
            continue

        text = _html_to_text(html)

        if _is_usable_policy_text(text):
            return PolicyDiscoveryResult(
                success=True,
                policy_text=text,
                source_url=url,
            )

        for policy_url in _extract_privacy_links(html, url):
            try:
                policy_html = _fetch_url(policy_url)
            except Exception:
                continue

            policy_text = _html_to_text(policy_html)

            if _is_usable_policy_text(policy_text):
                return PolicyDiscoveryResult(
                    success=True,
                    policy_text=policy_text,
                    source_url=policy_url,
                )

    return PolicyDiscoveryResult(
        success=False,
        error=(
            "We couldn't automatically locate an official privacy "
            "policy. Please paste the policy manually."
        ),
    )
