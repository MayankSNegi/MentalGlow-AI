import React, { useState } from "react";
import Back from "../common/back/Back";
import "./checkup.css";

const Checkup = () => {
  const [formData, setFormData] = useState({
    // Basic Demographics
    age: "",
    gender: "male",
    city: "",              // renamed from country
    relationship_status: "",

    // Lifestyle Factors
    sleep_hours: "",
    exercise_frequency: "",
    screen_time_hours: "",
    diet_quality: "",

    // Emotional & Mental Health
    stress_level: "",
    anxiety_level: "",
    mood: "neutral",
    motivation_level: "",
    concentration_level: "",

    // Social & Work/Study
    social_support: "",
    social_interaction_frequency: "",
    work_stress: "",
    is_student: "",
    is_employed: "",

    // Coping & Habits (REMOVED fields)
    household_responsibility: "",

    // Mental Awareness
    open_to_therapy: "",
    aware_of_mental_health: "",
  });

  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setPrediction(null);
    setError(null);

    try {
      const response = await fetch("https://mentalglow-ai-backend.onrender.com/api/predict/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      if (!response.ok) throw new Error("Prediction failed");
      const result = await response.json();
      setPrediction(result.prediction);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <>
      <Back title="Checkup Form" />
      <section className="checkup-section">
        <div className="container">
          <h1>Mental Wellness Self-Assessment</h1>
          <p>
            Take this short survey to understand your current mental wellness level.
            Your responses help AI provide personalized wellness insights.
          </p>

          <form onSubmit={handleSubmit} className="checkup-form">

            {/* --- BASIC INFO --- */}
            <h2>Personal Information</h2>
            <div className="form-group">
              <label>Age <span className="required-star">*</span> <small className="hint">(integer 10–100)</small></label>
              <input type="number" name="age" min="10" max="100"
                value={formData.age} onChange={handleChange} required />
            </div>

            <div className="form-group">
              <label>Gender <span className="required-star">*</span></label>
              <select name="gender" value={formData.gender} onChange={handleChange} required>
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="other">Other / Prefer not to say</option>
              </select>
            </div>

            <div className="form-group">
              <label>City <span className="required-star">*</span> <small className="hint">(any Indian city)</small></label>
              <input type="text" name="city" placeholder="e.g., Delhi, Mumbai, Bengaluru"
                value={formData.city} onChange={handleChange} required />
            </div>

            <div className="form-group">
              <label>Relationship Status <span className="required-star">*</span></label>
              <select name="relationship_status" value={formData.relationship_status} onChange={handleChange} required>
                <option value="">Select...</option>
                <option value="single">Single</option>
                <option value="in_relationship">In Relationship</option>
                <option value="married">Married</option>
                <option value="divorced">Divorced</option>
                <option value="widowed">Widowed</option>
              </select>
            </div>

            {/* --- LIFESTYLE --- */}
            <h2>Lifestyle & Routine</h2>
            <div className="form-group">
              <label>Average Sleep Hours per Day <span className="required-star">*</span> <small className="hint">(0–12)</small></label>
              <input type="number" name="sleep_hours" min="0" max="12"
                value={formData.sleep_hours} onChange={handleChange} required />
            </div>

            <div className="form-group">
              <label>Exercise Frequency (days/week) <span className="required-star">*</span> <small className="hint">(0–7)</small></label>
              <input type="number" name="exercise_frequency" min="0" max="7"
                value={formData.exercise_frequency} onChange={handleChange} required />
            </div>

            <div className="form-group">
              <label>Screen Time (hours/day) <span className="required-star">*</span> <small className="hint">(0–16)</small></label>
              <input type="number" name="screen_time_hours" min="0" max="16"
                value={formData.screen_time_hours} onChange={handleChange} required />
            </div>

            <div className="form-group">
              <label>Diet Quality (1 – Poor to 5 – Excellent) <span className="required-star">*</span></label>
              <input type="number" name="diet_quality" min="1" max="5"
                value={formData.diet_quality} onChange={handleChange} required />
            </div>

            {/* --- EMOTIONAL HEALTH --- */}
            <h2>Emotional & Psychological Health</h2>
            <div className="form-group">
              <label>Stress Level (1 – Low to 5 – High) <span className="required-star">*</span></label>
              <input type="number" name="stress_level" min="1" max="5"
                value={formData.stress_level} onChange={handleChange} required />
            </div>

            <div className="form-group">
              <label>Anxiety Level (1 – Low to 5 – High) <span className="required-star">*</span></label>
              <input type="number" name="anxiety_level" min="1" max="5"
                value={formData.anxiety_level} onChange={handleChange} required />
            </div>

            <div className="form-group">
              <label>Overall Mood <span className="required-star">*</span></label>
              <select name="mood" value={formData.mood} onChange={handleChange} required>
                <option value="low">Low</option>
                <option value="neutral">Neutral</option>
                <option value="high">Positive</option>
              </select>
            </div>

            <div className="form-group">
              <label>Motivation Level (1 – Low to 5 – High) <span className="required-star">*</span></label>
              <input type="number" name="motivation_level" min="1" max="5"
                value={formData.motivation_level} onChange={handleChange} required />
            </div>

            <div className="form-group">
              <label>Concentration Level (1 – Poor to 5 – Excellent) <span className="required-star">*</span></label>
              <input type="number" name="concentration_level" min="1" max="5"
                value={formData.concentration_level} onChange={handleChange} required />
            </div>

            {/* --- SOCIAL LIFE --- */}
            <h2>Social & Work-Life</h2>
            <div className="form-group">
              <label>Social Support (1 – None to 5 – Strong) <span className="required-star">*</span></label>
              <input type="number" name="social_support" min="1" max="5"
                value={formData.social_support} onChange={handleChange} required />
            </div>

            <div className="form-group">
              <label>Frequency of Social Interaction (days/week) <span className="required-star">*</span> <small className="hint">(0–7)</small></label>
              <input type="number" name="social_interaction_frequency" min="0" max="7"
                value={formData.social_interaction_frequency} onChange={handleChange} required />
            </div>

            <div className="form-group">
              <label>Work/Study Stress Level (1 – Low to 5 – High) <span className="required-star">*</span></label>
              <input type="number" name="work_stress" min="1" max="5"
                value={formData.work_stress} onChange={handleChange} required />
            </div>

            <div className="form-group">
              <label>Are you a Student? <span className="required-star">*</span></label>
              <select name="is_student" value={formData.is_student} onChange={handleChange} required>
                <option value="">Select...</option>
                <option value="1">Yes</option>
                <option value="0">No</option>
              </select>
            </div>

            <div className="form-group">
              <label>Are you Employed? <span className="required-star">*</span></label>
              <select name="is_employed" value={formData.is_employed} onChange={handleChange} required>
                <option value="">Select...</option>
                <option value="1">Yes</option>
                <option value="0">No</option>
              </select>
            </div>

            {/* --- HOUSEHOLD --- */}
            <h2>Home Responsibilities</h2>
            <div className="form-group">
              <label>Household Responsibility (1 – Low to 5 – High) <span className="required-star">*</span></label>
              <input type="number" name="household_responsibility" min="1" max="5"
                value={formData.household_responsibility} onChange={handleChange} required />
            </div>

            {/* --- MENTAL AWARENESS --- */}
            <h2>Mental Health Awareness</h2>
            <div className="form-group">
              <label>Are you open to therapy or counseling if needed? <span className="required-star">*</span></label>
              <select name="open_to_therapy" value={formData.open_to_therapy} onChange={handleChange} required>
                <option value="">Select...</option>
                <option value="1">Yes</option>
                <option value="0">No</option>
              </select>
            </div>

            <div className="form-group">
              <label>Do you consider mental health as important as physical health? <span className="required-star">*</span></label>
              <select name="aware_of_mental_health" value={formData.aware_of_mental_health} onChange={handleChange} required>
                <option value="">Select...</option>
                <option value="1">Yes</option>
                <option value="0">No</option>
              </select>
            </div>

            <button type="submit" className="submit-button">Get Prediction</button>
          </form>

          {prediction && (
            <div className="prediction-result">
              <h2>Predicted Mental Wellness Level: {prediction}</h2>
            </div>
          )}
          {error && <div className="error-message"><p>{error}</p></div>}
        </div>
      </section>
    </>
  );
};

export default Checkup;
