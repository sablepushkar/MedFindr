# MedFindr

**Version: 07.3 major**  
**Status:** Developmental / Urgency engine added & verified

MedFindr is a structured health-concern assistant prototype.  
It takes a free-text description of a health issue and returns a clear, sectioned response useful for patients or pharmacy/clinic staff.

---

### Current Capabilities (07.3 major)

- Simple text input for health concern
- Structured output sections
- Improved OpenFDA drug lookup with safety fields
- Transparent rule-based urgency / red-flag engine
- Curated sample concerns + evaluation set
- Strong safety disclaimers
- Clean separation of concerns (UI vs logic)

### How to run

```bash
pip install -r requirements.txt
streamlit run app.py
```

### Important Notice

**This is not medical advice.**  
MedFindr is a developmental research and portfolio prototype only.  
It must not be used for actual clinical decisions. Always consult a qualified healthcare professional.

---

### Project Structure

```
MedFindr/
├── app.py                      # Thin interface layer
├── config.py                   # Central configuration
├── utils/
│   ├── drug_lookup.py          # OpenFDA utility
│   └── urgency.py              # Transparent urgency engine
├── data/
│   ├── sample_concerns.json
│   └── evaluation_set.json
├── requirements.txt
└── README.md
```

---

### Version History

- **V0.7** – Initial working prototype
- **V07.1** – Foundation hardening
- **07.1 dev** – Sample data + evaluation set
- **07.2** – Drug module upgrade (Phase 1)
- **07.3 major** – Basic Red-Flag & Urgency Engine (verified)

---

Built as a focused med × pharma learning and portfolio project.
