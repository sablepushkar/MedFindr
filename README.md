# MedFindr

**Version: 09.0**  
**Status:** Developmental prototype (stable foundation)

MedFindr is a structured health-concern assistant designed as a focused med × pharma portfolio project.  
It takes a free-text description of a health issue and returns a clear, sectioned, and explainable response that can be useful for patients or pharmacy/clinic staff.

The current version prioritises clean architecture, transparency, and extensibility over feature completeness.

---

### What it does (09.0)

- Accepts a free-text health concern
- Produces a structured response with clear sections
- Transparent rule-based urgency / red-flag assessment
- Explainable risk layer (EBM interface ready for a real InterpretML model)
- OpenFDA drug lookup with safety-relevant fields
- Strong separation between UI and business logic
- Curated sample concerns + evaluation set for testing

### How to run

```bash
git clone https://github.com/sablepushkar/MedFindr.git
cd MedFindr
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
├── app.py                      # Thin rendering layer
├── config.py                   # Central configuration
├── utils/
│   ├── response_engine.py      # Structured response builder
│   ├── urgency.py              # Transparent rule-based urgency
│   ├── ebm_risk.py             # Explainable risk interface (EBM-ready)
│   └── drug_lookup.py          # OpenFDA utility
├── data/
│   ├── sample_concerns.json
│   └── evaluation_set.json
├── requirements.txt
└── README.md
```

---

### Design Principles

- Keep the interface simple and stable
- Keep all clinical logic isolated and testable
- Prefer transparent / glass-box methods
- Make future additions (real EBM model, dual-view, tools) low-friction

---

### Version History (summary)

- **V0.7 – 07.5** → Foundation, data, drug module, urgency engine, structured response engine
- **08.1 – 08.5** → Explainable risk layer (EBM interface) introduced and hardened
- **09.0** → Portfolio polish and stability pass

---

Built as a focused learning and portfolio project in the med × pharma domain.
