# MedFindr

**Version: 07.1 dev**  
**Status:** Developmental / Data foundation stage

MedFindr is a structured health-concern assistant prototype.  
It takes a free-text description of a health issue and returns a clear, sectioned response that can be useful for patients or pharmacy/clinic staff.

This is still early work. The current version focuses on a clean foundation and high-quality sample/evaluation data so that later clinical logic and models can be tested properly.

---

### Current Capabilities (07.1 dev)

- Simple text input for health concern
- Structured output sections
- Basic OpenFDA drug lookup
- Curated sample concerns + evaluation set
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
├── app.py
├── config.py
├── utils/
│   └── drug_lookup.py
├── data/
│   ├── sample_concerns.json      # Broad set for manual testing
│   └── evaluation_set.json       # Smaller labelled set for measuring progress
├── requirements.txt
└── README.md
```

---

### Version History

- **V0.7** – Initial working prototype
- **V07.1** – Foundation hardening
- **07.1 dev** – Sample data cleaning + evaluation set added

---

Built as a focused med × pharma learning and portfolio project.
