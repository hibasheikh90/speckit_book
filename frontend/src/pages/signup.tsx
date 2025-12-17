import React, { useState } from 'react';
import Layout from '@theme/Layout';
import { useAuth } from '../contexts/AuthContext';
import ExecutionEnvironment from '@docusaurus/ExecutionEnvironment';
import Link from '@docusaurus/Link';
import './signin.css';

function SignupPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const auth = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (password.length < 6) {
      setError('Password must be at least 6 characters');
      return;
    }

    setLoading(true);

    try {
      await auth.register(email, password);
      // After successful registration, redirect to login
      if (ExecutionEnvironment.canUseDOM) {
        window.location.href = '/signin';
      }
    } catch (err: any) {
      setError(err.message || 'Failed to register');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout title="Sign Up" description="Create an account for the Physical AI Textbook">
      <div className="auth-container">
        <div className="auth-box">
          <h1 className="auth-title">Sign up</h1>
          <form onSubmit={handleSubmit} className="auth-form">
            {error && <div className="auth-error">{error}</div>}
            <div className="auth-input-group">
              <label htmlFor="email" className="auth-label">Email Address</label>
              <input
                type="email"
                id="email"
                name="email"
                className="auth-input"
                required
                autoComplete="email"
                autoFocus
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <div className="auth-input-group">
              <label htmlFor="password" className="auth-label">Password</label>
              <input
                type="password"
                id="password"
                name="password"
                className="auth-input"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
            <div className="auth-input-group">
              <label htmlFor="confirmPassword" className="auth-label">Confirm Password</label>
              <input
                type="password"
                id="confirmPassword"
                name="confirmPassword"
                className="auth-input"
                required
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
              />
            </div>
            <button
              type="submit"
              className="auth-button"
              disabled={loading}
            >
              {loading ? 'Creating account...' : 'Sign Up'}
            </button>
            <div className="auth-link">
              <Link to="/signin">
                Already have an account? Sign in
              </Link>
            </div>
          </form>
        </div>
      </div>
    </Layout>
  );
}

export default SignupPage;
