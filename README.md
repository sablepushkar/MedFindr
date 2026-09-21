# MedFindr

**Version: V1.0 RD** (Redefined and Rechecked)  
**Status:** Developmental – Quality & consistency pass completed

MedFindr is a structured and explainable health-concern assistant built as a focused med × pharma portfolio project.  
It converts a free-text health concern into a clear, sectioned response with transparent urgency assessment and an explainable risk layer.

---

### Current Capabilities (V1.0 RD)

- Clean Structured Response Engine
- Transparent rule-based urgency / red-flag assessment
- Explainable risk layer (EBM interface + training pipeline)
- Patient / Staff dual view
- Evaluation script against labelled set
- OpenFDA drug lookup with safety fields
- Strong separation of concerns and consistent structure

### How to run

```bash
pip install -r requirements.txt
streamlit run app.py
```

### Optional but recommended

```bash
# Train the EBM model
python scripts/train_ebm.py

# Run evaluation
python scripts/evaluate.py
```

### Important Notice

**This is not medical advice.**  
MedFindr is a developmental research and portfolio prototype only.  
It must not be used for actual clinical decisions. Always consult a qualified healthcare professional.

---

### Project Structure

```
MedFindr/
├── app.py                      # Thin UI layer (Patient / Staff view)
├── config.py                   # Central configuration
├── scripts/
│   ├── train_ebm.py            # Train Explainable Boosting Machine
│   └── evaluate.py             # Evaluate urgency engine
├── utils/
│   ├── response_engine.py      # Structured response builder
│   ├── urgency.py              # Rule-based urgency engine
│   ├── ebm_risk.py             # Explainable risk module
│   └── drug_lookup.py          # OpenFDA utility
├── data/
│   ├── sample_concerns.json
│   └── evaluation_set.json
├── models/                     # Created after training
├── requirements.txt
└── README.md
```

---

### Version Journey (summary)

- **09.0** – Stable foundation
- **V09.1a** – Real EBM training pipeline
- **V09 Evolve** – Evaluation + Dual View
- **V1.0 RD** – Redefined and Rechecked (current)

Next planned milestone: **MedFindr X1.0** (Defined Version)

---

Built as a focused med × pharma learning and portfolio project.
