import React, { useEffect, useState } from 'react';
import './SwitchToggle.css';
import { useTranslation } from 'react-i18next';

const SwitchToggle = () => {
  const { i18n } = useTranslation(); // Hook from react-i18next to handle translations
  const [language, setLanguage] = useState("en");

  const changeLanguage = (lng) => {
    i18n.changeLanguage(lng);
    setLanguage(lng);
  };
  useEffect(() => {
    document.body.setAttribute("dir", language === "ar" ? "rtl" : "ltr");
  }, [language]);


  return (
    <div className="center">
      <input
        type="checkbox"
        id="toggle"
        checked={language === 'en'}
        onChange={() => changeLanguage(language === 'en' ? 'ar' : 'en')}
        style={{ display: 'none' }}
      />

      <label htmlFor="toggle" className="switch">
        <div className="mode">
          <div className="text">English</div>
        </div>
        <div className="mode">
          <div className="text">العربية</div>
        </div>
        <div className={`indicator right ${language === 'en' ? 'active' : ''}`}></div>
        <div className={`indicator left ${language === 'ar' ? 'active' : ''}`}></div>
      </label>
    </div>
  );
};

export default SwitchToggle;