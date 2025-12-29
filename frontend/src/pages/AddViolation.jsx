import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

export default function AddViolation() {
  const [vehicleNumber, setVehicleNumber] = useState("");
  const [violationType, setViolationType] = useState("");
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  // Handle image preview
  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);

    if (selectedFile) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result);
      };
      reader.readAsDataURL(selectedFile);
    } else {
      setPreview(null);
    }
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!file) {
      setMessage("Please select an image");
      return;
    }

    const formData = new FormData();
    formData.append("vehicle_number", vehicleNumber);
    formData.append("violation_type", violationType);
    formData.append("file", file);

    try {
      const res = await axios.post("http://127.0.0.1:8000/upload/violation", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setMessage("✅ " + res.data.message);
      setVehicleNumber("");
      setViolationType("");
      setFile(null);
      setPreview(null);

      // Redirect to dashboard
      setTimeout(() => {
        navigate("/");
      }, 1500);
    } catch (err) {
      // Show the actual error message from the API
      const errorMessage = err.response?.data?.detail || "Failed to upload violation";
      setMessage("❌ " + errorMessage);
      console.error(err);
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10 bg-white p-6 rounded-2xl shadow">
      <h2 className="text-2xl font-bold mb-4 text-center text-gray-700">
        Add New Violation
      </h2>

      <form onSubmit={handleSubmit} className="flex flex-col space-y-4">
        <input
          type="text"
          placeholder="Vehicle Number"
          value={vehicleNumber}
          onChange={(e) => setVehicleNumber(e.target.value)}
          required
          className="border border-gray-300 rounded-lg px-3 py-2"
        />

        {/* UPDATED DROPDOWN */}
        <select
          value={violationType}
          onChange={(e) => setViolationType(e.target.value)}
          required
          className="border border-gray-300 rounded-lg px-3 py-2"
        >
          <option value="">Select Violation Type</option>
          <option value="No Helmet">No Helmet</option>
          <option value="Mobile Usage">Mobile Usage</option>
          <option value="Triple Riding">Triple Riding</option>
        </select>

        <input
          type="file"
          accept="image/*"
          onChange={handleFileChange}
          required
          className="border border-gray-300 rounded-lg px-3 py-2"
        />

        {/* Image preview */}
        {preview && (
          <div className="mt-2 text-center">
            <img
              src={preview}
              alt="Preview"
              className="max-h-48 rounded-lg border border-gray-300 mx-auto"
            />
          </div>
        )}

        <button
          type="submit"
          className="bg-blue-600 text-white rounded-lg py-2 hover:bg-blue-700 transition"
        >
          Upload Violation
        </button>
      </form>

      {message && (
        <p className="mt-4 text-center text-green-600 font-semibold">
          {message}
        </p>
      )}
    </div>
  );
}
