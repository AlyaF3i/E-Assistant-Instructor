import React, { useState, useEffect } from "react";
import "./MyClasses.css";
import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";

const MyClasses = () => {
  const [classes, setClasses] = useState([]);
  const [errorMessage, setErrorMessage] = useState("");
  const navigate = useNavigate();
  const { t } = useTranslation(); // Initialize translation hook
  const apiUrl = process.env.REACT_APP_API_URL;

  useEffect(() => {
    fetchClasses();
  }, []);

  const fetchClasses = async () => {
    const username = localStorage.getItem("username"); // Get username from localStorage
    if (!username) {
      setErrorMessage("User not logged in");
      return;
    }

    try {
      const response = await fetch(`${apiUrl}api/classrooms/?UserName=${username}`, {
        headers: {
          Authorization: `Token ${localStorage.getItem("authToken")}`, // Pass the token in the header
        },
      });
      
      if (response.ok) {
        const data = await response.json();
        const classData = data.ClassRoomId.map((id, index) => ({
          id: id,
          ClassRoomName: data.ClassRoomName[index],
          studentCount: data.StudentNumbers[index],  // You can adjust this if there are students for each class in the future
        }));
        console.log(data)

        setClasses(classData);
      } else {
        const errorData = await response.json();
        setErrorMessage(errorData.error || "Failed to load classes");
      }
    } catch (error) {
      setErrorMessage("An error occurred while fetching classes.");
    }
  };
  const handleNavigate = (classData) => {
    navigate(`/class-details/${classData.id}`, {
      state: {
        ClassRoomName: classData.ClassRoomName,
        classId: classData.id,
      },
    });
  };
  return (
    <div className="myclasses-container">
    <h2 className="myclasses-title">{t("myCreatedClasses")}</h2>
    {errorMessage && <p className="error-message">{errorMessage}</p>}
    <div className="myclasses-list">
      {classes.length > 0 ? (
        classes.map((classItem) => (
          <div key={classItem.id} className="myclass-card" onClick={() => handleNavigate(classItem)}>
            <h3 className="myclass-card-title">{classItem.ClassRoomName}</h3>
            <div className="myclass-details">
              <p><strong>{t("studentsCount")}:</strong> {classItem.studentCount}</p> {/* Display the count of students */}
            </div>
          </div>
        ))
      ) : (
        <p>{t("noClassesAvailable")}</p>
      )}
    </div>
  </div>
  );
};

export default MyClasses;
