import React from "react";
import { BrowserRouter as Router, Routes, Route, useLocation } from "react-router-dom"; // Move Router import to the top
import CreateClassroom from "./CreateClassRoom";
import MyClasses from "./MyClasses";
import ClassDetails from "./ClassDetails";
import SectionDetails from "./SectionDetails";
import LoginPage from "./Login";
import QuizPage from "./QuizPage";
import SwitchToggle from "./SwitchToggle";
import Navbar from "./NavBar";
import PrivateRoute from "./PrivateRoute";
import "./App.css";
import "./i18n/i18n"; // Import i18n config

const App = () => {
  const location = useLocation();
  const showNavbar = location.pathname !== "/";

  return (
    <div className="app-container">
      <div className="language-switcher">
        <SwitchToggle />
      </div>
      {showNavbar && <Navbar />}

      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route
          path="/my-classes"
          element={
            <PrivateRoute>
              <MyClasses />
            </PrivateRoute>
          }
        />
        <Route
          path="/create-class"
          element={
            <PrivateRoute>
              <CreateClassroom />
            </PrivateRoute>
          }
        />
        <Route
          path="/class-details/:classId"
          element={
            <PrivateRoute>
              <ClassDetails />
            </PrivateRoute>
          }
        />
        <Route
          path="/class/:classId/section/:sectionId"
          element={
            <PrivateRoute>
              <SectionDetails />
            </PrivateRoute>
          }
        />
        <Route
          path="/quiz/:quiz_uuid"
          element={
            <PrivateRoute>
              <QuizPage />
            </PrivateRoute>
          }
        />
      </Routes>
    </div>
  );
};

// Wrap App in Router to enable useLocation and other routing hooks
const WrappedApp = () => (
  <Router>
    <App />
  </Router>
);

export default WrappedApp;
