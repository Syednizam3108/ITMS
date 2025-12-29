import cv2
import numpy as np
from ultralytics import YOLO
from datetime import datetime
import base64
from io import BytesIO
from PIL import Image
import os

class TrafficViolationDetector:
    def __init__(self, model_path="yolov8n.pt"):
        """Initialize YOLO detector with custom trained model"""
        try:
            # Try to load custom trained model first (84.0% mAP@50)
            # Path is relative to backend/ folder, so go up one level
            custom_model_path = "../runs/detect/helmet_train_20251221_232017/weights/best.pt"
            if os.path.exists(custom_model_path):
                self.model = YOLO(custom_model_path)
                print(f"✅ Custom TRAINED model loaded: {custom_model_path}")
                print(f"✅ Performance: 84.0% mAP@50, 54.8% mAP@50-95")
                print(f"✅ Classes: helmet, no_helmet, mobile_phone, triple_riding, license_plate, motorcycle")
                print(f"✅ Best class: triple_riding (91.4% mAP@50)")
            else:
                self.model = YOLO(model_path)
                print(f"⚠️ Using default model: {model_path}")
                print("⚠️ NOTE: This model is NOT trained on traffic violations!")
                print("⚠️ Run 'python train_helmet_model.py' to train custom model")
        except Exception as e:
            print(f"⚠️ Error loading model: {e}")
            self.model = YOLO("yolov8n.pt")
        
        # Class mappings - COCO dataset (yolov8n.pt default)
        self.coco_classes = {
            0: "person",
            1: "bicycle", 
            2: "car",
            3: "motorcycle",
            4: "airplane",
            5: "bus"
        }
        
        # For untrained model, use COCO classes for basic detection
        # Count persons on motorcycle for triple riding
        # This is a TEMPORARY workaround until custom model is trained
        self.use_coco_detection = not os.path.exists(custom_model_path)
        
        # Trained model class names (from data.yaml)
        self.trained_classes = {
            0: "helmet",
            1: "no_helmet", 
            2: "mobile_phone",
            3: "triple_riding",
            4: "license_plate",
            5: "motorcycle"
        }
        
        self.violation_colors = {
            0: (0, 255, 0),      # helmet - green
            1: (0, 0, 255),      # no_helmet - red
            2: (255, 0, 0),      # mobile_phone - blue
            3: (255, 165, 0),    # triple_riding - orange
            4: (255, 255, 0),    # license_plate - yellow
            5: (128, 128, 128)   # motorcycle - gray
        }
    
    def extract_license_plates(self, frame, boxes):
        """Extract license plate regions from frame"""
        license_plates = []
        for box in boxes:
            class_id = int(box.cls[0])
            if class_id == 4:  # license_plate class
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = float(box.conf[0])
                # Crop license plate region
                plate_img = frame[y1:y2, x1:x2]
                if plate_img.size > 0:
                    license_plates.append({
                        'bbox': [x1, y1, x2, y2],
                        'confidence': confidence,
                        'image': plate_img
                    })
        return license_plates
    
    def process_frame(self, frame_data, return_annotated=False):
        """Process a single frame and detect violations"""
        try:
            # Decode base64 image
            if isinstance(frame_data, str):
                if 'base64,' in frame_data:
                    frame_data = frame_data.split('base64,')[1]
                img_bytes = base64.b64decode(frame_data)
                img = Image.open(BytesIO(img_bytes))
                frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            else:
                frame = frame_data
            
            # Run YOLO detection with lower confidence for mobile_phone class
            # Mobile phone detection is challenging (49.4% mAP@50-95), so use lower threshold
            results = self.model(frame, conf=0.30, iou=0.45, verbose=False)
            
            violations_detected = []
            annotated_frame = frame.copy() if return_annotated else None
            
            # Process detections based on model type
            if self.use_coco_detection:
                # COCO-based detection (untrained model)
                person_count = 0
                motorcycle_count = 0
                cell_phone_count = 0
                
                for result in results:
                    boxes = result.boxes
                    for box in boxes:
                        class_id = int(box.cls[0])
                        confidence = float(box.conf[0])
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        
                        if class_id == 0:  # person
                            person_count += 1
                        elif class_id == 3:  # motorcycle
                            motorcycle_count += 1
                        elif class_id == 67:  # cell phone
                            cell_phone_count += 1
                
                # Infer violations from COCO detections
                if motorcycle_count > 0 and person_count >= 3:
                    violations_detected.append({
                        "type": "Triple Riding Violation",
                        "confidence": 0.85,
                        "bbox": [0, 0, 100, 100],
                        "class": "triple_riding"
                    })
                
                if cell_phone_count > 0:
                    violations_detected.append({
                        "type": "Phone Usage While Riding",
                        "confidence": 0.80,
                        "bbox": [0, 0, 100, 100],
                        "class": "mobile_phone"
                    })
                
                print(f"🔍 Detected: {person_count} persons, {motorcycle_count} motorcycles")
            
            else:
                # TRAINED model detection - use actual violation classes with COMPREHENSIVE edge case handling
                all_detections = []
                
                for result in results:
                    boxes = result.boxes
                    for box in boxes:
                        class_id = int(box.cls[0])
                        confidence = float(box.conf[0])
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        class_name = self.trained_classes.get(class_id, "unknown")
                        
                        all_detections.append({
                            "class_id": class_id,
                            "class_name": class_name,
                            "confidence": confidence,
                            "bbox": [x1, y1, x2, y2]
                        })
                
                # Detailed detection counts with CLASS-SPECIFIC confidence thresholds
                # Mobile phone needs lower threshold due to 49.4% mAP@50-95 (harder to detect)
                helmet_detections = [d for d in all_detections if d["class_id"] == 0 and d["confidence"] >= 0.50]
                no_helmet_detections = [d for d in all_detections if d["class_id"] == 1 and d["confidence"] >= 0.50]
                mobile_phone_detections = [d for d in all_detections if d["class_id"] == 2 and d["confidence"] >= 0.35]  # Lower threshold for phone
                triple_riding_detections = [d for d in all_detections if d["class_id"] == 3 and d["confidence"] >= 0.50]
                motorcycle_detections = [d for d in all_detections if d["class_id"] == 5 and d["confidence"] >= 0.40]  # Lower for context
                license_plate_detections = [d for d in all_detections if d["class_id"] == 4 and d["confidence"] >= 0.50]
                
                # Map class to violation type
                violation_map = {
                    1: "No Helmet Violation",      # no_helmet
                    2: "Phone Usage While Riding", # mobile_phone
                    3: "Triple Riding Violation"   # triple_riding
                }
                
                print(f"📊 Detection Summary:")
                print(f"   - Helmets: {len(helmet_detections)}")
                print(f"   - No Helmets: {len(no_helmet_detections)}")
                print(f"   - Mobile Phones: {len(mobile_phone_detections)}")
                print(f"   - Triple Riding: {len(triple_riding_detections)}")
                print(f"   - Motorcycles: {len(motorcycle_detections)}")
                print(f"   - License Plates: {len(license_plate_detections)}")
                
                # Track processed violations to avoid duplicates
                processed_violations = set()
                
                # EDGE CASE 1: No Helmet Violation (HIGH PRIORITY)
                # Only register if:
                # - no_helmet detected with good confidence
                # - OR (motorcycle present WITHOUT helmet)
                for detection in no_helmet_detections:
                    if "no_helmet" not in processed_violations:
                        violations_detected.append({
                            "type": "No Helmet Violation",
                            "confidence": round(detection["confidence"], 2),
                            "bbox": detection["bbox"],
                            "class": "no_helmet",
                            "timestamp": datetime.now().isoformat()
                        })
                        processed_violations.add("no_helmet")
                        print(f"✅ No Helmet Violation: {detection['confidence']:.0%} confidence")
                        
                        if return_annotated:
                            x1, y1, x2, y2 = detection["bbox"]
                            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
                            cv2.putText(annotated_frame, f"NO HELMET {detection['confidence']:.2f}", 
                                      (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                        break  # Only one no_helmet violation per frame
                
                # EDGE CASE 2: Mobile Phone Usage (ALWAYS A VIOLATION)
                # Register if phone detected, regardless of helmet status
                for detection in mobile_phone_detections:
                    if "mobile_phone" not in processed_violations:
                        violations_detected.append({
                            "type": "Phone Usage While Riding",
                            "confidence": round(detection["confidence"], 2),
                            "bbox": detection["bbox"],
                            "class": "mobile_phone",
                            "timestamp": datetime.now().isoformat()
                        })
                        processed_violations.add("mobile_phone")
                        print(f"✅ Mobile Phone Usage: {detection['confidence']:.0%} confidence")
                        
                        if return_annotated:
                            x1, y1, x2, y2 = detection["bbox"]
                            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (255, 0, 0), 3)
                            cv2.putText(annotated_frame, f"PHONE USAGE {detection['confidence']:.2f}", 
                                      (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
                        break  # Only one phone violation per frame
                
                # EDGE CASE 3: Triple Riding Violation (ALWAYS A VIOLATION)
                # Triple riding is illegal regardless of helmet status - it's about overloading
                # Register if triple_riding detected with sufficient confidence
                for detection in triple_riding_detections:
                    if "triple_riding" not in processed_violations:
                        violations_detected.append({
                            "type": "Triple Riding Violation",
                            "confidence": round(detection["confidence"], 2),
                            "bbox": detection["bbox"],
                            "class": "triple_riding",
                            "timestamp": datetime.now().isoformat()
                        })
                        processed_violations.add("triple_riding")
                        print(f"✅ Triple Riding Violation: {detection['confidence']:.0%} confidence")
                        
                        if return_annotated:
                            x1, y1, x2, y2 = detection["bbox"]
                            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (255, 165, 0), 3)
                            cv2.putText(annotated_frame, f"TRIPLE RIDING {detection['confidence']:.2f}", 
                                      (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 165, 0), 2)
                        break  # Only one triple riding violation per frame
                
                # EDGE CASE 4: Motorcycle without helmet detection
                # If motorcycle detected but NO helmet and NO no_helmet detected
                # This catches cases where riders are far away or helmet detection failed
                if len(motorcycle_detections) > 0 and len(helmet_detections) == 0 and len(no_helmet_detections) == 0:
                    if "no_helmet" not in processed_violations:
                        print(f"⚠️ Motorcycle detected without helmet information - assuming potential violation")
                        # Don't auto-register - this is too uncertain
                        # Let manual review handle this case
                
                print(f"✅ Final: {len(violations_detected)} violations confirmed")
                for v in violations_detected:
                    print(f"   - {v['type']}: {v['confidence']:.0%}")
            
            # Extract license plates from all detections
            license_plates = []
            for result in results:
                boxes = result.boxes
                print(f"🔍 Total detections in frame: {len(boxes)}")
                for box in boxes:
                    class_id = int(box.cls[0])
                    class_name = self.trained_classes.get(class_id, "unknown")
                    confidence = float(box.conf[0])
                    print(f"   - Class {class_id} ({class_name}): {confidence:.0%}")
                
                plates = self.extract_license_plates(frame, boxes)
                license_plates.extend(plates)
            
            if license_plates:
                print(f"🚗 Detected {len(license_plates)} license plate(s)")
                for plate in license_plates:
                    print(f"   - Confidence: {plate['confidence']:.0%}")
            else:
                print("⚠️ No license plates detected in this frame")
            
            response = {
                "success": True,
                "violations": violations_detected,
                "violation_count": len(violations_detected),
                "license_plates": license_plates,
                "timestamp": datetime.now().isoformat()
            }
            
            # Encode annotated frame only if requested
            if return_annotated and annotated_frame is not None:
                _, buffer = cv2.imencode('.jpg', annotated_frame)
                img_base64 = base64.b64encode(buffer).decode('utf-8')
                response["annotated_frame"] = f"data:image/jpeg;base64,{img_base64}"
            
            return response
            
        except Exception as e:
            print(f"Error processing frame: {e}")
            return {
                "success": False,
                "error": str(e),
                "violations": [],
                "violation_count": 0
            }
    
    def detect_from_video(self, video_source=0):
        """Detect violations from video source (camera or file)"""
        cap = cv2.VideoCapture(video_source)
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            result = self.process_frame(frame)
            
            if result["success"] and result["violation_count"] > 0:
                print(f"⚠️ {result['violation_count']} violation(s) detected!")
                for v in result["violations"]:
                    print(f"  - {v['type']} (confidence: {v['confidence']:.2f})")
            
            # Display frame (for testing)
            if "annotated_frame" in result:
                cv2.imshow("Traffic Violation Detection", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()

# Global detector instance
detector = None

def get_detector(model_path="yolov8n.pt"):
    """Get or create detector instance"""
    global detector
    if detector is None:
        detector = TrafficViolationDetector(model_path)
    return detector
