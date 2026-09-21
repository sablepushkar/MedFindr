# MedFindr

**Version: 07.2**  
**Status:** Developmental / Drug module strengthened

MedFindr is a structured health-concern assistant prototype.  
It takes a free-text description of a health issue and returns a clear, sectioned response that can be useful for patients or pharmacy/clinic staff.

Current focus remains on building a clean, reliable foundation before adding heavier clinical intelligence.

---

### Current Capabilities (07.2)

- Simple text input for health concern
- Structured output sections
- Improved OpenFDA drug lookup (better field extraction & safety snippets)
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
│   └── drug_lookup.py          # Strengthened in 07.2
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

---

Built as a focused med × pharma learning and portfolio project.
