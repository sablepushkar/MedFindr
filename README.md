# MedFindr

**Version: 07.5**  
**Status:** Developmental / Structured Response Engine (refined)

MedFindr is a structured health-concern assistant prototype.  
It converts a free-text health concern into a clear, sectioned response that can be useful for patients or pharmacy/clinic staff.

---

### Current Capabilities (07.5)

- Clean, typed Structured Response Engine
- Transparent rule-based urgency / red-flag assessment
- Improved OpenFDA drug lookup with safety-relevant fields
- Fully separated UI and business logic
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
├── app.py                      # Thin rendering layer only
├── config.py
├── utils/
│   ├── response_engine.py      # Core structured response builder
│   ├── urgency.py              # Transparent urgency engine
│   └── drug_lookup.py          # OpenFDA utility
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
- **07.3 major** – Basic Red-Flag & Urgency Engine
- **07.5** – Structured Response Engine (+ refinement pass)

---

Built as a focused med × pharma learning and portfolio project.
