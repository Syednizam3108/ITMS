# 🚦 Traffic Violation Detection Rules - Quick Reference

## 📋 Violation Detection Logic

### 1️⃣ No Helmet Violation

```
WHEN DETECTED:
✅ no_helmet class detected with ≥50% confidence

VIOLATION REGISTERED:
✅ Always (single occurrence per frame)

FINE AMOUNT:
₹500

EDGE CASES:
- Multiple no_helmet in frame → Register only ONE violation
- Helmet + no_helmet both detected → Register no_helmet violation (prioritize safety)
- Motorcycle without helmet info → No violation (insufficient evidence)
```

---

### 2️⃣ Mobile Phone Usage

```
WHEN DETECTED:
✅ mobile_phone class detected with ≥50% confidence

VIOLATION REGISTERED:
✅ ALWAYS - regardless of helmet status

FINE AMOUNT:
₹1,000

EDGE CASES:
- Phone + helmet → Still a violation
- Phone + no_helmet → Register BOTH violations separately
- Phone with 40% confidence → Skipped (below threshold)
```

---

### 3️⃣ Triple Riding Violation

```
WHEN DETECTED:
✅ triple_riding class detected with ≥50% confidence

VIOLATION REGISTERED:
✅ ALWAYS - Triple riding is illegal (overloading)
✅ Helmet status is IRRELEVANT

FINE AMOUNT:
₹1,500

SIMPLE LOGIC:
┌─────────────────────────────────────────────────────┐
│ Triple riding detected (≥50% confidence)            │
│ ✅ VIOLATION (overloading is illegal)               │
│                                                     │
│ Note: Helmet compliance is a SEPARATE violation    │
└─────────────────────────────────────────────────────┘

EDGE CASES:
- Triple (85%) + helmet (90%) + helmet (88%) → ✅ Triple riding violation
- Triple (85%) + helmet (90%) + no_helmet (92%) → ✅ BOTH violations (triple + no helmet)
- Triple (85%) + no helmet info → ✅ Triple riding violation only
- Triple (85%) + phone (80%) → ✅ BOTH violations
```

---

## 🎯 Confidence Thresholds

```python
MINIMUM CONFIDENCE REQUIRED:
├─ Helmet:          50%
├─ No Helmet:       50%
├─ Mobile Phone:    50%
├─ Triple Riding:   50%
├─ License Plate:   40%  # Lower threshold (harder to detect)
└─ Motorcycle:      50%

BELOW THRESHOLD:
⚠️ Detection logged but NOT saved to database
```

---

## ⏱️ Duplicate Prevention

```
COOLDOWN PERIOD: 30 seconds

DEDUPLICATION LOGIC:
┌──────────────────────────────────────────────────────┐
│ Same violation type within 30 seconds:              │
│ - Check violation_type                              │
│ - Check vehicle_number (if available)               │
│ - Skip if duplicate found                           │
└──────────────────────────────────────────────────────┘

EXAMPLES:
T=0s:  No helmet → ✅ Saved
T=10s: No helmet (same vehicle) → ⚠️ Skipped (duplicate)
T=35s: No helmet (same vehicle) → ✅ Saved (cooldown expired)

T=0s:  No helmet → ✅ Saved
T=5s:  Phone usage → ✅ Saved (different type)
```

---

## 🔢 Multiple Violations

```
SAME FRAME, MULTIPLE VIOLATIONS:
✅ Each violation type registered separately

EXAMPLE:
Detection: no_helmet (92%), mobile_phone (87%)
Result:
  ✅ Violation 1: No Helmet Violation (₹500)
  ✅ Violation 2: Phone Usage While Riding (₹1,000)
  💰 Total Fine: ₹1,500

DEDUPLICATION WITHIN FRAME:
Detection: no_helmet (92%), no_helmet (88%), no_helmet (85%)
Result:
  ✅ Only ONE "No Helmet Violation" registered (highest confidence: 92%)
```

---

## 📸 Image Upload Validation

```
VALIDATION STEPS:
1. AI processes uploaded image
2. Check if violations detected
3. Verify violation type matches user selection
4. Validate confidence ≥ 50%
5. Save to database

USER SELECTS "No Helmet":
├─ AI detects: no_helmet (92%) → ✅ Accepted
├─ AI detects: mobile_phone (87%) → ❌ Rejected (type mismatch)
├─ AI detects: nothing → ❌ Rejected (no violation found)
└─ AI detects: no_helmet (42%) → ⚠️ Accepted (with warning)

ERROR MESSAGES:
❌ "No violations detected in image"
❌ "You selected 'No Helmet' but AI detected: mobile_phone (87%)"
❌ "Detection confidence too low (35%). Upload clearer image."
```

---

## 🎥 Real-time Detection Flow

```
LIVE CAMERA FEED:
1. Capture frame every 3 seconds
2. Send to /detection/detect-snapshot
3. AI processes frame (no annotation for speed)
4. Filter by confidence ≥ 50%
5. Check for duplicates (30s cooldown)
6. Save high-confidence, non-duplicate violations
7. Return stats to frontend

STATS RETURNED:
{
  "total_detected": 3,
  "saved": 2,
  "skipped_low_confidence": 1,
  "skipped_duplicate": 0
}
```

---

## 🚗 Vehicle Number Generation

```
LICENSE PLATE DETECTED:
✅ Format: LP_YYYYMMDD_HHMMSS
✅ Example: LP_20251210_143052

NO LICENSE PLATE:
✅ Format: VEH_YYYYMMDDHHMMSS
✅ Example: VEH_20251210143052

MULTIPLE PLATES:
✅ Use highest confidence plate
```

---

## 📊 Detection Summary Logs

```bash
📊 Detection Summary:
   - Helmets: 2
   - No Helmets: 1
   - Mobile Phones: 1
   - Triple Riding: 0
   - Motorcycles: 1
   - License Plates: 1

✅ No Helmet Violation: 92% confidence
✅ Mobile Phone Usage: 87% confidence
✅ Final: 2 violations confirmed
```

---

## ⚙️ Configuration

**File:** `backend/app/config.py`

```python
# Adjust these values to tune detection

MIN_CONFIDENCE_GENERAL = 0.50      # 50% minimum
COOLDOWN_SECONDS = 30              # 30 seconds
MAX_VIOLATIONS_PER_FRAME = 5       # Max 5 violations

TRIPLE_RIDING_RULES = {
    "with_helmet": False,          # Triple + helmets = NO violation
    "with_no_helmet": True,        # Triple + no helmet = VIOLATION
    "no_helmet_info": True,        # Triple + unknown = VIOLATION
}

FINE_AMOUNTS = {
    "No Helmet Violation": 500.0,
    "Phone Usage While Riding": 1000.0,
    "Triple Riding Violation": 1500.0,
}
```

---

## 🧪 Testing Scenarios

```python
# Test 1: Triple riding with helmets
Input:  triple_riding (85%), helmet (90%), helmet (88%)
Expect: NO violation
Status: ✅ PASS

# Test 2: Phone + Helmet
Input:  mobile_phone (87%), helmet (90%)
Expect: Phone Usage Violation only
Status: ✅ PASS

# Test 3: Multiple no_helmet
Input:  no_helmet (92%), no_helmet (88%), no_helmet (75%)
Expect: ONE No Helmet Violation (92% confidence)
Status: ✅ PASS

# Test 4: Low confidence
Input:  no_helmet (42%)
Expect: Skipped (below 50%)
Status: ✅ PASS

# Test 5: Duplicate within 30s
T=0s:   no_helmet (90%)
T=15s:  no_helmet (92%)
Expect: First saved, second skipped
Status: ✅ PASS
```

---

## 📞 Common Questions

**Q: Why wasn't my violation detected?**
A: Check confidence score. Must be ≥50%. Try clearer image/angle.

**Q: Why does triple riding with helmets not count?**
A: Smart logic - riders are compliant despite overloading. Safety prioritized.

**Q: Can I change the cooldown period?**
A: Yes! Edit `COOLDOWN_SECONDS` in `backend/app/config.py`

**Q: What if multiple violations in one frame?**
A: Each TYPE is registered separately. Multiple same-type = ONE violation.

**Q: How to adjust confidence threshold?**
A: Edit `MIN_CONFIDENCE_GENERAL` in `config.py`

---

## 🎯 Best Practices

✅ Use clear, well-lit images for uploads
✅ Ensure camera is stable for real-time detection
✅ Review violations with <60% confidence manually
✅ Adjust thresholds based on your accuracy needs
✅ Monitor logs for edge cases and false positives

---

**For detailed edge case documentation, see:** `EDGE_CASES.md`
**For improvement summary, see:** `IMPROVEMENTS.md`
