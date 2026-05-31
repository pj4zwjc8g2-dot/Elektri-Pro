import nl from '../i18n/nl.json';
import fr from '../i18n/fr.json';

export type Locale = 'nl' | 'fr';

const translations = { nl, fr } as const;

export function t(locale: Locale) {
  return translations[locale];
}

export function altLocale(locale: Locale): Locale {
  return locale === 'nl' ? 'fr' : 'nl';
}

export function localePath(locale: Locale, path = '') {
  return `/${locale}${path ? `/${path.replace(/^\//, '')}` : '/'}`;
}
