#!/usr/bin/env python3
"""
Language Conversion Script
Updates Spanish (es) HTML pages to match English page structure.
Only updates inner HTML content - preserves navbar, language switcher, floating buttons, and footer.
"""

import os
import re

EN_TO_ES_MAPPING = {
    'about': 'es/sobre-nosotros',
    'services': 'es/servicios',
    'software-development': 'es/desarrollo-software',
    'app-development': 'es/desarrollo-aplicaciones',
    'web-development': 'es/desarrollo-web',
    'ai-development': 'es/desarrollo-ia',
    'seo-services': 'es/servicios-seo',
    'lead-generation': 'es/generacion-leads',
    'call-center': 'es/centro-llamadas',
    'data-security-db-maintenance': 'es/seguridad-datos-mantenimiento-bd',
    'projects': 'es/proyectos',
    'pricing': 'es/precios',
    'contact': 'es/contacto',
    'testimonials': 'es/testimonios',
    'blog': 'es/blog',
    'gallery': 'es/galeria',
    'industries': 'es/industrias',
    'case-study': 'es/caso-estudio',
    'faq': 'es/preguntas-frecuentes',
    'privacy-policy': 'es/politica-privacidad',
    'terms-and-conditions': 'es/terminos-condiciones',
    'refund-policy': 'es/politica-reembolso',
    'cookie-policy': 'es/politica-cookies',
    'gdpr-compliance': 'es/cumplimiento-rgpd',
    'free-consultation': 'es/consulta-gratuita',
    'request-quote': 'es/solicitar-presupuesto',
    'book-a-call': 'es/reservar-llamada',
}

def extract_inner_content(html):
    """Extract content between </header> and <footer>"""
    header_end = html.find('</header>')
    if header_end == -1:
        return None, None, None
    header_end += len('</header>')
    
    footer_start = html.find('<footer>')
    if footer_start == -1:
        floating_start = html.find('<div class="floating-buttons">')
        if floating_start == -1:
            return None, None, None
        footer_start = floating_start
    
    before = html[:header_end]
    inner = html[header_end:footer_start]
    after = html[footer_start:]
    
    return before, inner.strip(), after

def get_es_header_footer(es_html):
    """Get the header and footer parts from Spanish HTML (to preserve navbar, lang switcher, footer, floating buttons)"""
    header_end = es_html.find('</header>')
    if header_end == -1:
        return None, None
    header_end += len('</header>')
    
    footer_start = es_html.find('<footer>')
    if footer_start == -1:
        floating_start = es_html.find('<div class="floating-buttons">')
        if floating_start == -1:
            return None, None
        footer_start = floating_start
    
    before = es_html[:header_end]
    after = es_html[footer_start:]
    
    return before, after

def update_spanish_page(en_folder, es_folder):
    """Update a single Spanish page with English page structure"""
    en_path = f"{en_folder}/index.html"
    es_path = f"{es_folder}/index.html"
    
    if not os.path.exists(en_path):
        print(f"  English file not found: {en_path}")
        return False
    
    if not os.path.exists(es_path):
        print(f"  Spanish file not found: {es_path}")
        return False
    
    with open(en_path, 'r', encoding='utf-8') as f:
        en_html = f.read()
    
    with open(es_path, 'r', encoding='utf-8') as f:
        es_html = f.read()
    
    _, en_inner, _ = extract_inner_content(en_html)
    es_before, es_after = get_es_header_footer(es_html)
    
    if en_inner is None or es_before is None:
        print(f"  Could not extract content from {en_folder} or {es_folder}")
        return False
    
    new_es_html = es_before + "\n\n" + en_inner + "\n\n" + es_after
    
    with open(es_path, 'w', encoding='utf-8') as f:
        f.write(new_es_html)
    
    print(f"  Updated: {es_path}")
    return True

def main():
    print("=" * 60)
    print("Language Conversion Script")
    print("Updating Spanish pages with English page structure")
    print("(Preserving navbar, language switcher, floating buttons, footer)")
    print("=" * 60)
    print()
    
    success_count = 0
    fail_count = 0
    
    for en_folder, es_folder in EN_TO_ES_MAPPING.items():
        print(f"Processing: {en_folder} -> {es_folder}")
        if update_spanish_page(en_folder, es_folder):
            success_count += 1
        else:
            fail_count += 1
    
    print()
    print("=" * 60)
    print(f"Conversion complete!")
    print(f"  Success: {success_count}")
    print(f"  Failed: {fail_count}")
    print("=" * 60)

if __name__ == "__main__":
    main()
