#!/usr/bin/env python3
"""
Content Crawler Pro (CCPro) - Refactored Version
A powerful web content extraction tool with smart defaults and simple API.

Basic Usage:
    import asyncio
    from ccpro import crawl
    
    # Simple usage - just provide URL
    content = asyncio.run(crawl("https://example.com"))
    print(content)
    
    # With custom config
    from ccpro import ccpro, crawl
    
    config = ccpro(
        max_pages=10,
        extract_iframes=True,
        follow_links=True
    )
    content = asyncio.run(crawl("https://example.com", config))
"""

import asyncio
import json
import re
import time
import logging
import os
from typing import Dict, List, Any, Set, Optional, Union
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urljoin, urlparse, urlunparse
from dataclasses import dataclass, field, asdict
from enum import Enum
from collections import deque

from playwright.async_api import async_playwright, Page, Browser, BrowserContext
from bs4 import BeautifulSoup
import html2text

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


# ============================================================================
# PUBLIC API
# ============================================================================

def ccpro(**kwargs) -> 'Config':
    """
    Create a configuration object for the crawler with sensible defaults.
    
    Args:
        max_pages: Maximum number of pages to crawl (default: 1)
        max_depth: Maximum depth for link following (default: 0)
        follow_links: Whether to follow discovered links (default: False)
        extract_iframes: Extract content from iframes (default: True)
        extract_padlet_cards: Extract individual Padlet cards (default: True)
        headless: Run browser in headless mode (default: True)
        wait_time: Seconds to wait after page load (default: 2.0)
        scroll_count: Number of times to scroll (default: 2)
        output_dir: Directory to save results (default: None)
        verbose: Print progress messages (default: False)
        
    Returns:
        Config object with specified settings
    """
    return Config(**kwargs)


async def crawl(url: str, config: Optional['Config'] = None) -> Union[str, Dict[str, Any]]:
    """
    Crawl a URL and extract content as markdown.
    
    Args:
        url: The URL to crawl
        config: Optional configuration object (uses smart defaults if not provided)
        
    Returns:
        If single page: Returns markdown string
        If multiple pages: Returns dict with URLs as keys and markdown as values
    """
    config = config or Config()
    
    async with Crawler(config) as crawler:
        results = await crawler.crawl(url)
        
        # Simple return format
        if len(results) == 1:
            return list(results.values())[0]['markdown']
        else:
            return {url: data['markdown'] for url, data in results.items()}


async def crawl_with_auth(url: str, **kwargs) -> Union[str, Dict[str, Any]]:
    """
    Crawl a URL with interactive authentication enabled.
    
    This is a convenience function that automatically enables interactive authentication,
    allowing you to manually login to sites with CAPTCHA, 2FA, etc.
    
    Args:
        url: The URL to crawl
        **kwargs: Any additional configuration options
        
    Returns:
        Extracted content as markdown
    
    Example:
        content = await crawl_with_auth("https://protected-site.com")
    """
    # Force interactive authentication
    kwargs['interactive_auth'] = True
    config = ccpro(**kwargs)
    
    return await crawl(url, config)


# ============================================================================
# CONFIGURATION
# ============================================================================

@dataclass
class Config:
    """Simplified configuration with smart defaults."""
    
    # Basic crawling
    max_pages: int = 1
    max_depth: int = 0
    follow_links: bool = False
    
    # Content extraction
    extract_iframes: bool = True
    extract_padlet_cards: bool = True
    extract_youtube: bool = True
    extract_google_docs: bool = True
    
    # Browser settings
    headless: bool = True
    viewport_width: int = 1920
    viewport_height: int = 1080
    
    # Timing
    wait_time: float = 2.0
    scroll_count: int = 2
    scroll_delay: float = 1.0
    page_timeout: int = 30000
    
    # Output
    output_dir: Optional[str] = None
    save_as_json: bool = False
    verbose: bool = False
    
    # Advanced (usually don't need to change)
    concurrent_requests: int = 3
    crawl_delay: float = 0.5
    min_text_length: int = 25
    
    # Content filtering
    remove_navigation: bool = True
    remove_ads: bool = True
    
    # Interactive authentication
    interactive_auth: bool = False
    session_dir: str = "./.ccpro_sessions"
    session_expiry_days: int = 7
    button_position: Dict[str, str] = field(default_factory=lambda: {'top': '50%', 'left': '20px'})
    auth_timeout: int = 86400000  # 24 hours (essentially infinite for practical purposes)
    
    def to_dict(self) -> Dict:
        """Convert config to dictionary."""
        return asdict(self)


# ============================================================================
# AUTHENTICATION COMPONENTS
# ============================================================================

class SessionManager:
    """Manages browser session persistence for authenticated crawling."""
    
    def __init__(self, session_dir: str = "./.ccpro_sessions", expiry_days: int = 7):
        self.session_dir = Path(session_dir)
        self.session_dir.mkdir(exist_ok=True)
        self.expiry_days = expiry_days
    
    def get_session_path(self, url: str) -> Path:
        """Get the session file path for a given URL."""
        domain = urlparse(url).hostname or "unknown"
        return self.session_dir / f"{domain}.json"
    
    async def load_session(self, url: str) -> Optional[Dict]:
        """Load saved session if it exists and is valid."""
        session_path = self.get_session_path(url)
        
        if not session_path.exists():
            return None
        
        try:
            with open(session_path, 'r') as f:
                session = json.load(f)
            
            # Check expiry
            expires = datetime.fromisoformat(session.get('expires', '2000-01-01'))
            if datetime.now() > expires:
                session_path.unlink()  # Delete expired session
                return None
            
            return session
        except Exception as e:
            logger.warning(f"Failed to load session: {e}")
            return None
    
    async def save_session(self, context: BrowserContext, url: str):
        """Save current browser session."""
        try:
            session = {
                'cookies': await context.cookies(),
                'timestamp': datetime.now().isoformat(),
                'expires': (datetime.now() + timedelta(days=self.expiry_days)).isoformat()
            }
            
            session_path = self.get_session_path(url)
            with open(session_path, 'w') as f:
                json.dump(session, f, indent=2)
            
            logger.info(f"Session saved for {urlparse(url).hostname}")
        except Exception as e:
            logger.error(f"Failed to save session: {e}")
    
    async def apply_session(self, context: BrowserContext, session: Dict):
        """Apply saved session to browser context."""
        if session and 'cookies' in session:
            try:
                await context.add_cookies(session['cookies'])
                logger.info("Session restored from cache")
            except Exception as e:
                logger.warning(f"Failed to apply session: {e}")


class InteractiveAuthenticator:
    """Handles interactive authentication with floating UI button."""
    
    def __init__(self, config: Config):
        self.config = config
        self.session_manager = SessionManager(config.session_dir, config.session_expiry_days)
    
    def get_floating_ui_script(self) -> str:
        """Generate the JavaScript for the floating UI button."""
        # Fixed with proper CSS to override generic div styles
        return """
        (() => {
            console.log('CCPro: Starting UI injection');
            
            // Remove any existing UI
            const existing = document.getElementById('ccpro-simple-ui-x9z8y7');
            if (existing) existing.remove();
            
            // Create simple container with your exact CSS
            const container = document.createElement('div');
            container.id = 'ccpro-simple-ui-x9z8y7';
            container.className = 'ccpro-internal-do-not-scrape';
            container.style.cssText = 'position: fixed; bottom: 50%; left: 20px; z-index: 999999999; background: white; padding: 10px; border: 2px solid rgb(204, 204, 204); border-radius: 8px; width: auto; height: auto;';
            
            // Add title with proper CSS to override generic styles
            const title = document.createElement('div');
            title.textContent = 'CCPro Interactive';
            title.style.cssText = 'font-size: 16px; font-weight: bold; width: auto; height: auto; padding: 0; margin: 0 0 10px 0;';
            
            // Create start button
            const startBtn = document.createElement('button');
            startBtn.textContent = 'Start Crawling';
            startBtn.style.cssText = 'padding: 10px 20px; background: green; color: white; border: none; border-radius: 4px; margin-right: 10px; cursor: pointer;';
            startBtn.onclick = () => {
                console.log('CCPro: Start clicked');
                window.__ccproProceed = true;
                startBtn.textContent = 'Starting...';
                startBtn.disabled = true;
            };
            
            // Create cancel button
            const cancelBtn = document.createElement('button');
            cancelBtn.textContent = 'Cancel';
            cancelBtn.style.cssText = 'padding: 10px 20px; background: white; color: black; border: 1px solid #ccc; border-radius: 4px; cursor: pointer;';
            cancelBtn.onclick = () => {
                console.log('CCPro: Cancel clicked');
                window.__ccproCancel = true;
                container.style.display = 'none';
            };
            
            // Assemble everything
            container.appendChild(title);
            container.appendChild(startBtn);
            container.appendChild(cancelBtn);
            document.body.appendChild(container);
            
            // Initialize state
            window.__ccproProceed = false;
            window.__ccproCancel = false;
            
            console.log('CCPro: UI injection complete');
        })();
        """
    
    async def inject_floating_ui(self, page: Page):
        """Inject the floating UI into the page."""
        # Execute the script directly
        script = self.get_floating_ui_script()
        await page.evaluate(script)
        
        # Add console log to verify injection
        await page.evaluate("console.log('CCPro UI injection attempted')")
        
        # Verify UI was created
        ui_exists = await page.evaluate("() => !!document.getElementById('ccpro-container')")
        if ui_exists:
            logger.info("Floating UI successfully injected")
        else:
            logger.warning("Floating UI injection failed - retrying")
            # Try again with a delay
            await asyncio.sleep(1)
            await page.evaluate(script)
    
    async def wait_for_user_decision(self, page: Page) -> bool:
        """Wait for user to click Start or Cancel."""
        logger.info("Waiting for user authentication...")
        
        # Use a more robust approach that survives navigation
        start_time = datetime.now()
        timeout_seconds = self.config.auth_timeout / 1000
        
        while (datetime.now() - start_time).total_seconds() < timeout_seconds:
            try:
                # Check if user made a decision
                proceed = await page.evaluate('() => window.__ccproProceed === true')
                cancel = await page.evaluate('() => window.__ccproCancel === true')
                
                if proceed:
                    logger.info("User clicked 'Start Crawling' - proceeding")
                    # Hide the UI
                    try:
                        await page.evaluate('document.getElementById("ccpro-container") && (document.getElementById("ccpro-container").style.display = "none")')
                    except:
                        pass
                    return True
                elif cancel:
                    logger.info("User cancelled authentication")
                    return False
                    
            except Exception as e:
                # Page might be navigating, that's ok
                logger.debug(f"Evaluation error (likely navigation): {e}")
                
            # Wait a bit before checking again
            await asyncio.sleep(0.5)
        
        logger.warning("Authentication timeout")
        return False
    
    async def handle_authentication(self, page: Page, url: str, context: BrowserContext, force_ui: bool = True) -> bool:
        """Handle the full authentication flow."""
        # Check for existing session
        session = await self.session_manager.load_session(url)
        
        if session:
            await self.session_manager.apply_session(context, session)
            logger.info("Using cached session")
            # If force_ui is False and we have a session, skip UI
            if not force_ui:
                return True
        
        # Always show UI for interactive authentication
        logger.info("Showing interactive authentication UI")
        
        # Set up navigation handler to re-inject UI on every page
        async def on_navigation():
            try:
                await self.inject_floating_ui(page)
            except:
                pass  # Page might be navigating
        
        # Listen for navigation events
        page.on("load", lambda: asyncio.create_task(on_navigation()))
        page.on("domcontentloaded", lambda: asyncio.create_task(on_navigation()))
        
        # Initial injection
        await self.inject_floating_ui(page)
        
        # Wait for user to authenticate
        authenticated = await self.wait_for_user_decision(page)
        
        if authenticated:
            # Save the session for future use
            await self.session_manager.save_session(context, url)
        
        return authenticated


# ============================================================================
# CORE COMPONENTS
# ============================================================================

class ContentExtractor:
    """Handles all content extraction logic."""
    
    def __init__(self, config: Config):
        self.config = config
        self._setup_html2text()
    
    def _setup_html2text(self):
        """Configure html2text converter."""
        self.h2md = html2text.HTML2Text()
        self.h2md.ignore_links = False
        self.h2md.ignore_images = False
        self.h2md.body_width = 0
        self.h2md.protect_links = True
    
    def clean_html(self, html: str) -> str:
        """Remove unwanted elements from HTML."""
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove CCPro internal elements (including the UI container by ID)
        for element in soup.find_all(class_='ccpro-internal-do-not-scrape'):
            element.decompose()
        
        # Also remove by ID as a fallback
        ui_element = soup.find(id='ccpro-simple-ui-x9z8y7')
        if ui_element:
            ui_element.decompose()
        
        # Always remove these
        for tag in ['script', 'style', 'noscript', 'meta', 'link']:
            for element in soup.find_all(tag):
                element.decompose()
        
        # Remove navigation/ads if configured
        if self.config.remove_navigation:
            # Remove nav elements by tag name
            for tag in ['nav', 'header', 'footer']:
                for element in soup.find_all(tag):
                    element.decompose()
            
            # Remove nav elements by CSS selectors - includes WordPress menu classes
            for selector in ['.menu', '#menu', '[role="navigation"]', '.navigation', '#navigation',
                           '.wpmm-menu', '.mm-menu', '.navbar', '.nav-menu', '.site-navigation',
                           '.main-navigation', '.primary-navigation', '#site-navigation']:
                try:
                    for element in soup.select(selector):
                        element.decompose()
                except:
                    pass  # Skip invalid selectors
        
        if self.config.remove_ads:
            for selector in ['.advertisement', '.ads', '.ad', '.banner', '.popup']:
                try:
                    for element in soup.select(selector):
                        element.decompose()
                except:
                    pass  # Skip invalid selectors
        
        # Remove empty elements
        for elem in soup.find_all(['div', 'span', 'p']):
            if not elem.get_text(strip=True) or len(elem.get_text(strip=True)) < self.config.min_text_length:
                elem.decompose()
        
        return str(soup)
    
    def to_markdown(self, html: str, base_url: str = "") -> str:
        """Convert HTML to clean markdown."""
        cleaned = self.clean_html(html)
        markdown = self.h2md.handle(cleaned)
        
        # Clean up excessive newlines
        markdown = re.sub(r'\n{4,}', '\n\n\n', markdown)
        
        # Fix relative URLs
        if base_url:
            markdown = self._fix_relative_urls(markdown, base_url)
        
        return markdown
    
    def _fix_relative_urls(self, markdown: str, base_url: str) -> str:
        """Convert relative URLs to absolute."""
        def replace_url(match):
            text, url = match.groups()
            if not url.startswith(('http://', 'https://', 'mailto:', '//')):
                url = urljoin(base_url, url)
            return f'[{text}]({url})'
        
        return re.sub(r'\[([^\]]+)\]\(([^)]+)\)', replace_url, markdown)
    
    async def extract_iframes(self, page: Page) -> List[Dict[str, Any]]:
        """Extract iframe information from page."""
        return await page.evaluate("""
            () => {
                const iframes = [];
                document.querySelectorAll('iframe').forEach((iframe, index) => {
                    const src = iframe.src || iframe.getAttribute('data-src') || '';
                    if (src && !src.includes('about:blank')) {
                        iframes.push({
                            url: src,
                            title: iframe.title || iframe.getAttribute('aria-label') || `Iframe ${index + 1}`,
                            type: src.includes('padlet.com') ? 'padlet' :
                                  src.includes('youtube.com') ? 'youtube' :
                                  src.includes('docs.google.com') ? 'google_docs' : 'generic'
                        });
                    }
                });
                return iframes;
            }
        """)
    
    async def extract_padlet_cards(self, page: Page) -> List[Dict[str, Any]]:
        """Extract structured Padlet cards."""
        return await page.evaluate("""
            () => {
                const cards = [];
                const processedIds = new Set();
                
                document.querySelectorAll('.wish-wrapper').forEach((card, index) => {
                    const cardId = card.getAttribute('data-id') || card.getAttribute('data-cid');
                    if (cardId && processedIds.has(cardId)) return;
                    if (cardId) processedIds.add(cardId);
                    
                    const cardData = {
                        index: index + 1,
                        title: card.querySelector('[data-testid="postSubject"], h3')?.innerText?.trim() || '',
                        body: card.querySelector('[data-testid="postBody"], .wish-body-content')?.innerText?.trim() || '',
                        author: card.querySelector('[data-testid*="surfacePostAuthor"] a, .font-semibold')?.innerText?.trim() || '',
                        time: card.querySelector('time')?.innerText?.trim() || '',
                        attachmentUrl: card.querySelector('a[data-testid="showAttachmentPreview"]')?.href || '',
                        isPinned: !!card.querySelector('[data-name="pin_filled"]')
                    };
                    
                    if (cardData.title || cardData.body || cardData.attachmentUrl) {
                        cards.push(cardData);
                    }
                });
                
                return cards;
            }
        """)
    
    async def extract_links(self, page: Page) -> List[Dict[str, str]]:
        """Extract all links from page for crawling."""
        return await page.evaluate("""
            () => {
                const links = [];
                document.querySelectorAll('a[href]').forEach(a => {
                    const href = a.href;
                    const text = a.innerText || a.textContent || '';
                    if (href && !href.startsWith('javascript:') && !href.startsWith('mailto:')) {
                        links.push({href, text: text.substring(0, 100)});
                    }
                });
                return links;
            }
        """)


class BrowserController:
    """Manages browser lifecycle and page operations."""
    
    def __init__(self, config: Config):
        self.config = config
        self.playwright = None
        self.browser = None
        self.context = None
        self.authenticator = None
        
        # Initialize authenticator if interactive auth is enabled
        if config.interactive_auth:
            self.authenticator = InteractiveAuthenticator(config)
    
    async def start(self):
        """Initialize browser."""
        self.playwright = await async_playwright().start()
        
        # Force headless=False if interactive auth is enabled
        headless = self.config.headless and not self.config.interactive_auth
        
        self.browser = await self.playwright.chromium.launch(
            headless=headless,
            args=['--disable-blink-features=AutomationControlled']
        )
        
        self.context = await self.browser.new_context(
            viewport={'width': self.config.viewport_width, 'height': self.config.viewport_height},
            ignore_https_errors=True
        )
        
        # Anti-detection
        await self.context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        """)
    
    async def stop(self):
        """Cleanup browser resources."""
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
    
    async def new_page(self) -> Page:
        """Create a new page."""
        return await self.context.new_page()
    
    async def load_page(self, page: Page, url: str):
        """Load a page with proper waiting and scrolling."""
        # Use longer timeout if interactive auth is enabled
        timeout = self.config.auth_timeout if self.config.interactive_auth else self.config.page_timeout
        await page.goto(url, wait_until='domcontentloaded', timeout=timeout)
        await asyncio.sleep(self.config.wait_time)
        
        # Scroll to trigger lazy loading
        for _ in range(self.config.scroll_count):
            await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            await asyncio.sleep(self.config.scroll_delay)
    
    async def scroll_padlet(self, page: Page):
        """Special scrolling for Padlet to load all cards."""
        await page.evaluate("""
            async () => {
                // Find all scrollable containers
                const scrollables = Array.from(document.querySelectorAll('*')).filter(
                    el => el.scrollHeight > el.clientHeight || el.scrollWidth > el.clientWidth
                );
                
                // Scroll each container
                for (const el of scrollables) {
                    el.scrollTop = el.scrollHeight;
                    el.scrollLeft = el.scrollWidth;
                    await new Promise(r => setTimeout(r, 500));
                    el.scrollTop = 0;
                    el.scrollLeft = 0;
                    await new Promise(r => setTimeout(r, 500));
                }
                
                window.scrollTo(0, 0);
            }
        """)


class URLManager:
    """Manages URL queue and filtering."""
    
    def __init__(self, start_url: str, config: Config):
        self.start_domain = urlparse(start_url).netloc
        self.config = config
        
        self.visited = set()
        self.queue = deque()
        self.failed = {}
    
    def should_crawl(self, url: str, depth: int) -> bool:
        """Check if URL should be crawled."""
        if not url or url in self.visited:
            return False
        
        if depth > self.config.max_depth:
            return False
        
        if len(self.visited) >= self.config.max_pages:
            return False
        
        # Only crawl same domain by default
        if urlparse(url).netloc != self.start_domain:
            return False
        
        return True
    
    def normalize_url(self, url: str, base_url: str = "") -> str:
        """Normalize URL."""
        if not url or url.startswith(('#', 'javascript:', 'mailto:')):
            return None
        
        absolute = urljoin(base_url, url) if base_url else url
        parsed = urlparse(absolute)
        
        return urlunparse((
            parsed.scheme, parsed.netloc,
            parsed.path.rstrip('/') or '/',
            parsed.params, parsed.query, ''
        ))
    
    def add_url(self, url: str, source_url: str, depth: int) -> bool:
        """Add URL to queue if it should be crawled. Returns True if added."""
        normalized = self.normalize_url(url, source_url)
        if normalized and self.should_crawl(normalized, depth):
            self.queue.append((normalized, depth))
            return True
        return False
    
    def get_next(self) -> Optional[tuple]:
        """Get next URL to crawl."""
        return self.queue.popleft() if self.queue else None
    
    def mark_visited(self, url: str):
        """Mark URL as visited."""
        self.visited.add(url)


# ============================================================================
# MAIN CRAWLER
# ============================================================================

class Crawler:
    """Main crawler class with simplified interface."""
    
    def __init__(self, config: Config):
        self.config = config
        self.extractor = ContentExtractor(config)
        self.browser_controller = BrowserController(config)
        self.results = {}
        self.stats = {
            'pages_crawled': 0,
            'total_chars': 0,
            'iframes_extracted': 0,
            'start_time': None,
            'end_time': None
        }
        self.main_page = None  # Persistent page for interactive auth
        self.user_cancelled = False  # Track if user cancelled
    
    async def __aenter__(self):
        await self.browser_controller.start()
        return self
    
    async def __aexit__(self, *args):
        # Close main page if it exists
        if self.main_page:
            try:
                await self.main_page.close()
            except:
                pass
        await self.browser_controller.stop()
    
    async def crawl(self, start_url: str) -> Dict[str, Any]:
        """
        Main crawl method.
        
        Args:
            start_url: URL to start crawling from
            
        Returns:
            Dictionary with crawled content
        """
        self.stats['start_time'] = datetime.now()
        
        if self.config.verbose:
            print(f"\n{'='*60}")
            print(f"🌐 Starting crawl: {start_url}")
            print(f"📊 Config: {self.config.max_pages} pages, depth {self.config.max_depth}")
            if self.config.interactive_auth:
                print(f"🔐 Interactive authentication enabled")
            print(f"{'='*60}\n")
        
        # Initialize URL manager
        url_manager = URLManager(start_url, self.config)
        url_manager.add_url(start_url, "", 0)
        
        # Handle interactive authentication setup
        if self.config.interactive_auth:
            # Create persistent main page for UI
            self.main_page = await self.browser_controller.new_page()
            await self.browser_controller.load_page(self.main_page, start_url)
            
            # Setup and show authentication UI
            if self.browser_controller.authenticator:
                authenticated = await self.browser_controller.authenticator.handle_authentication(
                    self.main_page, start_url, self.browser_controller.context, force_ui=True
                )
                
                if not authenticated:
                    self.user_cancelled = True
                    if self.config.verbose:
                        print("❌ User cancelled authentication")
                    return {}
                
                # Keep the main page open for UI persistence
                if self.config.verbose:
                    print("✅ Authentication successful, starting crawl...")
        
        # Crawl loop
        while True:
            # Check if user cancelled
            if self.user_cancelled:
                if self.config.verbose:
                    print("🛑 Crawl cancelled by user")
                break
            
            # Check if we've reached max pages
            if self.stats['pages_crawled'] >= self.config.max_pages:
                if self.config.verbose:
                    print(f"📊 Reached max pages limit ({self.config.max_pages})")
                break
            
            # Check if main page is still alive (for interactive auth)
            if self.config.interactive_auth and self.main_page:
                try:
                    # Try to evaluate something on the page to check if it's still alive
                    await self.main_page.evaluate('() => true')
                except:
                    if self.config.verbose:
                        print("⚠️ Main page was closed unexpectedly, stopping crawl")
                    break
            
            next_item = url_manager.get_next()
            if not next_item:
                break
            
            url, depth = next_item
            url_manager.mark_visited(url)
            
            if self.config.verbose:
                print(f"[{self.stats['pages_crawled']+1}/{self.config.max_pages}] Crawling: {url}")
            
            await self._crawl_page(url, depth, url_manager)
            
            # Save results incrementally after each page
            if self.config.output_dir:
                self._save_results()
            
            if self.config.crawl_delay > 0:
                await asyncio.sleep(self.config.crawl_delay)
        
        self.stats['end_time'] = datetime.now()
        
        # Save results if configured
        if self.config.output_dir:
            self._save_results()
        
        if self.config.verbose:
            self._print_summary()
        
        return self.results
    
    async def _crawl_page(self, url: str, depth: int, url_manager: URLManager):
        """Crawl a single page."""
        page = None
        
        # Use main page if interactive auth is enabled, otherwise create new page
        if self.config.interactive_auth and self.main_page:
            page = self.main_page
            
            # Verify main page is still valid
            try:
                await page.evaluate('() => true')
            except:
                if self.config.verbose:
                    print("⚠️ Main page was closed, cannot continue crawling")
                raise Exception("Main page closed unexpectedly")
            
            # Navigate to new URL in same page
            await page.goto(url, wait_until='domcontentloaded', timeout=self.config.page_timeout)
            await asyncio.sleep(self.config.wait_time)
            
            # Check if user cancelled via the floating UI
            try:
                cancelled = await page.evaluate('() => window.__ccproCancel === true')
                if cancelled:
                    self.user_cancelled = True
                    raise Exception("User cancelled crawling")
            except Exception as e:
                if "User cancelled" in str(e):
                    raise
                # Ignore other errors during cancel check
        else:
            page = await self.browser_controller.new_page()
            await self.browser_controller.load_page(page, url)
        
        try:
            
            # Get content
            html = await page.content()
            title = await page.title()
            
            # Convert to markdown
            markdown = self.extractor.to_markdown(html, url)
            
            # Extract iframes if configured
            if self.config.extract_iframes:
                try:
                    iframes = await self.extractor.extract_iframes(page)
                    
                    if iframes:
                        if self.config.verbose:
                            print(f"  📎 Found {len(iframes)} iframes")
                        
                        # Process each iframe (with error handling)
                        try:
                            iframe_content = await self._process_iframes(iframes, depth)
                            if iframe_content:
                                markdown += "\n\n---\n## Embedded Content\n" + iframe_content
                        except Exception as iframe_error:
                            if self.config.verbose:
                                print(f"  ⚠️ Error processing iframes: {str(iframe_error)[:100]}")
                            markdown += f"\n\n---\n## Embedded Content\n⚠️ Failed to extract some iframe content: {str(iframe_error)[:100]}"
                except Exception as e:
                    if self.config.verbose:
                        print(f"  ⚠️ Failed to extract iframes: {str(e)[:100]}")
            
            # Extract links for further crawling
            if self.config.follow_links and depth < self.config.max_depth:
                try:
                    links = await self.extractor.extract_links(page)
                    added_count = 0
                    for link in links:
                        if url_manager.add_url(link['href'], url, depth + 1):
                            added_count += 1
                    
                    if self.config.verbose:
                        print(f"  🔗 Found {len(links)} links, added {added_count} new URLs to crawl")
                except Exception as e:
                    if self.config.verbose:
                        print(f"  ⚠️ Failed to extract links: {str(e)[:100]}")
            elif self.config.verbose and self.config.follow_links:
                print(f"  ⛔ Not following links (depth {depth} >= max_depth {self.config.max_depth})")
            
            # Store result
            self.results[url] = {
                'title': title,
                'markdown': markdown,
                'depth': depth,
                'length': len(markdown)
            }
            
            self.stats['pages_crawled'] += 1
            self.stats['total_chars'] += len(markdown)
            
            if self.config.verbose:
                print(f"  ✅ Extracted {len(markdown):,} chars")
            
        except Exception as e:
            if self.config.verbose:
                print(f"  ❌ Error: {str(e)[:100]}")
            self.results[url] = {
                'title': 'Error',
                'markdown': f"Failed to extract: {str(e)}",
                'depth': depth,
                'error': str(e)
            }
        
        finally:
            # Only close if not using persistent main page
            if not self.config.interactive_auth or page != self.main_page:
                await page.close()
    
    async def _process_iframes(self, iframes: List[Dict], depth: int) -> str:
        """Process embedded iframes."""
        content_parts = []
        
        for i, iframe in enumerate(iframes, 1):
            iframe_url = iframe['url']
            iframe_type = iframe.get('type', 'generic')
            
            if self.config.verbose:
                print(f"    🎯 Processing iframe {i}/{len(iframes)}: {iframe_type}")
            
            # Skip certain iframes
            if any(skip in iframe_url for skip in ['googletagmanager', 'recaptcha']):
                continue
            
            iframe_page = None
            try:
                # Create new page for iframe (separate from main page)
                iframe_page = await self.browser_controller.new_page()
                
                # Special handling for Padlet
                if iframe_type == 'padlet' and self.config.extract_padlet_cards:
                    await iframe_page.goto(iframe_url, wait_until='domcontentloaded')
                    await asyncio.sleep(3)
                    await self.browser_controller.scroll_padlet(iframe_page)
                    
                    cards = await self.extractor.extract_padlet_cards(iframe_page)
                    
                    if cards:
                        content_parts.append(f"\n### 📌 Padlet: {iframe['title']}")
                        content_parts.append(f"**URL**: {iframe_url}\n")
                        content_parts.append(f"**{len(cards)} cards found:**\n")
                        
                        for card in cards:
                            if card.get('isPinned'):
                                content_parts.append(f"\n**📌 Card {card['index']}: {card.get('title', 'Untitled')}**")
                            else:
                                content_parts.append(f"\n**Card {card['index']}: {card.get('title', 'Untitled')}**")
                            
                            if card.get('author'):
                                content_parts.append(f"- Author: {card['author']}")
                            if card.get('body'):
                                content_parts.append(f"- Content: {card['body']}")
                            if card.get('attachmentUrl'):
                                content_parts.append(f"- [Attachment]({card['attachmentUrl']})")
                
                # Regular iframe extraction
                else:
                    await self.browser_controller.load_page(iframe_page, iframe_url)
                    html = await iframe_page.content()
                    iframe_md = self.extractor.to_markdown(html, iframe_url)
                    
                    icon = {'youtube': '🎥', 'google_docs': '📄', 'padlet': '📌'}.get(iframe_type, '🔗')
                    content_parts.append(f"\n### {icon} {iframe['title']}")
                    content_parts.append(f"**URL**: {iframe_url}\n")
                    content_parts.append(iframe_md[:2000] + "..." if len(iframe_md) > 2000 else iframe_md)
                
                self.stats['iframes_extracted'] += 1
                
            except Exception as e:
                if self.config.verbose:
                    print(f"    ❌ Failed to process iframe: {str(e)[:100]}")
                content_parts.append(f"\n### ❌ {iframe['title']}")
                content_parts.append(f"Failed to extract: {str(e)[:100]}")
            
            finally:
                # Always close iframe page if it was created
                if iframe_page:
                    try:
                        await iframe_page.close()
                    except:
                        pass  # Page might already be closed
        
        return '\n'.join(content_parts)
    
    def _save_results(self):
        """Save results to file."""
        output_path = Path(self.config.output_dir)
        output_path.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if self.config.save_as_json:
            # Save as JSON
            json_file = output_path / f"crawl_{timestamp}.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, ensure_ascii=False)
            print(f"\n📁 Results saved to: {json_file}")
        else:
            # Save as markdown
            md_file = output_path / f"crawl_{timestamp}.md"
            with open(md_file, 'w', encoding='utf-8') as f:
                for url, data in self.results.items():
                    f.write(f"# {data['title']}\n")
                    f.write(f"**URL**: {url}\n\n")
                    f.write(data['markdown'])
                    f.write("\n\n---\n\n")
            print(f"\n📁 Results saved to: {md_file}")
    
    def _print_summary(self):
        """Print crawl summary."""
        duration = (self.stats['end_time'] - self.stats['start_time']).total_seconds()
        
        print(f"\n{'='*60}")
        print(f"📊 Crawl Complete")
        print(f"{'='*60}")
        print(f"⏱️  Duration: {duration:.1f} seconds")
        print(f"📄 Pages: {self.stats['pages_crawled']}")
        print(f"📝 Content: {self.stats['total_chars']:,} characters")
        print(f"🎯 Iframes: {self.stats['iframes_extracted']}")
        print(f"⚡ Speed: {self.stats['pages_crawled']/duration:.1f} pages/sec")


# ============================================================================
# QUICK TEST
# ============================================================================

async def test():
    """Test the refactored crawler."""
    
    # Test 1: Simple usage (zero config)
    print("Test 1: Simple usage")
    content = await crawl("https://example.com")
    print(f"Got {len(content)} chars of content\n")
    
    # Test 2: With config
    print("Test 2: With custom config")
    config = ccpro(
        max_pages=2,
        follow_links=True,
        extract_iframes=True,
        verbose=True
    )
    
    url = "https://example.com"
    content = await crawl(url, config)
    
    if isinstance(content, dict):
        print(f"\nCrawled {len(content)} pages")
        for url, markdown in content.items():
            print(f"  - {url}: {len(markdown)} chars")
    else:
        print(f"\nSingle page: {len(content)} chars")


async def test_interactive():
    """Test interactive authentication with example.com."""
    
    config = ccpro(
        interactive_auth=True,
        max_pages=3,  # Crawl 3 pages
        max_depth=2,  # Allow following links up to depth 2
        follow_links=True,
        extract_iframes=True,
        extract_padlet_cards=True,
        output_dir="ccpro_outputs",
        verbose=True
    )
    
    # Use example.com for testing (replace with actual protected site when needed)
    url = "https://example.com"
    
    print("\n" + "="*80)
    print("🔐 TESTING INTERACTIVE AUTH")
    print("="*80)
    print("📋 Instructions:")
    print("   1. Browser will open with the site")
    print("   2. Click the login link if needed")
    print("   3. Enter credentials and login")
    print("   4. Click 'Start Crawling' when ready")
    print("   5. System will crawl multiple pages")
    print("="*80)
    
    try:
        content = await crawl(url, config)
        
        if content:
            if isinstance(content, dict):
                print(f"\n✅ SUCCESS! Crawled {len(content)} pages:")
                total_chars = 0
                for page_url, page_content in content.items():
                    chars = len(page_content)
                    total_chars += chars
                    print(f"   • {page_url[:80]}...")
                    print(f"     {chars:,} characters")
                print(f"\n📊 Total content: {total_chars:,} characters")
            else:
                print(f"\n✅ SUCCESS! Crawled single page: {len(content):,} characters")
        else:
            print("\n❌ No content returned (possibly cancelled)")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # asyncio.run(test())
    # asyncio.run(test_interactive())  # Uncomment to test interactive auth
    pass