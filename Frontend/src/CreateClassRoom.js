import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next"; // Import translation hook
import "./CreateClassRoom.css";

const CreateClassroom = () => {
  const { t } = useTranslation(); // Initialize translation hook
  const navigate = useNavigate();
  const [students, setStudents] = useState([{ name: "", email: "" }]);
  const [formData, setFormData] = useState({
    ClassRoomName: "",
    Level: "",
    Disability: "",
    Subject: "",
    NumOfSections: "",
    StudentEmail: [],
  });
  const apiUrl = process.env.REACT_APP_API_URL;
  const [isStudentsSectionVisible, setIsStudentsSectionVisible] =
    useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [loading, setLoading] = useState(false); // Loading state

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleStudentChange = (index, event) => {
    const values = [...students];
    values[index][event.target.name] = event.target.value;
    setStudents(values);
  };

  const addStudent = () => {
    setStudents([...students, { name: "", email: "" }]);
  };

  const removeStudent = (index) => {
    const values = [...students];
    values.splice(index, 1);
    setStudents(values);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log(formData);
    setLoading(true); // Start loading

    // Extract student emails
    const studentDetails = students
      .filter((student) => student.name && student.email) // Only include students with both name and email
      .map((student) => ({
        Name: student.name,
        Email: student.email,
      }));

    // Update the formData to include the student details
    const updatedFormData = {
      ...formData,
      StudentEmail: studentDetails, // Add student details here
    };

    console.log(updatedFormData); // Log the updated dataToSubmit
    try {
      const response = await fetch(`${apiUrl}api/classroom/create/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(updatedFormData),
      });

      if (response.ok) {
        const result = await response.json();
        console.log("Classroom created successfully", result);
        navigate("/my-classes");
      } else {
        const errorData = await response.json();
        console.error("Error creating classroom:", errorData);
        setErrorMessage(t("error"));
      }
    } catch (error) {
      console.error("Error:", error);
      setErrorMessage(t("error"));
    } finally {
      setLoading(false); // Stop loading
    }
  };

  return (
    <div className="createclassroom-container">
      <form className="createclassroom-form" onSubmit={handleSubmit}>
        <h2 className="createclassroom-title">{t("createClassroom")}</h2>

        <div className="createclassroom-input-wrapper">
          <label className="createclassroom-label" htmlFor="ClassRoomName">
            {t("classroomName")}
          </label>
          <input
            type="text"
            id="ClassRoomName"
            name="ClassRoomName"
            className="createclassroom-input"
            value={formData.ClassRoomName}
            onChange={handleChange}
            required
          />
        </div>

        <div className="createclassroom-input-wrapper">
          <label className="createclassroom-label" htmlFor="Subject">
            {t("subject")}
          </label>
          <select
            id="Subject"
            name="Subject"
            className="createclassroom-select"
            value={formData.Subject}
            onChange={handleChange}
            required>
            <option value="">{t("selectOption")}</option>
            <option value="Math">{t("math")}</option>
            <option value="Science">{t("science")}</option>
            <option value="English">{t("english")}</option>
            <option value="Arabic">{t("arabic")}</option>
            <option value="History">{t("history")}</option>
            <option value="Geography">{t("geography")}</option>
            <option value="Art">{t("art")}</option>
            <option value="Physical Education">{t("physicalEducation")}</option>
            <option value="Computer Science">{t("computerScience")}</option>
            <option value="Biology">{t("biology")}</option>
            <option value="Chemistry">{t("chemistry")}</option>
            <option value="Physics">{t("physics")}</option>
          </select>
        </div>

        <div className="createclassroom-input-wrapper">
          <label className="createclassroom-label" htmlFor="Level">
            {t("level")}
          </label>
          <select
            id="Level"
            name="Level"
            className="createclassroom-select"
            value={formData.Level}
            onChange={handleChange}
            required>
            <option value="">{t("selectOption")}</option>
            {Array.from({ length: 10 }, (_, i) => i + 3).map((grade) => (
              <option key={grade} value={`Grade ${grade}`}>
                {t(`grade${grade}`, { defaultValue: `Grade ${grade}` })}
              </option>
            ))}
          </select>
        </div>

        <div className="createclassroom-input-wrapper">
          <label className="createclassroom-label" htmlFor="Disability">
            {t("disability")}
          </label>
          <select
            id="Disability"
            name="Disability"
            className="createclassroom-select"
            value={formData.Disability}
            onChange={handleChange}
            required>
            <option value="">{t("selectOption")}</option>
            <option value="yes">{t("yes")}</option>
            <option value="no">{t("no")}</option>
          </select>
        </div>

        <div className="createclassroom-input-wrapper">
          <label className="createclassroom-label" htmlFor="NumOfSections">
            {t("numOfSections")}
          </label>
          <input
            type="number"
            id="NumOfSections"
            name="NumOfSections"
            className="createclassroom-input"
            value={formData.NumOfSections}
            onChange={handleChange}
            required
          />
        </div>

        <div className="createclassroom-students-toggle">
          <h3
            onClick={() =>
              setIsStudentsSectionVisible(!isStudentsSectionVisible)
            }
            className="createclassroom-students-title">
            {isStudentsSectionVisible ? t("hideStudents") : t("addStudents")}
          </h3>
        </div>

        {isStudentsSectionVisible && (
          <div className="createclassroom-students-section">
            {students.map((student, index) => (
              <div key={index} className="createclassroom-student">
                <div className="createclassroom-input-wrapper">
                  <input
                    type="text"
                    name="name"
                    className="createclassroom-input"
                    placeholder={t("studentName")}
                    value={student.name}
                    onChange={(e) => handleStudentChange(index, e)}
                    required
                  />
                </div>
                <div className="createclassroom-input-wrapper">
                  <input
                    type="email"
                    name="email"
                    className="createclassroom-input"
                    placeholder={t("studentEmail")}
                    value={student.email}
                    onChange={(e) => handleStudentChange(index, e)}
                    required
                  />
                </div>
                {index !== -1 && (
                  <button
                    type="button"
                    className="createclassroom-remove-student-button"
                    onClick={() => removeStudent(index)}>
                    {t("removeStudent")}
                  </button>
                )}
              </div>
            ))}
            <button
              type="button"
              className="createclassroom-add-student-button"
              onClick={addStudent}>
              {t("addStudent")}
            </button>
          </div>
        )}

        {errorMessage && <p className="error-message">{errorMessage}</p>}

        <button
          type="submit"
          className="createclassroom-button"
          disabled={loading} // Disable button while loading
        >
          {loading ? (
            <div
              style={{
                display: "flex",
                flexDirection: "row",
                justifyContent: "center",
                alignItems: "center",
              }}>
              {t("Creating class")} &nbsp;<div className="spinner"></div>
            </div> // Show spinner while loading
          ) : (
            t("createClassroomButton")
          )}
        </button>
      </form>
    </div>
  );
};

export default CreateClassroom;
