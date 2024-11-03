import React, { useState } from "react";
import "./Login.css";
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';  // Import the translation hook

const LoginPage = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const { t, i18n } = useTranslation(); // Use the translation hook
    const navigate = useNavigate();
    const apiUrl = process.env.REACT_APP_API_URL;

    // Function to handle language change
    const changeLanguage = (lang) => {
        i18n.changeLanguage(lang);
    };

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch(`${apiUrl}api/login/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username,
                    password,
                }),
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('authToken', data.token);  // Store the token
                localStorage.setItem('username', username); // Store the username
                navigate('/my-classes'); // Redirect to the classes page after successful login
            } else {
                const errorData = await response.json();
                setErrorMessage(errorData.error || t('loginError'));
            }
        } catch (error) {
            setErrorMessage(t('loginErrorOccurred'));
        }
    };

    return (
        <div className="login-container">
            <div className="login-card">
                <h2 className="login-title">{t('login')}</h2> {/* Translated login title */}
                
                {errorMessage && <p className="error-message">{errorMessage}</p>}

                <form onSubmit={handleLogin}>
                    <div className="login-form-group">
                        <label htmlFor="username" className="login-form-group-label">
                            {t('username')} {/* Translated Username label */}
                        </label>
                        <input
                            type="text"
                            id="username"
                            className="login-form-group-input"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                            placeholder={t('enterUsername')}
                        />
                    </div>
                    <div className="login-form-group">
                        <label htmlFor="password" className="login-form-group-label">
                            {t('password')} {/* Translated Password label */}
                        </label>
                        <input
                            type="password"
                            id="password"
                            className="login-form-group-input"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                            placeholder={t('enterPassword')}
                        />
                    </div>
                    <button className="login-btn" type="submit">
                        {t('loginButton')} {/* Translated button text */}
                    </button>
                </form>
                
              
            </div>
            <button
                className="docs-btn"
                onClick={() => window.open(`${apiUrl}redoc`, "_blank")}
                >
                {t("API Docs")}
            </button>
        </div>
    );
};

export default LoginPage;
