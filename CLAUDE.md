# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
npm start          # Start dev server at http://localhost:3000
npm run build      # Build static site into build/
npm run serve      # Serve the built site locally
npm run clear      # Clear Docusaurus cache (use when encountering stale build issues)
```

## Architecture

This is a [Docusaurus v3](https://docusaurus.io/) personal engineering blog by ManhPT, written primarily in Vietnamese.

**Content sections** (each is a separate Docusaurus plugin instance):
- `blog/` → served at `/` (root) — main blog, configured as the site homepage
- `news/` → served at `/news` — short news posts
- `apps/` → served at `/apps` — apps documentation (docs plugin)

**Key config**: `docusaurus.config.js`
- The `docs` preset plugin is **disabled**; the `blog` preset takes the root route
- Default locale is `vi` (Vietnamese)
- `src/pages/index.js` was removed to fix duplicate route warning. The blog now serves as the homepage without conflicts.

## Blog Post Conventions

Blog posts live in `blog/YYYY-MM-DD-slug/index.md` (folder format). Each post must:

1. **Include a `<!-- truncate -->` marker** — required to create a preview on the listing page (`onUntruncatedBlogPosts: "warn"`)
2. **Use only pre-defined tags** from `blog/tags.yml` — inline tags trigger a warning (`onInlineTags: "warn"`). Add new tags to `blog/tags.yml` before using them.
3. **Reference authors** defined in `blog/authors.yml`. The only current author is `manhpt`.

News posts follow the same rules but use `news/authors.yml`.

## Frontmatter Template

```yaml
---
title: "Post title"
slug: url-slug
authors: [manhpt]
tags: [existing-tag-from-tags-yml]
date: YYYY-MM-DD
description: "Short description for SEO/preview"
---

Intro paragraph visible in listing...

<!-- truncate -->

Rest of the post...
```
