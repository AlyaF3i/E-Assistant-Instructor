import React, { useEffect, useState } from 'react';
import './QuizPage.css'; // Ensure you import the CSS file
import { useParams } from 'react-router-dom';
import { useTranslation } from 'react-i18next';  // Import the translation hook

const QuizPage = () => {
    const { quiz_uuid } = useParams(); // Get the quiz_uuid from URL params
    const { t, i18n } = useTranslation(); // Use the translation hook

  const [quizData, setQuizData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedAnswers, setSelectedAnswers] = useState({}); // State to track selected answers
  const apiUrl = process.env.REACT_APP_API_URL;

  const dummyQuizData = [

    {
      id: 1,
      text: 'What is the capital of France?',
      option_1: 'Berlin',
      option_2: 'Madrid',
      option_3: 'Paris',
      option_4: 'Rome',
    },
    {
      id: 2,
      text: 'Which planet is known as the Red Planet?',
      option_1: 'Earth',
      option_2: 'Mars',
      option_3: 'Jupiter',
      option_4: 'Saturn',
    },
    {
      id: 3,
      text: 'What is the largest ocean on Earth?',
      option_1: 'Atlantic Ocean',
      option_2: 'Indian Ocean',
      option_3: 'Arctic Ocean',
      option_4: 'Pacific Ocean',
    },
    {
      id: 4,
      text: 'Who wrote "To Kill a Mockingbird"?',
      option_1: 'Harper Lee',
      option_2: 'Mark Twain',
      option_3: 'Ernest Hemingway',
      option_4: 'F. Scott Fitzgerald',
    },
  ];

  useEffect(() => {
    const fetchQuizData = async () => {
      try {
        const response = await fetch(`${apiUrl}api/api/quiz/${quiz_uuid}/`, {
          method: 'GET', // Change to GET
          headers: {
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error('Failed to fetch quiz data');
        }

        const data = await response.json();
        console.log(data)
        // Check if data is empty and set dummy data if necessary
        if (data.length === 0) {
          setQuizData(dummyQuizData);
        } else {
          // Map the data to the desired structure
          const formattedData = data.questions.map(q => ({
            id: q.id,
            text: q.text,
            options: q.options,
          }));
          setQuizData(formattedData);
        }
      } catch (err) {
        // Set dummy data in case of error
        setQuizData(dummyQuizData);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchQuizData();
  }, []); // No dependency array

  const handleOptionChange = (questionId, selectedOptionIndex) => {
    setSelectedAnswers(prev => ({
      ...prev,
      [questionId]: selectedOptionIndex,
    }));
  };
  const handleSubmit = async () => {
    const answersToSubmit = {
      answers: selectedAnswers,
    };

    console.log('Submitting:', answersToSubmit);

    try {
      const response = await fetch(`${apiUrl}api/quiz/${quiz_uuid}/submit/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(answersToSubmit),
      });

      if (!response.ok) {
        throw new Error('Failed to submit answers');
      }

      const result = await response.json();
      console.log('Submission result:', result);
      // Handle successful submission here (e.g., show a success message)
    } catch (error) {
      console.error('Error submitting answers:', error);
      // Handle error here (e.g., show an error message)
    }
  };

 
  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="quiz-container">
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
                className={`option-item ${selectedAnswers[question.id] === index ? 'selected' : ''}`} // Add selected class conditionally
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
                <label htmlFor={`question-${question.id}-option-${index}`} className="option-label">
                  {option}
                </label>
              </li>
            ))}
          </ul>
        </div>
      ))}
            <button className="quiz-submit-button" onClick={handleSubmit}>
            {t('Submit')}
</button>
    </div>
  );
};

export default QuizPage;
