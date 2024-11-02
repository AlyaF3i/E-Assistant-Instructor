import React, { useEffect, useState } from "react";
import "./SectionDetails.css";
import { useParams } from "react-router-dom";
import { useTranslation } from "react-i18next";
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer,PieChart, Pie, Cell ,label } from 'recharts';
import SubmissionCounterCard from "./Counter";

const SectionDetails = () => {
  const { t } = useTranslation();
  const { sectionId } = useParams();
  const apiUrl = process.env.REACT_APP_API_URL;
  const [errorMessage, setErrorMessage] = useState("");
  const [sectionData, setSectionData] = useState("");
  const [content, setContent]= useState();
  const [formData, setFormData] = useState({
    selectedQuizOrAssignment: "",
    selectedContentType: "",
    numQuestions: 3,
    quizOrAssignmentName: "",
  });
  const [marksData, setMarksData] = useState()

  const renderLabel = (entry) => {
    const total = marksData?.NumberOfTotalStudents;
    const percentage = ((entry.value / total) * 100).toFixed(2);
    return `${entry.name}: ${percentage}%`;
  };
    const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    console.log(`${name}:`, value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const updatedFormData = {
      ...sectionData,
      classroom_id: sectionData.ClassRoomId,
      ContentType: formData.selectedContentType,
      section_id: sectionData.SectionId,
      section_name: sectionData.SectionName
    };
    console.log(updatedFormData);

    try {
      const response = await fetch(`${apiUrl}api/content-or-mindmap/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(updatedFormData),
      });

      if (response.ok) {
        if (formData.selectedContentType === "Content") {
          const contentData = await response.json(); // Assuming your API returns JSON
          setContent(contentData); // Save the content response
          console.log("Content received:", contentData);
        } else {
          const blob = await response.blob();
          const link = document.createElement("a");
          link.href = window.URL.createObjectURL(blob);

          const fileExtension = {
            mindmap: '.png',
            pdf: '.pdf',
          }[formData.selectedContentType] || '';

          let fileName = 'downloaded_file';
          const contentDisposition = response.headers.get('Content-Disposition');
          if (contentDisposition && contentDisposition.indexOf('attachment') !== -1) {
            const match = contentDisposition.match(/filename="?(.+)"?/);
            fileName = match ? match[1] : fileName;
          }

          link.download = fileName + fileExtension;
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
          console.log("File downloaded successfully");
        }
      } else {
        const errorData = await response.json();
        console.error("Error:", errorData);
        setErrorMessage(t("error"));
      }
    } catch (error) {
      console.error("Error:", error);
      setErrorMessage(t("error"));
    }
  };
  const handleSubmitSupport =(quizType)=> async (e) => {
    e.preventDefault();
    const supportcontent = {
      AssessmentType:quizType,
      SectionId: sectionData.SectionId,
      
    };
    console.log(supportcontent);

    try {
      const response = await fetch(`${apiUrl}api/quiz/support-content/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(supportcontent),
      });

      if (response.ok) {
      console.log("test")
      }
    } catch (error) {
      console.error("Error:", error);
      setErrorMessage(t("error"));
    }
  };
  const handleGenerateQuiz = async (e) => {
    e.preventDefault();
    const updatedFormData = {
      ...sectionData,
      ClassroomId: sectionData.ClassRoomId,
      SectionId: sectionData.SectionId,
      NumQuestions: formData.numQuestions,
      QuizAssignmentName: formData.quizOrAssignmentName,
      Type: formData.selectedQuizOrAssignment,
    };

    console.log(updatedFormData);
    try {
      const response = await fetch(`${apiUrl}api/quiz/create-assignment/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(updatedFormData),
      });

      if (response.ok) {
        const result = await response.json();
        console.log("Quiz created successfully", result);
      } else {
        const errorData = await response.json();
        console.error("Error creating quiz:", errorData);
        setErrorMessage(t("error"));
      }
    } catch (error) {
      console.error("Error:", error);
      setErrorMessage(t("error"));
    }
  };

  const fetchSectionDetails = async () => {
    try {
      const response = await fetch(`${apiUrl}api/section/${sectionId}/`);
      if (!response.ok) throw new Error("Failed to fetch classroom details");

      const data = await response.json();
      setSectionData(data);
const quizResponse = await axios.post(`${apiUrl}api/quiz/assessment-results/`, 
  {
    SectionId: data.SectionId,
    AssessmentType: "Quiz"
  },
  {
    headers: {
      'Content-Type': 'application/json',
    },
  }
);


        // Set the state with the mapped data
        setMarksData(quizResponse.data);
    

      console.log('Quiz submission result:', quizResponse.data );
    } catch (error) {
      console.error("Failed to fetch classroom details:", error);
      setErrorMessage("Failed to load classroom details. Please try again.");
    }
  };

  useEffect(() => {
    fetchSectionDetails();
    console.log(marksData)
  }, []);

  return (
    <div className="section-container">
      <h2 className="section-title">{t("Section Details")}</h2>
      {errorMessage && <p className="error-message">{errorMessage}</p>}
      <div className="section-card">
        <p><strong>{t("Section Name")}:</strong> {sectionData.SectionName}</p>
        <p><strong>{t("Has Quiz")}:</strong> {sectionData.HasQuiz ?<>{t("Yes")} &nbsp;&nbsp; <button className="generate-content-btn" onClick={handleSubmitSupport("Quiz")}>
          {t("Send support content")}
        </button></> : t("No")}</p>
        <p><strong>{t("Has Assignment")}:</strong> {sectionData.HasAssignment ? <>{t("Yes")} &nbsp;&nbsp; <button className="generate-content-btn" onClick={handleSubmitSupport("Assignment")}>
          {t("Send support content")}
        </button></> : t("No")}</p>
        <p><strong>{t("Classroom ID")}:</strong> {sectionData.ClassRoomId}</p>

        <div className="content-type-selector">
          <label htmlFor="content-type">{t("Select Content Type")}: </label>
          <select id="content-type" name="selectedContentType" onChange={handleChange}>
          <option value="">{t("Select")}</option>
            <option value="MindMap">{t("Mind map")}</option>
            <option value="Content">{t("Content")}</option>
            <option value="PDF">{t("PDF")}</option>
          </select>
        </div>
        {formData.selectedContentType?
        <button className="generate-content-btn" onClick={handleSubmit}>
          {t("Generate Content")}
        </button>:""
}
        <div className="content-type-selector">
          <label htmlFor="quiz-assignment">{t("Select Quiz or Assignment")}: </label>
          <select id="quiz-assignment" name="selectedQuizOrAssignment" onChange={handleChange}>
            <option value="">{t("Select")}</option>
            <option value="quiz">{t("Quiz")}</option>
               <option value="assignment">{t("Assignment")}</option>
          </select>
        </div>

        {formData.selectedQuizOrAssignment && (
          <div>
            <div className="SectionDetails-input-wrapper">
              <label htmlFor="quiz-assignment-name" className="createclassroom-label">{t("Enter Name")}: </label>
              <input
                type="text"
                id="quiz-assignment-name"
                name="quizOrAssignmentName"
                value={formData.quizOrAssignmentName}
                className="createclassroom-input"
                onChange={handleChange}
                placeholder={t("Enter quiz or assignment name")}
              />
              <label htmlFor="num-questions" className="createclassroom-label">{t("Enter Number of Questions")}: </label>
              <input
                type="number"
                id="num-questions"
                name="numQuestions"
                value={formData.numQuestions}
                className="createclassroom-input"
                onChange={handleChange}
                min="3"
                placeholder={t("Number of Questions")}
              />
            </div>
            <button className="generate-content-btn" onClick={handleGenerateQuiz}>
              {t("Generate Quiz/Assignment")}
            </button>
          </div>
        )}
        
      </div>

      {content &&
       <div className="section-card" style={{marginTop:"20px"}}>
        <h2 className="section-title">{t("Generated Content")}</h2>

        {content.generated_content.split('\n').map((line, index) => (
      <p key={index}>{line}</p>  // Each line is rendered in a new <p>
    ))}</div>}
    {marksData?.NumberOfSubmittedAssessment!==0?(<div>     <div className="section-card" style={{marginTop:"20px"}}>

<h3>{t("Marks Chart")}</h3>
<ResponsiveContainer width="100%" height={300}>
  <BarChart data={marksData?.StudentsQuizMark}>
    <XAxis dataKey="email" />
    <YAxis />
    <Tooltip />
    <Legend />
    <Bar dataKey="mark" fill="#82ca9d"/>
  </BarChart>
</ResponsiveContainer>
</div>
       <div className="section-card" style={{marginTop:"20px"}}>

<h3>{t("Quiz Submission Chart")}</h3>
<ResponsiveContainer width="100%" height={300}>
  <PieChart>
    <Pie
      data={[
        { name: t("Submitted"), value: marksData?.NumberOfSubmittedAssessment },
        { name: t("Not Submitted"), value:marksData?.NumberOfTotalStudents-marksData?.NumberOfSubmittedAssessment },
      ]}
      cx="50%"
      cy="50%"
      innerRadius={60} // This makes it a donut chart
      outerRadius={100}
      fill="#8884d8"
      labelLine={false}
      label={renderLabel}
    >
      {
        [{ name: t("Submitted"), value:  marksData?.NumberOfSubmittedAssessment  }, { name: t("Not Submitted"), value: marksData?.NumberOfTotalStudents-marksData?.NumberOfSubmittedAssessment }].map((entry, index) => (
          <Cell key={`cell-${index}`} fill={index === 0 ? "#82ca9d" : "#ff6347"} /> // Green for submitted, red for not submitted
        ))
      }
    </Pie>
    <Tooltip />
    <Legend
      layout="vertical"
      verticalAlign="middle"
      align="right"
      iconType="circle"
      formatter={(value, entry) => (
        <span style={{ color: entry.color }}>{value}</span>
      )}
    />
  </PieChart>
</ResponsiveContainer>
</div>
  <div style={{display:"flex",flexDirection:"row",justifyContent:"space-around"}}>
  <SubmissionCounterCard title={t("Submissions count")} totalSubmitted={ marksData?.NumberOfSubmittedAssessment }speed={1000} />
  <SubmissionCounterCard title={t("Non submissions count")} totalSubmitted={marksData?.NumberOfTotalStudents-marksData?.NumberOfSubmittedAssessment}speed={1000} />
  </div></div>):""}
  
    
    </div>
  );
};

export default SectionDetails;
