import React, { useEffect, useState } from "react";
import "./SwitchToggle.css";
import { useTranslation } from "react-i18next";

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
        checked={language === "en"}
        onChange={() => changeLanguage(language === "en" ? "ar" : "en")}
        className="react-switch-checkbox"
        id={`react-switch-new`}
        type="checkbox"
      />
      ع &nbsp;
      <label
        style={{ background: language === "en" ? "#ff7a00" : "#271f43" }}
        className="react-switch-label"
        htmlFor={`react-switch-new`}>
        <span className={`react-switch-button`} />
      </label>
      &nbsp; EN
    </div>
  );
};

export default SwitchToggle;
