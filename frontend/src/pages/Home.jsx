import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import LoginModal from '../components/feature/LoginModal';

export default function HomePage() {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [showLoginModal, setShowLoginModal] = useState(false);

  // Redirect to dashboard if already logged in
  useEffect(() => {
    if (user) {
      navigate('/dashboard');
    }
  }, [user, navigate]);

  const features = [
    {
      icon: 'ri-camera-ai-line',
      title: 'AI-Powered Detection',
      description: 'Advanced computer vision algorithms detect traffic violations in real-time with 98%+ accuracy using YOLOv8 and deep learning models.'
    },
    {
      icon: 'ri-car-line',
      title: 'Automatic Number Plate Recognition',
      description: 'Instantly identify vehicles with ANPR technology, automatically fetching owner details from integrated databases.'
    },
    {
      icon: 'ri-mail-send-line',
      title: 'Automated E-Challan',
      description: 'Generate and send digital challans automatically via email and SMS with payment links and violation evidence.'
    },
    {
      icon: 'ri-line-chart-line',
      title: 'Real-Time Analytics',
      description: 'Comprehensive dashboards with violation trends, hotspot mapping, and actionable insights for traffic management.'
    },
    {
      icon: 'ri-shield-check-line',
      title: 'Evidence Management',
      description: 'Capture and store high-quality images and videos as legal evidence for every detected violation.'
    },
    {
      icon: 'ri-time-line',
      title: '24/7 Monitoring',
      description: 'Continuous surveillance across multiple camera feeds with instant alerts for critical violations.'
    }
  ];

  const stats = [
    { value: '50K+', label: 'Violations Detected', icon: 'ri-alert-line' },
    { value: '98.5%', label: 'Detection Accuracy', icon: 'ri-checkbox-circle-line' },
    { value: '150+', label: 'Active Cameras', icon: 'ri-camera-line' },
    { value: '₹2.5Cr', label: 'Revenue Collected', icon: 'ri-money-rupee-circle-line' }
  ];

  const violationTypes = [
    { name: 'No Helmet', icon: 'ri-user-forbid-line', color: 'bg-red-500' },
    { name: 'Red Light Jump', icon: 'ri-traffic-light-line', color: 'bg-orange-500' },
    { name: 'Mobile Usage', icon: 'ri-smartphone-line', color: 'bg-yellow-500' },
    { name: 'Overloading', icon: 'ri-truck-line', color: 'bg-purple-500' },
    { name: 'Wrong Side', icon: 'ri-arrow-left-right-line', color: 'bg-pink-500' },
    { name: 'Speed Violation', icon: 'ri-speed-line', color: 'bg-indigo-500' }
  ];

  const howItWorks = [
    {
      step: '01',
      title: 'AI Detection',
      description: 'Smart cameras continuously monitor traffic and detect violations using advanced AI algorithms.',
      icon: 'ri-eye-line'
    },
    {
      step: '02',
      title: 'Vehicle Identification',
      description: 'ANPR technology instantly reads number plates and retrieves vehicle owner information.',
      icon: 'ri-search-eye-line'
    },
    {
      step: '03',
      title: 'Officer Review',
      description: 'Traffic officers review detected violations with complete evidence before approval.',
      icon: 'ri-user-search-line'
    },
    {
      step: '04',
      title: 'E-Challan Issued',
      description: 'Automated e-challans are generated and sent to vehicle owners with payment options.',
      icon: 'ri-file-list-3-line'
    }
  ];

  return (
    <div className="min-h-screen bg-white">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-40 transition-all duration-300 bg-white/95 backdrop-blur-sm shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 flex items-center justify-center bg-gradient-to-br from-teal-600 to-emerald-600 rounded-lg">
                <i className="ri-traffic-light-line text-white text-xl"></i>
              </div>
              <div>
                <h1 className="text-lg font-bold text-gray-900">TrafficAI</h1>
                <p className="text-xs text-gray-600">Smart Traffic Management</p>
              </div>
            </div>

            {/* Navigation Links */}
            <div className="hidden md:flex items-center gap-8">
              <a href="#features" className="text-sm font-medium text-gray-700 hover:text-teal-600 transition-colors cursor-pointer">
                Features
              </a>
              <a href="#how-it-works" className="text-sm font-medium text-gray-700 hover:text-teal-600 transition-colors cursor-pointer">
                How It Works
              </a>
              <a href="#violations" className="text-sm font-medium text-gray-700 hover:text-teal-600 transition-colors cursor-pointer">
                Violations
              </a>
              <a href="#contact" className="text-sm font-medium text-gray-700 hover:text-teal-600 transition-colors cursor-pointer">
                Contact
              </a>
            </div>

            {/* CTA Button */}
            <div>
              <button
                onClick={() => setShowLoginModal(true)}
                className="px-6 py-2 bg-teal-600 text-white rounded-lg text-sm font-medium hover:bg-teal-700 transition-colors whitespace-nowrap cursor-pointer"
              >
                <i className="ri-login-box-line mr-2"></i>
                Officer Login
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative pt-32 pb-20 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-teal-50 via-white to-emerald-50"></div>
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-20 left-10 w-72 h-72 bg-teal-500 rounded-full blur-3xl"></div>
          <div className="absolute bottom-20 right-10 w-96 h-96 bg-emerald-500 rounded-full blur-3xl"></div>
        </div>
        
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <div className="inline-flex items-center gap-2 px-4 py-2 bg-teal-100 text-teal-700 rounded-full text-sm font-medium mb-6">
                <i className="ri-sparkling-line"></i>
                AI-Powered Traffic Enforcement
              </div>
              <h1 className="text-5xl font-bold text-gray-900 mb-6 leading-tight">
                Intelligent Traffic Management for Safer Roads
              </h1>
              <p className="text-lg text-gray-600 mb-8 leading-relaxed">
                Revolutionize traffic enforcement with AI-powered violation detection, automated e-challan generation, and real-time analytics. Reduce accidents, improve compliance, and make roads safer for everyone.
              </p>
              <div className="flex flex-wrap gap-4">
                <button
                  onClick={() => navigate('/dashboard')}
                  className="px-8 py-3 bg-teal-600 text-white rounded-lg text-base font-semibold hover:bg-teal-700 transition-colors whitespace-nowrap cursor-pointer shadow-lg shadow-teal-600/30"
                >
                  <i className="ri-dashboard-line mr-2"></i>
                  Access Dashboard
                </button>
                <button
                  onClick={() => document.getElementById('how-it-works')?.scrollIntoView({ behavior: 'smooth' })}
                  className="px-8 py-3 bg-white border-2 border-gray-300 text-gray-700 rounded-lg text-base font-semibold hover:border-teal-600 hover:text-teal-600 transition-colors whitespace-nowrap cursor-pointer"
                >
                  <i className="ri-play-circle-line mr-2"></i>
                  Learn More
                </button>
              </div>
            </div>
            <div className="relative">
              <div className="relative rounded-2xl overflow-hidden shadow-2xl">
                <img 
                  src="https://readdy.ai/api/search-image?query=modern%20traffic%20control%20room%20with%20multiple%20surveillance%20camera%20monitors%20showing%20indian%20roads%20artificial%20intelligence%20detection%20system%20professional%20monitoring%20setup%20futuristic%20technology%20dashboard%20screens&width=600&height=500&seq=hero001&orientation=landscape" 
                  alt="Traffic monitoring control room with multiple surveillance camera feeds showing highways"
                  className="w-full h-full object-cover aspect-video"
                  onError={(e) => {
                    e.target.onerror = null;
                    e.target.style.display = 'none';
                    e.target.parentElement.innerHTML = '<div class="aspect-video bg-gradient-to-br from-gray-800 to-gray-900 flex items-center justify-center"><i class="ri-cctv-line text-white/40 text-9xl"></i></div>';
                  }}
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/40 via-transparent to-transparent"></div>
              </div>
              <div className="absolute -bottom-6 -left-6 bg-white rounded-xl shadow-xl p-4 border border-gray-200">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 flex items-center justify-center bg-green-100 rounded-lg">
                    <i className="ri-checkbox-circle-fill text-green-600 text-2xl"></i>
                  </div>
                  <div>
                    <p className="text-2xl font-bold text-gray-900">98.5%</p>
                    <p className="text-xs text-gray-600">Detection Accuracy</p>
                  </div>
                </div>
              </div>
              <div className="absolute -top-6 -right-6 bg-white rounded-xl shadow-xl p-4 border border-gray-200">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 flex items-center justify-center bg-teal-100 rounded-lg">
                    <i className="ri-camera-line text-teal-600 text-2xl"></i>
                  </div>
                  <div>
                    <p className="text-2xl font-bold text-gray-900">150+</p>
                    <p className="text-xs text-gray-600">Active Cameras</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section id="stats" className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-6">
            {stats.map((stat, index) => (
              <div key={index} className="bg-white rounded-xl p-6 shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
                <div className="w-12 h-12 flex items-center justify-center bg-teal-100 rounded-lg mb-4">
                  <i className={`${stat.icon} text-teal-600 text-2xl`}></i>
                </div>
                <p className="text-3xl font-bold text-gray-900 mb-1">{stat.value}</p>
                <p className="text-sm text-gray-600">{stat.label}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Violation Types */}
      <section id="violations" className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Detectable Violations</h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Our AI system can detect and classify multiple types of traffic violations with high accuracy
            </p>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            {violationTypes.map((violation, index) => (
              <div key={index} className="bg-white border border-gray-200 rounded-xl p-6 hover:shadow-lg transition-all hover:-translate-y-1 cursor-pointer">
                <div className={`w-14 h-14 flex items-center justify-center ${violation.color} rounded-lg mb-4 mx-auto`}>
                  <i className={`${violation.icon} text-white text-2xl`}></i>
                </div>
                <p className="text-sm font-semibold text-gray-900 text-center">{violation.name}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Powerful Features</h2>
            <p className="text-lg text-gray-600 max-w-3xl mx-auto">
              Comprehensive traffic management solution with cutting-edge AI technology and seamless automation
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <div key={index} className="bg-white rounded-xl p-8 shadow-sm border border-gray-200 hover:shadow-xl transition-all hover:-translate-y-1">
                <div className="w-14 h-14 flex items-center justify-center bg-teal-100 rounded-lg mb-6">
                  <i className={`${feature.icon} text-teal-600 text-2xl`}></i>
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-3">{feature.title}</h3>
                <p className="text-gray-600 leading-relaxed">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section id="how-it-works" className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">How It Works</h2>
            <p className="text-lg text-gray-600 max-w-3xl mx-auto">
              From detection to enforcement - a seamless automated workflow
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {howItWorks.map((item, index) => (
              <div key={index} className="relative">
                <div className="bg-gradient-to-br from-teal-50 to-emerald-50 rounded-xl p-8 border border-teal-200 hover:shadow-lg transition-shadow">
                  <div className="text-6xl font-bold text-teal-200 mb-4">{item.step}</div>
                  <div className="w-14 h-14 flex items-center justify-center bg-teal-600 rounded-lg mb-6">
                    <i className={`${item.icon} text-white text-2xl`}></i>
                  </div>
                  <h3 className="text-xl font-bold text-gray-900 mb-3">{item.title}</h3>
                  <p className="text-gray-600 leading-relaxed">{item.description}</p>
                </div>
                {index < howItWorks.length - 1 && (
                  <div className="hidden lg:block absolute top-1/2 -right-4 transform -translate-y-1/2">
                    <i className="ri-arrow-right-line text-3xl text-teal-300"></i>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-br from-teal-600 to-emerald-600 relative overflow-hidden">
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-0 left-0 w-96 h-96 bg-white rounded-full blur-3xl"></div>
          <div className="absolute bottom-0 right-0 w-96 h-96 bg-white rounded-full blur-3xl"></div>
        </div>
        <div className="relative max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl font-bold text-white mb-6">
            Ready to Transform Traffic Management?
          </h2>
          <p className="text-xl text-teal-50 mb-10 leading-relaxed">
            Join the future of intelligent traffic enforcement. Access the dashboard and start monitoring violations in real-time.
          </p>
          <div className="flex flex-wrap gap-4 justify-center">
            <button
              onClick={() => navigate('/dashboard')}
              className="px-10 py-4 bg-white text-teal-600 rounded-lg text-lg font-semibold hover:bg-gray-50 transition-colors whitespace-nowrap cursor-pointer shadow-xl"
            >
              <i className="ri-dashboard-line mr-2"></i>
              Access Dashboard
            </button>
            <button
              onClick={() => navigate('/live')}
              className="px-10 py-4 bg-teal-700 text-white rounded-lg text-lg font-semibold hover:bg-teal-800 transition-colors whitespace-nowrap cursor-pointer border-2 border-white/30"
            >
              <i className="ri-live-line mr-2"></i>
              View Live Detection
            </button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer id="contact" className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
            <div>
              <div className="flex items-center gap-3 mb-4">
                <div className="w-10 h-10 flex items-center justify-center bg-teal-600 rounded-lg">
                  <i className="ri-traffic-light-line text-white text-xl"></i>
                </div>
                <div>
                  <h3 className="text-lg font-bold">TrafficAI</h3>
                  <p className="text-xs text-gray-400">Smart Traffic Management</p>
                </div>
              </div>
              <p className="text-sm text-gray-400 leading-relaxed">
                AI-powered traffic management system for safer roads and efficient enforcement.
              </p>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Quick Links</h4>
              <ul className="space-y-2 text-sm text-gray-400">
                <li><a href="#features" className="hover:text-teal-400 transition-colors cursor-pointer">Features</a></li>
                <li><a href="#how-it-works" className="hover:text-teal-400 transition-colors cursor-pointer">How It Works</a></li>
                <li><a href="#stats" className="hover:text-teal-400 transition-colors cursor-pointer">Statistics</a></li>
                <li><button onClick={() => navigate('/dashboard')} className="hover:text-teal-400 transition-colors cursor-pointer">Dashboard</button></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">System</h4>
              <ul className="space-y-2 text-sm text-gray-400">
                <li><button onClick={() => navigate('/dashboard')} className="hover:text-teal-400 transition-colors cursor-pointer">Dashboard</button></li>
                <li><button onClick={() => navigate('/live')} className="hover:text-teal-400 transition-colors cursor-pointer">Live Detection</button></li>
                <li><button onClick={() => navigate('/analytics')} className="hover:text-teal-400 transition-colors cursor-pointer">Analytics</button></li>
                <li><button onClick={() => navigate('/violations')} className="hover:text-teal-400 transition-colors cursor-pointer">Violations</button></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Contact</h4>
              <ul className="space-y-2 text-sm text-gray-400">
                <li className="flex items-center gap-2">
                  <i className="ri-mail-line"></i>
                  support@trafficai.gov.in
                </li>
                <li className="flex items-center gap-2">
                  <i className="ri-phone-line"></i>
                  1800-XXX-XXXX
                </li>
                <li className="flex items-center gap-2">
                  <i className="ri-map-pin-line"></i>
                  Traffic Police HQ, India
                </li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 pt-8 flex flex-col md:flex-row items-center justify-between gap-4">
            <p className="text-sm text-gray-400">
              © 2025 TrafficAI. All rights reserved. Intelligent Traffic Management System.
            </p>
            <div className="flex gap-4">
              <a href="#" className="text-gray-400 hover:text-teal-400 transition-colors">
                <i className="ri-github-fill text-xl"></i>
              </a>
              <a href="#" className="text-gray-400 hover:text-teal-400 transition-colors">
                <i className="ri-twitter-fill text-xl"></i>
              </a>
              <a href="#" className="text-gray-400 hover:text-teal-400 transition-colors">
                <i className="ri-linkedin-fill text-xl"></i>
              </a>
            </div>
          </div>
        </div>
      </footer>

      {/* Login Modal */}
      {showLoginModal && (
        <LoginModal onClose={() => setShowLoginModal(false)} />
      )}
    </div>
  );
}
