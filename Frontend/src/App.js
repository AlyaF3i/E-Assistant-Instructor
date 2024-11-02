import React, { useEffect, useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { useTranslation } from "react-i18next";
import CreateClassroom from "./CreateClassRoom";
import MyClasses from "./MyClasses";
import ClassDetails from "./ClassDetails";
import SectionDetails from "./SectionDetails";
import LoginPage from "./Login";
import './App.css';
import './i18n/i18n'; // Import i18n config
import QuizPage from "./QuizPage";
import SwitchToggle from "./SwitchToggle";

const App = () => {

  return (
    <Router>
      <div className="language-switcher">
      <SwitchToggle/>
      </div>

      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/create-class" element={<CreateClassroom />} />
        <Route path="/my-classes" element={<MyClasses />} />
        <Route path="/class-details/:classId" element={<ClassDetails />} />
        <Route path="/class/:classId/section/:sectionId" element={<SectionDetails />} />
        <Route path="/quiz/:quiz_uuid" element={<QuizPage/>}/>
      </Routes>
    </Router>
  );
};

export default App;
