import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function LoginPage() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    rememberMe: false
  });

  const [errors, setErrors] = useState({});

  const validateForm = () => {
    const newErrors = {};

    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email is invalid';
    }

    if (!formData.password) {
      newErrors.password = 'Password is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setIsSubmitting(true);
    setError('');

    try {
      const result = await login(formData.email, formData.password);
      
      if (!result.success) {
        setError(result.error || 'Login failed. Please check your credentials.');
      }
    } catch (err) {
      setError('Login failed. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleChange = (field, value) => {
    setFormData({ ...formData, [field]: value });
    if (errors[field]) {
      setErrors({ ...errors, [field]: '' });
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-teal-50 via-white to-emerald-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <button
              onClick={() => navigate('/')}
              className="flex items-center gap-3 cursor-pointer"
            >
              <div className="w-10 h-10 flex items-center justify-center bg-gradient-to-br from-teal-600 to-emerald-600 rounded-lg">
                <i className="ri-traffic-light-line text-white text-xl"></i>
              </div>
              <div>
                <h1 className="text-lg font-bold text-gray-900">TrafficAI</h1>
                <p className="text-xs text-gray-600">Smart Traffic Management</p>
              </div>
            </button>
            <button
              onClick={() => navigate('/')}
              className="text-sm text-gray-600 hover:text-teal-600 transition-colors cursor-pointer flex items-center gap-2"
            >
              <i className="ri-arrow-left-line"></i>
              Back to Home
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="flex items-center justify-center px-4 sm:px-6 lg:px-8 py-16">
        <div className="max-w-md w-full">
          <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
            {/* Form Header */}
            <div className="bg-gradient-to-r from-teal-600 to-emerald-600 px-8 py-10 text-center">
              <div className="w-16 h-16 flex items-center justify-center bg-white/20 rounded-full mx-auto mb-4">
                <i className="ri-shield-user-line text-white text-3xl"></i>
              </div>
              <h2 className="text-3xl font-bold text-white mb-2">Officer Login</h2>
              <p className="text-teal-50">Access your Traffic Management Dashboard</p>
            </div>

            {/* Form */}
            <form onSubmit={handleSubmit} className="p-8">
              {/* Error Message */}
              {error && (
                <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4 flex items-start gap-3">
                  <i className="ri-error-warning-line text-red-600 text-xl flex-shrink-0"></i>
                  <div>
                    <p className="text-sm font-medium text-red-800">{error}</p>
                  </div>
                </div>
              )}

              {/* Email */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Email Address <span className="text-red-500">*</span>
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <i className="ri-mail-line text-gray-400"></i>
                  </div>
                  <input
                    type="email"
                    value={formData.email}
                    onChange={(e) => handleChange('email', e.target.value)}
                    className={`w-full pl-10 pr-4 py-3 border ${errors.email ? 'border-red-500' : 'border-gray-300'} rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent text-sm`}
                    placeholder="officer@trafficai.gov.in"
                  />
                </div>
                {errors.email && <p className="mt-1 text-xs text-red-500">{errors.email}</p>}
              </div>

              {/* Password */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Password <span className="text-red-500">*</span>
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <i className="ri-lock-line text-gray-400"></i>
                  </div>
                  <input
                    type="password"
                    value={formData.password}
                    onChange={(e) => handleChange('password', e.target.value)}
                    className={`w-full pl-10 pr-4 py-3 border ${errors.password ? 'border-red-500' : 'border-gray-300'} rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent text-sm`}
                    placeholder="Enter your password"
                  />
                </div>
                {errors.password && <p className="mt-1 text-xs text-red-500">{errors.password}</p>}
              </div>

              {/* Remember Me & Forgot Password */}
              <div className="flex items-center justify-between mb-6">
                <label className="flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    checked={formData.rememberMe}
                    onChange={(e) => handleChange('rememberMe', e.target.checked)}
                    className="w-4 h-4 text-teal-600 border-gray-300 rounded focus:ring-teal-500 cursor-pointer"
                  />
                  <span className="ml-2 text-sm text-gray-700">Remember me</span>
                </label>
                <button
                  type="button"
                  className="text-sm text-teal-600 hover:text-teal-700 font-medium cursor-pointer"
                >
                  Forgot Password?
                </button>
              </div>

              {/* Submit Button */}
              <button
                type="submit"
                disabled={isSubmitting}
                className="w-full py-3 bg-gradient-to-r from-teal-600 to-emerald-600 text-white rounded-lg text-base font-semibold hover:from-teal-700 hover:to-emerald-700 transition-all whitespace-nowrap cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 shadow-lg shadow-teal-600/30"
              >
                {isSubmitting ? (
                  <>
                    <i className="ri-loader-4-line animate-spin"></i>
                    Signing In...
                  </>
                ) : (
                  <>
                    <i className="ri-login-box-line"></i>
                    Sign In
                  </>
                )}
              </button>

              {/* Signup Link */}
              <p className="mt-6 text-center text-sm text-gray-600">
                Don't have an account?{' '}
                <button
                  type="button"
                  onClick={() => navigate('/signup')}
                  className="text-teal-600 hover:text-teal-700 font-medium cursor-pointer"
                >
                  Register here
                </button>
              </p>

              {/* Info Box */}
              <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
                <div className="flex gap-3">
                  <i className="ri-information-line text-blue-600 text-lg flex-shrink-0"></i>
                  <div className="text-xs text-blue-900">
                    <p className="font-medium mb-1">For Authorized Officers Only</p>
                    <p>This system is restricted to authorized traffic enforcement personnel. Unauthorized access is prohibited and may result in legal action.</p>
                  </div>
                </div>
              </div>
            </form>
          </div>

          {/* Quick Access Demo */}
          <div className="mt-6 bg-white rounded-xl shadow-md p-6">
            <h3 className="text-sm font-semibold text-gray-900 mb-3 flex items-center gap-2">
              <i className="ri-sparkling-line text-teal-600"></i>
              Quick Demo Access
            </h3>
            <div className="space-y-2 text-xs text-gray-600">
              <p><strong>Email:</strong> officer@trafficai.gov.in</p>
              <p><strong>Password:</strong> demo123</p>
              <p className="text-amber-600 italic">* Demo credentials for testing purposes only</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
