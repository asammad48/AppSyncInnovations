#!/usr/bin/env python3
"""
Fix SEO Meta Tags Script
Fixes canonical links, meta descriptions, titles, and OG tags for all language pages.
Only modifies <head> section - does not touch page content.
"""

import os
import re
from urllib.parse import quote

BASE_URL = "https://appsyncinnovations.com"

LANGUAGES = {
    'en': {'name': 'English', 'code': 'en'},
    'ar': {'name': 'Arabic', 'code': 'ar'},
    'es': {'name': 'Spanish', 'code': 'es'},
    'fr': {'name': 'French', 'code': 'fr'},
    'pt': {'name': 'Portuguese', 'code': 'pt'},
    'ca': {'name': 'Catalan', 'code': 'ca'},
    'de': {'name': 'German', 'code': 'de'},
    'tr': {'name': 'Turkish', 'code': 'tr'},
    'id': {'name': 'Indonesian', 'code': 'id'},
    'ur': {'name': 'Urdu', 'code': 'ur'},
}

PAGE_SEO = {
    'home': {
        'en': {
            'title': 'AppSync Innovations | Software Development & Digital Solutions',
            'description': 'AppSync Innovations delivers cutting-edge software development, app development, web development, lead generation, and call center services. Transform your business with our innovative solutions.',
            'keywords': 'software development, app development, web development, lead generation, call center, SaaS, digital solutions'
        },
        'es': {
            'title': 'AppSync Innovations | Desarrollo de Software y Soluciones Digitales',
            'description': 'AppSync Innovations ofrece desarrollo de software, aplicaciones móviles, desarrollo web, generación de leads y servicios de call center. Transforme su negocio con nuestras soluciones innovadoras.',
            'keywords': 'desarrollo de software, desarrollo de aplicaciones, desarrollo web, generación de leads, call center, SaaS, soluciones digitales'
        },
        'fr': {
            'title': 'AppSync Innovations | Développement Logiciel et Solutions Numériques',
            'description': 'AppSync Innovations propose le développement logiciel, applications mobiles, développement web, génération de prospects et services de centre d\'appels. Transformez votre entreprise avec nos solutions innovantes.',
            'keywords': 'développement logiciel, développement applications, développement web, génération de prospects, centre d\'appels, SaaS, solutions numériques'
        },
        'pt': {
            'title': 'AppSync Innovations | Desenvolvimento de Software e Soluções Digitais',
            'description': 'AppSync Innovations oferece desenvolvimento de software, aplicativos móveis, desenvolvimento web, geração de leads e serviços de call center. Transforme seu negócio com nossas soluções inovadoras.',
            'keywords': 'desenvolvimento de software, desenvolvimento de aplicativos, desenvolvimento web, geração de leads, call center, SaaS, soluções digitais'
        },
        'de': {
            'title': 'AppSync Innovations | Softwareentwicklung und Digitale Lösungen',
            'description': 'AppSync Innovations bietet Softwareentwicklung, App-Entwicklung, Webentwicklung, Lead-Generierung und Callcenter-Dienste. Transformieren Sie Ihr Unternehmen mit unseren innovativen Lösungen.',
            'keywords': 'Softwareentwicklung, App-Entwicklung, Webentwicklung, Lead-Generierung, Callcenter, SaaS, digitale Lösungen'
        },
        'ar': {
            'title': 'AppSync Innovations | تطوير البرمجيات والحلول الرقمية',
            'description': 'تقدم AppSync Innovations تطوير البرمجيات وتطبيقات الهاتف المحمول وتطوير المواقع وتوليد العملاء المحتملين وخدمات مراكز الاتصال. حول عملك مع حلولنا المبتكرة.',
            'keywords': 'تطوير البرمجيات, تطوير التطبيقات, تطوير المواقع, توليد العملاء المحتملين, مركز الاتصال, SaaS, حلول رقمية'
        },
        'tr': {
            'title': 'AppSync Innovations | Yazılım Geliştirme ve Dijital Çözümler',
            'description': 'AppSync Innovations yazılım geliştirme, mobil uygulama geliştirme, web geliştirme, potansiyel müşteri oluşturma ve çağrı merkezi hizmetleri sunmaktadır. İşletmenizi yenilikçi çözümlerimizle dönüştürün.',
            'keywords': 'yazılım geliştirme, uygulama geliştirme, web geliştirme, potansiyel müşteri oluşturma, çağrı merkezi, SaaS, dijital çözümler'
        },
        'id': {
            'title': 'AppSync Innovations | Pengembangan Perangkat Lunak dan Solusi Digital',
            'description': 'AppSync Innovations menyediakan pengembangan perangkat lunak, pengembangan aplikasi mobile, pengembangan web, generasi prospek, dan layanan pusat panggilan. Transformasi bisnis Anda dengan solusi inovatif kami.',
            'keywords': 'pengembangan perangkat lunak, pengembangan aplikasi, pengembangan web, generasi prospek, pusat panggilan, SaaS, solusi digital'
        },
        'ur': {
            'title': 'AppSync Innovations | سافٹ ویئر ڈویلپمنٹ اور ڈیجیٹل حل',
            'description': 'AppSync Innovations سافٹ ویئر ڈویلپمنٹ، موبائل ایپ ڈویلپمنٹ، ویب ڈویلپمنٹ، لیڈ جنریشن، اور کال سینٹر خدمات فراہم کرتا ہے۔ ہمارے جدید حل کے ساتھ اپنے کاروبار کو تبدیل کریں۔',
            'keywords': 'سافٹ ویئر ڈویلپمنٹ, ایپ ڈویلپمنٹ, ویب ڈویلپمنٹ, لیڈ جنریشن, کال سینٹر, SaaS, ڈیجیٹل حل'
        },
        'ca': {
            'title': 'AppSync Innovations | Desenvolupament de Programari i Solucions Digitals',
            'description': 'AppSync Innovations ofereix desenvolupament de programari, aplicacions mòbils, desenvolupament web, generació de clients potencials i serveis de centre de trucades. Transformeu el vostre negoci amb les nostres solucions innovadores.',
            'keywords': 'desenvolupament de programari, desenvolupament d\'aplicacions, desenvolupament web, generació de clients potencials, centre de trucades, SaaS, solucions digitals'
        },
    },
    'about': {
        'en': {
            'title': 'About Us | AppSync Innovations - Our Mission & Expert Team',
            'description': 'Learn about AppSync Innovations - our mission, values, and the expert team behind our innovative software development and digital transformation solutions. Trusted by businesses worldwide.',
            'keywords': 'about AppSync Innovations, software company, expert team, digital solutions, company mission, technology partner'
        },
        'es': {
            'title': 'Sobre Nosotros | AppSync Innovations - Nuestra Misión y Equipo',
            'description': 'Conozca AppSync Innovations - nuestra misión, valores y el equipo experto detrás de nuestras soluciones innovadoras de desarrollo de software y transformación digital. Confiado por empresas en todo el mundo.',
            'keywords': 'sobre AppSync Innovations, empresa de software, equipo experto, soluciones digitales, misión de la empresa, socio tecnológico'
        },
        'fr': {
            'title': 'À Propos | AppSync Innovations - Notre Mission et Équipe',
            'description': 'Découvrez AppSync Innovations - notre mission, nos valeurs et l\'équipe d\'experts derrière nos solutions innovantes de développement logiciel et de transformation numérique. Approuvé par les entreprises du monde entier.',
            'keywords': 'à propos AppSync Innovations, entreprise de logiciels, équipe d\'experts, solutions numériques, mission de l\'entreprise, partenaire technologique'
        },
        'pt': {
            'title': 'Sobre Nós | AppSync Innovations - Nossa Missão e Equipe',
            'description': 'Conheça a AppSync Innovations - nossa missão, valores e a equipe especializada por trás de nossas soluções inovadoras de desenvolvimento de software e transformação digital. Confiança de empresas em todo o mundo.',
            'keywords': 'sobre AppSync Innovations, empresa de software, equipe especializada, soluções digitais, missão da empresa, parceiro tecnológico'
        },
        'de': {
            'title': 'Über Uns | AppSync Innovations - Unsere Mission und Team',
            'description': 'Erfahren Sie mehr über AppSync Innovations - unsere Mission, Werte und das Expertenteam hinter unseren innovativen Softwareentwicklungs- und digitalen Transformationslösungen. Von Unternehmen weltweit vertraut.',
            'keywords': 'über AppSync Innovations, Softwareunternehmen, Expertenteam, digitale Lösungen, Unternehmensmission, Technologiepartner'
        },
        'ar': {
            'title': 'عن الشركة | AppSync Innovations - مهمتنا وفريقنا',
            'description': 'تعرف على AppSync Innovations - مهمتنا وقيمنا والفريق الخبير وراء حلولنا المبتكرة في تطوير البرمجيات والتحول الرقمي. موثوق به من قبل الشركات في جميع أنحاء العالم.',
            'keywords': 'عن AppSync Innovations, شركة برمجيات, فريق خبراء, حلول رقمية, مهمة الشركة, شريك تكنولوجي'
        },
        'tr': {
            'title': 'Hakkımızda | AppSync Innovations - Misyonumuz ve Ekibimiz',
            'description': 'AppSync Innovations hakkında bilgi edinin - misyonumuz, değerlerimiz ve yenilikçi yazılım geliştirme ve dijital dönüşüm çözümlerimizin arkasındaki uzman ekibimiz. Dünya çapında işletmeler tarafından güveniliyor.',
            'keywords': 'AppSync Innovations hakkında, yazılım şirketi, uzman ekip, dijital çözümler, şirket misyonu, teknoloji ortağı'
        },
        'id': {
            'title': 'Tentang Kami | AppSync Innovations - Misi dan Tim Ahli Kami',
            'description': 'Pelajari tentang AppSync Innovations - misi, nilai, dan tim ahli di balik solusi pengembangan perangkat lunak dan transformasi digital inovatif kami. Dipercaya oleh bisnis di seluruh dunia.',
            'keywords': 'tentang AppSync Innovations, perusahaan perangkat lunak, tim ahli, solusi digital, misi perusahaan, mitra teknologi'
        },
        'ur': {
            'title': 'ہمارے بارے میں | AppSync Innovations - ہمارا مشن اور ٹیم',
            'description': 'AppSync Innovations کے بارے میں جانیں - ہمارا مشن، اقدار، اور ہمارے جدید سافٹ ویئر ڈویلپمنٹ اور ڈیجیٹل تبدیلی کے حل کے پیچھے ماہر ٹیم۔ دنیا بھر کے کاروباروں کا اعتماد۔',
            'keywords': 'AppSync Innovations کے بارے میں, سافٹ ویئر کمپنی, ماہر ٹیم, ڈیجیٹل حل, کمپنی مشن, ٹیکنالوجی پارٹنر'
        },
        'ca': {
            'title': 'Sobre Nosaltres | AppSync Innovations - La Nostra Missió i Equip',
            'description': 'Conegueu AppSync Innovations - la nostra missió, valors i l\'equip d\'experts darrere de les nostres solucions innovadores de desenvolupament de programari i transformació digital. Confiat per empreses de tot el món.',
            'keywords': 'sobre AppSync Innovations, empresa de programari, equip d\'experts, solucions digitals, missió de l\'empresa, soci tecnològic'
        },
    },
    'services': {
        'en': {
            'title': 'Our Services | AppSync Innovations - Complete Digital Solutions',
            'description': 'Explore our comprehensive services: software development, app development, web development, AI solutions, SEO services, lead generation, and call center solutions. Custom solutions for your business needs.',
            'keywords': 'software development services, app development, web development, AI development, SEO services, lead generation, call center services, digital solutions'
        },
        'es': {
            'title': 'Nuestros Servicios | AppSync Innovations - Soluciones Digitales Completas',
            'description': 'Explore nuestros servicios completos: desarrollo de software, desarrollo de aplicaciones, desarrollo web, soluciones de IA, servicios SEO, generación de leads y soluciones de call center.',
            'keywords': 'servicios de desarrollo de software, desarrollo de aplicaciones, desarrollo web, desarrollo de IA, servicios SEO, generación de leads, servicios de call center'
        },
        'fr': {
            'title': 'Nos Services | AppSync Innovations - Solutions Numériques Complètes',
            'description': 'Découvrez nos services complets: développement logiciel, développement d\'applications, développement web, solutions IA, services SEO, génération de prospects et solutions de centre d\'appels.',
            'keywords': 'services de développement logiciel, développement d\'applications, développement web, développement IA, services SEO, génération de prospects, services de centre d\'appels'
        },
        'pt': {
            'title': 'Nossos Serviços | AppSync Innovations - Soluções Digitais Completas',
            'description': 'Explore nossos serviços completos: desenvolvimento de software, desenvolvimento de aplicativos, desenvolvimento web, soluções de IA, serviços de SEO, geração de leads e soluções de call center.',
            'keywords': 'serviços de desenvolvimento de software, desenvolvimento de aplicativos, desenvolvimento web, desenvolvimento de IA, serviços de SEO, geração de leads, serviços de call center'
        },
        'de': {
            'title': 'Unsere Dienstleistungen | AppSync Innovations - Komplette Digitale Lösungen',
            'description': 'Entdecken Sie unsere umfassenden Dienstleistungen: Softwareentwicklung, App-Entwicklung, Webentwicklung, KI-Lösungen, SEO-Dienste, Lead-Generierung und Callcenter-Lösungen.',
            'keywords': 'Softwareentwicklung Dienstleistungen, App-Entwicklung, Webentwicklung, KI-Entwicklung, SEO-Dienste, Lead-Generierung, Callcenter-Dienste'
        },
        'ar': {
            'title': 'خدماتنا | AppSync Innovations - حلول رقمية شاملة',
            'description': 'استكشف خدماتنا الشاملة: تطوير البرمجيات، تطوير التطبيقات، تطوير المواقع، حلول الذكاء الاصطناعي، خدمات تحسين محركات البحث، توليد العملاء المحتملين، وحلول مراكز الاتصال.',
            'keywords': 'خدمات تطوير البرمجيات, تطوير التطبيقات, تطوير المواقع, تطوير الذكاء الاصطناعي, خدمات SEO, توليد العملاء المحتملين, خدمات مراكز الاتصال'
        },
        'tr': {
            'title': 'Hizmetlerimiz | AppSync Innovations - Kapsamlı Dijital Çözümler',
            'description': 'Kapsamlı hizmetlerimizi keşfedin: yazılım geliştirme, uygulama geliştirme, web geliştirme, yapay zeka çözümleri, SEO hizmetleri, potansiyel müşteri oluşturma ve çağrı merkezi çözümleri.',
            'keywords': 'yazılım geliştirme hizmetleri, uygulama geliştirme, web geliştirme, yapay zeka geliştirme, SEO hizmetleri, potansiyel müşteri oluşturma, çağrı merkezi hizmetleri'
        },
        'id': {
            'title': 'Layanan Kami | AppSync Innovations - Solusi Digital Lengkap',
            'description': 'Jelajahi layanan komprehensif kami: pengembangan perangkat lunak, pengembangan aplikasi, pengembangan web, solusi AI, layanan SEO, generasi prospek, dan solusi pusat panggilan.',
            'keywords': 'layanan pengembangan perangkat lunak, pengembangan aplikasi, pengembangan web, pengembangan AI, layanan SEO, generasi prospek, layanan pusat panggilan'
        },
        'ur': {
            'title': 'ہماری خدمات | AppSync Innovations - مکمل ڈیجیٹل حل',
            'description': 'ہماری جامع خدمات دریافت کریں: سافٹ ویئر ڈویلپمنٹ، ایپ ڈویلپمنٹ، ویب ڈویلپمنٹ، AI حل، SEO خدمات، لیڈ جنریشن، اور کال سینٹر کے حل۔',
            'keywords': 'سافٹ ویئر ڈویلپمنٹ خدمات, ایپ ڈویلپمنٹ, ویب ڈویلپمنٹ, AI ڈویلپمنٹ, SEO خدمات, لیڈ جنریشن, کال سینٹر خدمات'
        },
        'ca': {
            'title': 'Els Nostres Serveis | AppSync Innovations - Solucions Digitals Completes',
            'description': 'Exploreu els nostres serveis complets: desenvolupament de programari, desenvolupament d\'aplicacions, desenvolupament web, solucions d\'IA, serveis SEO, generació de clients potencials i solucions de centre de trucades.',
            'keywords': 'serveis de desenvolupament de programari, desenvolupament d\'aplicacions, desenvolupament web, desenvolupament d\'IA, serveis SEO, generació de clients potencials, serveis de centre de trucades'
        },
    },
    'software-development': {
        'en': {
            'title': 'Software Development Services | AppSync Innovations',
            'description': 'Custom software development services tailored to your business needs. Enterprise solutions, SaaS platforms, and scalable applications built with modern technologies by our expert development team.',
            'keywords': 'custom software development, enterprise software, SaaS development, software solutions, business software, application development, software company'
        },
        'es': {
            'title': 'Servicios de Desarrollo de Software | AppSync Innovations',
            'description': 'Servicios de desarrollo de software personalizados adaptados a las necesidades de su negocio. Soluciones empresariales, plataformas SaaS y aplicaciones escalables construidas con tecnologías modernas.',
            'keywords': 'desarrollo de software personalizado, software empresarial, desarrollo SaaS, soluciones de software, software de negocios, desarrollo de aplicaciones'
        },
        'fr': {
            'title': 'Services de Développement Logiciel | AppSync Innovations',
            'description': 'Services de développement logiciel sur mesure adaptés aux besoins de votre entreprise. Solutions d\'entreprise, plateformes SaaS et applications évolutives construites avec des technologies modernes.',
            'keywords': 'développement logiciel sur mesure, logiciel d\'entreprise, développement SaaS, solutions logicielles, logiciel d\'entreprise, développement d\'applications'
        },
        'pt': {
            'title': 'Serviços de Desenvolvimento de Software | AppSync Innovations',
            'description': 'Serviços de desenvolvimento de software personalizados para as necessidades do seu negócio. Soluções empresariais, plataformas SaaS e aplicações escaláveis construídas com tecnologias modernas.',
            'keywords': 'desenvolvimento de software personalizado, software empresarial, desenvolvimento SaaS, soluções de software, software de negócios, desenvolvimento de aplicações'
        },
        'de': {
            'title': 'Softwareentwicklung Dienstleistungen | AppSync Innovations',
            'description': 'Maßgeschneiderte Softwareentwicklungsdienstleistungen für Ihre Geschäftsanforderungen. Unternehmenslösungen, SaaS-Plattformen und skalierbare Anwendungen mit modernsten Technologien.',
            'keywords': 'maßgeschneiderte Softwareentwicklung, Unternehmenssoftware, SaaS-Entwicklung, Softwarelösungen, Geschäftssoftware, Anwendungsentwicklung'
        },
        'ar': {
            'title': 'خدمات تطوير البرمجيات | AppSync Innovations',
            'description': 'خدمات تطوير برمجيات مخصصة تناسب احتياجات عملك. حلول المؤسسات ومنصات SaaS وتطبيقات قابلة للتوسع مبنية بتقنيات حديثة من فريقنا المتخصص.',
            'keywords': 'تطوير برمجيات مخصصة, برمجيات المؤسسات, تطوير SaaS, حلول البرمجيات, برمجيات الأعمال, تطوير التطبيقات'
        },
        'tr': {
            'title': 'Yazılım Geliştirme Hizmetleri | AppSync Innovations',
            'description': 'İşletme ihtiyaçlarınıza uygun özel yazılım geliştirme hizmetleri. Modern teknolojilerle oluşturulmuş kurumsal çözümler, SaaS platformları ve ölçeklenebilir uygulamalar.',
            'keywords': 'özel yazılım geliştirme, kurumsal yazılım, SaaS geliştirme, yazılım çözümleri, iş yazılımı, uygulama geliştirme'
        },
        'id': {
            'title': 'Layanan Pengembangan Perangkat Lunak | AppSync Innovations',
            'description': 'Layanan pengembangan perangkat lunak kustom yang disesuaikan dengan kebutuhan bisnis Anda. Solusi enterprise, platform SaaS, dan aplikasi skalabel yang dibangun dengan teknologi modern oleh tim ahli kami.',
            'keywords': 'pengembangan perangkat lunak kustom, perangkat lunak enterprise, pengembangan SaaS, solusi perangkat lunak, perangkat lunak bisnis, pengembangan aplikasi'
        },
        'ur': {
            'title': 'سافٹ ویئر ڈویلپمنٹ خدمات | AppSync Innovations',
            'description': 'آپ کے کاروباری ضروریات کے مطابق کسٹم سافٹ ویئر ڈویلپمنٹ خدمات۔ انٹرپرائز حل، SaaS پلیٹ فارمز، اور جدید ٹیکنالوجیز کے ساتھ بنائے گئے قابل توسیع ایپلیکیشنز۔',
            'keywords': 'کسٹم سافٹ ویئر ڈویلپمنٹ, انٹرپرائز سافٹ ویئر, SaaS ڈویلپمنٹ, سافٹ ویئر حل, بزنس سافٹ ویئر, ایپلیکیشن ڈویلپمنٹ'
        },
        'ca': {
            'title': 'Serveis de Desenvolupament de Programari | AppSync Innovations',
            'description': 'Serveis de desenvolupament de programari personalitzats adaptats a les necessitats del vostre negoci. Solucions empresarials, plataformes SaaS i aplicacions escalables construïdes amb tecnologies modernes.',
            'keywords': 'desenvolupament de programari personalitzat, programari empresarial, desenvolupament SaaS, solucions de programari, programari de negocis, desenvolupament d\'aplicacions'
        },
    },
    'app-development': {
        'en': {
            'title': 'App Development Services | iOS & Android Apps | AppSync Innovations',
            'description': 'Professional mobile app development for iOS and Android. Native and cross-platform applications with intuitive UI/UX design. Transform your ideas into powerful mobile solutions.',
            'keywords': 'mobile app development, iOS app development, Android app development, cross-platform apps, mobile applications, app design, app development company'
        },
        'es': {
            'title': 'Desarrollo de Aplicaciones | iOS y Android | AppSync Innovations',
            'description': 'Desarrollo profesional de aplicaciones móviles para iOS y Android. Aplicaciones nativas y multiplataforma con diseño UI/UX intuitivo. Transforme sus ideas en soluciones móviles potentes.',
            'keywords': 'desarrollo de aplicaciones móviles, desarrollo iOS, desarrollo Android, aplicaciones multiplataforma, aplicaciones móviles, diseño de apps'
        },
        'fr': {
            'title': 'Développement d\'Applications | iOS et Android | AppSync Innovations',
            'description': 'Développement professionnel d\'applications mobiles pour iOS et Android. Applications natives et multiplateformes avec design UI/UX intuitif. Transformez vos idées en solutions mobiles puissantes.',
            'keywords': 'développement d\'applications mobiles, développement iOS, développement Android, applications multiplateformes, applications mobiles, design d\'apps'
        },
        'pt': {
            'title': 'Desenvolvimento de Aplicativos | iOS e Android | AppSync Innovations',
            'description': 'Desenvolvimento profissional de aplicativos móveis para iOS e Android. Aplicativos nativos e multiplataforma com design UI/UX intuitivo. Transforme suas ideias em soluções móveis poderosas.',
            'keywords': 'desenvolvimento de aplicativos móveis, desenvolvimento iOS, desenvolvimento Android, aplicativos multiplataforma, aplicativos móveis, design de apps'
        },
        'de': {
            'title': 'App-Entwicklung | iOS und Android | AppSync Innovations',
            'description': 'Professionelle mobile App-Entwicklung für iOS und Android. Native und plattformübergreifende Anwendungen mit intuitivem UI/UX-Design. Verwandeln Sie Ihre Ideen in leistungsstarke mobile Lösungen.',
            'keywords': 'mobile App-Entwicklung, iOS-Entwicklung, Android-Entwicklung, plattformübergreifende Apps, mobile Anwendungen, App-Design'
        },
        'ar': {
            'title': 'تطوير التطبيقات | iOS و Android | AppSync Innovations',
            'description': 'تطوير تطبيقات محترف للهواتف المحمولة لنظامي iOS و Android. تطبيقات أصلية ومتعددة المنصات مع تصميم UI/UX بديهي. حول أفكارك إلى حلول محمولة قوية.',
            'keywords': 'تطوير تطبيقات الهاتف المحمول, تطوير iOS, تطوير Android, تطبيقات متعددة المنصات, تطبيقات الهاتف, تصميم التطبيقات'
        },
        'tr': {
            'title': 'Uygulama Geliştirme | iOS ve Android | AppSync Innovations',
            'description': 'iOS ve Android için profesyonel mobil uygulama geliştirme. Sezgisel UI/UX tasarımıyla yerel ve çapraz platform uygulamaları. Fikirlerinizi güçlü mobil çözümlere dönüştürün.',
            'keywords': 'mobil uygulama geliştirme, iOS geliştirme, Android geliştirme, çapraz platform uygulamalar, mobil uygulamalar, uygulama tasarımı'
        },
        'id': {
            'title': 'Layanan Pengembangan Aplikasi | iOS & Android | AppSync Innovations',
            'description': 'Pengembangan aplikasi mobile profesional untuk iOS dan Android. Aplikasi native dan cross-platform dengan desain UI/UX intuitif. Transformasi ide Anda menjadi solusi mobile yang powerful.',
            'keywords': 'pengembangan aplikasi mobile, pengembangan iOS, pengembangan Android, aplikasi cross-platform, aplikasi mobile, desain aplikasi'
        },
        'ur': {
            'title': 'ایپ ڈویلپمنٹ خدمات | iOS اور Android | AppSync Innovations',
            'description': 'iOS اور Android کے لیے پیشہ ورانہ موبائل ایپ ڈویلپمنٹ۔ بدیہی UI/UX ڈیزائن کے ساتھ نیٹو اور کراس پلیٹ فارم ایپلیکیشنز۔ اپنے خیالات کو طاقتور موبائل حل میں تبدیل کریں۔',
            'keywords': 'موبائل ایپ ڈویلپمنٹ, iOS ڈویلپمنٹ, Android ڈویلپمنٹ, کراس پلیٹ فارم ایپس, موبائل ایپلیکیشنز, ایپ ڈیزائن'
        },
        'ca': {
            'title': 'Desenvolupament d\'Aplicacions | iOS i Android | AppSync Innovations',
            'description': 'Desenvolupament professional d\'aplicacions mòbils per a iOS i Android. Aplicacions natives i multiplataforma amb disseny UI/UX intuïtiu. Transformeu les vostres idees en solucions mòbils potents.',
            'keywords': 'desenvolupament d\'aplicacions mòbils, desenvolupament iOS, desenvolupament Android, aplicacions multiplataforma, aplicacions mòbils, disseny d\'apps'
        },
    },
    'web-development': {
        'en': {
            'title': 'Web Development Services | Custom Websites | AppSync Innovations',
            'description': 'Professional web development services including responsive websites, e-commerce platforms, web applications, and CMS solutions. Modern, fast, and SEO-optimized websites for your business.',
            'keywords': 'web development, website design, responsive websites, e-commerce development, web applications, CMS development, custom websites'
        },
        'es': {
            'title': 'Desarrollo Web | Sitios Web Personalizados | AppSync Innovations',
            'description': 'Servicios profesionales de desarrollo web incluyendo sitios responsive, plataformas de comercio electrónico, aplicaciones web y soluciones CMS. Sitios web modernos, rápidos y optimizados para SEO.',
            'keywords': 'desarrollo web, diseño de sitios web, sitios responsive, desarrollo e-commerce, aplicaciones web, desarrollo CMS, sitios web personalizados'
        },
        'fr': {
            'title': 'Développement Web | Sites Web Sur Mesure | AppSync Innovations',
            'description': 'Services professionnels de développement web incluant sites responsive, plateformes e-commerce, applications web et solutions CMS. Sites web modernes, rapides et optimisés pour le SEO.',
            'keywords': 'développement web, conception de sites web, sites responsive, développement e-commerce, applications web, développement CMS, sites web sur mesure'
        },
        'pt': {
            'title': 'Desenvolvimento Web | Sites Personalizados | AppSync Innovations',
            'description': 'Serviços profissionais de desenvolvimento web incluindo sites responsivos, plataformas de e-commerce, aplicações web e soluções CMS. Sites modernos, rápidos e otimizados para SEO.',
            'keywords': 'desenvolvimento web, design de sites, sites responsivos, desenvolvimento e-commerce, aplicações web, desenvolvimento CMS, sites personalizados'
        },
        'de': {
            'title': 'Webentwicklung | Individuelle Websites | AppSync Innovations',
            'description': 'Professionelle Webentwicklungsdienste einschließlich responsiver Websites, E-Commerce-Plattformen, Webanwendungen und CMS-Lösungen. Moderne, schnelle und SEO-optimierte Websites.',
            'keywords': 'Webentwicklung, Website-Design, responsive Websites, E-Commerce-Entwicklung, Webanwendungen, CMS-Entwicklung, individuelle Websites'
        },
        'ar': {
            'title': 'تطوير المواقع | مواقع مخصصة | AppSync Innovations',
            'description': 'خدمات تطوير مواقع احترافية تشمل المواقع المتجاوبة ومنصات التجارة الإلكترونية وتطبيقات الويب وحلول إدارة المحتوى. مواقع حديثة وسريعة ومحسنة لمحركات البحث.',
            'keywords': 'تطوير المواقع, تصميم المواقع, مواقع متجاوبة, تطوير التجارة الإلكترونية, تطبيقات الويب, تطوير CMS, مواقع مخصصة'
        },
        'tr': {
            'title': 'Web Geliştirme | Özel Web Siteleri | AppSync Innovations',
            'description': 'Duyarlı web siteleri, e-ticaret platformları, web uygulamaları ve CMS çözümleri dahil profesyonel web geliştirme hizmetleri. Modern, hızlı ve SEO için optimize edilmiş web siteleri.',
            'keywords': 'web geliştirme, web sitesi tasarımı, duyarlı web siteleri, e-ticaret geliştirme, web uygulamaları, CMS geliştirme, özel web siteleri'
        },
        'id': {
            'title': 'Layanan Pengembangan Web | Website Kustom | AppSync Innovations',
            'description': 'Layanan pengembangan web profesional termasuk website responsif, platform e-commerce, aplikasi web, dan solusi CMS. Website modern, cepat, dan dioptimalkan untuk SEO.',
            'keywords': 'pengembangan web, desain website, website responsif, pengembangan e-commerce, aplikasi web, pengembangan CMS, website kustom'
        },
        'ur': {
            'title': 'ویب ڈویلپمنٹ خدمات | کسٹم ویب سائٹس | AppSync Innovations',
            'description': 'پیشہ ورانہ ویب ڈویلپمنٹ خدمات جن میں ریسپانسو ویب سائٹس، ای کامرس پلیٹ فارمز، ویب ایپلیکیشنز، اور CMS حل شامل ہیں۔ جدید، تیز، اور SEO کے لیے بہتر بنائی گئی ویب سائٹس۔',
            'keywords': 'ویب ڈویلپمنٹ, ویب سائٹ ڈیزائن, ریسپانسو ویب سائٹس, ای کامرس ڈویلپمنٹ, ویب ایپلیکیشنز, CMS ڈویلپمنٹ, کسٹم ویب سائٹس'
        },
        'ca': {
            'title': 'Desenvolupament Web | Llocs Web Personalitzats | AppSync Innovations',
            'description': 'Serveis professionals de desenvolupament web incloent llocs responsius, plataformes d\'e-commerce, aplicacions web i solucions CMS. Llocs web moderns, ràpids i optimitzats per a SEO.',
            'keywords': 'desenvolupament web, disseny de llocs web, llocs responsius, desenvolupament e-commerce, aplicacions web, desenvolupament CMS, llocs web personalitzats'
        },
    },
    'ai-development': {
        'en': {
            'title': 'AI Development Services | Machine Learning Solutions | AppSync Innovations',
            'description': 'Advanced AI and machine learning development services. Custom AI solutions, natural language processing, computer vision, and intelligent automation to transform your business operations.',
            'keywords': 'AI development, machine learning, artificial intelligence, NLP, computer vision, AI solutions, intelligent automation, deep learning'
        },
        'es': {
            'title': 'Desarrollo de IA | Soluciones de Machine Learning | AppSync Innovations',
            'description': 'Servicios avanzados de desarrollo de IA y machine learning. Soluciones de IA personalizadas, procesamiento de lenguaje natural, visión por computadora y automatización inteligente.',
            'keywords': 'desarrollo de IA, machine learning, inteligencia artificial, NLP, visión por computadora, soluciones de IA, automatización inteligente'
        },
        'fr': {
            'title': 'Développement IA | Solutions Machine Learning | AppSync Innovations',
            'description': 'Services avancés de développement IA et machine learning. Solutions IA sur mesure, traitement du langage naturel, vision par ordinateur et automatisation intelligente.',
            'keywords': 'développement IA, machine learning, intelligence artificielle, NLP, vision par ordinateur, solutions IA, automatisation intelligente'
        },
        'pt': {
            'title': 'Desenvolvimento de IA | Soluções de Machine Learning | AppSync Innovations',
            'description': 'Serviços avançados de desenvolvimento de IA e machine learning. Soluções de IA personalizadas, processamento de linguagem natural, visão computacional e automação inteligente.',
            'keywords': 'desenvolvimento de IA, machine learning, inteligência artificial, NLP, visão computacional, soluções de IA, automação inteligente'
        },
        'de': {
            'title': 'KI-Entwicklung | Machine Learning Lösungen | AppSync Innovations',
            'description': 'Fortgeschrittene KI- und Machine-Learning-Entwicklungsdienste. Maßgeschneiderte KI-Lösungen, natürliche Sprachverarbeitung, Computer Vision und intelligente Automatisierung.',
            'keywords': 'KI-Entwicklung, Machine Learning, künstliche Intelligenz, NLP, Computer Vision, KI-Lösungen, intelligente Automatisierung'
        },
        'ar': {
            'title': 'تطوير الذكاء الاصطناعي | حلول التعلم الآلي | AppSync Innovations',
            'description': 'خدمات متقدمة في تطوير الذكاء الاصطناعي والتعلم الآلي. حلول ذكاء اصطناعي مخصصة، معالجة اللغة الطبيعية، رؤية الكمبيوتر، والأتمتة الذكية لتحويل عمليات أعمالك.',
            'keywords': 'تطوير الذكاء الاصطناعي, التعلم الآلي, الذكاء الاصطناعي, NLP, رؤية الكمبيوتر, حلول الذكاء الاصطناعي, الأتمتة الذكية'
        },
        'tr': {
            'title': 'Yapay Zeka Geliştirme | Makine Öğrenimi Çözümleri | AppSync Innovations',
            'description': 'Gelişmiş yapay zeka ve makine öğrenimi geliştirme hizmetleri. Özel yapay zeka çözümleri, doğal dil işleme, bilgisayar görüşü ve akıllı otomasyon.',
            'keywords': 'yapay zeka geliştirme, makine öğrenimi, yapay zeka, NLP, bilgisayar görüşü, yapay zeka çözümleri, akıllı otomasyon'
        },
        'id': {
            'title': 'Layanan Pengembangan AI | Solusi Machine Learning | AppSync Innovations',
            'description': 'Layanan pengembangan AI dan machine learning tingkat lanjut. Solusi AI kustom, pemrosesan bahasa alami, computer vision, dan otomatisasi cerdas untuk mentransformasi operasi bisnis Anda.',
            'keywords': 'pengembangan AI, machine learning, kecerdasan buatan, NLP, computer vision, solusi AI, otomatisasi cerdas'
        },
        'ur': {
            'title': 'AI ڈویلپمنٹ خدمات | مشین لرننگ حل | AppSync Innovations',
            'description': 'جدید AI اور مشین لرننگ ڈویلپمنٹ خدمات۔ کسٹم AI حل، قدرتی زبان پروسیسنگ، کمپیوٹر ویژن، اور ذہین آٹومیشن آپ کے کاروباری آپریشنز کو تبدیل کرنے کے لیے۔',
            'keywords': 'AI ڈویلپمنٹ, مشین لرننگ, مصنوعی ذہانت, NLP, کمپیوٹر ویژن, AI حل, ذہین آٹومیشن'
        },
        'ca': {
            'title': 'Desenvolupament d\'IA | Solucions de Machine Learning | AppSync Innovations',
            'description': 'Serveis avançats de desenvolupament d\'IA i machine learning. Solucions d\'IA personalitzades, processament del llenguatge natural, visió per computador i automatització intel·ligent.',
            'keywords': 'desenvolupament d\'IA, machine learning, intel·ligència artificial, NLP, visió per computador, solucions d\'IA, automatització intel·ligent'
        },
    },
    'contact': {
        'en': {
            'title': 'Contact Us | Get in Touch | AppSync Innovations',
            'description': 'Get in touch with AppSync Innovations. Contact our team for software development, app development, and digital solutions. Request a free consultation or quote for your project.',
            'keywords': 'contact AppSync, get in touch, software development inquiry, free consultation, project quote, business contact'
        },
        'es': {
            'title': 'Contáctenos | Póngase en Contacto | AppSync Innovations',
            'description': 'Póngase en contacto con AppSync Innovations. Contacte nuestro equipo para desarrollo de software, aplicaciones y soluciones digitales. Solicite una consulta o presupuesto gratuito.',
            'keywords': 'contactar AppSync, ponerse en contacto, consulta de desarrollo, consulta gratuita, presupuesto de proyecto, contacto empresarial'
        },
        'fr': {
            'title': 'Contactez-Nous | Prenez Contact | AppSync Innovations',
            'description': 'Contactez AppSync Innovations. Contactez notre équipe pour le développement logiciel, applications et solutions numériques. Demandez une consultation ou un devis gratuit.',
            'keywords': 'contacter AppSync, prendre contact, demande de développement, consultation gratuite, devis de projet, contact entreprise'
        },
        'pt': {
            'title': 'Contato | Entre em Contato | AppSync Innovations',
            'description': 'Entre em contato com a AppSync Innovations. Contate nossa equipe para desenvolvimento de software, aplicativos e soluções digitais. Solicite uma consulta ou orçamento gratuito.',
            'keywords': 'contatar AppSync, entrar em contato, consulta de desenvolvimento, consulta gratuita, orçamento de projeto, contato empresarial'
        },
        'de': {
            'title': 'Kontakt | Nehmen Sie Kontakt Auf | AppSync Innovations',
            'description': 'Kontaktieren Sie AppSync Innovations. Kontaktieren Sie unser Team für Softwareentwicklung, App-Entwicklung und digitale Lösungen. Fordern Sie eine kostenlose Beratung oder ein Angebot an.',
            'keywords': 'AppSync kontaktieren, Kontakt aufnehmen, Entwicklungsanfrage, kostenlose Beratung, Projektangebot, Geschäftskontakt'
        },
        'ar': {
            'title': 'اتصل بنا | تواصل معنا | AppSync Innovations',
            'description': 'تواصل مع AppSync Innovations. اتصل بفريقنا لتطوير البرمجيات والتطبيقات والحلول الرقمية. اطلب استشارة مجانية أو عرض سعر لمشروعك.',
            'keywords': 'اتصل بـ AppSync, تواصل معنا, استفسار عن التطوير, استشارة مجانية, عرض سعر للمشروع, اتصال تجاري'
        },
        'tr': {
            'title': 'İletişim | Bize Ulaşın | AppSync Innovations',
            'description': 'AppSync Innovations ile iletişime geçin. Yazılım geliştirme, uygulama geliştirme ve dijital çözümler için ekibimizle iletişime geçin. Ücretsiz danışmanlık veya teklif isteyin.',
            'keywords': 'AppSync iletişim, bize ulaşın, geliştirme talebi, ücretsiz danışmanlık, proje teklifi, iş iletişimi'
        },
        'id': {
            'title': 'Hubungi Kami | Kontak | AppSync Innovations',
            'description': 'Hubungi AppSync Innovations. Kontak tim kami untuk pengembangan perangkat lunak, pengembangan aplikasi, dan solusi digital. Minta konsultasi gratis atau penawaran untuk proyek Anda.',
            'keywords': 'hubungi AppSync, kontak kami, pertanyaan pengembangan, konsultasi gratis, penawaran proyek, kontak bisnis'
        },
        'ur': {
            'title': 'رابطہ کریں | ہم سے رابطہ کریں | AppSync Innovations',
            'description': 'AppSync Innovations سے رابطہ کریں۔ سافٹ ویئر ڈویلپمنٹ، ایپ ڈویلپمنٹ، اور ڈیجیٹل حل کے لیے ہماری ٹیم سے رابطہ کریں۔ اپنے پروجیکٹ کے لیے مفت مشاورت یا کوٹیشن کی درخواست کریں۔',
            'keywords': 'AppSync سے رابطہ, ہم سے رابطہ کریں, ڈویلپمنٹ استفسار, مفت مشاورت, پروجیکٹ کوٹیشن, بزنس رابطہ'
        },
        'ca': {
            'title': 'Contacte | Poseu-vos en Contacte | AppSync Innovations',
            'description': 'Contacteu amb AppSync Innovations. Contacteu el nostre equip per a desenvolupament de programari, aplicacions i solucions digitals. Sol·liciteu una consulta o pressupost gratuït.',
            'keywords': 'contactar AppSync, posar-se en contacte, consulta de desenvolupament, consulta gratuïta, pressupost de projecte, contacte empresarial'
        },
    },
    'pricing': {
        'en': {
            'title': 'Pricing | Affordable Development Plans | AppSync Innovations',
            'description': 'Transparent pricing for software development, app development, and digital solutions. Flexible plans tailored to startups, SMBs, and enterprises. Get a custom quote for your project.',
            'keywords': 'software development pricing, app development cost, web development pricing, digital solutions cost, development plans, custom quote'
        },
        'es': {
            'title': 'Precios | Planes de Desarrollo Accesibles | AppSync Innovations',
            'description': 'Precios transparentes para desarrollo de software, aplicaciones y soluciones digitales. Planes flexibles para startups, PYMES y empresas. Obtenga un presupuesto personalizado.',
            'keywords': 'precios desarrollo de software, costo desarrollo de aplicaciones, precios desarrollo web, costo soluciones digitales, planes de desarrollo, presupuesto personalizado'
        },
        'fr': {
            'title': 'Tarifs | Plans de Développement Abordables | AppSync Innovations',
            'description': 'Tarifs transparents pour le développement logiciel, applications et solutions numériques. Plans flexibles pour startups, PME et entreprises. Obtenez un devis personnalisé.',
            'keywords': 'tarifs développement logiciel, coût développement applications, tarifs développement web, coût solutions numériques, plans de développement, devis personnalisé'
        },
        'pt': {
            'title': 'Preços | Planos de Desenvolvimento Acessíveis | AppSync Innovations',
            'description': 'Preços transparentes para desenvolvimento de software, aplicativos e soluções digitais. Planos flexíveis para startups, PMEs e empresas. Obtenha um orçamento personalizado.',
            'keywords': 'preços desenvolvimento de software, custo desenvolvimento de aplicativos, preços desenvolvimento web, custo soluções digitais, planos de desenvolvimento, orçamento personalizado'
        },
        'de': {
            'title': 'Preise | Erschwingliche Entwicklungspläne | AppSync Innovations',
            'description': 'Transparente Preise für Softwareentwicklung, App-Entwicklung und digitale Lösungen. Flexible Pläne für Startups, KMUs und Unternehmen. Erhalten Sie ein individuelles Angebot.',
            'keywords': 'Softwareentwicklung Preise, App-Entwicklung Kosten, Webentwicklung Preise, digitale Lösungen Kosten, Entwicklungspläne, individuelles Angebot'
        },
        'ar': {
            'title': 'الأسعار | خطط تطوير بأسعار معقولة | AppSync Innovations',
            'description': 'أسعار شفافة لتطوير البرمجيات والتطبيقات والحلول الرقمية. خطط مرنة للشركات الناشئة والشركات الصغيرة والمتوسطة والمؤسسات الكبيرة. احصل على عرض سعر مخصص لمشروعك.',
            'keywords': 'أسعار تطوير البرمجيات, تكلفة تطوير التطبيقات, أسعار تطوير المواقع, تكلفة الحلول الرقمية, خطط التطوير, عرض سعر مخصص'
        },
        'tr': {
            'title': 'Fiyatlandırma | Uygun Geliştirme Planları | AppSync Innovations',
            'description': 'Yazılım geliştirme, uygulama geliştirme ve dijital çözümler için şeffaf fiyatlandırma. Startuplar, KOBİler ve kurumsal şirketler için esnek planlar. Projeniz için özel teklif alın.',
            'keywords': 'yazılım geliştirme fiyatları, uygulama geliştirme maliyeti, web geliştirme fiyatları, dijital çözüm maliyeti, geliştirme planları, özel teklif'
        },
        'id': {
            'title': 'Harga | Paket Pengembangan Terjangkau | AppSync Innovations',
            'description': 'Harga transparan untuk pengembangan perangkat lunak, pengembangan aplikasi, dan solusi digital. Paket fleksibel untuk startup, UKM, dan enterprise. Dapatkan penawaran kustom untuk proyek Anda.',
            'keywords': 'harga pengembangan perangkat lunak, biaya pengembangan aplikasi, harga pengembangan web, biaya solusi digital, paket pengembangan, penawaran kustom'
        },
        'ur': {
            'title': 'قیمتیں | سستے ترقیاتی منصوبے | AppSync Innovations',
            'description': 'سافٹ ویئر ڈویلپمنٹ، ایپ ڈویلپمنٹ، اور ڈیجیٹل حل کے لیے شفاف قیمتیں۔ سٹارٹ اپس، SMBs، اور انٹرپرائزز کے لیے لچکدار منصوبے۔ اپنے پروجیکٹ کے لیے کسٹم کوٹیشن حاصل کریں۔',
            'keywords': 'سافٹ ویئر ڈویلپمنٹ قیمتیں, ایپ ڈویلپمنٹ لاگت, ویب ڈویلپمنٹ قیمتیں, ڈیجیٹل حل لاگت, ڈویلپمنٹ منصوبے, کسٹم کوٹیشن'
        },
        'ca': {
            'title': 'Preus | Plans de Desenvolupament Assequibles | AppSync Innovations',
            'description': 'Preus transparents per a desenvolupament de programari, aplicacions i solucions digitals. Plans flexibles per a startups, pimes i empreses. Obtingueu un pressupost personalitzat.',
            'keywords': 'preus desenvolupament de programari, cost desenvolupament d\'aplicacions, preus desenvolupament web, cost solucions digitals, plans de desenvolupament, pressupost personalitzat'
        },
    },
    'projects': {
        'en': {
            'title': 'Our Projects | Portfolio & Case Studies | AppSync Innovations',
            'description': 'Explore our portfolio of successful projects. Case studies showcasing software development, app development, and digital transformation solutions delivered to clients worldwide.',
            'keywords': 'software projects, app portfolio, case studies, development portfolio, client projects, success stories, project showcase'
        },
        'es': {
            'title': 'Nuestros Proyectos | Portafolio y Casos de Éxito | AppSync Innovations',
            'description': 'Explore nuestro portafolio de proyectos exitosos. Casos de estudio que muestran desarrollo de software, aplicaciones y soluciones de transformación digital entregadas a clientes en todo el mundo.',
            'keywords': 'proyectos de software, portafolio de apps, casos de estudio, portafolio de desarrollo, proyectos de clientes, historias de éxito'
        },
        'fr': {
            'title': 'Nos Projets | Portfolio et Études de Cas | AppSync Innovations',
            'description': 'Explorez notre portfolio de projets réussis. Études de cas présentant le développement logiciel, applications et solutions de transformation numérique livrées à des clients du monde entier.',
            'keywords': 'projets logiciels, portfolio d\'apps, études de cas, portfolio de développement, projets clients, histoires de succès'
        },
        'pt': {
            'title': 'Nossos Projetos | Portfólio e Estudos de Caso | AppSync Innovations',
            'description': 'Explore nosso portfólio de projetos bem-sucedidos. Estudos de caso mostrando desenvolvimento de software, aplicativos e soluções de transformação digital entregues a clientes em todo o mundo.',
            'keywords': 'projetos de software, portfólio de apps, estudos de caso, portfólio de desenvolvimento, projetos de clientes, histórias de sucesso'
        },
        'de': {
            'title': 'Unsere Projekte | Portfolio und Fallstudien | AppSync Innovations',
            'description': 'Entdecken Sie unser Portfolio erfolgreicher Projekte. Fallstudien zur Softwareentwicklung, App-Entwicklung und digitalen Transformation für Kunden weltweit.',
            'keywords': 'Softwareprojekte, App-Portfolio, Fallstudien, Entwicklungsportfolio, Kundenprojekte, Erfolgsgeschichten'
        },
        'ar': {
            'title': 'مشاريعنا | معرض الأعمال ودراسات الحالة | AppSync Innovations',
            'description': 'استكشف معرض مشاريعنا الناجحة. دراسات حالة تعرض تطوير البرمجيات والتطبيقات وحلول التحول الرقمي المقدمة للعملاء في جميع أنحاء العالم.',
            'keywords': 'مشاريع البرمجيات, معرض التطبيقات, دراسات الحالة, معرض التطوير, مشاريع العملاء, قصص النجاح'
        },
        'tr': {
            'title': 'Projelerimiz | Portföy ve Vaka Çalışmaları | AppSync Innovations',
            'description': 'Başarılı projelerimizin portföyünü keşfedin. Dünya çapındaki müşterilere sunulan yazılım geliştirme, uygulama geliştirme ve dijital dönüşüm çözümlerini gösteren vaka çalışmaları.',
            'keywords': 'yazılım projeleri, uygulama portföyü, vaka çalışmaları, geliştirme portföyü, müşteri projeleri, başarı hikayeleri'
        },
        'id': {
            'title': 'Proyek Kami | Portofolio dan Studi Kasus | AppSync Innovations',
            'description': 'Jelajahi portofolio proyek sukses kami. Studi kasus yang menampilkan pengembangan perangkat lunak, pengembangan aplikasi, dan solusi transformasi digital yang diberikan kepada klien di seluruh dunia.',
            'keywords': 'proyek perangkat lunak, portofolio aplikasi, studi kasus, portofolio pengembangan, proyek klien, kisah sukses'
        },
        'ur': {
            'title': 'ہمارے پروجیکٹس | پورٹ فولیو اور کیس اسٹڈیز | AppSync Innovations',
            'description': 'ہمارے کامیاب پروجیکٹس کا پورٹ فولیو دیکھیں۔ کیس اسٹڈیز جو دنیا بھر کے کلائنٹس کو فراہم کردہ سافٹ ویئر ڈویلپمنٹ، ایپ ڈویلپمنٹ، اور ڈیجیٹل تبدیلی کے حل دکھاتی ہیں۔',
            'keywords': 'سافٹ ویئر پروجیکٹس, ایپ پورٹ فولیو, کیس اسٹڈیز, ڈویلپمنٹ پورٹ فولیو, کلائنٹ پروجیکٹس, کامیابی کی کہانیاں'
        },
        'ca': {
            'title': 'Els Nostres Projectes | Portafoli i Estudis de Cas | AppSync Innovations',
            'description': 'Exploreu el nostre portafoli de projectes reeixits. Estudis de cas que mostren desenvolupament de programari, aplicacions i solucions de transformació digital lliurades a clients de tot el món.',
            'keywords': 'projectes de programari, portafoli d\'apps, estudis de cas, portafoli de desenvolupament, projectes de clients, històries d\'èxit'
        },
    },
}

FOLDER_TO_PAGE_MAP = {
    '': 'home',
    'about': 'about',
    'services': 'services',
    'software-development': 'software-development',
    'app-development': 'app-development',
    'web-development': 'web-development',
    'ai-development': 'ai-development',
    'contact': 'contact',
    'pricing': 'pricing',
    'projects': 'projects',
}

LANG_FOLDER_MAP = {
    'ar': {
        'عن-الشركة': 'about',
        'الخدمات': 'services',
        'تطوير-البرمجيات': 'software-development',
        'تطوير-التطبيقات': 'app-development',
        'تطوير-المواقع': 'web-development',
        'تطوير-الذكاء-الاصطناعي': 'ai-development',
        'اتصل-بنا': 'contact',
        'الأسعار': 'pricing',
        'المشاريع': 'projects',
    },
    'es': {
        'sobre-nosotros': 'about',
        'servicios': 'services',
        'desarrollo-software': 'software-development',
        'desarrollo-aplicaciones': 'app-development',
        'desarrollo-web': 'web-development',
        'desarrollo-ia': 'ai-development',
        'contacto': 'contact',
        'precios': 'pricing',
        'proyectos': 'projects',
    },
    'fr': {
        'a-propos': 'about',
        'services': 'services',
        'developpement-logiciel': 'software-development',
        'developpement-applications': 'app-development',
        'developpement-web': 'web-development',
        'developpement-ia': 'ai-development',
        'contact': 'contact',
        'tarifs': 'pricing',
        'projets': 'projects',
    },
    'pt': {
        'sobre-nos': 'about',
        'servicos': 'services',
        'desenvolvimento-software': 'software-development',
        'desenvolvimento-aplicativos': 'app-development',
        'desenvolvimento-web': 'web-development',
        'desenvolvimento-ia': 'ai-development',
        'contato': 'contact',
        'precos': 'pricing',
        'projetos': 'projects',
    },
    'de': {
        'ueber-uns': 'about',
        'dienstleistungen': 'services',
        'softwareentwicklung': 'software-development',
        'app-entwicklung': 'app-development',
        'webentwicklung': 'web-development',
        'ki-entwicklung': 'ai-development',
        'kontakt': 'contact',
        'preise': 'pricing',
        'projekte': 'projects',
    },
    'tr': {
        'hakkimizda': 'about',
        'hizmetler': 'services',
        'yazilim-gelistirme': 'software-development',
        'uygulama-gelistirme': 'app-development',
        'web-gelistirme': 'web-development',
        'yapay-zeka-gelistirme': 'ai-development',
        'iletisim': 'contact',
        'fiyatlandirma': 'pricing',
        'projeler': 'projects',
    },
    'id': {
        'tentang-kami': 'about',
        'layanan': 'services',
        'pengembangan-perangkat-lunak': 'software-development',
        'pengembangan-aplikasi': 'app-development',
        'pengembangan-web': 'web-development',
        'pengembangan-ai': 'ai-development',
        'kontak': 'contact',
        'harga': 'pricing',
        'proyek': 'projects',
    },
    'ur': {
        'ہمارے-بارے-میں': 'about',
        'خدمات': 'services',
        'سافٹ-ویئر-ڈویلپمنٹ': 'software-development',
        'ایپ-ڈویلپمنٹ': 'app-development',
        'ویب-ڈویلپمنٹ': 'web-development',
        'مصنوعی-ذہانت-کی-ترقی': 'ai-development',
        'رابطہ-کریں': 'contact',
        'قیمتیں': 'pricing',
        'پروجیکٹس': 'projects',
    },
    'ca': {
        'sobre-nosaltres': 'about',
        'serveis': 'services',
        'desenvolupament-programari': 'software-development',
        'desenvolupament-aplicacions': 'app-development',
        'desenvolupament-web': 'web-development',
        'desenvolupament-ia': 'ai-development',
        'contacte': 'contact',
        'preus': 'pricing',
        'projectes': 'projects',
    },
}


def get_page_type(file_path, lang_code):
    """Determine the page type from the file path"""
    parts = file_path.replace('\\', '/').split('/')
    
    if lang_code == 'en':
        if file_path == './index.html':
            return 'home'
        if len(parts) >= 2:
            folder = parts[1]
            return FOLDER_TO_PAGE_MAP.get(folder)
    else:
        if file_path == f'./{lang_code}/index.html':
            return 'home'
        if len(parts) >= 3:
            folder = parts[2]
            if lang_code in LANG_FOLDER_MAP:
                return LANG_FOLDER_MAP[lang_code].get(folder)
    
    return None


def get_canonical_url(file_path, lang_code):
    """Generate the correct canonical URL for the file"""
    path = file_path.replace('\\', '/').replace('./','').replace('/index.html', '/')
    if path == 'index.html':
        path = ''
    
    url = f"{BASE_URL}/{path}"
    if not url.endswith('/'):
        url += '/'
    
    return url


def update_meta_tags(html, lang_code, page_type, canonical_url):
    """Update meta tags in the HTML head section"""
    if page_type not in PAGE_SEO:
        return html
    
    lang_seo = PAGE_SEO[page_type].get(lang_code)
    if not lang_seo:
        lang_seo = PAGE_SEO[page_type].get('en', {})
    
    title = lang_seo.get('title', '')
    description = lang_seo.get('description', '')
    keywords = lang_seo.get('keywords', '')
    
    html = re.sub(r'<title>[^<]*</title>', f'<title>{title}</title>', html)
    
    html = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{description}">',
        html
    )
    
    if '<meta name="keywords"' in html:
        html = re.sub(
            r'<meta name="keywords" content="[^"]*">',
            f'<meta name="keywords" content="{keywords}">',
            html
        )
    else:
        html = re.sub(
            r'(<meta name="description" content="[^"]*">)',
            f'\\1\n  <meta name="keywords" content="{keywords}">',
            html
        )
    
    html = re.sub(
        r'<link rel="canonical" href="[^"]*">',
        f'<link rel="canonical" href="{canonical_url}">',
        html
    )
    
    html = re.sub(
        r'<meta property="og:title" content="[^"]*">',
        f'<meta property="og:title" content="{title}">',
        html
    )
    
    html = re.sub(
        r'<meta property="og:description" content="[^"]*">',
        f'<meta property="og:description" content="{description[:150]}">',
        html
    )
    
    html = re.sub(
        r'<meta property="og:url" content="[^"]*">',
        f'<meta property="og:url" content="{canonical_url}">',
        html
    )
    
    return html


def process_file(file_path, lang_code):
    """Process a single HTML file"""
    page_type = get_page_type(file_path, lang_code)
    canonical_url = get_canonical_url(file_path, lang_code)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    new_html = html
    
    new_html = re.sub(
        r'<link rel="canonical" href="[^"]*">',
        f'<link rel="canonical" href="{canonical_url}">',
        new_html
    )
    
    new_html = re.sub(
        r'<meta property="og:url" content="[^"]*">',
        f'<meta property="og:url" content="{canonical_url}">',
        new_html
    )
    
    if page_type:
        new_html = update_meta_tags(new_html, lang_code, page_type, canonical_url)
    
    if new_html != html:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_html)
        return True
    
    return False


def main():
    print("=" * 70)
    print("Fixing SEO Meta Tags (Title, Description, Keywords, Canonical URLs)")
    print("=" * 70)
    
    total_fixed = 0
    
    for root, dirs, files in os.walk('.'):
        if root.startswith('./.') or 'assets' in root or 'attached_assets' in root:
            continue
        
        for file in files:
            if file == 'index.html':
                file_path = os.path.join(root, file)
                
                path_parts = file_path.replace('\\', '/').split('/')
                if len(path_parts) >= 2:
                    potential_lang = path_parts[1]
                    if potential_lang in LANGUAGES and potential_lang != 'en':
                        lang_code = potential_lang
                    elif potential_lang in ['about', 'services', 'software-development', 'app-development', 
                                           'web-development', 'ai-development', 'contact', 'pricing', 'projects',
                                           'seo-services', 'lead-generation', 'call-center', 'data-security-db-maintenance',
                                           'testimonials', 'blog', 'gallery', 'industries', 'case-study', 'faq',
                                           'privacy-policy', 'terms-and-conditions', 'refund-policy', 'cookie-policy',
                                           'gdpr-compliance', 'free-consultation', 'request-quote', 'book-a-call',
                                           'lead-vendor-legal']:
                        lang_code = 'en'
                    else:
                        lang_code = 'en'
                else:
                    lang_code = 'en'
                
                if process_file(file_path, lang_code):
                    print(f"  Fixed: {file_path}")
                    total_fixed += 1
    
    print(f"\n{'=' * 70}")
    print(f"Total files updated: {total_fixed}")
    print("=" * 70)


if __name__ == "__main__":
    main()
