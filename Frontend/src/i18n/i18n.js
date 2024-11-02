import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

// Import translation files
import enTranslation from './EnglishTranslate.json';
import arTranslation from './ArabicTranslate.json';

i18n
  .use(initReactI18next) // Passes i18n down to react-i18next
  .init({
    resources: {
      en: { translation: enTranslation },
      ar: { translation: arTranslation },
    },
    lng: 'en', // Default language
    fallbackLng: 'en', // Fallback language if translation is not found
    interpolation: {
      escapeValue: false, // React already escapes by default
    },
  });

export default i18n;
