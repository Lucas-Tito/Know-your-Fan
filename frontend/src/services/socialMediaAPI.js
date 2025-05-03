// src/services/socialMediaAPI.js
export const linkBlueskyAccount = async (credentials) => {
    const response = await fetch('/api/social/link', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        platform: 'bluesky',
        credentials
      })
    });
    return response.json();
};