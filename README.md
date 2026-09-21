# MedFindr

**Version: 08.5**  
**Status:** Developmental / EBM layer hardened & ready for real model

MedFindr is a structured health-concern assistant prototype that produces clear, sectioned, and explainable responses.

---

### Current Capabilities (08.5)

- Clean Structured Response Engine
- Transparent rule-based urgency assessment
- Explainable Risk Assessment layer (EBM interface fully prepared)
- Improved OpenFDA drug lookup
- Strong separation of concerns
- Ready for a trained InterpretML EBM model to be dropped in

### How to run

```bash
pip install -r requirements.txt
streamlit run app.py
```

### Important Notice

**This is not medical advice.**  
MedFindr is a developmental research and portfolio prototype only.  
Always consult a qualified healthcare professional.

---

### Project Structure

```
MedFindr/
├── app.py
├── config.py
├── utils/
│   ├── response_engine.py
│   ├── urgency.py
│   ├── ebm_risk.py
│   └── drug_lookup.py
├── data/
│   ├── sample_concerns.json
│   └── evaluation_set.json
├── requirements.txt
└── README.md
```

---

### Version History

- **V0.7 → 07.5** – Foundation + Structured Response Engine
- **08.1 Beta testing EBM** – First EBM interface
- **08.5** – EBM layer hardened, model-loading path prepared

---

Built as a focused med × pharma learning and portfolio project.
