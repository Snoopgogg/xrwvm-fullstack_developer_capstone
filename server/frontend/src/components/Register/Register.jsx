import React, { useState } from "react";
import "./Register.css";
import Header from "../Header/Header";

const Register = () => {
  const [form, setForm] = useState({
    username: "",
    firstName: "",
    lastName: "",
    email: "",
    password: ""
  });
  const [message, setMessage] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((current) => ({ ...current, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setMessage("");

    if (Object.values(form).some((value) => !value.trim())) {
      setMessage("Please complete all five fields.");
      return;
    }

    setIsSubmitting(true);
    try {
      const response = await fetch("/djangoapp/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "same-origin",
        body: JSON.stringify({
          userName: form.username.trim(),
          firstName: form.firstName.trim(),
          lastName: form.lastName.trim(),
          email: form.email.trim(),
          password: form.password
        })
      });

      const result = await response.json().catch(() => ({}));
      if (!response.ok) {
        setMessage(result.message || result.error || "Registration could not be completed.");
        return;
      }

      setMessage(result.message || "Registration successful. You can now log in.");
      setForm({ username: "", firstName: "", lastName: "", email: "", password: "" });
    } catch (error) {
      setMessage("Unable to contact the registration service. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div>
      <Header />
      <main className="register_container">
        <h1 className="header">Create an account</h1>
        <form className="inputs" onSubmit={handleSubmit} noValidate>
          <label className="input" htmlFor="register-username">
            <span>Username</span>
            <input
              id="register-username"
              className="input_field"
              type="text"
              name="username"
              value={form.username}
              onChange={handleChange}
              autoComplete="username"
              required
            />
          </label>

          <label className="input" htmlFor="register-first-name">
            <span>First Name</span>
            <input
              id="register-first-name"
              className="input_field"
              type="text"
              name="firstName"
              value={form.firstName}
              onChange={handleChange}
              autoComplete="given-name"
              required
            />
          </label>

          <label className="input" htmlFor="register-last-name">
            <span>Last Name</span>
            <input
              id="register-last-name"
              className="input_field"
              type="text"
              name="lastName"
              value={form.lastName}
              onChange={handleChange}
              autoComplete="family-name"
              required
            />
          </label>

          <label className="input" htmlFor="register-email">
            <span>Email</span>
            <input
              id="register-email"
              className="input_field"
              type="email"
              name="email"
              value={form.email}
              onChange={handleChange}
              autoComplete="email"
              required
            />
          </label>

          <label className="input" htmlFor="register-password">
            <span>Password</span>
            <input
              id="register-password"
              className="input_field"
              type="password"
              name="password"
              value={form.password}
              onChange={handleChange}
              autoComplete="new-password"
              required
            />
          </label>

          <div className="submit_panel">
            <button className="submit" type="submit" disabled={isSubmitting}>
              {isSubmitting ? "Registering..." : "Register"}
            </button>
          </div>
          {message && <p role="status" aria-live="polite">{message}</p>}
          <p>Already have an account? <a href="/login">Log in</a></p>
        </form>
      </main>
    </div>
  );
};

export default Register;
