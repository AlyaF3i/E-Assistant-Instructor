import React, { useEffect, useState } from "react";
import "./ClassDetails.css";
import "./ClassDetails.css";
import { useNavigate, useParams } from "react-router-dom";
import { useTranslation } from "react-i18next";

const ClassDetails = () => {
  const { classId } = useParams();
  const navigate = useNavigate();
  const { t } = useTranslation(); // Initialize translation function

  const [classData, setClassData] = useState({
    ClassRoomName: "",
    Level: "",
    Disability: "",
    UserName: "",
    Subject: "",
    students: [],
    sections: [],
  });
  const apiUrl = process.env.REACT_APP_API_URL;

  const [studentEmail, setStudentEmail] = useState("");
  const [studentName, setStudentName] = useState("");

  const [errorMessage, setErrorMessage] = useState("");
  const [successMessage, setSuccessMessage] = useState("");
  const [showStudents, setShowStudents] = useState(true); // State to show/hide students
  const [isFetched, setIsFetched] = useState(false); // New state variable

  const handleAddStudent = async () => {
    setErrorMessage("");
    setSuccessMessage("");
    console.log(studentEmail);

    if (!validateEmail(studentEmail)) {
      setErrorMessage("Invalid email format");
      return;
    }
    try {
      const response = await fetch(`${apiUrl}api/add-student/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          classroom_id: classId,
          student_name: studentName,
          student_email: studentEmail,
        }),
      });

      if (response.ok) {
        setStudentName("");
        setStudentEmail("");
        setSuccessMessage("Student added successfully!");
        setIsFetched(true); // Set to true to trigger a re-fetch
      } else {
        const errorData = await response.json();
        setErrorMessage(errorData.error || "Failed to add student");
      }
    } catch (error) {
      console.error("Failed to add student:", error);
      setErrorMessage(
        "An error occurred while adding the student. Please try again."
      );
    }
  };

  const validateEmail = (email) => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
  };

  const removeStudent = (email) => {};

  useEffect(() => {
    fetchClassDetails();
  }, [isFetched]);

  const fetchClassDetails = async () => {
    try {
      const response = await fetch(`${apiUrl}api/classroom/${classId}/`);
      if (!response.ok) {
        throw new Error("Failed to fetch classroom details");
      }
      const data = await response.json();
      setClassData(data);
      console.log(data);
    } catch (error) {
      console.error("Failed to fetch classroom details:", error);
      setErrorMessage("Failed to load classroom details. Please try again.");
    }
  };

  const handleSectionClick = (section) => {
    console.log();
    navigate(`/class/${classId}/section/${section.SectionId}`, {
      state: {
        sectionId: section.SectionId,
      },
    });
  };
  return (
    <div className="classdetails-container">
      <h2 className="classdetails-title">{t("Class Details")}</h2>
      {errorMessage && <p className="error-message">{errorMessage}</p>}

      <div className="classdetails-card">
        <h3 className="classdetails-card-title">{classData.ClassRoomName}</h3>
        <div className="classdetails-info">
          <p>
            <strong>{t("Level")}:</strong> {classData.Level}
          </p>
          <p>
            <strong>{t("Disability")}:</strong> {classData.Disability}
          </p>
          <p>
            <strong>{t("Teacher")}:</strong> {classData.UserName}
          </p>
          <p>
            <strong>{t("Subject")}:</strong> {classData.Subject}
          </p>
        </div>

        {/* Toggle Show/Hide Students Button */}
        <button
          className="classdetails-toggle-button"
          onClick={() => setShowStudents(!showStudents)}>
          {showStudents ? t("Hide Students") : t("Show Students")}
        </button>

        {/* Students List */}
        {showStudents && (
          <>
            <h4 className="classdetails-sections-title">{t("Students")}</h4>
            <div className="classdetails-student-list">
              {classData.students.length > 0 ? (
                classData.students.map((student, index) => (
                  <div key={index} className="classdetails-student-item">
                    <p>{student}</p>
                    {/* <button
                      className="classdetails-remove-button"
                      onClick={() => removeStudent(student.email)}>
                      {t("Remove")}
                    </button> */}
                  </div>
                ))
              ) : (
                <p>{t("No students enrolled")}</p>
              )}
            </div>
          </>
        )}

        {/* Add New Student Form */}
        <div className="classdetails-add-student-form">
          <h4 className="classdetails-sections-title">{t("Add Student")}</h4>

          <input
            type="text"
            placeholder={t("Student Name")}
            value={studentName}
            required
            onChange={(e) => setStudentName(e.target.value)}
          />
          <input
            type="email"
            placeholder={t("Student Email")}
            required
            value={studentEmail}
            onChange={(e) => setStudentEmail(e.target.value)}
          />
          <button
            className="classdetails-add-button"
            onClick={handleAddStudent}>
            {t("Add Student")}
          </button>
        </div>

        {errorMessage && (
          <p id="error-message" className="error-message">
            {errorMessage}
          </p>
        )}
        {successMessage && (
          <p id="success-message" className="success-message">
            {successMessage}
          </p>
        )}

        <h4 className="classdetails-sections-title">{t("Sections")}</h4>
        <div className="sections-container">
          {classData.sections.length > 0 ? (
            classData.sections.map((section) => (
              <div
                className="section-card"
                key={section.id}
                onClick={() => handleSectionClick(section)}>
                <h4>{section.Title}</h4>
                <p>
                  {t("Description")}: {section.Description}
                </p>
              </div>
            ))
          ) : (
            <p>{t("No sections generated")}</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default ClassDetails;
