import os
import re

# Language configurations
languages = {
    'es': {'name': 'Español', 'flag': '🇪🇸', 'dir': 'ltr'},
    'fr': {'name': 'Français', 'flag': '🇫🇷', 'dir': 'ltr'},
    'pt': {'name': 'Português', 'flag': '🇵🇹', 'dir': 'ltr'},
    'ca': {'name': 'Català', 'flag': '🇪🇸', 'dir': 'ltr'},
    'ar': {'name': 'العربية', 'flag': '🇸🇦', 'dir': 'rtl'},
    'ur': {'name': 'اردو', 'flag': '🇵🇰', 'dir': 'rtl'},
}

# Pages to create (excluding index which already exists)
pages = [
    'about', 'services', 'software-development', 'app-development', 
    'web-development', 'lead-generation', 'call-center', 'projects',
    'gallery', 'pricing', 'faq', 'contact', 'blog', 'testimonials',
    'industries', 'case-study', 'free-consultation', 'request-quote',
    'book-a-call', 'privacy-policy', 'terms-and-conditions', 'refund-policy',
    'cookie-policy', 'gdpr-compliance'
]

# Read English pages as templates
for page in pages:
    en_path = f'{page}/index.html'
    if os.path.exists(en_path):
        with open(en_path, 'r') as f:
            content = f.read()
        
        for lang, config in languages.items():
            # Create directory
            lang_page_dir = f'{lang}/{page}'
            os.makedirs(lang_page_dir, exist_ok=True)
            
            # Modify content for this language
            new_content = content
            
            # Update html lang attribute
            if config['dir'] == 'rtl':
                new_content = re.sub(r'<html lang="en">', f'<html lang="{lang}" dir="rtl">', new_content)
            else:
                new_content = re.sub(r'<html lang="en">', f'<html lang="{lang}">', new_content)
            
            # Update canonical URL
            new_content = re.sub(
                r'<link rel="canonical" href="https://appsyncinnovations\.com/' + page + r'/"',
                f'<link rel="canonical" href="https://appsyncinnovations.com/{lang}/{page}/"',
                new_content
            )
            
            # Update navigation links to include language prefix
            nav_links = [
                ('href="/"', f'href="/{lang}/"'),
                ('href="/about/"', f'href="/{lang}/about/"'),
                ('href="/services/"', f'href="/{lang}/services/"'),
                ('href="/software-development/"', f'href="/{lang}/software-development/"'),
                ('href="/app-development/"', f'href="/{lang}/app-development/"'),
                ('href="/web-development/"', f'href="/{lang}/web-development/"'),
                ('href="/lead-generation/"', f'href="/{lang}/lead-generation/"'),
                ('href="/call-center/"', f'href="/{lang}/call-center/"'),
                ('href="/projects/"', f'href="/{lang}/projects/"'),
                ('href="/pricing/"', f'href="/{lang}/pricing/"'),
                ('href="/contact/"', f'href="/{lang}/contact/"'),
                ('href="/gallery/"', f'href="/{lang}/gallery/"'),
                ('href="/testimonials/"', f'href="/{lang}/testimonials/"'),
                ('href="/blog/"', f'href="/{lang}/blog/"'),
                ('href="/free-consultation/"', f'href="/{lang}/free-consultation/"'),
                ('href="/request-quote/"', f'href="/{lang}/request-quote/"'),
                ('href="/book-a-call/"', f'href="/{lang}/book-a-call/"'),
                ('href="/privacy-policy/"', f'href="/{lang}/privacy-policy/"'),
                ('href="/terms-and-conditions/"', f'href="/{lang}/terms-and-conditions/"'),
                ('href="/refund-policy/"', f'href="/{lang}/refund-policy/"'),
                ('href="/cookie-policy/"', f'href="/{lang}/cookie-policy/"'),
                ('href="/gdpr-compliance/"', f'href="/{lang}/gdpr-compliance/"'),
                ('href="/industries/"', f'href="/{lang}/industries/"'),
                ('href="/case-study/"', f'href="/{lang}/case-study/"'),
                ('href="/faq/"', f'href="/{lang}/faq/"'),
            ]
            
            for old, new in nav_links:
                new_content = new_content.replace(old, new)
            
            # Update current language in switcher
            new_content = new_content.replace(
                f'<li data-lang="{lang}" data-url="/{lang}/">',
                f'<li data-lang="{lang}" data-url="/{lang}/" class="active">'
            )
            new_content = new_content.replace(
                '<li data-lang="en" data-url="/" class="active">',
                '<li data-lang="en" data-url="/">'
            )
            
            # Update current language button display
            new_content = re.sub(
                r'<span class="lang-flag">🇺🇸</span>\s*<span class="lang-name">EN</span>',
                f'<span class="lang-flag">{config["flag"]}</span>\n                <span class="lang-name">{lang.upper()}</span>',
                new_content
            )
            
            # Write file
            output_path = f'{lang_page_dir}/index.html'
            with open(output_path, 'w') as f:
                f.write(new_content)
            
            print(f'Created: {output_path}')

print("\nDone! All language pages created.")
