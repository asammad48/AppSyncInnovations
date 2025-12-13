#!/usr/bin/env python3
"""
Fix Language Links Script
Fixes all navigation and footer links in language pages to point to correct language-specific URLs.
"""

import os
import re
import glob

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
            'lead-vendor-legal': 'ar/قانون-بائع-العملاء-المحتملين',
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
            'lead-vendor-legal': 'es/legal-proveedor-leads',
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
            'lead-vendor-legal': 'fr/legal-fournisseur-leads',
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
            'lead-vendor-legal': 'pt/legal-fornecedor-leads',
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
            'lead-vendor-legal': 'ca/legal-proveidor-leads',
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
            'lead-vendor-legal': 'de/lead-anbieter-rechtliches',
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
            'lead-vendor-legal': 'tr/lead-saglayici-yasal',
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
            'lead-vendor-legal': 'id/hukum-vendor-prospek',
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
            'lead-vendor-legal': 'ur/لیڈ-وینڈر-قانونی',
        }
    }
}


def fix_links_in_html(html, lang_code, lang_info):
    """Replace all English links with language-specific links"""
    pages = lang_info['pages']
    
    for en_page, lang_page in pages.items():
        if en_page == '':
            continue
        en_url = f'href="/{en_page}/"'
        lang_url = f'href="/{lang_page}/"'
        html = html.replace(en_url, lang_url)
    
    return html


def fix_language_files(lang_code, lang_info):
    """Fix all HTML files in a language folder"""
    lang_folder = lang_code
    
    if not os.path.exists(lang_folder):
        print(f"  Language folder not found: {lang_folder}")
        return 0
    
    html_files = []
    html_files.append(f"{lang_folder}/index.html")
    
    for root, dirs, files in os.walk(lang_folder):
        for file in files:
            if file == 'index.html':
                html_files.append(os.path.join(root, file))
    
    html_files = list(set(html_files))
    
    fixed_count = 0
    for html_path in html_files:
        if not os.path.exists(html_path):
            continue
            
        with open(html_path, 'r', encoding='utf-8') as f:
            original_html = f.read()
        
        fixed_html = fix_links_in_html(original_html, lang_code, lang_info)
        
        if fixed_html != original_html:
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(fixed_html)
            print(f"  Fixed: {html_path}")
            fixed_count += 1
        else:
            print(f"  No changes needed: {html_path}")
    
    return fixed_count


def main():
    print("=" * 60)
    print("Fixing Language Links")
    print("=" * 60)
    
    total_fixed = 0
    
    for lang_code, lang_info in LANGUAGES.items():
        print(f"\nProcessing {lang_info['name']} ({lang_code})")
        print("-" * 40)
        fixed = fix_language_files(lang_code, lang_info)
        total_fixed += fixed
        print(f"  Total fixed: {fixed} files")
    
    print("\n" + "=" * 60)
    print(f"Total files fixed across all languages: {total_fixed}")
    print("=" * 60)


if __name__ == "__main__":
    main()
