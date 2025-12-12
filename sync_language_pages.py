#!/usr/bin/env python3
"""
Language Page Sync Script
Copies English page structure to all language folders.
Preserves navbar, language switcher, footer, and floating buttons from target language pages.
User will translate the content manually.
"""

import os
import re

LANGUAGES = {
    'ar': {
        'name': 'Arabic',
        'dir': 'rtl',
        'pages': {
            '': 'ar',
            'about': 'ar/عن-الشركة',
            'services': 'ar/الخدمات',
            'software-development': 'ar/تطوير-البرمجيات',
            'app-development': 'ar/تطوير-التطبيقات',
            'web-development': 'ar/تطوير-المواقع',
            'ai-development': 'ar/تطوير-الذكاء-الاصطناعي',
            'seo-services': 'ar/خدمات-تحسين-محركات-البحث',
            'lead-generation': 'ar/توليد-العملاء-المحتملين',
            'call-center': 'ar/مركز-الاتصال',
            'data-security-db-maintenance': 'ar/امن-البيانات-صيانة-قواعد-البيانات',
            'projects': 'ar/المشاريع',
            'pricing': 'ar/الأسعار',
            'contact': 'ar/اتصل-بنا',
            'testimonials': 'ar/آراء-العملاء',
            'blog': 'ar/المدونة',
            'gallery': 'ar/معرض-الأعمال',
            'industries': 'ar/الصناعات',
            'case-study': 'ar/دراسة-حالة',
            'faq': 'ar/الأسئلة-الشائعة',
            'privacy-policy': 'ar/سياسة-الخصوصية',
            'terms-and-conditions': 'ar/الشروط-والأحكام',
            'refund-policy': 'ar/سياسة-الاسترداد',
            'cookie-policy': 'ar/سياسة-ملفات-تعريف-الارتباط',
            'gdpr-compliance': 'ar/الامتثال-للائحة-حماية-البيانات',
            'free-consultation': 'ar/استشارة-مجانية',
            'request-quote': 'ar/طلب-عرض-سعر',
            'book-a-call': 'ar/حجز-مكالمة',
        }
    },
    'es': {
        'name': 'Spanish',
        'dir': 'ltr',
        'pages': {
            '': 'es',
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
    },
    'fr': {
        'name': 'French',
        'dir': 'ltr',
        'pages': {
            '': 'fr',
            'about': 'fr/a-propos',
            'services': 'fr/services',
            'software-development': 'fr/developpement-logiciel',
            'app-development': 'fr/developpement-applications',
            'web-development': 'fr/developpement-web',
            'ai-development': 'fr/developpement-ia',
            'seo-services': 'fr/services-seo',
            'lead-generation': 'fr/generation-prospects',
            'call-center': 'fr/centre-appels',
            'data-security-db-maintenance': 'fr/securite-donnees-maintenance-bd',
            'projects': 'fr/projets',
            'pricing': 'fr/tarifs',
            'contact': 'fr/contact',
            'testimonials': 'fr/temoignages',
            'blog': 'fr/blog',
            'gallery': 'fr/galerie',
            'industries': 'fr/secteurs',
            'case-study': 'fr/etude-de-cas',
            'faq': 'fr/faq',
            'privacy-policy': 'fr/politique-confidentialite',
            'terms-and-conditions': 'fr/conditions-generales',
            'refund-policy': 'fr/politique-remboursement',
            'cookie-policy': 'fr/politique-cookies',
            'gdpr-compliance': 'fr/conformite-rgpd',
            'free-consultation': 'fr/consultation-gratuite',
            'request-quote': 'fr/demande-devis',
            'book-a-call': 'fr/reserver-appel',
        }
    },
    'pt': {
        'name': 'Portuguese',
        'dir': 'ltr',
        'pages': {
            '': 'pt',
            'about': 'pt/sobre-nos',
            'services': 'pt/servicos',
            'software-development': 'pt/desenvolvimento-software',
            'app-development': 'pt/desenvolvimento-aplicativos',
            'web-development': 'pt/desenvolvimento-web',
            'ai-development': 'pt/desenvolvimento-ia',
            'seo-services': 'pt/servicos-seo',
            'lead-generation': 'pt/geracao-leads',
            'call-center': 'pt/central-atendimento',
            'data-security-db-maintenance': 'pt/seguranca-dados-manutencao-bd',
            'projects': 'pt/projetos',
            'pricing': 'pt/precos',
            'contact': 'pt/contato',
            'testimonials': 'pt/depoimentos',
            'blog': 'pt/blog',
            'gallery': 'pt/galeria',
            'industries': 'pt/setores',
            'case-study': 'pt/estudo-de-caso',
            'faq': 'pt/perguntas-frequentes',
            'privacy-policy': 'pt/politica-privacidade',
            'terms-and-conditions': 'pt/termos-condicoes',
            'refund-policy': 'pt/politica-reembolso',
            'cookie-policy': 'pt/politica-cookies',
            'gdpr-compliance': 'pt/conformidade-lgpd',
            'free-consultation': 'pt/consulta-gratuita',
            'request-quote': 'pt/solicitar-orcamento',
            'book-a-call': 'pt/agendar-ligacao',
        }
    },
    'ca': {
        'name': 'Catalan',
        'dir': 'ltr',
        'pages': {
            '': 'ca',
            'about': 'ca/sobre-nosaltres',
            'services': 'ca/serveis',
            'software-development': 'ca/desenvolupament-programari',
            'app-development': 'ca/desenvolupament-aplicacions',
            'web-development': 'ca/desenvolupament-web',
            'ai-development': 'ca/desenvolupament-ia',
            'seo-services': 'ca/serveis-seo',
            'lead-generation': 'ca/generacio-clients-potencials',
            'call-center': 'ca/centre-trucades',
            'data-security-db-maintenance': 'ca/seguretat-dades-manteniment-bd',
            'projects': 'ca/projectes',
            'pricing': 'ca/preus',
            'contact': 'ca/contacte',
            'testimonials': 'ca/testimonis',
            'blog': 'ca/blog',
            'gallery': 'ca/galeria',
            'industries': 'ca/sectors',
            'case-study': 'ca/estudi-de-cas',
            'faq': 'ca/preguntes-frequents',
            'privacy-policy': 'ca/politica-privacitat',
            'terms-and-conditions': 'ca/termes-condicions',
            'refund-policy': 'ca/politica-reemborsament',
            'cookie-policy': 'ca/politica-cookies',
            'gdpr-compliance': 'ca/compliment-rgpd',
            'free-consultation': 'ca/consulta-gratuita',
            'request-quote': 'ca/sol·licitar-pressupost',
            'book-a-call': 'ca/reservar-trucada',
        }
    },
    'de': {
        'name': 'German',
        'dir': 'ltr',
        'pages': {
            '': 'de',
            'about': 'de/ueber-uns',
            'services': 'de/dienstleistungen',
            'software-development': 'de/softwareentwicklung',
            'app-development': 'de/app-entwicklung',
            'web-development': 'de/webentwicklung',
            'ai-development': 'de/ki-entwicklung',
            'seo-services': 'de/seo-dienstleistungen',
            'lead-generation': 'de/leadgenerierung',
            'call-center': 'de/callcenter',
            'data-security-db-maintenance': 'de/datensicherheit-datenbankwartung',
            'projects': 'de/projekte',
            'pricing': 'de/preise',
            'contact': 'de/kontakt',
            'testimonials': 'de/kundenstimmen',
            'blog': 'de/blog',
            'gallery': 'de/galerie',
            'industries': 'de/branchen',
            'case-study': 'de/fallstudie',
            'faq': 'de/haeufige-fragen',
            'privacy-policy': 'de/datenschutzerklaerung',
            'terms-and-conditions': 'de/agb',
            'refund-policy': 'de/rueckerstattungsrichtlinie',
            'cookie-policy': 'de/cookie-richtlinie',
            'gdpr-compliance': 'de/dsgvo-konformitaet',
            'free-consultation': 'de/kostenlose-beratung',
            'request-quote': 'de/angebot-anfordern',
            'book-a-call': 'de/gespraech-buchen',
        }
    },
    'tr': {
        'name': 'Turkish',
        'dir': 'ltr',
        'pages': {
            '': 'tr',
            'about': 'tr/hakkimizda',
            'services': 'tr/hizmetler',
            'software-development': 'tr/yazilim-gelistirme',
            'app-development': 'tr/uygulama-gelistirme',
            'web-development': 'tr/web-gelistirme',
            'ai-development': 'tr/yapay-zeka-gelistirme',
            'seo-services': 'tr/seo-hizmetleri',
            'lead-generation': 'tr/potansiyel-musteri-olusturma',
            'call-center': 'tr/cagri-merkezi',
            'data-security-db-maintenance': 'tr/veri-guvenligi-veritabani-bakimi',
            'projects': 'tr/projeler',
            'pricing': 'tr/fiyatlandirma',
            'contact': 'tr/iletisim',
            'testimonials': 'tr/referanslar',
            'blog': 'tr/blog',
            'gallery': 'tr/galeri',
            'industries': 'tr/sektorler',
            'case-study': 'tr/vaka-calismasi',
            'faq': 'tr/sss',
            'privacy-policy': 'tr/gizlilik-politikasi',
            'terms-and-conditions': 'tr/sartlar-ve-kosullar',
            'refund-policy': 'tr/iade-politikasi',
            'cookie-policy': 'tr/cerez-politikasi',
            'gdpr-compliance': 'tr/kvkk-uyumluluk',
            'free-consultation': 'tr/ucretsiz-danismanlik',
            'request-quote': 'tr/teklif-iste',
            'book-a-call': 'tr/gorusme-planla',
        }
    },
    'id': {
        'name': 'Indonesian',
        'dir': 'ltr',
        'pages': {
            '': 'id',
            'about': 'id/tentang-kami',
            'services': 'id/layanan',
            'software-development': 'id/pengembangan-perangkat-lunak',
            'app-development': 'id/pengembangan-aplikasi',
            'web-development': 'id/pengembangan-web',
            'ai-development': 'id/pengembangan-ai',
            'seo-services': 'id/layanan-seo',
            'lead-generation': 'id/generasi-prospek',
            'call-center': 'id/pusat-panggilan',
            'data-security-db-maintenance': 'id/keamanan-data-pemeliharaan-database',
            'projects': 'id/proyek',
            'pricing': 'id/harga',
            'contact': 'id/kontak',
            'testimonials': 'id/testimoni',
            'blog': 'id/blog',
            'gallery': 'id/galeri',
            'industries': 'id/industri',
            'case-study': 'id/studi-kasus',
            'faq': 'id/faq',
            'privacy-policy': 'id/kebijakan-privasi',
            'terms-and-conditions': 'id/syarat-ketentuan',
            'refund-policy': 'id/kebijakan-pengembalian',
            'cookie-policy': 'id/kebijakan-cookie',
            'gdpr-compliance': 'id/kepatuhan-gdpr',
            'free-consultation': 'id/konsultasi-gratis',
            'request-quote': 'id/minta-penawaran',
            'book-a-call': 'id/jadwalkan-panggilan',
        }
    },
    'ur': {
        'name': 'Urdu',
        'dir': 'rtl',
        'pages': {
            '': 'ur',
            'about': 'ur/ہمارے-بارے-میں',
            'services': 'ur/خدمات',
            'software-development': 'ur/سافٹ-ویئر-ڈویلپمنٹ',
            'app-development': 'ur/ایپ-ڈویلپمنٹ',
            'web-development': 'ur/ویب-ڈویلپمنٹ',
            'ai-development': 'ur/مصنوعی-ذہانت-کی-ترقی',
            'seo-services': 'ur/ایس-ای-او-خدمات',
            'lead-generation': 'ur/لیڈ-جنریشن',
            'call-center': 'ur/کال-سینٹر',
            'data-security-db-maintenance': 'ur/ڈیٹا-سیکیورٹی-ڈیٹابیس-مینٹیننس',
            'projects': 'ur/پروجیکٹس',
            'pricing': 'ur/قیمتیں',
            'contact': 'ur/رابطہ-کریں',
            'testimonials': 'ur/تعریفیں',
            'blog': 'ur/بلاگ',
            'gallery': 'ur/گیلری',
            'industries': 'ur/صنعتیں',
            'case-study': 'ur/کیس-اسٹڈی',
            'faq': 'ur/عمومی-سوالات',
            'privacy-policy': 'ur/رازداری-کی-پالیسی',
            'terms-and-conditions': 'ur/شرائط-و-ضوابط',
            'refund-policy': 'ur/واپسی-کی-پالیسی',
            'cookie-policy': 'ur/کوکی-پالیسی',
            'gdpr-compliance': 'ur/جی-ڈی-پی-آر-تعمیل',
            'free-consultation': 'ur/مفت-مشاورت',
            'request-quote': 'ur/کوٹیشن-کی-درخواست',
            'book-a-call': 'ur/کال-بک-کریں',
        }
    }
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


def get_lang_header_footer(lang_html):
    """Get the header and footer parts from language HTML (preserves navbar, lang switcher, footer, floating buttons)"""
    header_end = lang_html.find('</header>')
    if header_end == -1:
        return None, None
    header_end += len('</header>')
    
    footer_start = lang_html.find('<footer>')
    if footer_start == -1:
        floating_start = lang_html.find('<div class="floating-buttons">')
        if floating_start == -1:
            return None, None
        footer_start = floating_start
    
    before = lang_html[:header_end]
    after = lang_html[footer_start:]
    
    return before, after


def create_new_page_from_english(en_html, lang_code, lang_info, target_folder):
    """Create a new language page from English template - for pages that don't exist yet"""
    is_rtl = lang_info['dir'] == 'rtl'
    
    new_html = en_html
    new_html = re.sub(r'<html lang="en">', f'<html lang="{lang_code}"' + (' dir="rtl">' if is_rtl else '>'), new_html)
    if is_rtl:
        new_html = new_html.replace('<body class="page-transition">', '<body class="page-transition" dir="rtl">')
    
    new_html = re.sub(r'href="/"', f'href="/{lang_code}/"', new_html)
    
    return new_html


def update_existing_page(en_html, lang_html):
    """Update existing language page - preserve header/footer, copy English inner content"""
    _, en_inner, _ = extract_inner_content(en_html)
    lang_before, lang_after = get_lang_header_footer(lang_html)
    
    if en_inner is None or lang_before is None:
        return None
    
    return lang_before + "\n\n" + en_inner + "\n\n" + lang_after


def process_language(lang_code, lang_info):
    """Process all pages for a language"""
    print(f"\n{'='*60}")
    print(f"Processing {lang_info['name']} ({lang_code})")
    print(f"{'='*60}")
    
    success_count = 0
    fail_count = 0
    created_count = 0
    
    for en_page, target_folder in lang_info['pages'].items():
        if en_page == '':
            en_path = "index.html"
        else:
            en_path = f"{en_page}/index.html"
        
        target_path = f"{target_folder}/index.html"
        
        print(f"  Processing: {en_page or 'home'} -> {target_folder}")
        
        if not os.path.exists(en_path):
            print(f"    English file not found: {en_path}")
            fail_count += 1
            continue
        
        with open(en_path, 'r', encoding='utf-8') as f:
            en_html = f.read()
        
        if os.path.exists(target_path):
            with open(target_path, 'r', encoding='utf-8') as f:
                lang_html = f.read()
            
            new_html = update_existing_page(en_html, lang_html)
            if new_html is None:
                print(f"    Could not update page - structure issue")
                fail_count += 1
                continue
            action = "Updated"
        else:
            os.makedirs(target_folder, exist_ok=True)
            new_html = create_new_page_from_english(en_html, lang_code, lang_info, target_folder)
            if new_html is None:
                print(f"    Could not create page from template")
                fail_count += 1
                continue
            action = "Created"
            created_count += 1
        
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(new_html)
        
        print(f"    {action}: {target_path}")
        success_count += 1
    
    print(f"\n  Summary: {success_count} updated ({created_count} new), {fail_count} failed")
    return success_count, fail_count, created_count


def main():
    import sys
    
    if len(sys.argv) > 1:
        target_langs = sys.argv[1].split(',')
    else:
        target_langs = list(LANGUAGES.keys())
    
    print("=" * 60)
    print("Language Page Sync Script")
    print("Copies English content to language pages")
    print("Preserves: navbar, language switcher, footer, floating buttons")
    print("=" * 60)
    print(f"Target languages: {', '.join(target_langs)}")
    
    total_success = 0
    total_fail = 0
    total_created = 0
    
    for lang_code in target_langs:
        if lang_code not in LANGUAGES:
            print(f"Unknown language: {lang_code}")
            continue
        
        success, fail, created = process_language(lang_code, LANGUAGES[lang_code])
        total_success += success
        total_fail += fail
        total_created += created
    
    print("\n" + "=" * 60)
    print(f"Complete!")
    print(f"  Total updated: {total_success}")
    print(f"  New pages created: {total_created}")
    print(f"  Failed: {total_fail}")
    print("=" * 60)


if __name__ == "__main__":
    main()
