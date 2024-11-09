import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next"; // Import the translation hook
import { MdArrowBackIosNew } from "react-icons/md";
import "./NavBar.css";
import SwitchToggle from "./SwitchToggle";
//... other imports

const Navbar = () => {
  const [menuOpen, setMenuOpen] = useState(false); // State to manage menu visibility
  const navigate = useNavigate();
  const { t } = useTranslation(); // Use the translation hook

  const handleLogout = () => {
    localStorage.removeItem("authToken");
    navigate("/");
  };

  const handleBack = () => {
    navigate(-1);
  };

  const toggleMenu = () => {
    setMenuOpen(!menuOpen);
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className={`navbar-links ${menuOpen ? "active" : ""}`}>
          <div className="language-switcher">
            <SwitchToggle />
          </div>
          <Link to="/my-classes" className="navbar-link">
            {t("My Classes")}
          </Link>
          <Link to="/create-class" className="navbar-link">
            {t("Create Classroom")}
          </Link>
          <button
            className="navbar-button logout-button logout-mobile"
            onClick={handleLogout}>
            {t("Logout")}
          </button>
        </div>
        <div className="navbar-brand">
          <button className="back-button" onClick={handleBack}>
            <MdArrowBackIosNew
              style={{ fontSize: "x-large", marginTop: "5px" }}
            />
          </button>
        </div>
        <button className="menu-toggle" onClick={toggleMenu}>
          ☰
        </button>
      </div>
    </nav>
  );
};
export default Navbar;
