# 🚦 Intelligent Traffic Management System (ITMS)
## Pseudo Code Documentation

---

## 📋 Table of Contents
1. [System Overview](#system-overview)
2. [Backend Architecture](#backend-architecture)
3. [Core Components](#core-components)
4. [Frontend Architecture](#frontend-architecture)
5. [Training Pipeline](#training-pipeline)
6. [Data Flow](#data-flow)

---

## System Overview

### High-Level System Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                    ITMS System Architecture                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐      ┌──────────────┐    ┌─────────────┐│
│  │   Frontend   │ ───> │   Backend    │───>│  MongoDB    ││
│  │   (React)    │ <─── │  (FastAPI)   │<───│  Database   ││
│  └──────────────┘      └──────────────┘    └─────────────┘│
│         │                     │                             │
│         │                     ├──> YOLOv8 Model            │
│         │                     ├──> Email Service           │
│         │                     └──> Static Files            │
│         │                                                   │
│         └──> User Interface (Violations, Analytics, etc.)  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Backend Architecture

### 1. Main Application Entry Point

```pseudocode
FUNCTION initialize_application():
    // File: backend/main.py
    
    // Load environment variables
    LOAD environment_variables FROM .env
    
    // Create FastAPI application
    CREATE app AS FastAPI_instance WITH:
        title = "Intelligent Traffic Management System API"
        description = "Backend API for traffic violation management"
        version = "2.0.0"
    
    // Configure CORS middleware
    ADD_MIDDLEWARE to app:
        type = CORSMiddleware
        allowed_origins = ["http://localhost:5173", "http://127.0.0.1:5173"]
        allowed_credentials = TRUE
        allowed_methods = ["*"]
        allowed_headers = ["*"]
    
    // Setup static file directory
    SET static_directory = "app/static"
    IF static_directory NOT EXISTS:
        CREATE_DIRECTORY static_directory
    MOUNT static_files TO "/static" endpoint
    
    // Register API routers
    INCLUDE router FOR violations
    INCLUDE router FOR officers
    INCLUDE router FOR analytics
    INCLUDE router FOR upload
    INCLUDE router FOR detection
    
    // Root endpoint
    DEFINE route GET "/" AS:
        RETURN {
            message: "Welcome to ITMS API",
            version: "1.0.0",
            database: "MongoDB",
            status: "running"
        }
    
    // Health check endpoint
    DEFINE route GET "/health" AS:
        RETURN {
            status: "healthy",
            timestamp: CURRENT_TIMESTAMP
        }
    
    RETURN app

END FUNCTION
```

---

### 2. YOLOv8 Traffic Violation Detector

```pseudocode
CLASS TrafficViolationDetector:
    // File: backend/app/yolo_detector.py
    
    // Class Properties
    PROPERTY model: YOLO_model
    PROPERTY trained_classes: DICTIONARY
    PROPERTY violation_colors: DICTIONARY
    PROPERTY use_coco_detection: BOOLEAN
    PROPERTY confidence_threshold: FLOAT = 0.50
    
    // Constructor
    FUNCTION initialize(model_path):
        SET custom_model_path = "../runs/detect/train_*/weights/best.pt"
        
        TRY:
            IF custom_model_path EXISTS:
                LOAD model FROM custom_model_path
                PRINT "✅ Custom trained model loaded (90.3% mAP@50)"
                SET use_coco_detection = FALSE
            ELSE:
                LOAD model FROM default_path
                PRINT "⚠️ Using default YOLOv8n model"
                SET use_coco_detection = TRUE
        CATCH exception:
            LOAD model FROM "yolov8n.pt"
            PRINT "⚠️ Error loading model"
        
        // Define class mappings
        SET trained_classes = {
            0: "helmet",
            1: "no_helmet",
            2: "mobile_phone",
            3: "triple_riding",
            4: "license_plate",
            5: "motorcycle"
        }
        
        // Define violation colors for visualization
        SET violation_colors = {
            0: GREEN,      // helmet
            1: RED,        // no_helmet
            2: BLUE,       // mobile_phone
            3: ORANGE,     // triple_riding
            4: YELLOW,     // license_plate
            5: GRAY        // motorcycle
        }
    END FUNCTION
    
    // Main detection function
    FUNCTION process_frame(frame_data, return_annotated):
        TRY:
            // Decode input frame
            IF frame_data IS base64_string:
                frame = DECODE_BASE64_TO_IMAGE(frame_data)
            ELSE:
                frame = frame_data
            
            // Run YOLO detection
            results = model.detect(frame, 
                                  confidence=0.50, 
                                  iou=0.45, 
                                  verbose=FALSE)
            
            // Initialize result containers
            SET violations_detected = EMPTY_LIST
            SET annotated_frame = NULL
            
            IF return_annotated:
                annotated_frame = COPY(frame)
            
            // Process detection results
            FOR EACH result IN results:
                FOR EACH box IN result.boxes:
                    SET class_id = box.class_id
                    SET confidence = box.confidence
                    SET bbox = [x1, y1, x2, y2]
                    SET class_name = trained_classes[class_id]
                    
                    // Skip low confidence detections
                    IF confidence < confidence_threshold:
                        CONTINUE
                    
                    // Categorize violation
                    violation_info = {
                        type: class_name,
                        confidence: confidence,
                        bbox: bbox,
                        class_id: class_id
                    }
                    
                    // Draw bounding box if annotation requested
                    IF return_annotated:
                        color = violation_colors[class_id]
                        DRAW_RECTANGLE(annotated_frame, bbox, color)
                        DRAW_TEXT(annotated_frame, 
                                class_name + " " + confidence,
                                bbox, color)
                    
                    ADD violation_info TO violations_detected
            
            // Extract license plates
            license_plates = EXTRACT_LICENSE_PLATES(frame, results.boxes)
            
            // Encode annotated frame if needed
            IF return_annotated AND annotated_frame IS NOT NULL:
                annotated_image = ENCODE_IMAGE_TO_BASE64(annotated_frame)
            
            RETURN {
                success: TRUE,
                violations: violations_detected,
                license_plates: license_plates,
                annotated_frame: annotated_image,
                total_detections: LENGTH(violations_detected)
            }
            
        CATCH exception AS error:
            RETURN {
                success: FALSE,
                error: error.message,
                violations: [],
                license_plates: []
            }
    END FUNCTION
    
    // Extract license plate regions
    FUNCTION extract_license_plates(frame, boxes):
        SET license_plates = EMPTY_LIST
        
        FOR EACH box IN boxes:
            IF box.class_id == LICENSE_PLATE_CLASS:
                SET bbox = [x1, y1, x2, y2]
                SET confidence = box.confidence
                
                // Crop license plate region
                plate_image = CROP(frame, bbox)
                
                IF plate_image.size > 0:
                    ADD {
                        bbox: bbox,
                        confidence: confidence,
                        image: plate_image
                    } TO license_plates
        
        RETURN license_plates
    END FUNCTION
    
    // Process uploaded image
    FUNCTION process_uploaded_image(image_path):
        // Read image from file
        frame = READ_IMAGE(image_path)
        
        // Process frame with annotation
        result = CALL process_frame(frame, return_annotated=TRUE)
        
        // Save annotated image if violations detected
        IF result.success AND LENGTH(result.violations) > 0:
            annotated_path = GENERATE_ANNOTATED_PATH(image_path)
            SAVE_IMAGE(result.annotated_frame, annotated_path)
            result.annotated_path = annotated_path
        
        RETURN result
    END FUNCTION

END CLASS
```

---

### 3. Detection Router (Real-time & Snapshot)

```pseudocode
MODULE DetectionRouter:
    // File: backend/app/routers/detection.py
    
    // Constants
    CONSTANT UPLOAD_DIR = "app/static/uploads"
    CONSTANT COOLDOWN_SECONDS = 30
    CONSTANT MIN_CONFIDENCE = 0.50
    
    // Helper function: Check for duplicate violations
    FUNCTION is_duplicate_violation(violation_type, vehicle_number, cooldown_seconds):
        SET cutoff_time = CURRENT_TIME - cooldown_seconds
        
        // Build query
        SET query = {
            violation_type: violation_type,
            timestamp: GREATER_THAN_OR_EQUAL cutoff_time
        }
        
        // If vehicle number is known, check same vehicle + violation
        IF vehicle_number IS VALID:
            query.vehicle_number = vehicle_number
        
        // Check database for recent duplicate
        recent_violation = DATABASE.find_one(query)
        
        RETURN recent_violation EXISTS
    END FUNCTION
    
    // Endpoint: Detect violations from snapshot
    FUNCTION detect_snapshot(frame_data):
        TRY:
            // Get detector instance
            detector = GET_DETECTOR()
            
            // Process frame without annotation for speed
            result = detector.process_frame(frame_data.frame, 
                                           return_annotated=FALSE)
            
            // EDGE CASE 1: Detection failed
            IF NOT result.success:
                RETURN {
                    success: FALSE,
                    error: result.error,
                    violations: [],
                    violation_count: 0,
                    saved_to_db: 0
                }
            
            // Extract or generate vehicle number
            license_plates = result.license_plates
            
            IF license_plates EXISTS AND LENGTH(license_plates) > 0:
                best_plate = MAX(license_plates BY confidence)
                vehicle_number = "LP_" + TIMESTAMP()
                PRINT "📋 License plate detected"
            ELSE:
                vehicle_number = "VEH_" + TIMESTAMP()
            
            SET saved_count = 0
            SET skipped_count = 0
            
            // EDGE CASE 2: No violations detected
            violations = result.violations
            IF violations IS EMPTY:
                RETURN {
                    success: TRUE,
                    violations: [],
                    violation_count: 0,
                    saved_to_db: 0,
                    message: "No violations detected"
                }
            
            // Process each violation
            FOR EACH violation IN violations:
                SET violation_type = violation.type
                SET confidence = violation.confidence
                
                // EDGE CASE 3: Low confidence - skip
                IF confidence < MIN_CONFIDENCE:
                    PRINT "⚠️ Skipping low confidence detection"
                    INCREMENT skipped_count
                    CONTINUE
                
                // EDGE CASE 4: Duplicate detection
                IF is_duplicate_violation(violation_type, vehicle_number):
                    PRINT "⚠️ Skipping duplicate"
                    INCREMENT skipped_count
                    CONTINUE
                
                // Calculate fine amount
                fine_amount = CALCULATE_FINE(violation_type)
                
                // Save to database
                violation_document = {
                    vehicle_number: vehicle_number,
                    violation_type: violation_type,
                    confidence: confidence,
                    bbox: violation.bbox,
                    fine_amount: fine_amount,
                    status: "pending",
                    timestamp: CURRENT_TIMESTAMP,
                    detection_class: violation.class_id
                }
                
                // Insert into MongoDB
                inserted = DATABASE.insert_one(violation_document)
                INCREMENT saved_count
                
                // Send email notification
                TRY:
                    email_service = GET_EMAIL_SERVICE()
                    AWAIT email_service.send_violation_email(
                        vehicle_number: vehicle_number,
                        violation_type: violation_type,
                        fine_amount: fine_amount,
                        location: "Real-time Detection",
                        timestamp: CURRENT_TIMESTAMP,
                        violation_id: inserted.id,
                        confidence: confidence
                    )
                CATCH email_error:
                    PRINT "⚠️ Email notification failed"
            
            RETURN {
                success: TRUE,
                violations: violations,
                violation_count: LENGTH(violations),
                saved_to_db: saved_count,
                skipped: skipped_count,
                timestamp: CURRENT_TIMESTAMP
            }
            
        CATCH exception AS error:
            PRINT "❌ Error in detection:", error
            RETURN {
                success: FALSE,
                error: error.message
            }
    END FUNCTION
    
    // WebSocket endpoint: Real-time video detection
    ASYNC FUNCTION websocket_detection(websocket):
        AWAIT websocket.accept()
        detector = GET_DETECTOR()
        
        TRY:
            WHILE TRUE:
                // Receive frame from client
                frame_data = AWAIT websocket.receive_json()
                
                // Process frame with annotation
                result = detector.process_frame(frame_data.frame, 
                                               return_annotated=TRUE)
                
                // Send annotated frame back to client
                response = {
                    annotated_frame: result.annotated_frame,
                    violations: result.violations,
                    total_detections: result.total_detections,
                    timestamp: CURRENT_TIMESTAMP
                }
                
                AWAIT websocket.send_json(response)
        
        CATCH WebSocketDisconnect:
            PRINT "🔌 Client disconnected"
        
        CATCH exception AS error:
            PRINT "❌ WebSocket error:", error
            AWAIT websocket.close()
    END FUNCTION
    
    // Endpoint: Upload and detect violations
    FUNCTION upload_and_detect(file):
        TRY:
            // Validate file
            IF NOT file.is_image():
                RETURN {
                    success: FALSE,
                    error: "Invalid file type"
                }
            
            // Save uploaded file
            filename = GENERATE_UNIQUE_FILENAME(file.name)
            file_path = UPLOAD_DIR + "/" + filename
            SAVE_FILE(file, file_path)
            
            // Process uploaded image
            detector = GET_DETECTOR()
            result = detector.process_uploaded_image(file_path)
            
            // Save violations to database
            IF result.success AND LENGTH(result.violations) > 0:
                FOR EACH violation IN result.violations:
                    violation_document = {
                        vehicle_number: "MANUAL_UPLOAD",
                        violation_type: violation.type,
                        confidence: violation.confidence,
                        image_path: file_path,
                        fine_amount: CALCULATE_FINE(violation.type),
                        status: "pending",
                        timestamp: CURRENT_TIMESTAMP
                    }
                    DATABASE.insert_one(violation_document)
            
            RETURN {
                success: TRUE,
                violations: result.violations,
                image_path: file_path,
                annotated_path: result.annotated_path
            }
        
        CATCH exception AS error:
            RETURN {
                success: FALSE,
                error: error.message
            }
    END FUNCTION

END MODULE
```

---

### 4. Violations Management Router

```pseudocode
MODULE ViolationsRouter:
    // File: backend/app/routers/violations.py
    
    // Helper: Convert MongoDB document to dict
    FUNCTION violation_helper(violation_document):
        RETURN {
            id: STRING(violation_document._id),
            vehicle_number: violation_document.vehicle_number,
            violation_type: violation_document.violation_type,
            location: violation_document.location,
            officer_id: violation_document.officer_id,
            status: violation_document.status,
            fine_amount: violation_document.fine_amount,
            image_path: violation_document.image_path,
            timestamp: violation_document.timestamp,
            confidence: violation_document.confidence,
            detection_class: violation_document.detection_class,
            bbox: violation_document.bbox
        }
    END FUNCTION
    
    // Endpoint: Get all violations
    FUNCTION get_violations(skip, limit, status_filter):
        SET query = EMPTY_DICT
        
        IF status_filter IS PROVIDED:
            query.status = status_filter
        
        // Query database with pagination
        violations = DATABASE.violations_collection
            .find(query)
            .sort("timestamp", DESCENDING)
            .skip(skip)
            .limit(limit)
        
        SET result_list = EMPTY_LIST
        FOR EACH violation IN violations:
            ADD violation_helper(violation) TO result_list
        
        RETURN result_list
    END FUNCTION
    
    // Endpoint: Get specific violation by ID
    FUNCTION get_violation(violation_id):
        // Validate ObjectId
        IF NOT VALID_OBJECTID(violation_id):
            THROW HTTPException(400, "Invalid violation ID")
        
        // Find violation in database
        violation = DATABASE.violations_collection
            .find_one({_id: ObjectId(violation_id)})
        
        IF violation IS NULL:
            THROW HTTPException(404, "Violation not found")
        
        RETURN violation_helper(violation)
    END FUNCTION
    
    // Endpoint: Create new violation manually
    FUNCTION create_violation(vehicle_number, violation_type, 
                            location, officer_id, fine_amount):
        // Create violation document
        violation_data = {
            vehicle_number: vehicle_number,
            violation_type: violation_type,
            location: location,
            officer_id: officer_id,
            fine_amount: fine_amount,
            status: "pending",
            timestamp: CURRENT_TIMESTAMP,
            image_path: NULL
        }
        
        // Insert into database
        result = DATABASE.violations_collection.insert_one(violation_data)
        created_violation = DATABASE.violations_collection
            .find_one({_id: result.inserted_id})
        
        // Send email notification
        TRY:
            email_service = GET_EMAIL_SERVICE()
            AWAIT email_service.send_violation_email(
                vehicle_number: vehicle_number,
                violation_type: violation_type,
                fine_amount: fine_amount,
                location: location OR "N/A",
                timestamp: violation_data.timestamp,
                violation_id: STRING(result.inserted_id),
                image_path: NULL,
                confidence: NULL
            )
        CATCH email_error:
            PRINT "⚠️ Failed to send email"
        
        RETURN {
            message: "Violation created successfully",
            violation: violation_helper(created_violation)
        }
    END FUNCTION
    
    // Endpoint: Update violation
    FUNCTION update_violation(violation_id, update_data):
        // Validate ObjectId
        IF NOT VALID_OBJECTID(violation_id):
            THROW HTTPException(400, "Invalid violation ID")
        
        // Remove null/empty fields
        update_fields = FILTER_NON_NULL(update_data)
        
        IF update_fields IS EMPTY:
            THROW HTTPException(400, "No valid fields to update")
        
        // Update in database
        result = DATABASE.violations_collection.update_one(
            {_id: ObjectId(violation_id)},
            {$set: update_fields}
        )
        
        IF result.modified_count == 0:
            THROW HTTPException(404, "Violation not found")
        
        // Fetch updated violation
        updated_violation = DATABASE.violations_collection
            .find_one({_id: ObjectId(violation_id)})
        
        RETURN {
            message: "Violation updated successfully",
            violation: violation_helper(updated_violation)
        }
    END FUNCTION
    
    // Endpoint: Delete violation
    FUNCTION delete_violation(violation_id):
        // Validate ObjectId
        IF NOT VALID_OBJECTID(violation_id):
            THROW HTTPException(400, "Invalid violation ID")
        
        // Delete from database
        result = DATABASE.violations_collection.delete_one(
            {_id: ObjectId(violation_id)}
        )
        
        IF result.deleted_count == 0:
            THROW HTTPException(404, "Violation not found")
        
        RETURN {
            message: "Violation deleted successfully"
        }
    END FUNCTION

END MODULE
```

---

### 5. Email Notification Service

```pseudocode
CLASS EmailService:
    // File: backend/app/email_service.py
    
    // Properties
    PROPERTY sendgrid_api_key: STRING
    PROPERTY sender_email: STRING
    PROPERTY recipient_email: STRING
    
    // Constructor
    FUNCTION initialize():
        SET sendgrid_api_key = ENVIRONMENT_VARIABLE("SENDGRID_API_KEY")
        SET sender_email = ENVIRONMENT_VARIABLE("SENDER_EMAIL")
        SET recipient_email = "syednizamsyed225@gmail.com"
    END FUNCTION
    
    // Send violation email with penalty slip
    ASYNC FUNCTION send_violation_email(vehicle_number, violation_type,
                                       fine_amount, location, timestamp,
                                       violation_id, image_path, confidence):
        TRY:
            IF sendgrid_api_key IS EMPTY:
                PRINT "⚠️ SendGrid API key not configured"
                RETURN FALSE
            
            // Create HTML penalty slip
            html_body = CREATE_PENALTY_SLIP_HTML(
                vehicle_number,
                violation_type,
                fine_amount,
                location,
                timestamp,
                violation_id,
                confidence
            )
            
            // Create email message
            message = CREATE_EMAIL(
                from: sender_email,
                to: recipient_email,
                subject: "🚨 Traffic Violation Alert - " + violation_type,
                html_content: html_body
            )
            
            // Attach violation image if available
            IF image_path IS PROVIDED AND FILE_EXISTS(image_path):
                TRY:
                    image_data = READ_FILE(image_path)
                    encoded_image = BASE64_ENCODE(image_data)
                    
                    attachment = CREATE_ATTACHMENT(
                        content: encoded_image,
                        filename: BASENAME(image_path),
                        type: "image/jpeg"
                    )
                    
                    ATTACH attachment TO message
                CATCH image_error:
                    PRINT "⚠️ Could not attach image"
            
            // Send via SendGrid
            sendgrid_client = INITIALIZE_SENDGRID(sendgrid_api_key)
            response = sendgrid_client.send(message)
            
            IF response.status_code IN [200, 202]:
                PRINT "✅ Email sent successfully"
                RETURN TRUE
            ELSE:
                PRINT "⚠️ SendGrid error:", response.status_code
                RETURN FALSE
        
        CATCH exception AS error:
            PRINT "❌ Failed to send email:", error
            RETURN FALSE
    END FUNCTION
    
    // Create HTML penalty slip
    FUNCTION create_penalty_slip_html(vehicle_number, violation_type,
                                     fine_amount, location, timestamp,
                                     violation_id, confidence):
        SET confidence_text = ""
        IF confidence IS PROVIDED:
            confidence_text = " (Confidence: " + PERCENTAGE(confidence) + ")"
        
        // Generate HTML template
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; }
                .penalty-slip { 
                    max-width: 600px; 
                    margin: 0 auto;
                    border: 2px solid #333;
                    padding: 20px;
                }
                .header { 
                    background: #dc2626; 
                    color: white; 
                    padding: 20px;
                    text-align: center;
                }
                .details { margin: 20px 0; }
                .detail-row { 
                    padding: 10px;
                    border-bottom: 1px solid #ddd;
                }
                .label { font-weight: bold; }
                .fine-amount { 
                    font-size: 24px;
                    color: #dc2626;
                    font-weight: bold;
                }
                .footer {
                    margin-top: 20px;
                    padding-top: 20px;
                    border-top: 2px solid #333;
                    font-size: 12px;
                    color: #666;
                }
            </style>
        </head>
        <body>
            <div class="penalty-slip">
                <div class="header">
                    <h1>🚨 TRAFFIC VIOLATION NOTICE</h1>
                    <p>Intelligent Traffic Management System</p>
                </div>
                
                <div class="details">
                    <div class="detail-row">
                        <span class="label">Violation ID:</span>
                        <span>""" + violation_id + """</span>
                    </div>
                    <div class="detail-row">
                        <span class="label">Vehicle Number:</span>
                        <span>""" + vehicle_number + """</span>
                    </div>
                    <div class="detail-row">
                        <span class="label">Violation Type:</span>
                        <span>""" + violation_type + confidence_text + """</span>
                    </div>
                    <div class="detail-row">
                        <span class="label">Location:</span>
                        <span>""" + location + """</span>
                    </div>
                    <div class="detail-row">
                        <span class="label">Date & Time:</span>
                        <span>""" + FORMAT_DATETIME(timestamp) + """</span>
                    </div>
                    <div class="detail-row">
                        <span class="label">Fine Amount:</span>
                        <span class="fine-amount">₹""" + fine_amount + """</span>
                    </div>
                </div>
                
                <div class="footer">
                    <p>This is an automated violation notice.</p>
                    <p>Please pay the fine within 15 days.</p>
                    <p>For queries, contact: traffic@itms.gov</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        RETURN html
    END FUNCTION

END CLASS
```

---

### 6. Database Connection

```pseudocode
MODULE Database:
    // File: backend/app/database.py
    
    // Configuration
    SET MONGODB_URL = ENVIRONMENT_VARIABLE("MONGODB_URL") 
                     OR "mongodb://localhost:27017"
    SET DATABASE_NAME = "traffic_management"
    
    // Initialize async MongoDB client for FastAPI
    client = CREATE_ASYNC_MONGO_CLIENT(MONGODB_URL)
    database = client[DATABASE_NAME]
    
    // Define collections
    violations_collection = database["violations"]
    officers_collection = database["officers"]
    
    // Helper function to get database instance
    FUNCTION get_database():
        RETURN database
    END FUNCTION
    
    // Create indexes for optimization
    FUNCTION create_indexes():
        // Index on timestamp for fast sorting
        violations_collection.create_index("timestamp", DESCENDING)
        
        // Index on vehicle_number for deduplication
        violations_collection.create_index("vehicle_number")
        
        // Compound index for duplicate checking
        violations_collection.create_index({
            "violation_type": 1,
            "timestamp": -1
        })
        
        // Index on status for filtering
        violations_collection.create_index("status")
    END FUNCTION

END MODULE
```

---

## Frontend Architecture

### 1. Main Application Component

```pseudocode
COMPONENT App:
    // File: frontend/src/App.jsx
    
    FUNCTION render():
        RETURN (
            <AppProvider>
                <Router>
                    <div className="flex h-screen">
                        // Sidebar navigation
                        <Sidebar />
                        
                        <div className="flex-1 flex flex-col">
                            // Top navigation bar
                            <Navbar />
                            
                            // Main content area
                            <main className="flex-1 p-6 overflow-y-auto">
                                <AppRouter />
                            </main>
                        </div>
                    </div>
                </Router>
            </AppProvider>
        )
    END FUNCTION

END COMPONENT
```

### 2. Application Context (State Management)

```pseudocode
CONTEXT AppContext:
    // File: frontend/src/context/AppContext.jsx
    
    // Global state
    STATE violations = []
    STATE officers = []
    STATE analytics = {}
    STATE loading = FALSE
    STATE error = NULL
    
    // API base URL
    CONSTANT API_URL = "http://localhost:8000"
    
    // Fetch violations from backend
    ASYNC FUNCTION fetchViolations(status_filter):
        SET loading = TRUE
        SET error = NULL
        
        TRY:
            SET url = API_URL + "/violations"
            IF status_filter:
                url = url + "?status=" + status_filter
            
            response = AWAIT FETCH(url)
            data = AWAIT response.json()
            
            SET violations = data
            
        CATCH exception AS error:
            SET error = error.message
            PRINT "❌ Failed to fetch violations:", error
        
        FINALLY:
            SET loading = FALSE
    END FUNCTION
    
    // Create new violation
    ASYNC FUNCTION createViolation(violation_data):
        SET loading = TRUE
        
        TRY:
            response = AWAIT FETCH(API_URL + "/violations", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON_STRINGIFY(violation_data)
            })
            
            data = AWAIT response.json()
            
            // Refresh violations list
            AWAIT fetchViolations()
            
            RETURN {success: TRUE, data: data}
            
        CATCH exception AS error:
            RETURN {success: FALSE, error: error.message}
        
        FINALLY:
            SET loading = FALSE
    END FUNCTION
    
    // Update violation status
    ASYNC FUNCTION updateViolation(violation_id, update_data):
        TRY:
            response = AWAIT FETCH(
                API_URL + "/violations/" + violation_id,
                {
                    method: "PUT",
                    headers: {"Content-Type": "application/json"},
                    body: JSON_STRINGIFY(update_data)
                }
            )
            
            data = AWAIT response.json()
            
            // Refresh violations list
            AWAIT fetchViolations()
            
            RETURN {success: TRUE, data: data}
            
        CATCH exception AS error:
            RETURN {success: FALSE, error: error.message}
    END FUNCTION
    
    // Delete violation
    ASYNC FUNCTION deleteViolation(violation_id):
        TRY:
            response = AWAIT FETCH(
                API_URL + "/violations/" + violation_id,
                {method: "DELETE"}
            )
            
            // Refresh violations list
            AWAIT fetchViolations()
            
            RETURN {success: TRUE}
            
        CATCH exception AS error:
            RETURN {success: FALSE, error: error.message}
    END FUNCTION
    
    // Fetch analytics data
    ASYNC FUNCTION fetchAnalytics():
        TRY:
            response = AWAIT FETCH(API_URL + "/analytics")
            data = AWAIT response.json()
            SET analytics = data
            
        CATCH exception AS error:
            PRINT "❌ Failed to fetch analytics:", error
    END FUNCTION
    
    // Provide context to children
    RETURN {
        violations,
        officers,
        analytics,
        loading,
        error,
        fetchViolations,
        createViolation,
        updateViolation,
        deleteViolation,
        fetchAnalytics
    }

END CONTEXT
```

### 3. Real-time Detection Page

```pseudocode
PAGE RealTimeDetection:
    // State management
    STATE video_stream = NULL
    STATE websocket = NULL
    STATE detecting = FALSE
    STATE current_frame = NULL
    STATE violations_detected = []
    
    // Initialize webcam and WebSocket
    FUNCTION initialize():
        TRY:
            // Request camera access
            stream = AWAIT navigator.mediaDevices.getUserMedia({
                video: TRUE,
                audio: FALSE
            })
            
            SET video_stream = stream
            
            // Connect to WebSocket
            ws = NEW WebSocket("ws://localhost:8000/detection/live")
            
            ws.onopen = FUNCTION():
                PRINT "🔌 Connected to detection server"
                SET websocket = ws
                START_DETECTION()
            
            ws.onmessage = FUNCTION(event):
                data = JSON_PARSE(event.data)
                SET current_frame = data.annotated_frame
                SET violations_detected = data.violations
            
            ws.onerror = FUNCTION(error):
                PRINT "❌ WebSocket error:", error
            
        CATCH exception AS error:
            PRINT "❌ Failed to initialize:", error
    END FUNCTION
    
    // Start real-time detection
    FUNCTION start_detection():
        SET detecting = TRUE
        
        // Capture and send frames continuously
        SET interval = EVERY 100ms DO:
            IF websocket AND websocket.readyState == OPEN:
                // Capture current frame from video
                frame = CAPTURE_VIDEO_FRAME(video_stream)
                
                // Convert to base64
                base64_frame = CANVAS_TO_BASE64(frame)
                
                // Send to backend
                websocket.send(JSON_STRINGIFY({
                    frame: base64_frame,
                    timestamp: CURRENT_TIMESTAMP
                }))
    END FUNCTION
    
    // Stop detection
    FUNCTION stop_detection():
        SET detecting = FALSE
        
        IF websocket:
            websocket.close()
        
        IF video_stream:
            video_stream.getTracks().forEach(track => track.stop())
    END FUNCTION
    
    // Take snapshot and save violation
    ASYNC FUNCTION take_snapshot():
        IF NOT current_frame:
            ALERT "No frame available"
            RETURN
        
        TRY:
            response = AWAIT FETCH(API_URL + "/detection/detect-snapshot", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON_STRINGIFY({
                    frame: current_frame
                })
            })
            
            result = AWAIT response.json()
            
            IF result.success:
                SHOW_SUCCESS("Violation saved: " + result.saved_to_db + " items")
            ELSE:
                SHOW_ERROR("Failed to save: " + result.error)
                
        CATCH exception AS error:
            SHOW_ERROR("Error:", error)
    END FUNCTION
    
    // Render UI
    FUNCTION render():
        RETURN (
            <div className="detection-page">
                <h1>Real-time Traffic Violation Detection</h1>
                
                // Video display
                <div className="video-container">
                    <img src={current_frame} alt="Detection feed" />
                </div>
                
                // Controls
                <div className="controls">
                    <button onClick={start_detection} disabled={detecting}>
                        Start Detection
                    </button>
                    <button onClick={stop_detection} disabled={!detecting}>
                        Stop Detection
                    </button>
                    <button onClick={take_snapshot}>
                        Take Snapshot & Save
                    </button>
                </div>
                
                // Violations list
                <div className="violations-list">
                    <h2>Detected Violations</h2>
                    {violations_detected.map(violation =>
                        <div className="violation-card">
                            <p>Type: {violation.type}</p>
                            <p>Confidence: {violation.confidence}%</p>
                        </div>
                    )}
                </div>
            </div>
        )
    END FUNCTION
    
    // Cleanup on unmount
    FUNCTION cleanup():
        stop_detection()
    END FUNCTION

END PAGE
```

---

## Training Pipeline

### Model Training Script

```pseudocode
SCRIPT TrainModel:
    // File: scripts/train_model.py
    
    FUNCTION main():
        PRINT "🔍 Checking GPU availability..."
        
        // Check for GPU/CUDA
        IF CUDA_IS_AVAILABLE():
            PRINT "✅ GPU detected:", GET_GPU_NAME()
            PRINT "GPU Memory:", GET_GPU_MEMORY(), "GB"
            SET device = "cuda"
        ELSE:
            PRINT "⚠️ No GPU detected - using CPU (slow)"
            PRINT "Install CUDA-enabled PyTorch for GPU training"
            SET device = "cpu"
        
        // Setup data.yaml configuration
        SET data_yaml_path = "dataset/data.yaml"
        SET base_path = ABSOLUTE_PATH("dataset")
        SET train_path = base_path + "/images/train"
        SET val_path = base_path + "/images/val"
        
        // Create data.yaml content
        yaml_content = """
        train: """ + train_path + """
        val: """ + val_path + """
        
        nc: 6
        names:
          - helmet
          - no_helmet
          - mobile_phone
          - triple_riding
          - license_plate
          - motorcycle
        """
        
        // Write updated data.yaml
        WRITE_FILE(data_yaml_path, yaml_content)
        PRINT "✅ data.yaml updated with absolute paths"
        
        // Initialize YOLO model
        PRINT "📦 Loading YOLOv8n base model..."
        model = LOAD_YOLO_MODEL("yolov8n.pt")
        
        // Training configuration
        training_config = {
            data: data_yaml_path,
            epochs: 100,
            imgsz: 640,
            batch: 16,
            device: device,
            patience: 20,
            save: TRUE,
            plots: TRUE,
            cache: TRUE,
            
            // Augmentation parameters
            hsv_h: 0.015,      // Hue augmentation
            hsv_s: 0.7,        // Saturation augmentation
            hsv_v: 0.4,        // Value augmentation
            degrees: 10.0,      // Rotation
            translate: 0.1,     // Translation
            scale: 0.5,         // Scaling
            shear: 0.0,         // Shearing
            perspective: 0.0,   // Perspective
            flipud: 0.0,        // Vertical flip
            fliplr: 0.5,        // Horizontal flip
            mosaic: 1.0,        // Mosaic augmentation
            mixup: 0.1,         // Mixup augmentation
            
            // Optimizer settings
            optimizer: "SGD",
            lr0: 0.01,          // Initial learning rate
            lrf: 0.01,          // Final learning rate
            momentum: 0.937,
            weight_decay: 0.0005,
            warmup_epochs: 3.0,
            warmup_momentum: 0.8,
            
            // Other settings
            project: "runs/detect",
            name: "train_" + TIMESTAMP(),
            exist_ok: TRUE,
            pretrained: TRUE,
            verbose: TRUE
        }
        
        PRINT "🚀 Starting training..."
        PRINT "Configuration:", training_config
        
        // Train the model
        results = model.train(**training_config)
        
        PRINT "✅ Training completed!"
        PRINT "Results saved to:", results.save_dir
        PRINT "Best model:", results.save_dir + "/weights/best.pt"
        
        // Validate the model
        PRINT "🧪 Validating model..."
        metrics = model.val()
        
        PRINT "📊 Validation Metrics:"
        PRINT "  mAP@50:", metrics.map50
        PRINT "  mAP@50-95:", metrics.map
        PRINT "  Precision:", metrics.precision
        PRINT "  Recall:", metrics.recall
        
        // Export model
        PRINT "📦 Exporting model..."
        model.export(format="onnx")
        
        PRINT "✅ All done! Model ready for deployment"
        
    END FUNCTION
    
    // Execute training
    IF __name__ == "__main__":
        main()

END SCRIPT
```

### Dataset Preparation Script

```pseudocode
SCRIPT PrepareDataset:
    // File: scripts/create_train_val_test_split.py
    
    FUNCTION split_dataset(images_dir, labels_dir, output_dir):
        // Split ratios
        SET TRAIN_RATIO = 0.70
        SET VAL_RATIO = 0.20
        SET TEST_RATIO = 0.10
        
        PRINT "📂 Loading dataset..."
        
        // Get all image files
        image_files = GET_FILES(images_dir, extensions=[".jpg", ".png"])
        PRINT "Total images:", LENGTH(image_files)
        
        // Shuffle for random split
        SHUFFLE(image_files)
        
        // Calculate split sizes
        total_images = LENGTH(image_files)
        train_size = FLOOR(total_images * TRAIN_RATIO)
        val_size = FLOOR(total_images * VAL_RATIO)
        test_size = total_images - train_size - val_size
        
        PRINT "Split:"
        PRINT "  Train:", train_size, "images"
        PRINT "  Val:", val_size, "images"
        PRINT "  Test:", test_size, "images"
        
        // Split images
        train_images = image_files[0:train_size]
        val_images = image_files[train_size:train_size+val_size]
        test_images = image_files[train_size+val_size:]
        
        // Create output directories
        CREATE_DIRECTORY(output_dir + "/images/train")
        CREATE_DIRECTORY(output_dir + "/images/val")
        CREATE_DIRECTORY(output_dir + "/images/test")
        CREATE_DIRECTORY(output_dir + "/labels/train")
        CREATE_DIRECTORY(output_dir + "/labels/val")
        CREATE_DIRECTORY(output_dir + "/labels/test")
        
        // Copy files to respective directories
        PRINT "📋 Copying train images..."
        FOR EACH image IN train_images:
            COPY_FILE(image, output_dir + "/images/train/")
            label_file = GET_LABEL_FILE(image, labels_dir)
            IF label_file EXISTS:
                COPY_FILE(label_file, output_dir + "/labels/train/")
        
        PRINT "📋 Copying validation images..."
        FOR EACH image IN val_images:
            COPY_FILE(image, output_dir + "/images/val/")
            label_file = GET_LABEL_FILE(image, labels_dir)
            IF label_file EXISTS:
                COPY_FILE(label_file, output_dir + "/labels/val/")
        
        PRINT "📋 Copying test images..."
        FOR EACH image IN test_images:
            COPY_FILE(image, output_dir + "/images/test/")
            label_file = GET_LABEL_FILE(image, labels_dir)
            IF label_file EXISTS:
                COPY_FILE(label_file, output_dir + "/labels/test/")
        
        PRINT "✅ Dataset split complete!"
        PRINT "Output directory:", output_dir
    END FUNCTION
    
    // Get corresponding label file for image
    FUNCTION get_label_file(image_path, labels_dir):
        filename = BASENAME(image_path)
        name_without_ext = REMOVE_EXTENSION(filename)
        label_file = labels_dir + "/" + name_without_ext + ".txt"
        RETURN label_file
    END FUNCTION

END SCRIPT
```

---

## Data Flow

### Complete System Data Flow

```pseudocode
FLOW ViolationDetectionFlow:
    
    // === REAL-TIME DETECTION FLOW ===
    STEP 1: User opens real-time detection page
        Frontend: REQUEST camera access
        Frontend: ESTABLISH WebSocket connection to backend
    
    STEP 2: Camera stream starts
        Frontend: CAPTURE video frame every 100ms
        Frontend: CONVERT frame to base64
        Frontend: SEND frame via WebSocket to backend
    
    STEP 3: Backend processes frame
        Backend: RECEIVE frame from WebSocket
        Backend: DECODE base64 to image
        Backend: RUN YOLOv8 detection on frame
        Backend: DETECT violations (helmet, no_helmet, mobile_phone, etc.)
        Backend: ANNOTATE frame with bounding boxes
        Backend: ENCODE annotated frame to base64
        Backend: SEND annotated frame + violations back to frontend
    
    STEP 4: Frontend displays results
        Frontend: RECEIVE annotated frame
        Frontend: DISPLAY annotated frame in video player
        Frontend: SHOW detected violations list
    
    STEP 5: User takes snapshot
        Frontend: USER clicks "Take Snapshot" button
        Frontend: SEND current frame to /detection/detect-snapshot
    
    STEP 6: Backend saves violation
        Backend: PROCESS frame (detect violations)
        Backend: EXTRACT or GENERATE vehicle number
        Backend: CHECK for duplicate violations (30s cooldown)
        Backend: FILTER low confidence detections (<50%)
        Backend: CALCULATE fine amounts
        Backend: SAVE violations to MongoDB
        Backend: SEND email notification via SendGrid
        Backend: RETURN success response
    
    STEP 7: Confirmation
        Frontend: SHOW success/error message
        Frontend: UPDATE violations list
    
    // === IMAGE UPLOAD FLOW ===
    STEP 1: User uploads image
        Frontend: USER selects image file
        Frontend: SEND image via POST to /upload
    
    STEP 2: Backend processes upload
        Backend: RECEIVE uploaded file
        Backend: VALIDATE file type (image only)
        Backend: SAVE file to static/uploads directory
        Backend: RUN YOLOv8 detection on image
        Backend: DETECT violations
        Backend: GENERATE annotated image
        Backend: SAVE annotated image
    
    STEP 3: Backend saves to database
        Backend: CREATE violation records
        Backend: SAVE to MongoDB with image paths
        Backend: SEND email notifications
        Backend: RETURN detection results
    
    STEP 4: Frontend shows results
        Frontend: DISPLAY original image
        Frontend: DISPLAY annotated image
        Frontend: SHOW detected violations
        Frontend: SHOW confidence scores
    
    // === VIOLATION MANAGEMENT FLOW ===
    STEP 1: Fetch violations
        Frontend: SEND GET request to /violations
        Backend: QUERY MongoDB violations_collection
        Backend: SORT by timestamp (descending)
        Backend: APPLY filters (status, date range)
        Backend: RETURN violations array
        Frontend: DISPLAY in table/grid
    
    STEP 2: Update violation
        Frontend: USER changes status to "paid" or "resolved"
        Frontend: SEND PUT request to /violations/{id}
        Backend: VALIDATE violation_id
        Backend: UPDATE document in MongoDB
        Backend: RETURN updated violation
        Frontend: REFRESH violations list
    
    STEP 3: Delete violation
        Frontend: USER clicks delete
        Frontend: CONFIRM action
        Frontend: SEND DELETE request to /violations/{id}
        Backend: VALIDATE violation_id
        Backend: DELETE document from MongoDB
        Backend: RETURN success
        Frontend: REMOVE from list
    
    // === ANALYTICS FLOW ===
    STEP 1: Fetch analytics
        Frontend: SEND GET request to /analytics
        Backend: AGGREGATE violations data
        Backend: COUNT total violations
        Backend: GROUP by violation type
        Backend: GROUP by date/time
        Backend: CALCULATE statistics (avg fine, etc.)
        Backend: RETURN analytics object
    
    STEP 2: Display analytics
        Frontend: RENDER charts and graphs
        Frontend: SHOW key metrics cards
        Frontend: DISPLAY trends
    
    // === EMAIL NOTIFICATION FLOW ===
    STEP 1: Violation created/detected
        Backend: VIOLATION saved to database
        Backend: GET violation details
    
    STEP 2: Generate email
        Backend: CREATE HTML penalty slip
        Backend: INCLUDE violation details
        Backend: ATTACH violation image (if available)
    
    STEP 3: Send via SendGrid
        Backend: INITIALIZE SendGrid client
        Backend: CREATE email message
        Backend: SEND email
        Backend: LOG result (success/failure)
    
    STEP 4: Email delivery
        SendGrid: DELIVER email to recipient
        Recipient: RECEIVE penalty slip notification

END FLOW
```

---

## Detection Logic & Edge Cases

### Violation Detection Rules

```pseudocode
FUNCTION determine_violations(detections):
    // Input: List of YOLO detections
    // Output: List of violations to save
    
    SET violations = EMPTY_LIST
    
    // Count detections by class
    helmet_count = COUNT(detections WHERE class == "helmet")
    no_helmet_count = COUNT(detections WHERE class == "no_helmet")
    mobile_phone_count = COUNT(detections WHERE class == "mobile_phone")
    triple_riding_count = COUNT(detections WHERE class == "triple_riding")
    motorcycle_count = COUNT(detections WHERE class == "motorcycle")
    license_plate_count = COUNT(detections WHERE class == "license_plate")
    
    // RULE 1: Mobile Phone Usage
    // ALWAYS a violation if detected with high confidence
    IF mobile_phone_count > 0:
        FOR EACH mobile_detection IN detections WHERE class == "mobile_phone":
            IF mobile_detection.confidence >= 0.50:
                ADD {
                    type: "mobile_phone",
                    confidence: mobile_detection.confidence,
                    fine_amount: 1000,
                    severity: "HIGH"
                } TO violations
                PRINT "📱 Mobile phone usage detected - VIOLATION"
    
    // RULE 2: Triple Riding (Overloading)
    // ALWAYS a violation if 3+ riders detected
    IF triple_riding_count > 0:
        FOR EACH triple_detection IN detections WHERE class == "triple_riding":
            IF triple_detection.confidence >= 0.50:
                ADD {
                    type: "triple_riding",
                    confidence: triple_detection.confidence,
                    fine_amount: 2000,
                    severity: "HIGH"
                } TO violations
                PRINT "👥 Triple riding detected - VIOLATION (overloading)"
    
    // RULE 3: No Helmet
    // Only violation if motorcycle is present AND rider has no helmet
    IF no_helmet_count > 0 AND motorcycle_count > 0:
        FOR EACH no_helmet_detection IN detections WHERE class == "no_helmet":
            IF no_helmet_detection.confidence >= 0.50:
                ADD {
                    type: "no_helmet",
                    confidence: no_helmet_detection.confidence,
                    fine_amount: 500,
                    severity: "MEDIUM"
                } TO violations
                PRINT "🪖 No helmet detected - VIOLATION"
    
    // EDGE CASE 1: Helmet detected but no motorcycle
    // Not a violation - just informational
    IF helmet_count > 0 AND motorcycle_count == 0:
        PRINT "ℹ️ Helmet detected without motorcycle - not a traffic violation"
    
    // EDGE CASE 2: Both helmet and no_helmet detected
    // Prioritize no_helmet (violation)
    IF helmet_count > 0 AND no_helmet_count > 0:
        PRINT "⚠️ Mixed helmet detections - prioritizing no_helmet violation"
    
    // EDGE CASE 3: License plate detection
    // Not a violation itself, but useful for vehicle identification
    IF license_plate_count > 0:
        PRINT "🔢 License plate detected - used for vehicle identification"
    
    // EDGE CASE 4: Motorcycle without any rider detection
    // Could be parked - not a violation
    IF motorcycle_count > 0 AND (helmet_count + no_helmet_count) == 0:
        PRINT "🏍️ Motorcycle detected without rider - likely parked"
    
    RETURN violations
END FUNCTION
```

### Deduplication Logic

```pseudocode
FUNCTION check_duplicate_violation(violation_type, vehicle_number, cooldown_seconds):
    // Prevent saving duplicate violations within cooldown period
    
    SET cutoff_time = CURRENT_TIME - SECONDS(cooldown_seconds)
    
    // Build query
    query = {
        "violation_type": violation_type,
        "timestamp": {"$gte": cutoff_time}
    }
    
    // If vehicle number is known, check same vehicle
    IF vehicle_number AND NOT vehicle_number.startsWith("VEH_"):
        query["vehicle_number"] = vehicle_number
        PRINT "🔍 Checking duplicate for vehicle:", vehicle_number
    ELSE:
        PRINT "🔍 Checking duplicate for violation type:", violation_type
    
    // Query database
    recent = DATABASE.find_one(query)
    
    IF recent EXISTS:
        time_diff = CURRENT_TIME - recent.timestamp
        PRINT "⏰ Duplicate found from", time_diff, "seconds ago"
        RETURN TRUE
    ELSE:
        PRINT "✅ No duplicate found - violation is new"
        RETURN FALSE
END FUNCTION
```

---

## Summary

This pseudo code documentation covers:

1. **Backend System**: FastAPI application, routers, and middleware
2. **YOLOv8 Detector**: Real-time object detection and violation classification
3. **Database Operations**: MongoDB integration with async operations
4. **Email Service**: SendGrid integration for penalty slip notifications
5. **Frontend Application**: React components and state management
6. **Training Pipeline**: Model training and dataset preparation
7. **Data Flow**: Complete request-response cycles
8. **Edge Cases**: Violation detection rules and deduplication logic

### Key Performance Metrics
- **Model Accuracy**: 90.3% mAP@50, 63.8% mAP@50-95
- **Confidence Threshold**: 50% minimum for saving violations
- **Deduplication**: 30-second cooldown per violation type
- **Detection Classes**: 6 classes (helmet, no_helmet, mobile_phone, triple_riding, license_plate, motorcycle)

### Technologies Used
- **Backend**: Python, FastAPI, Motor (async MongoDB)
- **AI Model**: YOLOv8n (Ultralytics)
- **Database**: MongoDB
- **Email**: SendGrid API
- **Frontend**: React, Tailwind CSS, Vite
- **Real-time**: WebSockets

---

*Document Generated: December 20, 2025*
*Project: Intelligent Traffic Management System (ITMS)*
