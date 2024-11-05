import React, { useEffect, useState } from "react";
import "./QuizPage.css"; // Ensure you import the CSS file
import { useParams } from "react-router-dom";
import { useTranslation } from "react-i18next"; // Import the translation hook

const QuizPage = () => {
  const { quiz_uuid } = useParams(); // Get the quiz_uuid from URL params
  const { t } = useTranslation(); // Use the translation hook
  const [loading2, setLoading2] = useState(false);

  const [quizData, setQuizData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedAnswers, setSelectedAnswers] = useState({}); // State to track selected answers
  const apiUrl = process.env.REACT_APP_API_URL;
  const [submitMessage, setSubmitMessage] = useState();
  useEffect(() => {
    const fetchQuizData = async () => {
      try {
        const response = await fetch(`${apiUrl}api/api/quiz/${quiz_uuid}/`, {
          method: "GET", // Change to GET
          headers: {
            "Content-Type": "application/json",
          },
        });

        if (!response.ok) {
          throw new Error("Failed to fetch quiz data");
        }

        const data = await response.json();
        // Check if data is empty and set dummy data if necessary

        // Map the data to the desired structure
        const formattedData = data.questions.map((q) => ({
          id: q.id,
          text: q.text,
          options: q.options,
        }));
        setQuizData(formattedData);
      } catch (err) {
        setError(err.message);
        console.log(error);
      } finally {
        setLoading(false);
      }
    };

    fetchQuizData();
  }, []); // No dependency array

  const handleOptionChange = (questionId, selectedOptionIndex) => {
    setSelectedAnswers((prev) => ({
      ...prev,
      [questionId]: selectedOptionIndex,
    }));
  };
  const handleSubmit = async () => {
    setLoading2(true);
    const answersToSubmit = {
      answers: selectedAnswers,
    };

    console.log("Submitting:", answersToSubmit);

    try {
      const response = await fetch(`${apiUrl}api/quiz/${quiz_uuid}/submit/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(answersToSubmit),
      });

      if (!response.ok) {
        throw new Error("Failed to submit answers");
      }

      if (response.ok) {
        const result = await response.json();
        setLoading2(false);
        setSubmitMessage(result.message);

        // Wait for 4 seconds before closing the window
        // setTimeout(() => {
        //   window.close();
        // }, 4000);
      }
      // Handle successful submission here (e.g., show a success message)
    } catch (error) {
      console.error("Error submitting answers:", error);
      // Handle error here (e.g., show an error message)
    }
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="quiz-container">
      {submitMessage ? (
        <div className="quiz-submit-message">
          <h3>{t("Answers submitted successfully!")}</h3>
        </div>
      ) : (
        <div>
          <h1 className="quiz-title">Quiz</h1>
          {quizData.map((question) => (
            <div key={question.id} className="quiz-question">
              <h3 className="question-text">{question.text}</h3>
              <ul className="options-list">
                {[
                  question.options[0],
                  question.options[1],
                  question.options[2],
                  question.options[3],
                ].map((option, index) => (
                  <li
                    key={index}
                    className={`option-item ${
                      selectedAnswers[question.id] === index ? "selected" : ""
                    }`} // Add selected class conditionally
                    onClick={() => handleOptionChange(question.id, index)} // Handle option click
                  >
                    <input
                      type="radio"
                      id={`question-${question.id}-option-${index}`}
                      name={`question-${question.id}`}
                      className="option-input"
                      checked={selectedAnswers[question.id] === index} // Check if this option is selected
                      readOnly // Prevent default behavior since we handle selection with onClick
                    />
                    <label
                      htmlFor={`question-${question.id}-option-${index}`}
                      className="option-label">
                      {option}
                    </label>
                  </li>
                ))}
              </ul>
            </div>
          ))}
          <button
            className="quiz-submit-button"
            disabled={loading2}
            onClick={handleSubmit}>
            {t("Submit")}
          </button>
        </div>
      )}
    </div>
  );
};

export default QuizPage;
