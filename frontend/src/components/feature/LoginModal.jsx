import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function LoginModal({ onClose }) {
  const navigate = useNavigate();
  const [isClosing, setIsClosing] = useState(false);

  const handleClose = () => {
    setIsClosing(true);
    setTimeout(() => {
      onClose();
    }, 200);
  };

  const handleLogin = () => {
    navigate('/login');
    onClose();
  };

  const handleSignup = () => {
    navigate('/signup');
    onClose();
  };

  return (
    <div
      className={`fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm transition-opacity duration-200 ${
        isClosing ? 'opacity-0' : 'opacity-100'
      }`}
      onClick={handleClose}
    >
      <div
        className={`bg-white rounded-2xl shadow-2xl max-w-md w-full mx-4 overflow-hidden transform transition-all duration-200 ${
          isClosing ? 'scale-95 opacity-0' : 'scale-100 opacity-100'
        }`}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="relative bg-gradient-to-br from-teal-600 to-emerald-600 p-8 text-white">
          <button
            onClick={handleClose}
            className="absolute top-4 right-4 w-8 h-8 flex items-center justify-center rounded-full hover:bg-white/20 transition-colors"
          >
            <i className="ri-close-line text-xl"></i>
          </button>
          <div className="w-16 h-16 flex items-center justify-center bg-white/20 rounded-2xl mb-4">
            <i className="ri-shield-user-line text-4xl"></i>
          </div>
          <h2 className="text-2xl font-bold mb-2">Welcome to TrafficAI</h2>
          <p className="text-teal-100 text-sm">Access your officer dashboard</p>
        </div>

        {/* Content */}
        <div className="p-8">
          <div className="space-y-4">
            <button
              onClick={handleLogin}
              className="w-full px-6 py-4 bg-teal-600 text-white rounded-xl font-semibold hover:bg-teal-700 transition-colors flex items-center justify-center gap-2 shadow-lg shadow-teal-600/30"
            >
              <i className="ri-login-box-line text-xl"></i>
              Officer Login
            </button>

            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-gray-300"></div>
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-4 bg-white text-gray-500">or</span>
              </div>
            </div>

            <button
              onClick={handleSignup}
              className="w-full px-6 py-4 bg-white border-2 border-gray-300 text-gray-700 rounded-xl font-semibold hover:border-teal-600 hover:text-teal-600 transition-colors flex items-center justify-center gap-2"
            >
              <i className="ri-user-add-line text-xl"></i>
              Create Account
            </button>
          </div>

          <div className="mt-6 pt-6 border-t border-gray-200">
            <p className="text-xs text-gray-500 text-center">
              <i className="ri-information-line mr-1"></i>
              For authorized traffic officers only. Unauthorized access is prohibited.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
