# MedFindr

**Version: 08.1 Beta testing EBM**  
**Status:** Developmental / First Explainable Risk Layer (Beta)

MedFindr is a structured health-concern assistant prototype.  
It converts a free-text health concern into a clear, sectioned, explainable response.

---

### Current Capabilities (08.1)

- Clean Structured Response Engine
- Transparent rule-based urgency assessment
- **New:** EBM-style explainable risk layer (beta placeholder with full interface)
- Improved OpenFDA drug lookup
- Fully separated UI and business logic
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
│   ├── response_engine.py
│   ├── urgency.py
│   ├── ebm_risk.py             # New in 08.1
│   └── drug_lookup.py
├── data/
│   ├── sample_concerns.json
│   └── evaluation_set.json
├── requirements.txt
└── README.md
```

---

### Version History

- **V0.7** → **07.5** – Foundation + Structured Response Engine
- **08.1 Beta testing EBM** – First Explainable Risk Layer (interface ready)

---

Built as a focused med × pharma learning and portfolio project.
