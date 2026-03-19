---
name: baoyu-fetch-tweet
description: Fetches Twitter/X content using x-tweet-fetcher. Use when user provides Twitter/X links and needs content extraction.
---

# Fetch Tweet

Fetches Twitter/X content using the global x-tweet-fetcher tool.

## Usage

When user provides a Twitter/X link:

```bash
python3 ~/.openclaw/tools/x-tweet-fetcher/scripts/fetch_tweet.py --url "URL"
```

## Example

```bash
python3 ~/.openclaw/tools/x-tweet-fetcher/scripts/fetch_tweet.py \
  --url "https://x.com/username/status/123456"
```

## Output

Returns JSON with:
- tweet.author: Author name
- tweet.screen_name: Username
- tweet.article.title: Tweet title
- tweet.article.full_text: Full content
- tweet.likes: Like count
- tweet.retweets: Retweet count
- tweet.views: View count
