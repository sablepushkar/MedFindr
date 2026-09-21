# MedFindr

**Version: V07.1**  
**Status:** Developmental / Early foundation stage

MedFindr is a structured health-concern assistant prototype.  
It takes a free-text description of a health issue and returns a clear, sectioned response that can be useful for patients or pharmacy/clinic staff.

This is still early work. The current version focuses on a clean, stable foundation so that more advanced pieces (better urgency logic, explainable models, stronger drug handling, etc.) can be added cleanly later.

---

### Current Capabilities (V07.1)

- Simple text input for health concern
- Structured output sections
- Basic OpenFDA drug lookup
- Sample concerns for testing
- Strong safety disclaimers

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
├── app.py                 # Main Streamlit interface (kept deliberately simple)
├── config.py              # Basic configuration
├── utils/
│   ├── drug_lookup.py     # OpenFDA utility
│   └── __init__.py
├── data/
│   └── sample_concerns.json
├── requirements.txt
└── README.md
```

More modules will be introduced in later versions as features are added.

---

### Version History

- **V0.7** – Initial working prototype
- **V07.1** – Foundation hardening (structure, typing, safety, error handling)

---

Built as a focused med × pharma learning and portfolio project.
