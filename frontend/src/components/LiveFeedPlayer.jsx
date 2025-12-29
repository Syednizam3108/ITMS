import React, { useEffect, useRef, useState } from 'react'
import { FiCamera, FiAlertCircle, FiRefreshCw, FiAlertTriangle } from 'react-icons/fi'

export default function LiveFeedPlayer() {
  const videoRef = useRef(null)
  const canvasRef = useRef(null)
  const [streaming, setStreaming] = useState(false)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(true)
  const [detectionEnabled, setDetectionEnabled] = useState(false)
  const [violations, setViolations] = useState([])
  const [detectionResults, setDetectionResults] = useState(null)

  const startCamera = async () => {
    setLoading(true)
    setError(null)
    setStreaming(false)
    
    try {
      // Stop any existing stream
      if (videoRef.current?.srcObject) {
        const tracks = videoRef.current.srcObject.getTracks()
        tracks.forEach(track => track.stop())
      }

      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: { 
          width: { ideal: 1920 },
          height: { ideal: 1080 },
          facingMode: 'environment'  // Use back camera for road monitoring
        },
        audio: false
      })
      
      if (videoRef.current) {
        videoRef.current.srcObject = stream
        // Wait for video to be ready
        videoRef.current.onloadedmetadata = () => {
          videoRef.current.play().then(() => {
            setStreaming(true)
            setLoading(false)
          }).catch(err => {
            console.error("Video play error:", err)
            setError("Failed to play video: " + err.message)
            setLoading(false)
          })
        }
      }
    } catch (err) {
      console.error("Camera access error:", err)
      let errorMsg = "Camera access denied. Please allow camera permissions in your browser."
      if (err.name === 'NotFoundError') {
        errorMsg = "No camera found on this device."
      } else if (err.name === 'NotAllowedError') {
        errorMsg = "Camera permission denied. Click the camera icon in the address bar to allow access."
      } else if (err.name === 'NotReadableError') {
        errorMsg = "Camera is already in use by another application."
      }
      setError(errorMsg)
      setLoading(false)
    }
  }

  const captureAndDetect = async () => {
    if (!videoRef.current || !canvasRef.current || !streaming) return

    const canvas = canvasRef.current
    const video = videoRef.current
    
    canvas.width = video.videoWidth
    canvas.height = video.videoHeight
    
    const ctx = canvas.getContext('2d')
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height)
    
    // Convert to base64 with HIGH QUALITY (0.95 instead of 0.6) for better detection
    const frameData = canvas.toDataURL('image/jpeg', 0.95)
    
    try {
      const response = await fetch('http://127.0.0.1:8000/detection/detect-snapshot', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ frame: frameData })
      })
      
      const result = await response.json()
      
      if (result.success) {
        setDetectionResults(result)
        
        // Show notification if violations detected
        if (result.violations && result.violations.length > 0) {
          setViolations(prev => {
            const newViolations = [...result.violations, ...prev].slice(0, 10)
            return newViolations
          })
        }
      }
    } catch (err) {
      console.error('Detection error:', err)
    }
  }

  useEffect(() => {
    startCamera()
    
    // Cleanup
    return () => {
      if (videoRef.current?.srcObject) {
        const tracks = videoRef.current.srcObject.getTracks()
        tracks.forEach(track => track.stop())
      }
    }
  }, [])

  useEffect(() => {
    let interval
    if (detectionEnabled && streaming) {
      // Detect every 2 seconds for faster response
      interval = setInterval(captureAndDetect, 2000)
    }
    return () => clearInterval(interval)
  }, [detectionEnabled, streaming])

  return (
    <div className="space-y-4">
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold flex items-center gap-2">
            <FiCamera className="text-blue-600" />
            Live Camera Feed with AI Detection
          </h3>
          <div className="flex gap-2">
            <button
              onClick={() => setDetectionEnabled(!detectionEnabled)}
              disabled={!streaming}
              className={`px-4 py-2 rounded-lg font-medium transition ${
                detectionEnabled 
                  ? 'bg-red-600 hover:bg-red-700 text-white' 
                  : 'bg-green-600 hover:bg-green-700 text-white'
              } disabled:opacity-50 disabled:cursor-not-allowed`}
            >
              {detectionEnabled ? '⏸ Stop Detection' : '▶ Start Detection'}
            </button>
            <span className={`px-3 py-1 rounded-full text-xs font-medium flex items-center gap-1 ${
              streaming ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
            }`}>
              <span className={`w-2 h-2 rounded-full ${streaming ? 'bg-green-600 animate-pulse' : 'bg-gray-400'}`}></span>
              {streaming ? 'LIVE' : 'OFFLINE'}
            </span>
          </div>
        </div>

        <div className="relative bg-gray-900 rounded-lg overflow-hidden" style={{ aspectRatio: '16/9' }}>
          <video 
            ref={videoRef} 
            autoPlay 
            playsInline 
            muted
            className="w-full h-full object-cover"
          />
          
          <canvas 
            ref={canvasRef}
            className="hidden"
          />

          {loading && (
            <div className="absolute inset-0 flex flex-col items-center justify-center text-white bg-gray-900">
              <FiRefreshCw className="w-12 h-12 animate-spin mb-4" />
              <p className="text-lg">Accessing camera...</p>
              <p className="text-xs text-gray-400 mt-2">Please allow camera permissions if prompted</p>
            </div>
          )}

          {error && (
            <div className="absolute inset-0 flex flex-col items-center justify-center text-white p-8 bg-gray-900">
              <FiAlertCircle className="w-16 h-16 text-yellow-500 mb-4" />
              <p className="text-lg mb-2 font-semibold">Camera Access Required</p>
              <p className="text-sm text-gray-300 mb-6 text-center max-w-md">{error}</p>
              <button 
                onClick={startCamera}
                className="px-6 py-3 bg-blue-600 hover:bg-blue-700 rounded-lg transition flex items-center gap-2 font-medium"
              >
                <FiRefreshCw /> Retry Camera Access
              </button>
            </div>
          )}

          {detectionEnabled && detectionResults && (
            <div className="absolute top-4 left-4 bg-black/70 text-white px-4 py-2 rounded-lg">
              <div className="text-sm">
                <span className="font-semibold">Violations Detected: </span>
                <span className={detectionResults.violation_count > 0 ? 'text-red-400 font-bold' : 'text-green-400'}>
                  {detectionResults.violation_count}
                </span>
              </div>
            </div>
          )}
        </div>

        <div className="mt-4 grid grid-cols-4 gap-4 text-center text-sm">
          <div className="p-3 bg-gray-50 rounded-lg">
            <div className="text-xs text-gray-500 mb-1">Resolution</div>
            <div className="font-semibold">1280x720</div>
          </div>
          <div className="p-3 bg-gray-50 rounded-lg">
            <div className="text-xs text-gray-500 mb-1">FPS</div>
            <div className="font-semibold">30</div>
          </div>
          <div className="p-3 bg-gray-50 rounded-lg">
            <div className="text-xs text-gray-500 mb-1">Status</div>
            <div className={`font-semibold ${streaming ? 'text-green-600' : 'text-gray-600'}`}>
              {streaming ? 'Active' : 'Inactive'}
            </div>
          </div>
          <div className={`p-3 rounded-lg ${detectionResults?.violation_count > 0 ? 'bg-red-50' : 'bg-gray-50'}`}>
            <div className="text-xs text-gray-500 mb-1">AI Detection</div>
            <div className={`font-semibold ${detectionEnabled ? 'text-blue-600' : 'text-gray-600'}`}>
              {detectionEnabled ? 'Running' : 'Stopped'}
            </div>
          </div>
        </div>
      </div>

      {/* Violations Panel */}
      {violations.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h4 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <FiAlertTriangle className="text-red-600" />
            Recent Violations Detected ({violations.length})
          </h4>
          <div className="space-y-3 max-h-96 overflow-y-auto">
            {violations.map((violation, index) => (
              <div key={index} className="flex items-center justify-between p-4 bg-gradient-to-r from-red-50 to-orange-50 border-l-4 border-red-600 rounded-lg shadow-sm hover:shadow-md transition">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="px-2 py-1 bg-red-600 text-white text-xs font-bold rounded">
                      VIOLATION
                    </span>
                    <p className="font-bold text-red-900">{violation.type}</p>
                  </div>
                  <p className="text-sm text-gray-700 mb-1">
                    <span className="font-semibold">Confidence:</span> {(violation.confidence * 100).toFixed(1)}%
                  </p>
                  <p className="text-xs text-gray-500">
                    📸 Snapshot saved • {new Date(violation.timestamp).toLocaleString()}
                  </p>
                </div>
                <div className="text-right">
                  <div className="text-xs text-gray-500 mb-1">Auto-Saved</div>
                  <div className="text-green-600 text-2xl">✓</div>
                </div>
              </div>
            ))}
          </div>
          <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-lg text-sm text-blue-800">
            💡 <strong>Note:</strong> All violations are automatically saved to the database with snapshots for review.
          </div>
        </div>
      )}
    </div>
  )
}
