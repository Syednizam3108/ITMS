import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function SignupPage() {
  const navigate = useNavigate();
  const { register } = useAuth();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    fullName: '',
    officerId: '',
    email: '',
    phone: '',
    department: '',
    designation: '',
    password: '',
    confirmPassword: '',
    agreeTerms: false
  });

  const [errors, setErrors] = useState({});

  const departments = [
    'Traffic Police',
    'Highway Patrol',
    'City Traffic Management',
    'Regional Transport Office',
    'Traffic Control Room'
  ];

  const designations = [
    'Traffic Constable',
    'Head Constable',
    'Sub-Inspector',
    'Inspector',
    'Deputy Superintendent',
    'Superintendent'
  ];

  const validateForm = () => {
    const newErrors = {};

    if (!formData.fullName.trim()) {
      newErrors.fullName = 'Full name is required';
    }

    if (!formData.officerId.trim()) {
      newErrors.officerId = 'Officer ID is required';
    }

    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email is invalid';
    }

    if (!formData.phone.trim()) {
      newErrors.phone = 'Phone number is required';
    } else if (!/^\d{10}$/.test(formData.phone.replace(/\D/g, ''))) {
      newErrors.phone = 'Phone number must be 10 digits';
    }

    if (!formData.department) {
      newErrors.department = 'Department is required';
    }

    if (!formData.designation) {
      newErrors.designation = 'Designation is required';
    }

    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters';
    }

    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }

    if (!formData.agreeTerms) {
      newErrors.agreeTerms = 'You must agree to the terms and conditions';
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
      const result = await register(
        formData.email,
        formData.password,
        formData.fullName,
        'officer'
      );
      
      if (result.success) {
        navigate('/dashboard');
      } else {
        setError(result.error || 'Registration failed. Please try again.');
      }
    } catch (err) {
      setError('Registration failed. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleChange = (field, value) => {
    setFormData({ ...formData, [field]: value });
    // Clear error when user starts typing
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
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
          {/* Form Header */}
          <div className="bg-gradient-to-r from-teal-600 to-emerald-600 px-8 py-8 text-center">
            <div className="w-16 h-16 flex items-center justify-center bg-white/20 rounded-full mx-auto mb-4">
              <i className="ri-user-add-line text-white text-3xl"></i>
            </div>
            <h2 className="text-3xl font-bold text-white mb-2">Officer Registration</h2>
            <p className="text-teal-50">Create your account to access the Traffic Management System</p>
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

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Full Name */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Full Name <span className="text-red-500">*</span>
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <i className="ri-user-line text-gray-400"></i>
                  </div>
                  <input
                    type="text"
                    value={formData.fullName}
                    onChange={(e) => handleChange('fullName', e.target.value)}
                    className={`w-full pl-10 pr-4 py-2.5 border ${errors.fullName ? 'border-red-500' : 'border-gray-300'} rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent text-sm`}
                    placeholder="Enter your full name"
                  />
                </div>
                {errors.fullName && <p className="mt-1 text-xs text-red-500">{errors.fullName}</p>}
              </div>

              {/* Officer ID */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Officer ID <span className="text-red-500">*</span>
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <i className="ri-shield-user-line text-gray-400"></i>
                  </div>
                  <input
                    type="text"
                    value={formData.officerId}
                    onChange={(e) => handleChange('officerId', e.target.value)}
                    className={`w-full pl-10 pr-4 py-2.5 border ${errors.officerId ? 'border-red-500' : 'border-gray-300'} rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent text-sm`}
                    placeholder="e.g., OFFICER001"
                  />
                </div>
                {errors.officerId && <p className="mt-1 text-xs text-red-500">{errors.officerId}</p>}
              </div>

              {/* Email */}
              <div>
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
                    className={`w-full pl-10 pr-4 py-2.5 border ${errors.email ? 'border-red-500' : 'border-gray-300'} rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent text-sm`}
                    placeholder="officer@trafficai.gov.in"
                  />
                </div>
                {errors.email && <p className="mt-1 text-xs text-red-500">{errors.email}</p>}
              </div>

              {/* Phone */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Phone Number <span className="text-red-500">*</span>
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <i className="ri-phone-line text-gray-400"></i>
                  </div>
                  <input
                    type="tel"
                    value={formData.phone}
                    onChange={(e) => handleChange('phone', e.target.value)}
                    className={`w-full pl-10 pr-4 py-2.5 border ${errors.phone ? 'border-red-500' : 'border-gray-300'} rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent text-sm`}
                    placeholder="10-digit mobile number"
                  />
                </div>
                {errors.phone && <p className="mt-1 text-xs text-red-500">{errors.phone}</p>}
              </div>

              {/* Department */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Department <span className="text-red-500">*</span>
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <i className="ri-building-line text-gray-400"></i>
                  </div>
                  <select
                    value={formData.department}
                    onChange={(e) => handleChange('department', e.target.value)}
                    className={`w-full pl-10 pr-4 py-2.5 border ${errors.department ? 'border-red-500' : 'border-gray-300'} rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent text-sm cursor-pointer`}
                  >
                    <option value="">Select department</option>
                    {departments.map((dept) => (
                      <option key={dept} value={dept}>{dept}</option>
                    ))}
                  </select>
                </div>
                {errors.department && <p className="mt-1 text-xs text-red-500">{errors.department}</p>}
              </div>

              {/* Designation */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Designation <span className="text-red-500">*</span>
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <i className="ri-medal-line text-gray-400"></i>
                  </div>
                  <select
                    value={formData.designation}
                    onChange={(e) => handleChange('designation', e.target.value)}
                    className={`w-full pl-10 pr-4 py-2.5 border ${errors.designation ? 'border-red-500' : 'border-gray-300'} rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent text-sm cursor-pointer`}
                  >
                    <option value="">Select designation</option>
                    {designations.map((desig) => (
                      <option key={desig} value={desig}>{desig}</option>
                    ))}
                  </select>
                </div>
                {errors.designation && <p className="mt-1 text-xs text-red-500">{errors.designation}</p>}
              </div>

              {/* Password */}
              <div>
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
                    className={`w-full pl-10 pr-4 py-2.5 border ${errors.password ? 'border-red-500' : 'border-gray-300'} rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent text-sm`}
                    placeholder="Minimum 8 characters"
                  />
                </div>
                {errors.password && <p className="mt-1 text-xs text-red-500">{errors.password}</p>}
              </div>

              {/* Confirm Password */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Confirm Password <span className="text-red-500">*</span>
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <i className="ri-lock-line text-gray-400"></i>
                  </div>
                  <input
                    type="password"
                    value={formData.confirmPassword}
                    onChange={(e) => handleChange('confirmPassword', e.target.value)}
                    className={`w-full pl-10 pr-4 py-2.5 border ${errors.confirmPassword ? 'border-red-500' : 'border-gray-300'} rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent text-sm`}
                    placeholder="Re-enter password"
                  />
                </div>
                {errors.confirmPassword && <p className="mt-1 text-xs text-red-500">{errors.confirmPassword}</p>}
              </div>
            </div>

            {/* Terms and Conditions */}
            <div className="mt-6">
              <label className="flex items-start cursor-pointer">
                <input
                  type="checkbox"
                  checked={formData.agreeTerms}
                  onChange={(e) => handleChange('agreeTerms', e.target.checked)}
                  className={`w-4 h-4 text-teal-600 border-gray-300 rounded focus:ring-teal-500 cursor-pointer mt-0.5 ${errors.agreeTerms ? 'border-red-500' : ''}`}
                />
                <span className="ml-2 text-sm text-gray-700">
                  I agree to the <button type="button" className="text-teal-600 hover:text-teal-700 font-medium cursor-pointer">Terms and Conditions</button> and <button type="button" className="text-teal-600 hover:text-teal-700 font-medium cursor-pointer">Privacy Policy</button>
                </span>
              </label>
              {errors.agreeTerms && <p className="mt-1 text-xs text-red-500">{errors.agreeTerms}</p>}
            </div>

            {/* Info Box */}
            <div className="mt-6 bg-amber-50 border border-amber-200 rounded-lg p-4">
              <div className="flex gap-3">
                <i className="ri-information-line text-amber-600 text-lg flex-shrink-0"></i>
                <div className="text-xs text-amber-900">
                  <p className="font-medium mb-1">Registration Notice</p>
                  <p>Your registration will be reviewed by the system administrator. You will receive a confirmation email once your account is approved.</p>
                </div>
              </div>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={isSubmitting}
              className="w-full mt-8 py-3 bg-gradient-to-r from-teal-600 to-emerald-600 text-white rounded-lg text-base font-semibold hover:from-teal-700 hover:to-emerald-700 transition-all whitespace-nowrap cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 shadow-lg shadow-teal-600/30"
            >
              {isSubmitting ? (
                <>
                  <i className="ri-loader-4-line animate-spin"></i>
                  Creating Account...
                </>
              ) : (
                <>
                  <i className="ri-user-add-line"></i>
                  Create Officer Account
                </>
              )}
            </button>

            {/* Login Link */}
            <p className="mt-6 text-center text-sm text-gray-600">
              Already have an account?{' '}
              <button
                type="button"
                onClick={() => navigate('/login')}
                className="text-teal-600 hover:text-teal-700 font-medium cursor-pointer"
              >
                Login here
              </button>
            </p>
          </form>
        </div>
      </div>
    </div>
  );
}
