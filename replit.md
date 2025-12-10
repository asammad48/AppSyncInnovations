# AppSync Innovations Website

## Overview
A multilingual static website for AppSync Innovations - a SaaS company offering software development, app development, web development, lead generation, and call center services.

## Project Structure
```
/                     - Root (English pages)
/assets/css/          - Stylesheets
/assets/js/           - JavaScript files
/assets/images/       - Image assets
/assets/icons/        - Icons and favicons
/es/                  - Spanish pages
/fr/                  - French pages
/pt/                  - Portuguese pages
/ca/                  - Catalan pages
/ar/                  - Arabic pages (RTL)
/ur/                  - Urdu pages (RTL)
```

## Languages Supported
- English (root - default)
- Spanish (/es/)
- French (/fr/)
- Portuguese (/pt/)
- Catalan (/ca/)
- Arabic (/ar/) - RTL
- Urdu (/ur/) - RTL

## Pages
- Homepage
- About, Services, Contact, Pricing, FAQ
- Service pages: Software Development, App Development, Web Development, Lead Generation, Call Center, AI Development, SEO Services
- Projects, Gallery, Blog, Testimonials, Industries, Case Studies
- Marketing: Free Consultation, Request Quote, Book a Call
- Legal: Privacy Policy, Terms & Conditions, Refund Policy, Cookie Policy, GDPR Compliance, Lead Vendor Legal

## Recent Updates (December 2025)
- Enhanced RTL support for Arabic (ar) and Urdu (ur) with proper navigation and footer translations
- Added AI Development service page (/ai-development/)
- Added SEO Services page (/seo-services/)
- Added Lead Vendor Legal page with TCPA, GDPR, CCPA compliance (/lead-vendor-legal/)
- Shortened navbar items to single words to prevent wrapping issues
- Updated all language pages with proper navigation links to their respective language versions

## Running the Server
```bash
python server.py
```
Server runs on port 5000.

## SEO Features
- Clean URLs (no .html extensions)
- Hreflang tags for multilingual SEO
- Canonical URLs
- Open Graph and Twitter Cards
- XML Sitemap
- robots.txt
- JSON-LD Schema markup
- PWA manifest

## Technologies
- HTML5, CSS3, JavaScript
- Python (static file server)
- No framework dependencies - pure static site
