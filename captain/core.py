"""
⚓ CAPTAIN AI Core Engine
Main AI class for web search and answer generation with citations.
"""

from openai import OpenAI
from duckduckgo_search import DDG
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import os


class PerplexityClone:
    """A Perplexity-like AI that searches the web and gives cited answers"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the AI with your OpenAI API key.
        
        Get your free API key at: https://platform.openai.com/signup
        First $5 credit is free for new users.
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "API key required! Set OPENAI_API_KEY environment variable "
                "or pass it as argument.\n"
                "Get free key: https://platform.openai.com/signup"
            )
        
        self.client = OpenAI(api_key=self.api_key)
        self.search_engine = DDG()
        self.conversation_history = []
    
    def search_web(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search the web and return results with URLs and snippets"""
        results = []
        
        try:
            search_results = self.search_engine.text(query, max_results=max_results)
            
            for result in search_results:
                results.append({
                    'title': result.get('title', ''),
                    'url': result.get('href', ''),
                    'snippet': result.get('body', '')
                })
        except Exception as e:
            print(f"⚠️ Search error: {e}")
        
        return results
    
    def fetch_content(self, url: str, max_length: int = 1500) -> str:
        """Fetch and clean content from a URL"""
        if not url or url.startswith('javascript'):
            return ""
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove unwanted elements
            for tag in soup(["script", "style", "nav", "footer", "header", "form"]):
                tag.decompose()
            
            # Get text and clean it
            text = soup.get_text(separator='\n', strip=True)
            
            # Remove extra whitespace
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            cleaned_text = '\n'.join(lines)
            
            return cleaned_text[:max_length] if cleaned_text else ""
            
        except Exception as e:
            return ""
    
    def build_context_with_citations(self, search_results: List[Dict]) -> tuple:
        """
        Build context string and citation map from search results.
        Returns: (context_string, citation_map)
        """
        context_parts = []
        citation_map = {}  # source_number -> url
        
        valid_sources = 0
        
        for i, result in enumerate(search_results, 1):
            if not result['url'] or result['url'].startswith('javascript'):
                continue
            
            # Fetch content
            content = self.fetch_content(result['url'])
            
            if content:  # Only include if we got content
                valid_sources += 1
                citation_map[valid_sources] = result['url']
                
                context_parts.append(
                    f"[Source {valid_sources}]: {result['title']}\n"
                    f"URL: {result['url']}\n"
                    f"Content: {content}\n"
                )
        
        context = "\n\n".join(context_parts)
        return context, citation_map
    
    def ask(self, query: str, use_history: bool = True) -> str:
        """
        Main function: Search the web + generate answer with citations.
        
        Args:
            query: The question to answer
            use_history: Whether to include conversation history for follow-ups
        
        Returns:
            Answer with inline citations like [source: 1]
        """
        
        print(f"\n🔍 Searching for: \"{query}\"")
        
        # Step 1: Search the web
        search_results = self.search_web(query, max_results=8)
        
        if not search_results:
            return "❌ I couldn't find any relevant information online."
        
        print(f"✅ Found {len(search_results)} search results")
        
        # Step 2: Build context from search results
        context, citation_map = self.build_context_with_citations(search_results)
        
        if not context:
            return "⚠️ Found search results but couldn't fetch content from any sources."
        
        print(f"📚 Retrieved content from {len(citation_map)} sources")
        
        # Step 3: Build the prompt with conversation history if needed
        if use_history and self.conversation_history:
            history_text = "\n".join([
                f"User: {msg['user']}\nAssistant: {msg['assistant']}"
                for msg in self.conversation_history[-3:]  # Last 3 turns
            ])
            history_prompt = f"""Previous conversation:
{history_text}

"""
        else:
            history_prompt = ""
        
        # System prompt
        system_prompt = """You are CAPTAIN AI, an AI assistant that provides accurate, well-researched answers with citations. 

Rules:
1. Use the search results to answer the question accurately
2. Cite sources using [source: 1] format AFTER each factual claim (not at the end)
3. Be concise, factual, and helpful
4. If information is contradictory, mention that clearly
5. If you don't find relevant information, say so honestly
6. Never make up sources or citations
7. Include a \"Sources\" section at the end listing all used URLs

Format your answer clearly with headings if needed."""
        
        # User prompt
        user_prompt = f"""{history_prompt}Search Results:
{context}

Question: {query}

Answer the question using the search results above. Include inline citations like [source: 1] after each factual claim. End with a \"Sources\" section listing all URLs you used."""
        
        print("🤖 Generating answer with citations...")
        
        # Step 4: Generate response with LLM
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,  # Lower = more factual, less creative
                max_tokens=1500,
                top_p=0.9
            )
            
            answer = response.choices[0].message.content
            
            # Store in conversation history
            self.conversation_history.append({
                'user': query,
                'assistant': answer
            })
            
            # Keep history manageable
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]
            
            print("✅ Answer generated!\n")
            return answer
            
        except Exception as e:
            error_msg = str(e)
            if "API key" in error_msg.lower():
                return f"❌ Invalid API key. Get a free key at: https://platform.openai.com/signup"
            elif "rate limit" in error_msg.lower():
                return f"❌ Rate limit exceeded. Wait a moment and try again."
            else:
                return f"❌ Error generating response: {e}"
    
    def reset_conversation(self):
        """Clear conversation history for a fresh start"""
        self.conversation_history = []
        print("🗑️ Conversation history cleared.")