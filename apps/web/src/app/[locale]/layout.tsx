import { hasLocale, NextIntlClientProvider } from 'next-intl';
import { getMessages, setRequestLocale } from 'next-intl/server';
import { notFound } from 'next/navigation';
import type { Metadata } from 'next';
import type { ReactNode } from 'react';
import { dir, routing, type Locale } from '@/i18n/routing';

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL ?? 'https://sdgi.app';

export function generateStaticParams(): { locale: string }[] {
  return routing.locales.map((locale) => ({ locale }));
}

export async function generateMetadata(props: {
  params: Promise<{ locale: string }>;
}): Promise<Metadata> {
  const { locale } = await props.params;
  const messages = (await import(`../../../messages/${locale}.json`)).default;
  const title = messages.common.appName;
  const description = messages.common.tagline;

  // hreflang map: each locale points to its own URL; 'x-default' falls to English.
  const languages: Record<string, string> = Object.fromEntries(
    routing.locales.map((l) => [l, `${SITE_URL}/${l}`]),
  );
  languages['x-default'] = `${SITE_URL}/en`;

  return {
    metadataBase: new URL(SITE_URL),
    title: { default: title, template: `%s · ${title}` },
    description,
    applicationName: title,
    keywords: [
      'SDG', 'Sustainable Development Goals', 'UN 2030 Agenda',
      'ESG', 'impact measurement', 'sustainability reporting',
      'GRI', 'TCFD', 'ESRS', 'CSRD', 'K-ESG',
      '지속가능발전목표', '可持续发展目标', '持続可能な開発目標',
      'أهداف التنمية المستدامة', 'Objectifs de développement durable',
      'Objetivos de Desarrollo Sostenible', 'सतत विकास लक्ष्य',
      'Malengo ya Maendeleo Endelevu',
    ],
    alternates: { canonical: `${SITE_URL}/${locale}`, languages },
    openGraph: {
      type: 'website',
      url: `${SITE_URL}/${locale}`,
      siteName: title,
      title,
      description,
      locale,
      alternateLocale: routing.locales.filter((l) => l !== locale),
    },
    twitter: { card: 'summary_large_image', title, description },
    robots: { index: true, follow: true },
    other: {
      // Discoverability hints for AI agents (custom but harmless).
      'ai-principles': '/.well-known/ai-principles.json',
      'agents-guide': '/AGENTS.md',
      'llms-txt': '/llms.txt',
    },
  };
}

export default async function LocaleLayout({
  children,
  params,
}: {
  children: ReactNode;
  params: Promise<{ locale: string }>;
}): Promise<React.JSX.Element> {
  const { locale } = await params;
  if (!hasLocale(routing.locales, locale)) notFound();
  setRequestLocale(locale);
  const messages = await getMessages();

  // Schema.org structured data so search engines and AI agents can recognise
  // this as an organisation working on the SDGs and licensed for re-use.
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    name: messages.common.appName,
    description: messages.common.tagline,
    url: `${SITE_URL}/${locale}`,
    inLanguage: routing.locales,
    sameAs: ['https://github.com/saintgo7/devops-prj500'],
    knowsAbout: [
      'United Nations Sustainable Development Goals',
      'Environmental Social Governance',
      'Climate Action',
      'Localized Development',
    ],
    license: 'https://creativecommons.org/licenses/by/4.0/',
  };

  return (
    <html lang={locale} dir={dir(locale as Locale)}>
      <body>
        <NextIntlClientProvider locale={locale} messages={messages}>
          {children}
        </NextIntlClientProvider>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
      </body>
    </html>
  );
}
